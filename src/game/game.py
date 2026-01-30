import cv2
import pygame
import random
from .fruit import Fruit
from src.IA.handDetector import HandPoseDetector
from .fruitType import TypeFruit


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fruits = []
        self.last_spawn = pygame.time.get_ticks()
        self.spawn_delay = 2000

    def spawn_fruit(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn >= self.spawn_delay:
            fruit_type = random.choice(list(TypeFruit))
            x_pos = random.randint(50, self.screen_width - 50)
            y_pos = 0
            self.fruits.append(Fruit(fruitType=fruit_type, position=(x_pos, y_pos), speed=5))
            self.last_spawn = current_time

    def update(self,hand_box):
        self.spawn_fruit()
        for fruit in self.fruits:
            fruit.move()
            if(fruit.collides_with_hand(hand_box)):
                self.fruits.remove(fruit)
                fruit.cut()

    def draw(self, screen, camera_surface):
        screen.blit(camera_surface, (0, 0))
        for fruit in self.fruits:
            fruit.draw(screen)

def create_game():
    pygame.init()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fruit Ninja Camera")
    clock = pygame.time.Clock()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    detector = HandPoseDetector()

    game = Game(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()
        if not ret:
            break


        # Détection YOLO
        detector.process(frame)
        hands_box = detector.get_hands_box()

        # Dessin OpenCV
        frame = detector.draw(frame)

        # Conversion OpenCV → Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0, 1)
        camera_surface = pygame.surfarray.make_surface(frame)

        game.update(hands_box)
        game.draw(screen, camera_surface)

        for (x1, y1, x2, y2) in hands_box:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (x1, y1, x2 - x1, y2 - y1),
                2
            )

        pygame.display.flip()
        clock.tick(60)

    cap.release()
    pygame.quit()
if __name__ == "__main__":
    create_game()