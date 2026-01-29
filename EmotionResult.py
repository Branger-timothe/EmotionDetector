import cv2
from deepface import DeepFace
import os
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class EmotionResult:
    """Classe pour stocker les résultats d'analyse d'émotions"""
    dominant_emotion: str
    emotions: Dict[str, float]
    region: Dict[str, int]

    @classmethod
    def from_deepface_result(cls, result: Dict) -> 'EmotionResult':
        """Crée un EmotionResult à partir d'un résultat DeepFace"""
        return cls(
            dominant_emotion=result.get('dominant_emotion', 'unknown'),
            emotions=result.get('emotion', {}),
            region=result.get('region', {})
        )


class EmotionDetector:
    """Gestionnaire de la détection d'émotions via DeepFace"""

    def __init__(self, detector_backend: str = 'opencv',
                 enforce_detection: bool = False):
        """
        Initialise le détecteur d'émotions

        Args:
            detector_backend: Backend de détection ('opencv', 'ssd', 'mtcnn', etc.)
            enforce_detection: Si True, lève une erreur si aucun visage détecté
        """
        self.detector_backend = detector_backend
        self.enforce_detection = enforce_detection
        self._configure_tensorflow()

    @staticmethod
    def _configure_tensorflow():
        """Configure TensorFlow pour éviter les warnings"""
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    def analyze(self, frame) -> List[EmotionResult]:
        """
        Analyse les émotions dans une image

        Args:
            frame: Image à analyser (format numpy array)

        Returns:
            Liste d'EmotionResult pour chaque visage détecté
        """
        try:
            results = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=self.enforce_detection,
                detector_backend=self.detector_backend
            )

            # DeepFace peut retourner un dict ou une liste
            if isinstance(results, dict):
                results = [results]

            return [EmotionResult.from_deepface_result(r) for r in results]

        except Exception as e:
            print(f"Erreur lors de l'analyse : {e}")
            return []


class VideoCapture:
    """Gestionnaire de capture vidéo"""

    def __init__(self, camera_index: int = 0):
        """
        Initialise la capture vidéo

        Args:
            camera_index: Index de la caméra (0 par défaut)
        """
        self.camera_index = camera_index
        self.cap = None

    def start(self) -> bool:
        """
        Démarre la capture vidéo

        Returns:
            True si la capture est initialisée, False sinon
        """
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print(f"Erreur : Impossible d'accéder à la caméra {self.camera_index}")
            return False
        return True

    def read(self):
        """Lit une frame de la vidéo"""
        if self.cap is None:
            return False, None
        return self.cap.read()

    def release(self):
        """Libère les ressources de la capture vidéo"""
        if self.cap is not None:
            self.cap.release()


class EmotionVisualizer:
    """Gestionnaire de l'affichage des résultats"""

    def __init__(self, window_name: str = "Détection d'Émotions"):
        """
        Initialise le visualiseur

        Args:
            window_name: Nom de la fenêtre d'affichage
        """
        self.window_name = window_name

    def draw_results(self, frame, results: List[EmotionResult]):
        """
        Dessine les résultats sur l'image

        Args:
            frame: Image sur laquelle dessiner
            results: Liste des résultats d'émotions
        """
        for result in results:
            self._draw_face_box(frame, result.region)
            self._draw_emotion_text(frame, result)

    def _draw_face_box(self, frame, region: Dict[str, int]):
        """Dessine un rectangle autour du visage"""
        x = region.get('x', 0)
        y = region.get('y', 0)
        w = region.get('w', 0)
        h = region.get('h', 0)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def _draw_emotion_text(self, frame, result: EmotionResult):
        """Affiche l'émotion dominante et les scores"""
        region = result.region
        x = region.get('x', 0)
        y = region.get('y', 0)

        # Émotion dominante
        text = f"{result.dominant_emotion}"
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Top 3 émotions avec scores
        sorted_emotions = sorted(result.emotions.items(),
                                 key=lambda x: x[1], reverse=True)[:3]

        for i, (emotion, score) in enumerate(sorted_emotions):
            text = f"{emotion}: {score:.1f}%"
            cv2.putText(frame, text, (x, y + 30 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    def show(self, frame):
        """Affiche l'image dans une fenêtre"""
        cv2.imshow(self.window_name, frame)

    @staticmethod
    def cleanup():
        """Ferme toutes les fenêtres OpenCV"""
        cv2.destroyAllWindows()


class EmotionDetectionApp:
    """Application de détection d'émotions"""

    def __init__(self, camera_index: int = 0):
        """
        Initialise l'application

        Args:
            camera_index: Index de la caméra à utiliser
        """
        self.camera = VideoCapture(camera_index)
        self.detector = EmotionDetector()
        self.visualizer = EmotionVisualizer()
        self.running = False

    def start(self):
        """Lance l'application de détection d'émotions"""
        if not self.camera.start():
            return

        print("Détection lancée. Appuyez sur 'q' pour quitter.")
        self.running = True
        self._main_loop()
        self._cleanup()

    def _main_loop(self):
        """Boucle principale de traitement"""
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                print("Erreur de lecture de la caméra")
                break

            # Analyse des émotions
            results = self.detector.analyze(frame)

            # Affichage des résultats
            self.visualizer.draw_results(frame, results)
            self.visualizer.show(frame)

            # Vérifie si l'utilisateur veut quitter
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()

    def stop(self):
        """Arrêter l'application"""
        self.running = False

    def _cleanup(self):
        """Nettoyer les ressources"""
        self.camera.release()
        self.visualizer.cleanup()
        print("Application fermée proprement")


def main():
    """Point d'entrée de l'application"""
    app = EmotionDetectionApp(camera_index=0)
    app.start()


if __name__ == "__main__":
    main()