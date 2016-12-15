import Tkinter
from battle_client import *
from battle_login import *
import threading
import time
from ScrolledText import ScrolledText


"""
#Class that make a board for the battleship game and listen the server and represent the action in the GUI

# Main methods:

    spectate - become a spectator( send a request to the server and listen all the action during the game and
    show them in the log board

    initMessageBoard - initialize a log board, listen server to view a log

    initShootBoard - initialize a board where the user make a shoot

    initPositioning - initialize capabilities to set the ship

    initShipBoard - initializating a board where the user will set up his ships and when the game will starts
    receive the hits

    listen_server_game - processed the protocols 5, 6, 7, 11 in the protocol


"""

class Board(Frame):
    def __init__(self, root, size, client, login = None):
        self.login = login
        self.client = client
        self.size = size
        self.board = [[None] * self.size for _ in xrange(self.size)]
        self.root = root
        self.killed = 0
        # self.whoose_turn_label = Label(self.root, text="Your Turn", font=('New Times Romans', 14), fg='purple')
        # self.whoose_turn_label.grid(row=0, column=3, sticky=E + W + N)
        # self.whoose_turn_label.grid_remove()

        self.isMyTurn = False
        self.isclicked = False
        self.current_players_info = Label(self.root, text='Current Players: ')
        self.ifOnline = False

        self.leave_button = Tkinter.Button(self.root, text='Leave', command=self.leave_game)

        self.start_spectate_button = Tkinter.Button(self.root, text="You lose...Become spectacular?", fg='red',
                                            font=('New Times Romans', 12), command=self.spectate)
        self.start_spectate_button.grid(row=1, column=3, padx=10)
        self.start_spectate_button.grid_remove()

        self.master_restart_button = Tkinter.Button(self.root, text='Restart Game', command=self.restart_cmd)
        self.master_restart_button.grid(row=1, column=4)
        self.master_restart_button.grid_remove()

        self.master_kill_button = Tkinter.Button(self.root, text='Leave Game')
        self.master_kill_button.grid(row=1, column=5, padx=10)
        self.master_kill_button.grid_remove()

    def restart_cmd(self, isMaster=True):
        if (not self.root):
            return
        self.isMyTurn = False
        self.isclicked = False
        self.root.destroy()
        self.client.restart_game_session(True, "1")
        root = Tkinter.Tk()
        board = Board(root, int(self.size), self.client)
        board.initShipBoard()
        board.initPositioning()
        root.mainloop()


    def spectate(self):
        self.start_spectate_button.destroy()
        lp = threading.Thread(target=self.stashrt_spectate, args=())
        lp.setDaemon(True)
        lp.start()


    def start_spectate(self):
        spec_request = self.client.become_spectacular()
        if spec_request == 1:
            self.message_board.insert(END, 'Entered in spectate mode!' + '\n')
        while True:
            spec_request = self.client.become_spectacular()
            time.sleep(1)
            if spec_request:
                if spec_request == 1:
                    continue
                if len(spec_request) > 1:
                    x, y = spec_request[0].split(',')
                    self.message_board.insert(END, 'Damage in cell: ' + x + ' ' + y + '\n')
                    if len(spec_request) > 2:
                        for player in spec_request[1].split(','):
                            self.message_board.insert(END, 'Hitted players: ' + player + '\n')
                    if len(spec_request) == 3:
                        if len(spec_request[2]):
                            for sp in spec_request[2].split(','):
                                self.message_board.insert(END,
                                                          'Sink info. players:' + sp + "loosing ships!!!" '\n')






    def leave_game(self):
        if self.client.client_leave():
            global placement
            del placement[:]
            client = self.client
            self.root.destroy()
            #del self
            root = Tkinter.Tk()
            editor = Login(root, client)
            editor.isServerChoosed = True
            del self
            editor.initUI()
            #root.mainloop()


    def check_client_type(self):
        return self.client.get_type()

    def initMessageBoard(self):
        # Create message board label
        message_board_name = Tkinter.Label(self.root, text='Game log!', font=('times', 14))
        message_board_name.grid(row=2, column=0, columnspan=2)

        # Create message text with schrollbar
        self.message_board = ScrolledText(self.root, width=45, height=10, undo=True)
        self.message_board.grid(row=3, column=0, columnspan=2)

    def initShipBoard(self):
        self.root.title("Battleships!")

        # Create a ship board frame
        ship_board = Tkinter.Frame(self.root, background='black')
        ship_board.grid(row=1, column=0, padx=5)

        boardName = Tkinter.Label(self.root, text='Your Board', fg='black', font=('times', 16))
        boardName.grid(row=0, column=0, pady=15)

        # Create a ship board cells
        for i in xrange(self.size):
            for j in xrange(self.size):
                cell = Tkinter.Label(ship_board, text=' ' * 10 , bg='light sky blue')
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.bind('<Button-1>', lambda e, i=i, j=j: self.setShip(i, j, e))
                self.board[i][j] = cell

    def initShootBoard(self):
        # Create a shoot board frame
        shoot_panel = Tkinter.Frame(self.root, background='black')
        shoot_panel.grid(row=1, column=1, padx=5)

        boardName = Tkinter.Label(self.root, text='Your Shoots', fg='black', font=('times', 16))
        boardName.grid(row=0, column=1, pady=15)

        # Create a shoot board cells
        for i in xrange(self.size):
            for j in xrange(self.size):
                cell = Tkinter.Label(shoot_panel, text=' ' * 10, bg='white')
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
        #ships = [1, 1, 1, 1, 1]
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
                    hitter, x, y = shoot_status[1].split(',')
                    self.message_board.insert(END, hitter + ' hit in ' + x + ' ' + y + '\n')
                    if self.board[int(x)][int(y)].cget('bg') != 'red':
                        self.board[int(x)][int(y)].config(bg='red')
                        self.killed += 1
                elif shoot_status[0] == '4':
                    self.message_board.insert(END, 'Got ' + shoot_status[1] + ' points!\n')
                if len(shoot_status[2]) != 0:
                    sink_ships = ''
                    for ship in shoot_status[2].split(','):
                        sink_ships += ship + ' '
                    self.message_board.insert(END, 'Sink info. players:: ' + sink_ships + "are loosing ships!!!" '\n')
                return
        except AssertionError as e:
            #print e
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

        self.direction_label = Tkinter.Label(self.root, text='Set direction')
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

        self.set_direction = Tkinter.Button(self.root, text='Horizontally', command=change_direction)
        self.set_direction.grid(row=1, column=1, sticky=N)

        self.ship_label = Tkinter.Label(self.root, text="Current ship:")
        self.ship_label.grid(row=0, column=2, sticky=S)

        self.current_ship_label = Tkinter.Label(self.root, text="Carrier: 5", fg='red')
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


        self.reset_ships_label = Tkinter.Label(self.root, text="Reset ships")
        self.reset_ships_label.grid(row=0, column=3, sticky=S)

        self.reset_ships = Tkinter.Button(self.root, text="OK", width=10, command=reset_ships_)
        self.reset_ships.grid(row=1, column=3, sticky=N)



        def start_game():
            ships_coordinates = map(str, placement)
            while True:
                send_coordinates = self.client.send_ships(ships_coordinates)
                if send_coordinates:
                    if self.client.get_type() == 1:
                        self.confirm_players_button = Tkinter.Button(self.root,
                                                             text="Confirm the number of players",
                                                             command=self.master_confirm)
                        self.confirm_players_button.grid(row=1, column=2, sticky=E + W + N)
                        lp = threading.Thread(target=self.listen_players, args=())
                        lp.setDaemon(True)
                        lp.start()
                    else:
                        global t
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
                    time.sleep(1)
        except (TclError, TypeError, AssertionError) as e:
            return

    #def listen_shoot(self):


    def master_confirm(self):
        response = self.client.master_confirm_game()
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
                # response, '-------> response'
                if response == 'wait':
                    time.sleep(1)
                    continue
                if not response:
                    if self.killed == 17:
                        self.start_spectate_button.grid()
                        self.leave_button.config(fg='red',
                                            font=('New Times Romans', 12),)
                        return
                    if self.client.new_round_check() == self.client.get_client_nickname():
                        self.isMyTurn = True
                        try:
                            self.message_board.insert(END, 'Your turn! \n')
                        except AttributeError:
                            pass
                        time.sleep(1)
                    else:
                        self.isMyTurn = False
                        time.sleep(1)
                    shoot_status = self.client.handle_shoot(False, None, None)
                    while True:
                        if not shoot_status:
                            if end_connection == 10:
                                #print 'Lost connection'
                                break
                            shoot_status = self.client.handle_shoot(False, None, None)
                            time.sleep(1)
                            end_connection += 1
                            continue
                        else:
                            if shoot_status[0] == '1':
                                hitter, x, y = shoot_status[1].split(',')
                                self.message_board.insert(END, hitter + ' hit in ' + x + ' ' + y + '\n')
                                if self.board[int(x)][int(y)].cget('bg') != 'red':
                                    self.board[int(x)][int(y)].config(bg='red')
                                    self.killed += 1
                            if shoot_status[0] == '4':
                                self.message_board.insert(END, 'Got ' + shoot_status[1] + ' points! \n')
                            #print shoot_status, 'shoot status'
                            if len(shoot_status[2]) != 0:
                                sink_ships = ''
                                for ship in shoot_status[2].split(','):
                                    sink_ships += ship + ' '
                                self.message_board.insert(END,
                                                            'Sink info. players:' + sink_ships + "loosing ships!!!" '\n')

                            break
                else:
                    self.message_board.insert(END,
                                              'The winner is: ' + response + '\n')
                    isMaster = self.client.who_is_master()
                   # if isMaster == self.client.get_client_nickname():
                     #   self.master_kill_button.grid()
                    self.master_restart_button.grid()
                    i = 0
                    while True:
                        response = self.client.restart_game_session(False, "1")
                        if not response:
                            return
                        elif response == 'restart':
                            pass
                        elif response == 'kill':
                            pass
                        time.sleep(2)
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