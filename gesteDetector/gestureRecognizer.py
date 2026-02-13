from __future__ import annotations
from pathlib import Path
import urllib.request
import cv2
import numpy as np


# mapping des points MediaPipe pour chaque doigt
# format: (mcp, pip, dip, tip)
FINGER_JOINTS = {
    "Thumb":  (1, 2, 3, 4),
    "Index":  (5, 6, 7, 8),
    "Middle": (9, 10, 11, 12),
    "Ring":   (13, 14, 15, 16),
    "Pinky":  (17, 18, 19, 20),
}


def _clamp(x, a, b):
    # garde x entre a et b
    return max(a, min(b, x))


def _angle_3pts(a, b, c):
    """
    calcule l'angle ABC en degrés
    permet de savoir si un doigt est plié ou tendu
    """
    ba = a - b
    bc = c - b
    nba = np.linalg.norm(ba)
    nbc = np.linalg.norm(bc)

    if nba < 1e-6 or nbc < 1e-6:
        return 180.0

    cosang = float(np.dot(ba, bc) / (nba * nbc))
    cosang = _clamp(cosang, -1.0, 1.0)
    return float(np.degrees(np.arccos(cosang)))


def finger_states(kpts2d):
    """
    retourne l'état des doigts

    True  = doigt tendu
    False = doigt plié
    """
    pts = {i: kpts2d[i].astype(np.float32) for i in range(21)}

    angles = {}
    angles["Thumb"] = _angle_3pts(pts[1], pts[2], pts[3])

    for name in ["Index", "Middle", "Ring", "Pinky"]:
        mcp, pip, dip, tip = FINGER_JOINTS[name]
        angles[name] = _angle_3pts(pts[mcp], pts[pip], pts[dip])

    extended = {}
    extended["Thumb"]  = angles["Thumb"] > 155
    extended["Index"]  = angles["Index"] > 165
    extended["Middle"] = angles["Middle"] > 165
    extended["Ring"]   = angles["Ring"] > 165
    extended["Pinky"]  = angles["Pinky"] > 165

    return extended


def detect_gesture(kpts2d):
    """
    gestes détectés :

    - main ouverte
    - pouce en l air
    - ok
    - poing ferme
    - deux doigts
    """

    ext = finger_states(kpts2d)

    thumb_ext = ext["Thumb"]
    idx = ext["Index"]
    mid = ext["Middle"]
    ring = ext["Ring"]
    pinky = ext["Pinky"]

    wrist = kpts2d[0].astype(np.float32)
    index_mcp = kpts2d[5].astype(np.float32)

    palm_size = float(np.linalg.norm(index_mcp - wrist))
    if palm_size < 1e-6:
        palm_size = 1.0

    thumb_tip = kpts2d[4].astype(np.float32)

    # distance pouce -> main
    d_thumb = float(np.linalg.norm(thumb_tip - index_mcp)) / palm_size

    THUMB_STICKY = 0.55

    thumb_is_stuck = d_thumb < THUMB_STICKY
    thumb_is_detached = d_thumb > (THUMB_STICKY + 0.10)

    # =========================
    # OK (pouce touche index)
    # =========================
    index_tip = kpts2d[8].astype(np.float32)
    d_ti = float(np.linalg.norm(thumb_tip - index_tip)) / palm_size

    if d_ti < 0.35 and mid and ring and pinky:
        return "ok"

    # =========================
    # MAIN OUVERTE ✋
    # 4 doigts tendus + pouce décollé
    # =========================
    if idx and mid and ring and pinky and thumb_is_detached:
        return "main ouverte"

    # =========================
    # DEUX DOIGTS ✌️
    # =========================
    if idx and mid and not ring and not pinky:
        return "deux doigts"

    # =========================
    # POING / POUCE EN L AIR
    # =========================
    if not idx and not mid and not ring and not pinky:

        if thumb_is_stuck:
            return "poing ferme"

        if thumb_is_detached and thumb_ext:
            return "pouce en l air"

        return "poing ferme"

    return ""


# dossier pour stocker les modèles
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "hand_assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

PALM_ONNX_URL = "https://huggingface.co/opencv/palm_detection_mediapipe/resolve/main/palm_detection_mediapipe_2023feb.onnx"
HAND_ONNX_URL = "https://huggingface.co/opencv/handpose_estimation_mediapipe/resolve/main/handpose_estimation_mediapipe_2023feb.onnx"

MP_PALMDET_URL = "https://huggingface.co/spaces/opencv/handpose_estimation_mediapipe/raw/main/mp_palmdet.py"
MP_HANDPOSE_URL = "https://huggingface.co/spaces/opencv/handpose_estimation_mediapipe/raw/main/mp_handpose.py"


def _download_if_missing(url: str, dst: Path):
    if dst.exists() and dst.stat().st_size > 0:
        return
    print("download:", dst.name)
    tmp = dst.with_suffix(".tmp")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(dst)


def _ensure_assets():
    palm = ASSETS_DIR / "palm.onnx"
    hand = ASSETS_DIR / "hand.onnx"
    mp1 = ASSETS_DIR / "mp_palmdet.py"
    mp2 = ASSETS_DIR / "mp_handpose.py"

    _download_if_missing(PALM_ONNX_URL, palm)
    _download_if_missing(HAND_ONNX_URL, hand)
    _download_if_missing(MP_PALMDET_URL, mp1)
    _download_if_missing(MP_HANDPOSE_URL, mp2)

    return palm, hand, mp1, mp2


def _import_helpers(p1: Path, p2: Path):
    import importlib.util

    def load(name, path):
        spec = importlib.util.spec_from_file_location(name, str(path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    return load("_mp_palmdet", p1), load("_mp_handpose", p2)


class HandPoseDetector:

    def __init__(self):
        palm, hand, p1, p2 = _ensure_assets()
        palmdet_mod, handpose_mod = _import_helpers(p1, p2)

        self.palmdet = palmdet_mod.MPPalmDet(modelPath=str(palm))
        self.handpose = handpose_mod.MPHandPose(modelPath=str(hand))

        self.last_results = []

    def process(self, frame):
        self.last_results = []
        palms = self.palmdet.infer(frame)

        if palms is None or len(palms) == 0:
            return []

        for palm in palms:
            hand = self.handpose.infer(frame, palm)
            if hand is None:
                continue

            hand = np.asarray(hand).reshape(-1)

            bbox = hand[0:4].astype(int)
            lm = hand[4:67].reshape(21, 3)[:, :2]

            self.last_results.append({
                "bbox": tuple(bbox),
                "kpts": lm
            })

        return self.last_results

    def get_hands_box(self):
        return [r["bbox"] for r in self.last_results]

    def draw(self, frame):
        if not self.last_results:
            return frame

        gesture = detect_gesture(self.last_results[0]["kpts"])

        if gesture:
            cv2.putText(frame, gesture, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)

        for r in self.last_results:
            x1, y1, x2, y2 = r["bbox"]

            for (x, y) in r["kpts"]:
                cv2.circle(frame, (int(x), int(y)), 4, (0, 0, 255), -1)

            cv2.rectangle(frame, (x1, y1), (x2, y2),
                          (0, 255, 0), 2)

        return frame

    def detect(self, frame):
        self.process(frame)
        return self.draw(frame)


def main():
    cap = cv2.VideoCapture(0)
    detector = HandPoseDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = detector.detect(frame)

        cv2.imshow("hand detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()