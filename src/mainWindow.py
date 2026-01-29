import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Detecteur d'emotion")
        self.root.geometry("1000x600")
        self.root.configure(bg="#252033")

        self.create_header()
        self.create_video_frame()
        self.setup_controls()

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
        self.control_panel.pack(side="right", fill="y")

        tk.Label(self.control_panel, text="STATISTIQUES", font=("Helvetica", 12, "bold"), bg="#ecf0f1").pack(pady=10)

        self.emotion_status = tk.Label(self.control_panel, text="Attente...", font=("Helvetica", 14), bg="#ecf0f1",
                                       fg="#e67e22")
        self.emotion_status.pack(pady=20)

        ttk.Separator(self.control_panel, orient='horizontal').pack(fill='x', padx=10, pady=10)

        self.btn_start = ttk.Button(self.control_panel, text="Lancer Caméra", command=self.start_cam_placeholder)
        self.btn_start.pack(pady=10, padx=20, fill='x')

        self.btn_quit = ttk.Button(self.control_panel, text="Quitter", command=self.root.quit)
        self.btn_quit.pack(side="bottom", pady=20, padx=20, fill='x')



    def start_cam_placeholder(self):
        print("Signal : Démarrage de la caméra...")
        self.create_button_afer_start()

        self.emotion_status.config(text="Analyse en cours", fg="green")

    def stop_cam_placeholder(self):
        print("Signal : Arrêt de la caméra...")
        self.hide_button_afer_stop()
        self.emotion_status.config(text="Arrêté", fg="red")

    def start_game_placeholder(self):
        print("Signal : Démarrage du jeu")
        self.btn_end_game = ttk.Button(self.control_panel, text="Arrêter Jeu", command=self.end_game_placeholder)
        self.btn_end_game.pack(pady=10, padx=20, fill='x')


    def end_game_placeholder(self):
        print("Signal : Arrêt du jeu")
        self.btn_end_game.pack_forget()

    def create_button_afer_start(self):
        self.btn_stop = ttk.Button(self.control_panel, text="Arrêter", command=self.stop_cam_placeholder)
        self.btn_stop.pack(pady=10, padx=20, fill='x')

        self.btn_game = ttk.Button(self.control_panel, text="Lancer Jeu", command=self.start_game_placeholder)
        self.btn_game.pack(pady=10, padx=20, fill='x')


    def hide_button_afer_stop(self):
        self.btn_stop.pack_forget()
        self.btn_game.pack_forget()
        self.btn_end_game.pack_forget()




if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()