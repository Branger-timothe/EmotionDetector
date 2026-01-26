from pathlib import Path

import cv2
from ultralytics import YOLO

# path to model file
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "../../model/best.pt"


class HandPoseDetector:
    def __init__(self, model_path=MODEL_PATH):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, conf=0.3, verbose=False)

        for r in results:
            if r.keypoints is None:
                continue

            kpts = r.keypoints.xy.cpu().numpy()

            for hand in kpts:
                # Draw the points on the hand
                for (x, y) in hand:
                    cv2.circle(
                        frame,
                        (int(x), int(y)),
                        4,
                        (0, 0, 255),
                        -1
                    )
                # box around the hand calculated by the points
                x1, y1 = hand[:, 0].min(), hand[:, 1].min()
                x2, y2 = hand[:, 0].max(), hand[:, 1].max()

                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )

        return frame


# Just below ,the exemple on how use the model
def main():
    detector = HandPoseDetector()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur caméra")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = detector.detect(frame)
        cv2.imshow("Hand Pose Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
