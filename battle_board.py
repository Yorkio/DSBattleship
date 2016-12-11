from Tkinter import *


class Board(Frame):
    def __init__(self, root, size):
        self.size = size
        self.board = [[None] * self.size for _ in xrange(self.size)]
        self.root = root
        self.initShipBoard()
        #self.initShootBoard()
        self.initPositioning()

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
                self.board[i][j] = cell

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
        ships = [5, 4, 3, 3, 2]
        types = ["Carrier: 5", "Battleship: 4", "Cruiser: 3", "Submarine: 3", "Destroyer: 2", "No one left!"]

        def check_square(x, y):
            try:
                for shift_x in xrange(-1, 2):
                    for shift_y in xrange(-1, 2):
                        if self.board[x + shift_x][y + shift_y].cget('bg') == "green":
                            return False
            except IndexError:
                pass
            return True

        global ship

        global placement

        if ship >= len(ships):
            return

        if direction == 0:
            if j + ships[ship] > self.size:
                return
            for _ in xrange(ships[ship]):
                if not check_square(i, j + _):
                    return

            for _ in xrange(ships[ship]):
                self.board[i][j + _].config(bg='green')
            placement.append((i, j, ships[ship], direction))
            ship += 1
            self.current_ship_label.config(text=types[ship])

        else:
            if i + ships[ship] > self.size:
                return
            for _ in xrange(ships[ship]):
                if not check_square(i + _, j):
                    return


            for _ in xrange(ships[ship]):
                self.board[i + _][j].config(bg='green')
            ship += 1
            self.current_ship_label.config(text=types[ship])


    def shoot(self, i, j, event):
        event.widget.config(bg='grey')
        print i, j

    def initPositioning(self):
        global k
        k = 0

        global placement
        placement = []

        global direction
        direction = 0

        global ship
        ship = 0

        direction_label = Label(self.root, text='Set direction')
        direction_label.grid(row=0, column=1, padx=5, sticky=S)

        # Set the direction of the  ship
        def change_direction():
            global k, direction
            k += 1

            if k % 2 == 0:
                set_direction.config(text='Horizontally')
                direction = 0
            else:
                set_direction.config(text='Vertically')
                direction = 1

        set_direction = Button(self.root, text='Horizontally', command=change_direction)
        set_direction.grid(row=1, column=1, sticky=N)


        ship_label = Label(self.root, text="Current ship:")
        ship_label.grid(row=0, column=2, sticky=S)

        self.current_ship_label = Label(self.root, text="Carrier: 5", fg='red')
        self.current_ship_label.grid(row=1, column=2, sticky=N)

        def reset_ships():
            global placement
            global ship
            ship = 0
            del placement[:]

            self.current_ship_label.config(text="Carrier: 5")

            for i in xrange(self.size):
                for j in xrange(self.size):
                    self.board[i][j].config(bg="light sky blue")

        reset_ships_label = Label(self.root, text="Reset ships")
        reset_ships_label.grid(row=0, column=3, sticky=S)

        reset_ships = Button(self.root, text="OK", width=10, command=reset_ships)
        reset_ships.grid(row=1, column=3, sticky=N)


# root = Tk()
# editor = Board(root, 10)
# root.mainloop()


