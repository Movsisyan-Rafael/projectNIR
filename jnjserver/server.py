import msgpack
import socket
import time
import pygame

from jnjserver.additional_data import *
from jnjserver.terrain import *
from jnjserver.entity import *
from jnjserver.world import *
from jnjserver.player import *


class Server:
    """Сервер.

    Класс реализующий общение с клиентами.

    Attributes:
        world (World): Мир.
        running (bool): Работает ли сервер.
        main_socket (socket): Сокет сервера.
        clock (Clock) Часы.
        ip: (str): IP.
        port (int): Порт.
        john (Player): Джон (игрок).
        josh (Player): Джош (игрок).
        players (List(Player)): Список игроков.


    """

    def __init__(self, ip: str, port: int):
        """Сервер.

        Класс реализующий общение с клиентами.
        Сервер работает на предоставленных IP и порту.

        Args:
            ip (str): IP сервера.
            port (int): Порт сервера.
        """
        tileset = TileSetLoader.load("jnjserver/tiles.json")
        entityset = EntitySetLoader.load("jnjserver/entities_types.json")
        terrain = TerrainLoader.load("jnjserver/terrain.csv")
        additional_data = AdditionalDataLoader.load("jnjserver/additional_data.json")
        self.world = World(tileset, entityset, terrain, additional_data)
        self.running = True
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.main_socket.bind((ip, port))
        self.main_socket.setblocking(True)

        self.clock = pygame.time.Clock()

        self.ip = ip
        self.port = port

        self.john = None
        self.josh = None
        self.players = []

    def connect_players(self):
        """Подключить игроков.

        Принимает попытки подключения игроками.
        Ожидает присоединения двух игроков.
        """
        player_ids = ['john', 'josh']

        while not (self.josh and self.john):
            try:
                message, address = self.main_socket.recvfrom(1024)

                player_id = player_ids[0]
                player_entity = Entity(self.world.entityset.get("player"), self.world.checkpoints[player_id][0].clone(),
                                       6)
                player_entity.player_id = player_id
                player_entity.checkpoints = self.world.checkpoints[player_id]
                player_entity.current_checkpoint = player_entity.checkpoints[0]
                self.world.add_entity(player_entity)
                player = Player(player_id, self.main_socket, address, player_entity)
                if player_id == "john":
                    self.john = player
                else:
                    self.josh = player
                print(f'Подключился ', address)
                player_ids = player_ids[1:]
            except:
                print("Ожидание игроков")
            time.sleep(1)
        self.players = [self.john, self.josh]

    def send_startup_data(self):
        """Отправить стартовые данные.
        
        Отправляет данные, нужные для начала работы клиентов.
        """
        print("Отправка стартовых данных")
        data_base = self.world.startup_data()

        for player in self.players:
            data = data_base
            data["player_entity"] = player.entity.dict()
            data["player_id"] = player.id
            player.send_data(msgpack.packb(data))

    def check_game_over(self):
        """Проверить условия завершения игры.

        Проверяет не закончились жизни у одного из игроков, или не коснулся ли один игрок принцессы.
        При выполнении условий, отправляет команду завершения игры на клиенты, выключает сервер и завершает программу.
        """
        for player_for_check in self.players:
            if player_for_check.entity.health <= 0:
                print("PIZDECNAHUY")
                self.running = False
                winner = self.players.copy()
                winner.remove(player_for_check)
                winner = winner[0]
                for player in self.players:
                    player.send_data(msgpack.packb({
                        "type": "game_over",
                        "looser": player_for_check.id.upper(),
                        "winner": winner.id.upper()
                    }))
                print(f"Игра окончена, победил {winner.id.upper()}")
                break
            if player_for_check.entity.is_in_princess:
                self.running = False
                looser = self.players.copy()
                looser.remove(player_for_check)
                looser = looser[0]
                for player in self.players:
                    player.send_data(msgpack.packb({
                        "type": "game_over",
                        "looser": looser.id.upper(),
                        "winner": player_for_check.id.upper()
                    }))
                print(f"Игра окончена, победил {player_for_check.id.upper()}")
                break

    def send_update_data(self):
        """Отправить обновления.

        Отправляет обновления клиентам. 
        """
        data_base = self.world.extract_updates()

        for player in self.players:
            try:
                data = data_base
                data["player_entity"] = player.entity.dict()
                player.send_data(msgpack.packb(data))
            except:
                pass

    def receive_players_input(self):
        """Получить данные о вводе с клиентов.

        Принимает данные о вводе с клиентов и передаёт игрокам для обработки.
        """
        for _ in range(len(self.players)):
            try:
                player_input = self.main_socket.recv(1024)
                player_input = msgpack.unpackb(player_input)
                if player_input["player"] == "john":
                    self.john.process_input(player_input)
                else:
                    self.josh.process_input(player_input)
            except:
                pass

    def start(self):
        """Запустить.

        Запускает сервер.
        """
        print(f"Запуск сервера, IP:{self.ip}, PORT:{self.port}")
        self.connect_players()
        self.send_startup_data()
        time.sleep(1)
        while self.running:
            self.receive_players_input()
            self.world.update()
            self.check_game_over()
            self.send_update_data()
            self.clock.tick(30)
