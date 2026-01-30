from pathlib import Path

import pygame

from .fruitType import TypeFruit

base_dir = Path(__file__).resolve().parent.parent.parent
assets_dir = base_dir / "assets" / "fruits"
class Fruit:
    def __init__(self, fruitType: TypeFruit, position=(100, 100), speed=5):
        from pathlib import Path
        import pygame

        self.isCut = False
        self.fruitType = fruitType
        self.position = list(position)
        self.speed = speed

        # Chemin absolu vers assets/fruits/
        base_dir = Path(__file__).resolve().parent.parent
        assets_dir = base_dir / "assets" / "fruits"

        self.image_whole = pygame.image.load(str(assets_dir / f"{fruitType.value}.png")).convert_alpha()
        self.image_cut_1 = pygame.image.load(str(assets_dir / f"{fruitType.value}_half_1.png")).convert_alpha()

        self.image_whole = pygame.transform.smoothscale(self.image_whole, (self.image_whole.get_width() // 2,
                                                                           self.image_whole.get_height() // 2))
        self.image_cut_1 = pygame.transform.smoothscale(self.image_cut_1, (self.image_cut_1.get_width() // 2,
                                                                           self.image_cut_1.get_height() // 2))

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

    def get_box(self):
        return (
            self.rect.left,
            self.rect.top,
            self.rect.right,
            self.rect.bottom
        )

    def collides_with_hand(self, hand_box):
        fruit_rect = self.rect
        print(hand_box)

        for (x1, y1, x2, y2) in hand_box:
            hand_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)

            if fruit_rect.colliderect(hand_rect):
                print("collisionnnnnnnn")
                return True

        return False


if __name__ == "__main__":
    #exemple d'initialisation
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Fruit Tombe")
    clock = pygame.time.Clock()

    # ---------- Crée un fruit ----------
    fruit = Fruit(fruitType=TypeFruit.APPLE, position=(100,100),speed=5)

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
