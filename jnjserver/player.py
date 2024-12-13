from jnjserver.entity import Entity


class Player:
    """Игрок.

    Класс, предоставляющий интерфейс взаимодействия сервера с сущностью игрока.

    Attributes:
        id (str): ID игрока ("john", "josh").
        sock (socket): сокет.
        address (Any): адрес.
        entity: (Entity): сущность.
    """

    def __init__(self, player_id: str, sock, address, entity: Entity):
        """Игрок

        Args:
            player_id (str): ID игрока ("john", "josh")
            sock (_type_): _description_
            address (_type_): _description_
            entity (Entity): _description_
        """
        self.id = player_id
        self.sock = sock
        self.address = address
        self.entity = entity

    def process_input(self, player_input: dict):
        """Обработать данные ввода

        Обрабатывает данные присланные с клиента. Отвечает за команды движения сущности игрока.

        Args:
            player_input (dict): Данные ввода
        """
        if player_input["walking"]:
            self.entity.walk(player_input["walking"], 0.24)
        if player_input["jumping"]:
            self.entity.jump(1.1)

    def send_data(self, data: dict):
        """Отправить данные клиенту

        Отправляет данные клиенту, связанному с игроком.

        Args:
            data (dict): Данные для отправки
        """
        self.sock.sendto(data, self.address)
