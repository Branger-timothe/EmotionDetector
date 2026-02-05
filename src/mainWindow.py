import pygame

import src.EmotionResult as ER

import tkinter as tk
from src.EmotionStatistics import EmotionStatistics
from tkinter import ttk
from queue import Queue
from PIL import Image, ImageTk

import threading
import cv2
import time

#from IA.handDetector import HandPoseDetector
from src.game.game import Game, create_fruit_ninja_game


class MainWindow:
    def __init__(self, root):
        """
        Initialise les attributs de la classe permettant de generer l'interface utilisateur
        les bouttons permettent de demarrer la camera et de debuter l'analyse des emotions et ensuite du jeu
        """
        self.root = root
        self.root.title("Detecteur d'emotion")
        self.root.geometry("1000x600")
        self.root.configure(bg="#252033")

        self.create_header()
        self.create_video_frame()
        self.setup_controls()

        self.detector = ER.EmotionDetector()
        self.camera = ER.VideoCapture(0)
        self.visualizer = ER.EmotionVisualizer()
        self.is_running = False

        self.btn_start = ttk.Button(self.control_panel, text="Lancer Caméra", command=self.start_cam_placeholder)
        self.btn_start.pack(pady=10, padx=20, fill='x')
        self.btn_stop = ttk.Button(self.control_panel, text="Arrêter Caméra", command=self.stop_cam_placeholder)
        self.btn_game = ttk.Button(self.control_panel, text="Lancer Jeu", command=self.start_game_placeholder)
        self.btn_game.pack(pady=10, padx=20, fill='x')
        self.btn_end_game = ttk.Button(self.control_panel, text="Arrêter Jeu", command=self.end_game_placeholder)
        self.btn_quit = ttk.Button(self.control_panel, text="Quitter", command=self.on_closing)
        self.btn_quit.pack(side="bottom", pady=20, padx=20, fill='x')

        self.frame_count = 0
        self.last_results = []

        self.frame_queue = Queue(maxsize=1)
        self.analysis_thread = None
        self.is_analyzing = False

        self.stats = EmotionStatistics()

    def create_header(self):
        self.header = tk.Frame(self.root, bg="#6C6091", height=60)
        self.header.pack(fill="x")

        self.title_label = tk.Label(self.header, text="DETECTION D'EXPRESSIONS FACIALES", fg="white", bg="#6C6091",
                                    font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=15)
        self.main_container = tk.Frame(self.root, bg="#595566")
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)

    def create_video_frame(self):
        self.video_frame = tk.Frame(self.main_container, bg="black", width=500, height=400)
        self.video_frame.pack(side="left", fill='both', expand=True)
        self.video_label = tk.Label(self.video_frame, text="Flux Vidéo", fg="white", bg="black")
        self.video_label.pack(expand=True)

    def setup_controls(self):
        self.control_panel = tk.Frame(self.main_container, bg="#6C6091", width=400)
        self.control_panel.pack_propagate(False)
        self.control_panel.pack(side="right", fill="y")

        tk.Label(self.control_panel, text="STATISTIQUES", font=("Helvetica", 12, "bold"), bg="#ecf0f1").pack(pady=10)

        self.emotion_status = tk.Label(self.control_panel, text="Attente...", font=("Helvetica", 14), bg="#ecf0f1",fg="#e67e22")
        self.emotion_status.pack(pady=20)

        ttk.Separator(self.control_panel, orient='horizontal').pack(fill='x', padx=10, pady=10)


    def start_cam_placeholder(self):
        self.video_label.config(image="", text="Chargement du flux vidéo...")
        self.root.update_idletasks()
        print("Signal : Démarrage de la caméra...")
        if self.camera.start():
            self.is_running = True

            self.is_analyzing = True
            self.analysis_thread = threading.Thread(target=self.background_analysis, daemon=True)
            self.analysis_thread.start()

            self.create_button_afer_start()
            self.update_loop()

    def stop_cam_placeholder(self):
        self.stats.generer_graphique_emotions()
        self.video_label.config(image="", text="Flux video...")
        self.root.update_idletasks()
        print("Signal : Arrêt de la caméra...")
        self.emotion_status.config(text="Arrêté", fg="red")

        self.is_running = False
        self.is_analyzing = False  # Arrêter le thread d'analyse
        self.camera.release()

        self.video_label.config(image="")
        self.hide_button_afer_stop()

    def start_game_placeholder(self):
        print("Signal : Démarrage du jeu")

        if self.is_running:
            print("Arrêt automatique de la caméra pour le jeu...")
            self.stop_cam_placeholder()

        if self.btn_game:
            self.btn_game.pack_forget()
        self.btn_end_game.pack(pady=10, padx=20, fill='x')
        game_thread = threading.Thread(
            target=create_fruit_ninja_game,
            daemon=True
        )
        game_thread.start()

    def end_game_placeholder(self):
        print("Signal : Arrêt du jeu")
        if self.btn_end_game:
            self.btn_end_game.pack_forget()
        self.btn_game.pack(pady=10, padx=20, fill='x')

    def create_button_afer_start(self):
        if self.btn_start:
            self.btn_start.pack_forget()
        if self.btn_stop:
            self.btn_stop.pack(pady=10, padx=20, fill='x')
        if self.btn_game:
            self.btn_game.pack(pady=10, padx=20, fill='x')

    def hide_button_afer_stop(self):
        if self.btn_stop:
            self.btn_stop.pack_forget()
        #if self.btn_game:
            #self.btn_game.pack_forget()
        if self.btn_end_game:
            self.btn_end_game.pack_forget()
        self.btn_start.pack(pady=10, padx=20, fill='x', after=self.emotion_status)

    def background_analysis(self):
        """Boucle tournant dans un thread séparé"""
        while self.is_analyzing:
            if not self.frame_queue.empty():
                frame_to_analyze = self.frame_queue.get()
                results = self.detector.analyze(frame_to_analyze)
                for r in results:
                    for key in ['x', 'y', 'w', 'h']:
                        r.region[key] *= 2

                self.last_results = results
                self.stats.extraire_stats_essentielles(results)
            else:
                time.sleep(0.01)  # Petite pause pour éviter de saturer le CPU

    def update_loop(self):
        if self.is_running:
            ret, frame = self.camera.read()
            if ret:
                if self.frame_queue.empty():
                    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                    self.frame_queue.put(small_frame)
                self.visualizer.draw_results(frame, self.last_results)

                if self.last_results:
                    top_emotion = self.last_results[0].dominant_emotion
                    self.emotion_status.config(text=f"Émotion : {top_emotion}", fg="#2ecc71")
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            self.root.after(10, self.update_loop)

    def on_closing(self):
        self.is_running = False
        self.camera.release()
        self.root.destroy()

    def get_latest_frame(self):
        if self.camera:
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()