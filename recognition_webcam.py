import cv2
import numpy as np
import os
import pickle
import time
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


#   SISTEMA DE ACESSO
authorized_people = {"Breno", "IlleeSilva"}
last_access = {}

def access_control(name, cooldown=5):
    agora = time.time()

    if name not in authorized_people:
        return "Acesso NEGADO"

    if name in last_access and agora - last_access[name] < cooldown:
        return "Acesso já liberado"

    last_access[name] = agora
    return "Acesso LIBERADO"


#   CARREGA RECONHECEDOR
def load_recognizer(option, training_data):
    if option == "eigenfaces":
        face_classifier = cv2.face.EigenFaceRecognizer_create()
    elif option == "fisherfaces":
        face_classifier = cv2.face.FisherFaceRecognizer_create()
    else:
        face_classifier = cv2.face.LBPHFaceRecognizer_create()

    if not os.path.exists(training_data):
        raise FileNotFoundError("Arquivo de treinamento não encontrado")

    face_classifier.read(training_data)
    return face_classifier


recognizer_type = "lbph"
training_data = "lbph_classifier.yml"
threshold = 10e5

face_classifier = load_recognizer(recognizer_type, training_data)

with open("face_names.pickle", "rb") as f:
    original_labels = pickle.load(f)
    face_names = {v: k for k, v in original_labels.items()}


#   DETECTOR DE ROSTOS
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def recognize_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.1, 5)

    status = None

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (90, 120))

        pred, conf = face_classifier.predict(roi)

        name = face_names.get(pred, "Não identificado") if conf <= threshold else "Não identificado"

        status = access_control(name)

        color = (0,255,0) if status == "Acesso LIBERADO" else (0,0,255)

        cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    return frame, status

#   INTERFACE 
class FaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portaria Inteligente – Reconhecimento Facial")
        self.root.geometry("1000x800")
        self.root.configure(bg="#0d0d0d")

        self.running = False

        self.colors = {
            "bg": "#0d0d0d",
            "card": "#1a1a1a",
            "text": "#e6e6e6",
            "accent": "#4da6ff",
            "success": "#4dff88",
            "error": "#ff4d4d",
        }

        self.build_ui()

    #   UI
    def build_ui(self):

        top = tk.Frame(self.root, bg="#111", height=70)
        top.pack(fill="x")

        tk.Label(
            top,
            text="🛂 PORTARIA INTELIGENTE",
            fg=self.colors["accent"],
            bg="#111",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=10)

        card = tk.Frame(self.root, bg=self.colors["card"], bd=2, relief="ridge")
        card.pack(pady=20, padx=20)

        self.video_label = tk.Label(card, bg=self.colors["card"])
        self.video_label.pack(pady=20, padx=20)

        self.status_label = tk.Label(
            card,
            text="Sistema parado",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 20, "bold")
        )
        self.status_label.pack(pady=20)

        buttons = tk.Frame(self.root, bg=self.colors["bg"])
        buttons.pack(pady=15)

        self.create_button(buttons, "▶ Iniciar Reconhecimento", self.start).pack(pady=10)
        self.create_button(buttons, "■ Parar", self.stop, variant="danger").pack(pady=10)
        self.create_button(buttons, "✖ Sair", self.exit, variant="danger").pack(pady=10)


    #   BOTÕES
    def create_button(self, parent, text, cmd, variant="normal"):
        color_normal = "#333" if variant=="normal" else "#661111"
        color_hover  = "#444" if variant=="normal" else "#882222"

        btn = tk.Label(
            parent,
            text=text,
            bg=color_normal,
            fg="white",
            font=("Segoe UI", 14, "bold"),
            padx=25,
            pady=12,
            cursor="hand2"
        )
        btn.bind("<Button-1>", lambda e: cmd())
        btn.bind("<Enter>", lambda e: btn.config(bg=color_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=color_normal))

        return btn


    #   CONTROLE
    def start(self):
        if self.running:
            return
        self.running = True
        threading.Thread(target=self.loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.status_label.config(text="Sistema parado", fg=self.colors["text"])

    def exit(self):
        self.running = False
        self.root.quit()

    #   LOOP DE VÍDEO
    def loop(self):
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a câmera!")
            return

        while self.running:
            ret, frame = cam.read()
            if not ret:
                break

            frame, status = recognize_faces(frame)

            if status:
                if status == "Acesso LIBERADO":
                    self.status_label.config(text=status, fg=self.colors["success"])
                elif status == "Acesso NEGADO":
                    self.status_label.config(text=status, fg=self.colors["error"])
                else:
                    self.status_label.config(text=status, fg=self.colors["accent"])

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(rgb))

            self.video_label.config(image=img)
            self.video_label.image = img

        cam.release()


#   MAIN
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceApp(root)
    root.mainloop()
