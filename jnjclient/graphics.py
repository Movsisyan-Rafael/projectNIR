import pygame
from typing import List

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Camera:
    """Камера.

    Используется для определения сдвига при отрисовке мира.

    Attributes:
        x (int): Координата x.
        y (int): Координата y.
        z (int): Коэффициент масштабирования.
    """

    def __init__(self, z=8):
        """Камера.

        Используется для определения сдвига при отрисовке мира.

        Args:
            z (int, optional): Коэффициент масштабирования. По умолчанию 8.
        """
        self.x = 0
        self.y = 0
        self.z = z

    def update(self, player):
        """Обновить состояние камеры.

        Изменение координат камеры на координаты предоставленного игрока.

        Args:
            player (dict): Игрок.
        """
        self.x = player["position"]["x"]
        self.y = player["position"]["y"]


class Drawer:
    """Рисовальщик.

    Класс отвечающий за отрисовку игрового мира и внутриигрового интерфейса.

    Attributes:
        camera (Camera): Камера.
        screen (Surface): Экран pygame.
        tile_images (dict): Словарь изображений плиток.
        heart_image (Surface): Изображение сердца (для отображения здоровья).
        checkpoint_active_image (Surface): Изображение активного чекпоинта.
        checkpoint_inactive_image (Surface): Изображение неактивного чекпоинта.
        princess_image (Surface): Изображение принцессы.
        player_images (dict): Словарь изображений игрока.
        boosts_names (dict): Словарь названий усилений.
        animation_frame (int): Текущий кадр анимации.
        font (Font): Обычный шрифт.
        game_over_font (Font): Шрифт экрана конца игры.

    """

    def __init__(self, camera, screen):
        """Рисовальщик.

        Класс отвечающий за отрисовку игрового мира и внутриигрового интерфейса.

        Args:
            camera (Camera): Камера.
            screen (Surface): Экран pygame.
        """
        self.camera = camera
        self.screen = screen
        self.tile_images = {
            "dirt": pygame.image.load("jnjclient/assets/textures/tiles/dirt.png"),
            "grass": pygame.image.load("jnjclient/assets/textures/tiles/grass.png"),
            "bricks": pygame.image.load("jnjclient/assets/textures/tiles/bricks.png"),
            "crate": pygame.image.load("jnjclient/assets/textures/tiles/crate.png"),
            "upgrade": pygame.image.load("jnjclient/assets/textures/tiles/upgrade.png"),
        }

        self.heart_image = pygame.transform.scale(pygame.image.load("jnjclient/assets/textures/heart.png"), (32, 32))
        self.checkpoint_active_image = pygame.image.load("jnjclient/assets/textures/checkpoint_active.png")
        self.checkpoint_inactive_image = pygame.image.load("jnjclient/assets/textures/checkpoint_inactive.png")
        self.princess_image = pygame.image.load("jnjclient/assets/textures/princess.png")

        self.player_images = {
            "default": pygame.image.load("jnjclient/assets/textures/player/player_default.png"),
            "jump": pygame.image.load("jnjclient/assets/textures/player/player_jump.png"),
            "run_0": pygame.image.load("jnjclient/assets/textures/player/player_run_0.png"),
            "run_1": pygame.image.load("jnjclient/assets/textures/player/player_run_1.png")
        }

        self.boosts_names = {
            "jump_boost": "Усиление прыжка",
            "speed_boost": "Увеличение скорости",
            "double_jump": "Двойной прыжок",
            "breaking_through": "Пробитие"
        }

        self.animation_frame = 0

        self.font = pygame.font.SysFont(None, 32)
        self.game_over_font = pygame.font.SysFont(None, 72)

    def draw_image(self, image, pos):
        """Нарисовать извображение.

        Рисует предоставленное изображение на предоставленных координатах относительно камеры.

        Args:
            image (Surface): Изображение pygame.
            pos (dict): Словарь с координатами.
        """
        image = pygame.transform.scale(image, (
            image.get_size()[0] * self.camera.z / 16, image.get_size()[1] * self.camera.z / 16))
        self.screen.blit(image, ((pos["x"] - self.camera.x) * self.camera.z + SCREEN_WIDTH / 2,
                                 (pos["y"] - self.camera.y) * self.camera.z + SCREEN_HEIGHT / 2))

    def draw_entity(self, entity: dict):
        """Нарисовать сущность.

        Рисут предоставленную сущность.

        Args:
            entity (dict): Словарь сущности.
        """
        if entity["type"] == "player":
            self.draw_player(entity)
        else:
            pass  # Заглущка

    def draw_player(self, entity: dict):
        """Нарисовать игрока.

        Рисует предоставленную сущность игрока.

        Args:
            entity (dict): Словарь игрока.
        """
        image = self.player_images["default"]
        if entity["velocity"]["x"] != 0:
            if self.animation_frame % 2 == 0:
                image = self.player_images["run_0"]
            else:
                image = self.player_images["run_1"]
        if not entity["is_on_ground"]:
            image = self.player_images["jump"]
        if entity["velocity"]["x"] < 0:
            image = pygame.transform.flip(image, 1, 0)
        self.draw_image(image, entity["position"])

    def update_animation_frame(self):
        """Обновить кадр анимации.

        Увеличивет свойство animation_frame на 1, сбрасывает до 0 при достижении 128.
        """
        self.animation_frame = (self.animation_frame + 1) % 128

    def draw_grid(self, grid: List[List[str]]):
        """Нарисовать сетку.

        Рисует сетку плиток ландшафта.

        Args:
            grid (List[List[str]]): Сетка плиток.
        """
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] != '':
                    self.draw_image(self.tile_images[grid[x][y]], {"x": x, "y": y})

    def draw_entities(self, entities: dict):
        """Нарисовать сущности.

        Рисует все сущности из предоставленного словаря.

        Args:
            entities (dict): Словарь сущностей.
        """
        for entity in entities.values():
            self.draw_entity(entity)

    def draw_health(self, entity: dict):
        """Нарисовать здоровье.

        Рисует здоровье предоставленной сущности в виде кол-ва сердечек в левом верхнем углу экрана.

        Args:
            entity (dict): Словарь сущности.
        """
        for i in range(entity["health"]):
            self.screen.blit(self.heart_image, (32 + i * 36, 32))

    def draw_boosts(self, entity: dict):
        """Нарисовать усиления.

        Рисует здорусиления предоставленной сущности в левом верхнем углу экрана под здоровьем.

        Args:
            entity (dict): Словарь сущности.
        """
        boosts = [boost for boost in entity["boosts"].keys() if entity["boosts"][boost]]
        row = 0
        for boost in boosts:
            img = self.font.render(self.boosts_names[boost] + ": " + str(int(entity["boosts"][boost] / 30)) + " секунд",
                                   True, (255, 0, 0))
            self.screen.blit(img, (32, 64 + row * 36))
            row += 1

    def draw_checkpoints(self, player_entity: dict):
        """Нарисовать чекпоинты.

        Рисует чекпоинты предоставленной сущности. Активный чекпоинт ярче.

        Args:
            player_entity (_type_): Словарь сущности.
        """
        for checkpoint in player_entity["checkpoints"]:
            image = self.checkpoint_inactive_image
            if checkpoint == player_entity["current_checkpoint"]:
                image = self.checkpoint_active_image
            self.draw_image(image, checkpoint)

    def draw_princess(self, princess: dict):
        """Нарисовать принцессу

        Рисует принцессу.

        Args:
            princess (dict): Словарь координат принцессы.
        """
        self.draw_image(self.princess_image, princess)

    def draw_game_over(self, game_over: dict):
        """Нарисовать экран завершения игры.

        Рисует экран завершения игры, содержащий победителя и проигравшего.

        Args:
            game_over (dict): Словарь конца игры.
        """
        self.screen.fill((0, 0, 0))
        image_row_1 = self.game_over_font.render(f"ИГРА ОКОНЧЕНА", True, (255, 0, 0))
        image_row_2 = self.game_over_font.render(f"ПОБЕДИЛ: {game_over['winner']}", True, (255, 0, 0))
        image_row_3 = self.game_over_font.render(f"ПРОИГРАЛ: {game_over['looser']}", True, (255, 0, 0))
        self.screen.blit(image_row_1, (128, 128))
        self.screen.blit(image_row_2, (128, 170))
        self.screen.blit(image_row_3, (128, 212))
        pygame.display.update()

    def draw(self, princess: dict, grid: List[List[str]], entities: dict, player_entity: dict):
        """Нарисовать кадр.

        Вызыват все методы отрисовки игрового мира в правильном порядке.

        Args:
            princess (dict): Словарь координат принцессы.
            grid (List[List[str]]): Сетка плиток.
            entities (dict): Словарь сущностей.
            player_entity (dict): Словарь сущности игрока.
        """
        self.screen.fill((192, 235, 255))
        self.draw_grid(grid)
        self.draw_checkpoints(player_entity)
        self.draw_entities(entities)
        self.draw_princess(princess)
        self.update_animation_frame()
        self.draw_health(player_entity)
        self.draw_boosts(player_entity)
        pygame.display.update()
