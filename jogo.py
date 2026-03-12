# pyinstaller --onefile --name "Gingada Divina" --icon="assets/kairos_central.png" --hidden-import="mediapipe.solutions.pose" --hidden-import="mediapipe.solutions.pose_landmark" --add-data "assets;assets" --add-data "[caminho mediapipe];mediapipe" jogo.py

import os
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_q

import flecha
from pose_tracking import PoseTracking
import sequencia
from settings import path_assets, tamanho_tela, fps, resource_path, getModo, setModo

import calibrate
from camera import Camera


class Jogo:
    def __init__(self):
        pygame.init()

        self.pose_tracking = PoseTracking()
        self.cap = Camera()

        ########
        # Metade das coisas aqui podem ir para settings.py
        # Alguém devia resolver isso .-.
        ########

        self.running = True
        self.tamanho = tamanho_tela
        self.score = 0
        self.changeSpeedThreshold = 8
        self.feedback = None
        self.superficie = pygame.display.set_mode(
            size=self.tamanho, flags=pygame.FULLSCREEN, display=0
        )

        pygame.display.set_caption("exergamejam")
        self.origin = (0, 0, 0)
        self.fonte = pygame.font.SysFont("aakar", 35) 

        self.imagemEsteira = pygame.image.load(resource_path(os.path.join(path_assets, "esteira-resize.png")))
        self.imagemMoldura = pygame.image.load(resource_path(os.path.join(path_assets, "fundo.png")))
        self.imagemKairos = pygame.image.load(resource_path(os.path.join(path_assets, "kairos_central.png")))

        self.menuBackgroundAsset = pygame.image.load(resource_path(os.path.join(path_assets, "background_temple.png")))
        self.startButtonAsset = pygame.image.load(resource_path(os.path.join(path_assets, "start.png")))
        self.rankingButtonAsset = pygame.image.load(resource_path(os.path.join(path_assets, "ranking.png")))

        self.somCerto = pygame.mixer.Sound(os.path.join(path_assets, "snd_dumbvictory.wav"))
        self.somCerto.set_volume(0.2)
        self.somErrado = pygame.mixer.Sound(os.path.join(path_assets, "snd_hurt1.wav"))
        songs = {
            "sangueferve": {
                "name": "Sidney Magal",
                "file": "sangueferve.mp3",
                # "file": "snd_dumbvictory.wav",
                "bpm": 167.61,
                "offset": 0.3,
            },
            # 'timmaia': {
            #     'name': 'Tim Maia',
            #     'file': 'timmaia.mp3',
            #     'bpm': 139.53, # double beat
            #     'offset': 0.35
            # }
        }
        self.song = random.choice(list(songs.values()))
        self.musica_acabou = pygame.USEREVENT

        #  N
        # O L
        #  S
        __N = 220
        __S = 450
        __L = 490
        __O = 180
        self.flechaNO = flecha.Flecha(
            x=__O,
            y=__N,
            image=pygame.image.load(resource_path(os.path.join(path_assets, "seta_copas.png"))),
            number=1,
        )
        self.flechaSO = flecha.Flecha(
            x=__O,
            y=__S,
            image=pygame.image.load(resource_path(os.path.join(path_assets, "seta_paus.png"))),
            number=2,
        )
        self.flechaSL = flecha.Flecha(
            x=__L,
            y=__S,
            image=pygame.image.load(resource_path(os.path.join(path_assets, "seta_ouros.png"))),
            number=3,
        )
        self.flechaNL = flecha.Flecha(
            x=__L,
            y=__N,
            image=pygame.image.load(resource_path(os.path.join(path_assets, "seta_espadas.png"))),
            number=4,
        )
        self.corApertandoNO = (0, 0, 0)
        self.corApertandoSO = (0, 0, 0)
        self.corApertandoSL = (0, 0, 0)
        self.corApertandoNL = (0, 0, 0)

        self.next = sequencia.Sequencia(
            tamanho_tela[0]//2,
            -200,
            self.song['bpm'],
            offset=self.song['offset']
        )
        self.totalAcertos = [[0,0],[0,0],[0,0],[0,0]]

    def menu(self):
        in_menu = True
        modo = getModo(True)
        clock = pygame.time.Clock()

        button_width = 256
        button_height = 96
        button_spacing = 20

        start_button_x = (self.tamanho[0] - button_width) // 2
        start_button_y = (
            (self.tamanho[1] - button_height) // 2
            - (button_height // 2)
            - (button_spacing // 2)
            + button_height
            + button_spacing
        )
        start_button_rect = pygame.Rect(
            start_button_x, start_button_y, button_width, button_height
        )

        ranking_button_x = (self.tamanho[0] - button_width) // 2
        ranking_button_y = start_button_y + button_height + button_spacing
        ranking_button_rect = pygame.Rect(
            ranking_button_x, ranking_button_y, button_width, button_height
        )

        # Disabled for now
        ranking_button_disabled = self.rankingButtonAsset.copy()
        ranking_button_disabled.set_alpha(100)

        while in_menu and self.running:
            clock.tick(fps)
            self.load_camera()
            self.get_feet_position()
            self.cap.display_camera()  # Display AFTER skeleton is drawn

            x, y = self.pose_tracking.get_feet_center()
            left_foot_x, left_foot_y = self.pose_tracking.get_left_foot()
            right_foot_x, right_foot_y = self.pose_tracking.get_right_foot()

            # Show raw normalized coordinates too
            # if self.pose_tracking.pose_detected:
            #     raw_l = f"({self.pose_tracking.feet1_x:.2f}, {self.pose_tracking.feet1_y:.2f})"
            #     raw_r = f"({self.pose_tracking.feet2_x:.2f}, {self.pose_tracking.feet2_y:.2f})"
            # else:
            #     raw_l = raw_r = "N/A"

            #print(
            #    f"Pose: {self.pose_tracking.pose_detected} | "
            #    f"InCal: {self.pose_tracking.feet_in_calibration_area} | "
            #    f"Center: ({x}, {y}) | "
            #    f"Left: ({left_foot_x}, {left_foot_y}) raw:{raw_l} | "
            #    f"Right: ({right_foot_x}, {right_foot_y}) raw:{raw_r}"
            #)

            # Check if feet center is over start button
            if x is not None and y is not None:
                if start_button_rect.collidepoint(x, y):
                    in_menu = False

            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(e.pos):
                        in_menu = False
                    if ranking_button_rect.collidepoint(e.pos):
                        in_menu = False
                if e.type == KEYDOWN:
                    if e.key == pygame.K_1:
                        setModo('classico')
                    if e.key == pygame.K_2:
                        setModo('ambos')
                    if e.key == pygame.K_3:
                        setModo('esquerdo')
                    if e.key == pygame.K_4:
                        setModo('direito')
                    
                    modo = getModo(True) 

                    if e.key == pygame.K_c:
                        calibrate.calibrar_ttea()
                    if e.key == pygame.K_ESCAPE:
                        self.running = False

            self.superficie.fill(self.origin)
            self.superficie.blit(self.menuBackgroundAsset, (0, 0))

            self.superficie.blit(
                self.startButtonAsset, (start_button_x, start_button_y)
            )

            self.superficie.blit(self.fonte.render(f'Modo de Jogo: {modo}', True, (255,255,255)), (200, 200))

            # self.superficie.blit(
            #     self.rankingButtonAsset, (ranking_button_x, ranking_button_y)
            # )

            # Draw circles around feet positions
            self.draw_circle()

            pygame.display.update()

    def run(self):
        # Mainloop
        input = 0
        points = 0
        streak = 0
        self.feedback = None
        self.next.hardreset()

        clock = pygame.time.Clock()
        gaming = True

        pygame.mixer.music.load(os.path.join(path_assets, self.song["file"]))
        pygame.mixer.music.play()


        # Initialize clock to prevent large first dt value
        clock.tick()

        while self.running and gaming:
            dt_ms = clock.tick(fps)
            dt = dt_ms / 1000.0

            # ----- Eventos -----
            gaming = pygame.mixer.music.get_busy()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.running = False
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.running = False
                    if e.key == K_q:
                        pygame.mixer.music.stop()
                        gaming = False

            # ----- Update camera and feet position -----
            self.load_camera()
            self.get_feet_position()
            self.cap.display_camera()

            left_foot_x, left_foot_y = self.pose_tracking.get_left_foot()
            right_foot_x, right_foot_y = self.pose_tracking.get_right_foot()

            # ----- Update -----
            # Check mouse input (original)
            if self.flechaNO.update() != 0:
                input = self.flechaNO.number  # 1
            elif self.flechaNL.update() != 0:
                input = self.flechaNL.number  # 4
            elif self.flechaSO.update() != 0:
                input = self.flechaSO.number  # 2
            elif self.flechaSL.update() != 0:
                input = self.flechaSL.number  # 3

            # Check feet input (new - alternative)
            if input == 0:
                # Check left foot
                left_foot_input = self.check_foot_on_arrow(left_foot_x, left_foot_y)
                right_foot_input = self.check_foot_on_arrow(right_foot_x, right_foot_y)

                modo = getModo()
                if modo == 'classico':
                    if left_foot_input != 0: # Eu não lembro porque faz essa verificação. Averigue a situação
                        input = left_foot_input
                    else:
                        # Check right foot
                        if right_foot_input != 0:
                            input = right_foot_input

                elif modo == 'ambos':
                    if left_foot_input != 0 and left_foot_input == right_foot_input:
                        input = left_foot_input
                
                elif modo == 'esquerdo':
                    input = left_foot_input

                elif modo == 'direito':
                    input = right_foot_input

            self.next.update(dt)

            
            # Verifica se foi apertado o botão certo
            if self.next.next == input and self.next.rect.y >= 10:
                if 10 <= self.next.rect.y < 40 or  100 < self.next.rect.y <= 130:
                    self.feedback = "Quase"
                    points = 1
                    self.next.acertou()
                elif 40 <= self.next.rect.y <= 55 or 85 <= self.next.rect.y <= 100:
                    self.feedback = "Boa!"
                    points = 5
                    self.next.acertou()
                elif 55 < self.next.rect.y < 85:
                    self.feedback = "Perfeito!!"
                    points = 10
                    self.next.acertou()
                    # self.somCerto.play() # Still can't find a not annoying sfx
                
                streak = streak + 1 if -2 <= speed < 2 else streak
                self.score += points
            
            if self.next.rect.y > 130:
                self.feedback = ""
                streak = streak - 1 if -2 < speed <= 2 else streak
                self.feedback = "Tarde demais!"
                self.next.errou()
            
            if (streak % self.changeSpeedThreshold == 0):
                speed = streak // self.changeSpeedThreshold
                self.next.changeSpeed(speed)
            # elif input != 0:
            #     self.feedback = "Miss"
            #     points = 0
            #     self.somErrado.play()
            #     pass

            input = 0

            # ----- Render -----
            self.superficie.fill(self.origin)
            self.superficie.blit(self.imagemMoldura, (0, 0))
            self.superficie.blit(
                self.fonte.render(f"Artista: {self.song['name']}", True, (255, 255, 255)),
                (25, 25),
            )
            self.superficie.blit(
                self.fonte.render(f"Velocidade: {speed}", True, (255, 255, 255)),
                (25, 60),
            )
            self.superficie.blit(
                self.fonte.render(f"Pontuação: {self.score}", True, (255, 255, 255)),
                (25, 95),
            )
            if self.feedback:
                self.superficie.blit(
                    self.fonte.render(f"{self.feedback}", True, (255, 255, 255)),
                    (25, 130),
                )
            self.superficie.blit(self.imagemEsteira, (tamanho_tela[0] // 2 - 75, -50))

            
            self.render_flechas()
            self.next.render(self.superficie)

            # Draw feet circles
            self.draw_circle()


            pygame.display.update()

    
    def finish(self):
        if self.running:
            clock = pygame.time.Clock()
            count = 0
            while count < 60*7:
                clock.tick(60)
                for e in pygame.event.get():
                    if e.type == KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            self.running = False
                self.superficie.fill(self.origin)
                self.superficie.blit(self.imagemMoldura, (0, 0))
                self.superficie.blit(self.fonte.render(f'Parabéns!!', True, (255,255,255)), (25, 25))
                self.superficie.blit(self.fonte.render(f'Pontuação: {self.score}', True, (255,255,255)), (25, 60))
                self.render_flechas()

                NOPos = list(self.flechaNO.getPos())
                NOPos[1] -= 35
                NOPos = tuple(NOPos)
                NOPct = self.next.getPercentage(0)

                SOPos = list(self.flechaSO.getPos())
                SOPos[1] -= 35
                SOPos = tuple(SOPos)
                SOPct = self.next.getPercentage(1)

                SLPos = list(self.flechaSL.getPos())
                SLPos[1] -= 35
                SLPos = tuple(SLPos)
                SLPct = self.next.getPercentage(2)

                NLPos = list(self.flechaNL.getPos())
                NLPos[1] -= 35
                NLPos = tuple(NLPos)
                NLPct = self.next.getPercentage(3)

                self.superficie.blit(self.fonte.render(f'Acertos: {self.next.pontos[0][1]}/{self.next.pontos[0][0]} ({NOPct}%)', True, (255,255,255)), NOPos)
                self.superficie.blit(self.fonte.render(f'Acertos: {self.next.pontos[1][1]}/{self.next.pontos[1][0]} ({SOPct}%)', True, (255,255,255)), SOPos)
                self.superficie.blit(self.fonte.render(f'Acertos: {self.next.pontos[2][1]}/{self.next.pontos[2][0]} ({SLPct}%)', True, (255,255,255)), SLPos)
                self.superficie.blit(self.fonte.render(f'Acertos: {self.next.pontos[3][1]}/{self.next.pontos[3][0]} ({NLPct}%)', True, (255,255,255)), NLPos)

                pygame.display.flip()
                count += 1
            count = 0
            self.score = 0

    def load_camera(self):
        self.cap.load_camera()

    def render_flechas(self):
        self.flechaNO.render(self.superficie)
        self.flechaNL.render(self.superficie)
        self.flechaSO.render(self.superficie)
        self.flechaSL.render(self.superficie)

    def draw_circle(self):
        x, y = self.pose_tracking.get_feet_center()
        left_foot_x, left_foot_y = self.pose_tracking.get_left_foot()
        right_foot_x, right_foot_y = self.pose_tracking.get_right_foot()
        if left_foot_x is not None and left_foot_y is not None:
            # Blue filled circle for left foot
            pygame.draw.circle(
                self.superficie,
                (0, 0, 255),
                (int(left_foot_x), int(left_foot_y)),
                30,
                0,
            )

        if right_foot_x is not None and right_foot_y is not None:
            # Red filled circle for right foot
            pygame.draw.circle(
                self.superficie,
                (255, 0, 0),
                (int(right_foot_x), int(right_foot_y)),
                30,
                0,
            )

        if x is not None and y is not None:
            # Green filled circle for center
            pygame.draw.circle(
                self.superficie, (0, 255, 0), (int(x), int(y)), 35, 0
            )

    def get_feet_position(self):
        self.cap.frame = self.pose_tracking.scan_feets(self.cap.frame)
        return self.pose_tracking.get_feet_center()

    def check_foot_on_arrow(self, foot_x, foot_y):
        """Check if a foot is over any arrow and return the arrow number (1-4) or 0"""
        if foot_x is None or foot_y is None:
            return 0

        foot_point = (foot_x, foot_y)

        if self.flechaNO.rect.collidepoint(foot_point):
            return self.flechaNO.number  # 1
        elif self.flechaNL.rect.collidepoint(foot_point):
            return self.flechaNL.number  # 4
        elif self.flechaSO.rect.collidepoint(foot_point):
            return self.flechaSO.number  # 2
        elif self.flechaSL.rect.collidepoint(foot_point):
            return self.flechaSL.number  # 3

        return 0


if __name__ == "__main__":
    g = Jogo()
    while g.running:
        g.menu()
        g.run()
        g.finish()

    pygame.quit()
