from Tkinter import *

class Login(Frame):
    def __init__(self, root):
        self.root = root
        self.initUI()

    def initUI(self):

        # Return the chosen game server
        def choose_game():
            try:
                return game_servers.get(game_servers.curselection())
            except TclError:
                return

        self.root.title("Battleships!")

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


root = Tk()
editor = Login(root)
root.mainloop()

