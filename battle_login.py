from Tkinter import *


class Login(Frame):
    def __init__(self, root):
        self.root = root
        #self.initUI()
        #self.get_nickname()
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

        create_game = Button(login_form, text='Create New Game!', width=20, bg='light blue', font=('times', 14))
        create_game.grid(row=0, column=1)

        join_game = Button(login_form, text='Join Game!', font=('times', 14), bg='light blue', command=choose_game)
        join_game.grid(row=0, column=0, sticky=W+E)

        game_servers = Listbox(login_form, width=20, height=10, font=10, bg='ghost white', activestyle='none')
        game_servers.grid(row=1, column=0)

        # Sample
        for item in ["one", "two", "three", "four"]:
            game_servers.insert(END, item)

    def get_nickname(self):
        nickname_form = Frame(self.root)
        nickname_form.grid(row=0, column=0)

        nickname_label = Label(nickname_form, text="Please, enter your nickname", font=('times', 12))
        nickname_label.grid(row=0, column=0)

        nickname_entry = Entry(nickname_form)
        nickname_entry.grid(row=0, column=1, pady=5)

        def check_nickname():
            nickname = nickname_form.get()
            if not nickname:
                return
            return nickname

        nickname_button = Button(nickname_form, text='OK!', width=10, command=check_nickname)
        nickname_button.grid(row=1, column=0, sticky=E + W, columnspan=2)




root = Tk()
editor = Login(root)
root.mainloop()

