import matplotlib.pyplot as plt
class EmotionStatistics:
    def __init__(self):
        self.emotions_count = {}
        self.ages = []
        self.total_stats = 0
        self.historique_scores = []

    def extraire_stats_essentielles(self, results):
        if not results:
            return
        res = results[0]
        self.total_stats += 1
        self.ages.append(res.age)
        dom_emotion = res.dominant_emotion
        if dom_emotion in self.emotions_count:
            self.emotions_count[dom_emotion] += 1
        else:
            self.emotions_count[dom_emotion] = 1
        mapping_echelle = {
            'happy': 10, 'surprise': 5, 'neutral': 0,
            'fear': -4, 'sad': -7, 'disgust': -9, 'angry': -10
        }
        score_graphique = mapping_echelle.get(dom_emotion, 0)
        if not hasattr(self, 'historique_scores'):
            self.historique_scores = []
        self.historique_scores.append(score_graphique)


    def generer_graphique_emotions(self):
        if not hasattr(self, 'historique_scores') or not self.historique_scores:
            print("Aucune donnée disponible pour générer le graphique.")
            return
        indices = range(len(self.historique_scores))

        plt.figure(figsize=(10, 5))
        plt.plot(indices, self.historique_scores, marker='o', color='#2c3e50', linewidth=2, label="Humeur")
        plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)

        plt.ylim(-11, 11)
        plt.yticks(
            [-10, -7, -4, 0, 5, 10],
            ['Angry (-10)', 'Sad (-7)', 'Fear (-4)', 'Neutral (0)', 'Surprise (5)', 'Happy (10)']
        )

        plt.title(f"Évolution des émotions (Total: {self.total_stats} analyses)")
        plt.xlabel("Nombre de captures")
        plt.ylabel("Variation des emotions")
        plt.grid(axis='y', linestyle=':', alpha=0.6)

        if self.ages:
            age_moyen = sum(self.ages) / len(self.ages)
            plt.figtext(0.15, 0.8, f"Âge moyen détecté : {age_moyen:.1f} ans", fontsize=10,
                        bbox={"facecolor": "orange", "alpha": 0.2})

        plt.savefig('../datas/evolution_emotions.png')
        plt.show()
        self.generer_camembert_emotions()

    def generer_camembert_emotions(self):
        if not self.emotions_count:
            print("Aucune donnée d'émotion pour générer le camembert.")
            return
        labels = list(self.emotions_count.keys())
        values = list(self.emotions_count.values())

        couleurs_map = {
            'happy': '#2ecc71','neutral': '#95a5a6','sad': '#3498db','fear': '#9b59b6','angry': '#e74c3c','surprise': '#f1c40f', 'disgust': '#1abc9c'
        }
        couleurs = [couleurs_map.get(emotion, '#bdc3c7') for emotion in labels]
        plt.figure(figsize=(8, 8))
        plt.pie(values,labels=labels,autopct='%1.1f%%',startangle=140,colors=couleurs,shadow=True)
        plt.title(f"Répartition globale des émotions\n(Basé sur {self.total_stats} analyses)")
        plt.savefig('../datas/repartition_emotions_camembert.png')
        plt.show()
