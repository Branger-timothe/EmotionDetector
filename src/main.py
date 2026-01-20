from deepface import DeepFace
import os

# On vérifie si l'image existe avant de tester
img_path = "../datas/test_image.png"

if os.path.exists(img_path):
    print("Image trouvée, lancement de l'analyse...")
    # On teste juste l'émotion
    objs = DeepFace.analyze(img_path = img_path, actions = ['emotion'])
    print(f"Résultat : {objs[0]['dominant_emotion']}")
else:
    print(f"Erreur : Pose le fichier '{img_path}' dans le dossier du projet !")