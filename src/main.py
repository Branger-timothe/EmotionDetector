import cv2
from deepface import DeepFace
import os

# On force l'utilisation du CPU pour éviter les soucis de pilotes GPU au début
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def start_emotion_detection():
    # 1. Initialisation de la capture vidéo (0 est l'index de la webcam par défaut)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'accéder à la webcam.")
        return

    print("Détection lancée. Appuyez sur 'q' pour quitter.")

    while True:
        # 2. Lire une image depuis la webcam
        ret, frame = cap.read()
        if not ret:
            break

        try:
            # 3. Analyser l'émotion sur l'image actuelle
            # enforce_detection=False évite que le code plante si aucun visage n'est vu
            # detector_backend='opencv' est le plus rapide pour du temps réel
            results = DeepFace.analyze(frame, actions=['emotion'],
                                       enforce_detection=False,
                                       detector_backend='opencv')

            # DeepFace renvoie une liste (un dictionnaire par visage détecté)
            for res in results:
                # Récupérer les coordonnées du visage pour dessiner un carré
                x, y, w, h = res['region']['x'], res['region']['y'], res['region']['w'], res['region']['h']
                emotion = res['dominant_emotion']

                # 4. Dessiner un rectangle autour du visage
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # 5. Écrire l'émotion au-dessus du rectangle
                cv2.putText(frame, emotion, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        except Exception as e:
            print(f"Erreur d'analyse : {e}")

        # 6. Afficher le résultat dans une fenêtre
        cv2.imshow('Detection d\'Emotions - Appuyez sur q pour quitter', frame)

        # 7. Sortir de la boucle si on appuie sur la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Nettoyage à la fin
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_emotion_detection()