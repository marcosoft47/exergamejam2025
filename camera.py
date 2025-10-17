import cv2
import settings


class Camera:
    def __init__(self):
        # Load camera
        self.cap = cv2.VideoCapture(0)
        self.ret, self.frame = self.cap.read()

        # Get actual webcam resolution
        if self.ret:
            altura_webcam, largura_webcam, _ = self.frame.shape
            settings.largura_webcam = largura_webcam
            settings.altura_webcam = altura_webcam
            print(f"Webcam resolution: {largura_webcam}x{altura_webcam}")

    def load_camera(self):
        self.ret, self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame, 1)

        cv2.line(
            self.frame,
            (settings.pontos_calibracao[0]),
            (settings.pontos_calibracao[1]),
            (settings.verde),
            2,
        )
        cv2.line(
            self.frame,
            (settings.pontos_calibracao[1]),
            (settings.pontos_calibracao[3]),
            (settings.verde),
            2,
        )
        cv2.line(
            self.frame,
            (settings.pontos_calibracao[2]),
            (settings.pontos_calibracao[0]),
            (settings.verde),
            2,
        )
        cv2.line(
            self.frame,
            (settings.pontos_calibracao[2]),
            (settings.pontos_calibracao[3]),
            (settings.verde),
            2,
        )

        cv2.circle(self.frame, (settings.pontos_calibracao[0]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[1]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[2]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[3]), 5, settings.azul, 3)

    def display_camera(self):
        cv2.imshow("Tela de Captura", self.frame)
        cv2.waitKey(1)

    def close_camera(self):
        self.cap.release()
        cv2.destroyWindow("Tela de Captura")
