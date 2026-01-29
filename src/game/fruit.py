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
        base_dir = Path(__file__).resolve().parent.parent.parent
        assets_dir = base_dir / "assets" / "fruits"

        # Affichage de débogage
        print(f"Chemin des assets : {assets_dir}")
        print(f"Fichiers dans assets/fruits : {[f.name for f in assets_dir.iterdir()]}")
        print(f"Recherche de : {fruitType.value}.png")

        # Chargement des images avec gestion d'erreur
        print(str(assets_dir / f"{fruitType.value}.png"))

        self.image_whole = pygame.image.load(str(assets_dir / f"{fruitType.value}.png")).convert_alpha()
        self.image_cut_1 = pygame.image.load(str(assets_dir / f"{fruitType.value}_half_1.png")).convert_alpha()


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
