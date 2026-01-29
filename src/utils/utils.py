import cv2
def analyseImages(results,frame):
    for res in results:
        # Récupérer les coordonnées du visage pour dessiner un carré
        x, y, w, h = res['region']['x'], res['region']['y'], res['region']['w'], res['region']['h']
        emotion = res['dominant_emotion']

        # 4. Dessiner un rectangle autour du visage
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 5. Écrire l'émotion au-dessus du rectangle
        cv2.putText(frame, emotion, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)