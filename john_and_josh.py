from tkinter import *
from tkinter import ttk
import socket
from jnjserver.server import Server
from jnjclient.client import Client
from threading import Thread


# Подключение
def join_game(ip: str, port: int):
    """Подключиться.

    Args:
        ip (str): IP.
        port (int): Порт.
    """
    root.destroy()
    client = Client(ip, port)
    client.start()


def create_game(port: int):
    """Создать игру.

    Args:
        port (int): Порт.
    """
    root.destroy()
    ip = socket.gethostbyname(socket.gethostname())
    server = Server(ip, port)
    Thread(target=server.start).start()
    client = Client(ip, port)
    client.start()


root = Tk()
root.title("J'n'J Launcher")
root.geometry("400x520")
root.resizable(False, False)

main_frame = ttk.Frame()

game_title_label = ttk.Label(main_frame, text="John 'n' Josh")
game_title_label.pack(anchor=N, padx=5, pady=5)

join_frame = ttk.Frame(main_frame, relief=SOLID, borderwidth=5)
join_label = ttk.Label(join_frame, text="Подключиться к игре")
join_label.pack(anchor=N, padx=5, pady=5)

join_ip_frame = ttk.Frame(join_frame)
join_ip_label = ttk.Label(join_ip_frame, text="Адрес:")
join_ip_label.pack(side=LEFT, padx=5, pady=5)
ip_var = StringVar()
join_ip_entry = ttk.Entry(join_ip_frame, textvariable=ip_var)
join_ip_entry.insert(END, socket.gethostbyname(socket.gethostname()))
join_ip_entry.pack(side=RIGHT, padx=5, pady=5)
join_ip_frame.pack(anchor=N, padx=5, pady=5, fill=X)

join_port_frame = ttk.Frame(join_frame)
join_port_label = ttk.Label(join_port_frame, text="Порт:")
join_port_label.pack(side=LEFT, padx=5, pady=5)
join_port_var = StringVar()
join_port_entry = ttk.Entry(join_port_frame, textvariable=join_port_var)
join_port_entry.insert(END, '5656')
join_port_entry.pack(side=RIGHT, padx=5, pady=5)
join_port_frame.pack(anchor=N, padx=5, pady=5, fill=X)

join_button = ttk.Button(join_frame, text="Подключиться",
                         command=lambda: join_game(ip_var.get(), int(join_port_var.get())))
join_button.pack(anchor=N, padx=5, pady=5, fill=X)
join_frame.pack(anchor=N, padx=5, pady=5, fill=X)

create_game_frame = ttk.Frame(main_frame, relief=SOLID, borderwidth=5)
create_game_label = ttk.Label(create_game_frame, text="Создать игру")
create_game_label.pack(anchor=N, padx=5, pady=5)

create_game_port_frame = ttk.Frame(create_game_frame)
create_game_port_label = ttk.Label(create_game_port_frame, text="Порт:")
create_game_port_label.pack(side=LEFT, padx=5, pady=5)
create_game_port_var = StringVar()
create_game_port_entry = ttk.Entry(create_game_port_frame, textvariable=create_game_port_var)
create_game_port_entry.insert(END, '5656')
create_game_port_entry.pack(side=RIGHT, padx=5, pady=5)
create_game_port_frame.pack(anchor=N, padx=5, pady=5, fill=X)

create_game_button = ttk.Button(create_game_frame, text="Создать",
                                command=lambda: create_game(int(create_game_port_var.get())))
create_game_button.pack(anchor=N, padx=5, pady=5, fill=X)
create_game_frame.pack(anchor=S, padx=5, pady=5, fill=X)

main_frame.pack(padx=10, pady=10, fill=BOTH)

root.mainloop()
