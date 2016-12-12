from Tkinter import *
from battle_client import *
from battle_board import *
import tkMessageBox
import threading

class Login(Frame):
    def __init__(self, root, server_id='127.0.0.1'):

        self.server_id = server_id

        self.client = Client(self.server_id)

        self.root = root

        self.root.title("Battleships!")

    def initUI(self):
        # Return the chosen game server
        def choose_game():
            try:
                return game_servers.get(game_servers.curselection())
            except TclError:
                return

        login_form = Frame(self.root)
        login_form.grid(row=0, column=0)

        def set_board_size(self):

            board_size = Frame(self.root)
            board_size.grid(row=0, column=0)

            board_size_label = Label(board_size, text="Enter board size", font=('times', 12))
            board_size_label.grid(row=0, column=0)

            board_size_entry = Entry(board_size)
            board_size_entry.grid(row=0, column=1, pady=5)

            def check_board_size():
                board_size = board_size_entry.get()
                if 10 < board_size < 40:
                    return board_size
                else:
                    tkMessageBox.showinfo("Error! Board size must be less than 40 and bigger than 10")


        def new_game():
            self.root.destroy()
            self.client.set_type(1)
            root = Tk()
            board = Board(root, 10, self.client)
            board.initShipBoard()
            board.initPositioning()
            root.mainloop()


        create_game = Button(login_form, text='Create New Game!', width=20,
                             bg='light blue', font=('times', 14), command=new_game)
        create_game.grid(row=0, column=1)

        join_game = Button(login_form, text='Join Game!', font=('times', 14), bg='light blue', command=choose_game)
        join_game.grid(row=0, column=0, sticky=W+E)

        game_servers = Listbox(login_form, width=20, height=10, font=10, bg='ghost white', activestyle='none')
        game_servers.grid(row=1, column=0)



        def get_game_sessions():
            try:
                while True:
                    game_sessions = self.client.get_game_list()
                    if game_sessions:
                        for game_id, game_size in game_sessions:
                            game_servers.insert(END, game_id + game_size)
                    else:
                        print 'Lol'
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
            self.initUI()

        nickname_button = Button(nickname_form, text='OK!', width=10, command=check_nickname)
        nickname_button.grid(row=1, column=0, sticky=E + W, columnspan=2)

root = Tk()
editor = Login(root)
editor.get_nickname()
root.mainloop()

