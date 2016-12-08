from Tkinter import *


class Board(Frame):
    def __init__(self, root, size):
        self.size = size
        self.root = root
        self.initShipBoard()
        self.initShootBoard()

    def initShipBoard(self):
        self.root.title("Battleships!")

        # Create a ship board frame
        ship_board = Frame(self.root, background='black')
        ship_board.grid(row=1, column=0, padx=5)

        boardName = Label(root, text='Your Board', fg='black', font=('times', 16))
        boardName.grid(row=0, column=0, pady=15)

        # Create a ship board cells
        for i in xrange(self.size):
            for j in xrange(self.size):
                cell = Label(ship_board, text=' ' * 10 , bg='light sky blue')
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.bind('<Button-1>', lambda e, i=i, j=j: self.setShip(i, j, e))

    def initShootBoard(self):
        # Create a shoot board frame
        shoot_panel = Frame(self.root, background='black')
        shoot_panel.grid(row=1, column=1, padx=5)

        boardName = Label(root, text='Your Shoots', fg='black', font=('times', 16))
        boardName.grid(row=0, column=1, pady=15)

        # Create a shoot board cells
        for i in xrange(self.size):
            for j in xrange(self.size):
                cell = Label(shoot_panel, text=' ' * 10, bg='white')
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.pack_propagate(0)
                cell.bind('<Button-1>',lambda e, i=i, j=j: self.shoot(i,j,e))

    def setShip(self, i, j, event):
        event.widget.config(bg='green')
        print i, j

    def shoot(self, i, j, event):
        event.widget.config(bg='grey')
        print i, j


root = Tk()
editor = Board(root, 10)
root.mainloop()


