from Tkinter import *
from battle_client import *
from battle_login import *
import threading
import time
from ships_generator import *
from ScrolledText import ScrolledText

temp_var = 0

class Board(Frame):
    def __init__(self, root, size, client):
        self.client = client
        self.size = size
        self.board = [[None] * self.size for _ in xrange(self.size)]
        self.root = root

        # self.whoose_turn_label = Label(self.root, text="Your Turn", font=('New Times Romans', 14), fg='purple')
        # self.whoose_turn_label.grid(row=0, column=3, sticky=E + W + N)
        # self.whoose_turn_label.grid_remove()

        self.isMyTurn = False
        self.isclicked = False
        self.current_players_info = Label(self.root, text='Current Players: ')
        self.ifOnline = False

        self.leave_button = Button(self.root, text='Leave', command=self.leave_game)


    def leave_game(self):
        if self.client.client_leave():
            global placement
            del placement[:]
            client = self.client
            self.root.destroy()
            #del self
            #root = Tk()
            editor = Login(None, client)
            editor.isServerChoosed = True
            del self
            editor.initUI()
            #root.mainloop()


    def check_client_type(self):
        return self.client.get_type()

    def initMessageBoard(self):
        # Create message board label
        message_board_name = Label(self.root, text='Game log!', font=('times', 14))
        message_board_name.grid(row=2, column=0, columnspan=2)

        # Create message text with schrollbar
        self.message_board = ScrolledText(self.root, width=45, height=10, undo=True)
        self.message_board.grid(row=3, column=0, columnspan=2)

    def initShipBoard(self):
        self.root.title("Battleships!")

        # Create a ship board frame
        ship_board = Frame(self.root, background='black')
        ship_board.grid(row=1, column=0, padx=5)

        boardName = Label(self.root, text='Your Board', fg='black', font=('times', 16))
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

        boardName = Label(self.root, text='Your Shoots', fg='black', font=('times', 16))
        boardName.grid(row=0, column=1, pady=15)

        # Create a shoot board cells
        for i in xrange(self.size):
            for j in xrange(self.size):
                cell = Label(shoot_panel, text=' ' * 10, bg='white')
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.pack_propagate(0)
                cell.bind('<Button-1>',lambda e, i=i, j=j: self.shoot(i,j,e))


        if self.client.get_type() == 1:
            self.current_players_info.grid(row=0, column=2)

        #self.shoot_button = Button(self.root, text="SHOOT!")
        #self.shoot_button.grid(row=)
        self.leave_button.grid(row=1, column=2)


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
            plc = (i, j, ships[ship], direction)
            for i, pl in enumerate(plc):
                if i != 3:
                    placement.append(str(pl) + ',')
                else:
                    placement.append(str(pl) + '#')
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
            plc = (i, j, ships[ship], direction)
            for i, pl in enumerate(plc):
                if i != 3:
                    placement.append(str(pl) + ',')
                else:
                    placement.append(str(pl) + '#')
            ship += 1
            self.current_ship_label.config(text=types[ship])
        if ship == len(ships):
            self.confirm_choice.config(state="normal")

    def shoot(self, i, j, event):
        try:
            if self.isMyTurn:
                event.widget.config(bg='grey')
                shoot_status = self.client.handle_shoot(True, i, j)
                self.isMyTurn = False
                if not shoot_status:
                    return
                elif shoot_status[0] == '1':
                    print shoot_status, 'shoot status if [0]'
                    hitter, x, y = shoot_status[1].split(',')
                    self.message_board.insert(END, hitter + ' hit in ' + x + ' ' + y + '\n')
                    self.board[int(x)][int(y)].config(bg='red')
                elif shoot_status[0] == '4':
                    self.message_board.insert(END, 'Got ' + shoot_status[1] + ' points!\n')
                if len(shoot_status[2]) != 0:
                    sink_ships = ''
                    for ship in shoot_status[2].split(','):
                        sink_ships += ship + ' '
                        self.message_board.insert(END, 'Sink info. players: ' + sink_ships + "are loosing ships!!!" '\n')
        except AssertionError as e:
            print e
            pass


    def initPositioning(self):
        global k
        k = 0

        global placement
        placement = []

        global direction
        direction = 0

        global ship
        ship = 0

        self.direction_label = Label(self.root, text='Set direction')
        self.direction_label.grid(row=0, column=1, padx=5, sticky=S)

        # Set the direction of the  ship


        def change_direction():
            global k, direction
            k += 1

            if k % 2 == 0:
                self.set_direction.config(text='Horizontally')
                direction = 0
            else:
                self.set_direction.config(text='Vertically')
                direction = 1

        self.set_direction = Button(self.root, text='Horizontally', command=change_direction)
        self.set_direction.grid(row=1, column=1, sticky=N)

        self.ship_label = Label(self.root, text="Current ship:")
        self.ship_label.grid(row=0, column=2, sticky=S)

        self.current_ship_label = Label(self.root, text="Carrier: 5", fg='red')
        self.current_ship_label.grid(row=1, column=2, sticky=N)



        def reset_ships_():
            self.confirm_choice.config(state="disabled")
            global placement
            global ship
            ship = 0
            del placement[:]

            self.current_ship_label.config(text="Carrier: 5")

            for i in xrange(self.size):
                for j in xrange(self.size):
                    self.board[i][j].config(bg="light sky blue")


        self.reset_ships_label = Label(self.root, text="Reset ships")
        self.reset_ships_label.grid(row=0, column=3, sticky=S)

        self.reset_ships = Button(self.root, text="OK", width=10, command=reset_ships_)
        self.reset_ships.grid(row=1, column=3, sticky=N)



        def start_game():
            ships_coordinates = map(str, placement)
            while True:
                send_coordinates = self.client.send_ships(ships_coordinates)
                if send_coordinates:
                    if self.client.get_type() == 1:
                        self.confirm_players_button = Button(self.root,
                                                             text="Confirm the number of players",
                                                             command=self.master_confirm)
                        self.confirm_players_button.grid(row=1, column=2, sticky=E + W + N)
                        lp = threading.Thread(target=self.listen_players, args=())
                        lp.setDaemon(True)
                        lp.start()
                    else:
                        t = threading.Thread(target=self.listen_server_game, args=())
                        t.setDaemon(True)
                        t.start()

                    self.destroy_positioning()
                    self.initShootBoard()
                    self.initMessageBoard()
                    break

        self.confirm_choice = Button(self.root, text="Start game",
                                fg='purple3', font=('times', 12), state=DISABLED, command=start_game)

        self.confirm_choice.grid(row=2, column=1, sticky=E + W, columnspan=3)

    def listen_players(self):
        try:
            while True:
                if self.isclicked is True:
                    return
                if self.client.get_type() == 1:
                    self.current_players_info.config(text="Number of players: " + self.client.get_number_of_players())
                    time.sleep(3)
        except (TclError, TypeError, AssertionError) as e:
            return

    #def listen_shoot(self):


    def master_confirm(self):
        response = self.client.master_confirm_game()
        print response
        if response:
            self.confirm_players_button.destroy()
            self.isclicked = True
            d = threading.Thread(target=self.listen_server_game, args=())
            d.setDaemon(True)
            d.start()
        else:
            return

    def listen_server_game(self):
        try:
            while True:
                end_connection = 0
                response = self.client.win_check()
                if response == 'wait':
                    time.sleep(3)
                    continue
                if not response:
                    if self.client.new_round_check() == self.client.get_client_nickname():
                        self.isMyTurn = True
                        self.message_board.insert(END, 'Your turn! \n')
                        time.sleep(3)
                    else:
                        self.isMyTurn = False
                        time.sleep(3)
                    shoot_status = self.client.handle_shoot(False, None, None)
                    while True:
                        if not shoot_status:
                            if end_connection == 10:
                                print 'Lost connection'
                                break
                            shoot_status = self.client.handle_shoot(False, None, None)
                            time.sleep(1)
                            end_connection += 1
                            continue
                        else:
                            if shoot_status[0] == '1':
                                hitter, x, y = shoot_status[1].split(',')
                                self.message_board.insert(END, hitter + ' hit in ' + x + ' ' + y + '\n')
                                self.board[int(x)][int(y)].config(bg='red')
                            if shoot_status[0] == '4':
                                self.message_board.insert(END, 'Got ' + shoot_status[1] + ' points! \n')

                            if len(shoot_status[2]) != 0:
                                print shoot_status[2], 'shoot status[2]'
                                sink_ships = ''
                                for ship in shoot_status[2].split(','):
                                    sink_ships += ship + ' '
                                self.message_board.insert(END,
                                                            'Sink info. players:' + sink_ships + "loosing ships!!!" '\n')
                            break
        except AssertionError as e:
            pass
        except TypeError:
            return


    def destroy_positioning(self):
        self.set_direction.destroy()
        self.ship_label.destroy()
        self.current_ship_label.destroy()
        self.reset_ships_label.destroy()
        self.direction_label.destroy()
        self.confirm_choice.destroy()
        self.reset_ships.destroy()
