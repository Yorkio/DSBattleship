from Tkinter import *
from battle_client import *
import battle_board
import tkMessageBox
import threading
import time

class Login(Frame):
    def __init__(self, root, client):
        self.server_id = ''
        if (client == None):
            self.client = Client()
        else:
            self.client = client
        self.root = root
        if (root):
            self.root.title("Battleships!")
        self.isServerChoosed = False

    def choose_server(self):

        avaliable_servers_frame = Frame(self.root)
        avaliable_servers_frame.grid(row=0, column=0)

        avaliable_servers = Listbox(avaliable_servers_frame, width=40,
                                    height=5, font=('times', 14), bg='ghost white', activestyle='none')
        avaliable_servers.grid(row=1, column=0)

        server_label = Label(avaliable_servers_frame, text="Choose the server!",
                             fg='purple3', font=('times', 14))
        server_label.grid(row=0, column=0)

        def choose_server():
            try:
                server_id = avaliable_servers.get(avaliable_servers.curselection())
                self.isServerChoosed = True
                if (self.root):
                    self.root.destroy()
                root = Tk()
                self.client.set_server_id(server_id)
                editor = Login(root, self.client)
                editor.get_nickname()
                root.mainloop()
            except TclError:
                return

        server_select_button = Button(avaliable_servers_frame, text="OK!",
                                      font=('times', 14), bg='ghost white', command=choose_server)
        server_select_button.grid(row=2, column=0, sticky=W+E)

        def get_avaliable_servers():
            if self.isServerChoosed:
                return
            try:
                while True:
                    server_list = []
                    collision = 0
                    while True:
                        srv = self.client.get_server()
                        if srv not in server_list:
                            server_list.append(srv)
                        else:
                            if collision < 5:
                                collision += 1
                                continue
                            elif collision == 5:
                                for s in server_list:
                                    avaliable_servers.insert(END, s)
                                break
                    time.sleep(5)
                    avaliable_servers.delete(0, END)
            except TclError:
                return

        t = threading.Thread(target=get_avaliable_servers, args=())
        t.setDaemon(True)
        t.start()

    def set_board_size(self):

        board_size = Frame(self.root)
        board_size.grid(row=0, column=0)

        board_size_label = Label(board_size, text="Enter a board size", font=('times', 12))
        board_size_label.grid(row=0, column=0)

        board_size_entry = Entry(board_size)
        board_size_entry.grid(row=0, column=1, pady=5)

        def check_board_size():
            board_size = board_size_entry.get()
            try:
                if 10 <= int(board_size) <= 40:
                    if (self.root):
                        self.root.destroy()
                    self.client.set_type(1)
                    self.client.send_type(None, board_size)
                    root = Tk()
                    board = battle_board.Board(root, int(board_size), self.client)

                    board.initShipBoard()
                    board.initPositioning()
                    root.mainloop()
                else:
                    tkMessageBox.showerror("Error!", "Board size must be less than 40 and bigger than 10 cells!")
            except ValueError:
                return

        confirm_size = Button(board_size, text='OK!', command=check_board_size)
        confirm_size.grid(row=1, column=0, sticky=W + E, columnspan=2)

    def initUI(self):
        # Return the chosen game server
        def choose_game():
            try:
                session = game_servers.get(game_servers.curselection())
                if " / " not in session:
                    return
                else:
                    game_id, game_board_size, number_of_players = session.split(" / ")
                    self.client.send_type(game_id)
                    self.root.destroy()
                    root = Tk()
                    board = battle_board.Board(root, int(game_board_size), self.client)
                    board.initShipBoard()
                    board.initPositioning()
                    root.mainloop()

            except TclError:
                return

        login_form = Frame(self.root)
        login_form.grid(row=0, column=0)


        def new_game():
            if (self.root):
                self.root.destroy()
            root = Tk()
            editor = Login(root, self.client)
            editor.set_board_size()
            root.mainloop()

        create_game = Button(login_form, text='Create New Game!', width=20,
                             bg='light blue', font=('times', 14), command=new_game)
        create_game.grid(row=0, column=1)

        join_game = Button(login_form, text='Join Game!', font=('times', 14), bg='light blue', command=choose_game)
        join_game.grid(row=0, column=0, sticky=W+E)

        game_servers = Listbox(login_form, width=60, height=10, font=10, bg='ghost white', activestyle='none')
        game_servers.grid(row=1, column=0)

        def get_game_sessions():
            try:
                while True:
                    game_sessions = self.client.get_game_list()
                    if game_sessions:
                        for game_info in game_sessions:
                            game_info = game_info.split(';')
                            game_servers.insert(END, game_info[0] + " / " + game_info[1] + " / " + game_info[2])
                    else:
                        game_servers.insert(END, "No active games!")
                    time.sleep(3)
                    game_servers.delete(0, END)
            except TclError:
                return

        t = threading.Thread(target=get_game_sessions, args=())
        t.setDaemon(True)
        t.start()

    def get_nickname(self):
        nickname_form = Frame(self.root)
        nickname_form.grid(row=0, column=0)

        nickname_label = Label(nickname_form, text="Please, enter your nickname", font=('times', 12))
        nickname_label.grid(row=0, column=0)

        nickname_entry = Entry(nickname_form)
        nickname_entry.grid(row=0, column=1, pady=5)

        def check_nickname():
            nickname = nickname_entry.get()
            if not nickname or not self.client.isFreeName(nickname):
                return
            self.client.set_client_nickname(nickname)
            self.initUI()

        nickname_button = Button(nickname_form, text='OK!', width=10, command=check_nickname)
        nickname_button.grid(row=1, column=0, sticky=E + W, columnspan=2)

if __name__ == "__main__":
    root = Tk()
    editor = Login(root, None)
    editor.choose_server()
    root.mainloop()
