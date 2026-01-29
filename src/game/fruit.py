import pygame

import fruitType


class Fruit:
    def __init__(self, fruitType: fruitType, position=(100, 100),speed=5):
        self.isCut = False
        self.fruitType = fruitType
        self.position = list(position)
        self.speed = speed
        self.image_whole = pygame.image.load(f"../assets/fruits/{fruitType.value}.png").convert_alpha()
        self.image_cut_1 = pygame.image.load(f"../assets/fruits/{fruitType.value}_half_1.png").convert_alpha()

        self.current_image = self.image_whole
        self.rect = self.current_image.get_rect(center=self.position)

    def cut(self):
        self.isCut = True
        self.current_image = self.image_cut_1

    def move(self):
        self.position[1] += self.speed
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.current_image, self.rect)


if __name__ == "__main__":
    #exemple d'initialisation
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Fruit Tombe")
    clock = pygame.time.Clock()

    # ---------- Crée un fruit ----------
    fruit = Fruit(fruitType=fruitType.TypeFruit.APPLE, position=(100,100),speed=5)

    # ---------- Boucle principale ----------
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mise à jour
        fruit.move()

        # Affichage
        screen.fill((0, 0, 0))  # fond noir
        fruit.draw(screen)
        pygame.display.flip()

        clock.tick(60)  # 60 FPS

    pygame.quit()
