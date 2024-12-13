import socket
import time

import msgpack
import pygame

from jnjclient.graphics import Drawer, Camera
from jnjclient.server_updates_handler import ServerUpdatesHandler


class Client:
    """Клиент

    Класс для обмена данными с сервером.

    Attributes:
        ip: (str): IP.
        port (int): Порт.
        running (bool): Работает ли клиент.
        sock (socket): Сокет клиента.
        screen (Surface): Экран pygame.
        clock (Clock): Часы.
        server (ServerUpdatesHandler): Обработчик обновлений сервера.
        id (str): ID игрока.
        camera (Camera): Камера.
        drawer (Drawer): Рисовальщик
    """

    def __init__(self, ip: str, port: int):
        """Клиент

        Класс для обмена данными с сервером.

        Args:
            ip (str): IP сервера.
            port (int): Порт сервера.
        """
        self.ip = ip
        self.port = port

        self.running = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto("connection".encode(), (ip, port))

        pygame.init()
        pygame.display.set_caption("John 'n' Josh")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.server = None
        self.id = None

        self.camera = Camera(32)
        self.drawer = Drawer(self.camera, self.screen)

    def receive_startup_data(self):
        """Получить обновления сервера.

        Получяет обновления, присылаемые сервером, обрабатывает их.
        """
        startup_data = self.sock.recv(65536)
        startup_data = msgpack.unpackb(startup_data)
        self.server = ServerUpdatesHandler(startup_data)
        self.id = self.server.id
        pygame.display.set_caption(self.id.upper())

    def start(self):
        """Запустить клиент.
        Запускает клиент.
        Отправляет запрос на подключение серверу.
        При готовности запускает цикл.
        """
        self.receive_startup_data()

        walking = False
        jumping = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_w, pygame.K_SPACE]:
                        jumping = True

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                walking = "left"
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                walking = "right"
            else:
                walking = False

            self.sock.sendto(msgpack.packb(
                {
                    "player": self.id,
                    "walking": walking,
                    "jumping": jumping
                }
            ), (self.ip, self.port))
            jumping = False

            try:
                update_data = self.sock.recv(1024)
                update_data = msgpack.unpackb(update_data)
                if update_data["type"] == "update":
                    self.server.process_update(update_data)
                elif update_data["type"] == "game_over":
                    self.drawer.draw_game_over(update_data)
                    pygame.time.wait(10000)
                    pygame.quit()
                    break
            except:
                pass

            self.camera.update(self.server.player_entity)
            self.drawer.draw(self.server.princess, self.server.grid, self.server.entities, self.server.player_entity)
