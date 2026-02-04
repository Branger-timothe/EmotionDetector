import cv2
from deepface import DeepFace
import os
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class EmotionResult:
    """Classe pour stocker les résultats d'analyse (émotions + âge)"""
    dominant_emotion: str
    emotions: Dict[str, float]
    age: int
    dominant_gender: Optional[str]
    dominant_race: Optional[str]
    region: Dict[str, int]

    @classmethod
    def from_deepface_result(cls, result: Dict) -> 'EmotionResult':
        """Crée un AnalysisResult à partir d'un résultat DeepFace"""
        return cls(
            dominant_emotion=result.get('dominant_emotion', 'unknown'),
            emotions=result.get('emotion', {}),
            age=result.get('age', 0),
            dominant_gender=result.get('dominant_gender'),
            dominant_race=result.get('dominant_race'),
            region=result.get('region', {})
        )


class EmotionDetector:
    """Gestionnaire de l'analyse faciale via DeepFace (émotions + âge)"""

    def __init__(self, detector_backend: str = 'opencv',
                 enforce_detection: bool = False,
                 actions: List[str] = None):
        """
        Initialise l'analyseur facial

        Args:
            detector_backend: Backend de détection ('opencv', 'ssd', 'mtcnn', etc.)
            enforce_detection: Si True, lève une erreur si aucun visage détecté
            actions: Liste des analyses à effectuer ['emotion', 'age', 'gender', 'race']
        """
        self.detector_backend = detector_backend
        self.enforce_detection = enforce_detection
        self.actions = actions or ['emotion', 'age']  # Par défaut: émotion + âge
        self._configure_tensorflow()

    @staticmethod
    def _configure_tensorflow():
        """Configure TensorFlow pour éviter les warnings"""
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    def analyze(self, frame) -> List[EmotionResult]:
        """
        Analyse le visage dans une image (émotions + âge)

        Args:
            frame: Image à analyser (format numpy array)

        Returns:
            Liste d'AnalysisResult pour chaque visage détecté
        """
        try:
            results = DeepFace.analyze(
                frame,
                actions=self.actions,
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
    """Gestionnaire de l'affichage des résultats (émotions + âge)"""

    def __init__(self, window_name: str = "Détection Visage - Émotions & Âge"):
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
            results: Liste des résultats d'analyse
        """
        for result in results:
            self._draw_face_box(frame, result.region)
            self._draw_info_text(frame, result)

    def _draw_face_box(self, frame, region: Dict[str, int]):
        """Dessine un rectangle autour du visage"""
        x = region.get('x', 0)
        y = region.get('y', 0)
        w = region.get('w', 0)
        h = region.get('h', 0)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def _draw_info_text(self, frame, result: EmotionResult):
        """Affiche l'émotion dominante, l'âge et les scores"""
        region = result.region
        x = region.get('x', 0)
        y = region.get('y', 0)
        w = region.get('w', 0)

        # Émotion dominante + Âge + genre et race si présent
        text = f"{result.dominant_emotion} | Age: {result.age}"
        if result.dominant_gender:
            text2 = f"Gender: {result.dominant_gender}"
            cv2.putText(frame, text2, (0, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        if result.dominant_race:
            text3 = f"Race: {result.dominant_race}"
            cv2.putText(frame, text3, (0, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, text, (0, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Top 3 émotions avec scores
        sorted_emotions = sorted(result.emotions.items(),
                                 key=lambda x: x[1], reverse=True)[:3]

        for i, (emotion, score) in enumerate(sorted_emotions):
            text = f"{emotion}: {score:.1f}%"
            cv2.putText(frame, text, (x+w+10, y + 30 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    def show(self, frame):
        """Affiche l'image dans une fenêtre"""
        cv2.imshow(self.window_name, frame)

    @staticmethod
    def cleanup():
        """Ferme toutes les fenêtres OpenCV"""
        cv2.destroyAllWindows()