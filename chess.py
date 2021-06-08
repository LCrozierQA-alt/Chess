import numpy as np
import datetime

class Game() :
    def __init__(self) :
        board = []
        [board.append([Square(), Square(), Square(), Square(), Square(), Square(), Square(), Square(), ]) for i in
         range(8)]
        self.board = np.array(board)


class Square() :
    def __init__(self) :
        self.color = "square"
        self.type = "square"
        self.id = "00"

    def __repr__(self) :
        return "_"


class Player :
    def __init__(self, color, gameboard, mins, secs) :
        self.legal_moves = []
        self.vict_list = []
        self.color = color
        self.list = []
        self.gameboard = gameboard
        self.king = None
        self.time = datetime.timedelta(minutes=mins, seconds=secs)
        self.delta = None


    def __repr__(self) :
        return self.color

    def legal_lister(self, other) :
        self.legal_moves = []
        for p in range(8) :
            for q in range(8) :
                for piece in self.list :
                    if piece.piece_parser((p, q), other) :
                        memory = [piece.position,self.gameboard[p][q]]
                        self.gameboard[memory[0][0]][memory[0][1]].position = Square()
                        other.list = [piece for piece in other.list if piece !=memory[1]]
                        piece.position = (p,q)
                        self.gameboard[p][q] = piece
                        if not any([piece.piece_parser(self.king.position, other) for piece in other.list]):
                            self.legal_moves.append(Move(piece, (p, q)))
                        self.gameboard[p][q] = memory[1]
                        self.gameboard[memory[0][0]][memory[0][1]] = piece
                        if type(memory[1]) != type(Square()):
                            other.list.append(memory[1])
                        piece.position = memory[0]


class Piece() :
    id_counter = 10
    def __init__(self, color, position, type, game_board, player) :
        self.color = color
        self.position = position
        self.type = type
        self.board = game_board
        self.board[self.position[0], self.position[1]] = self
        self.player = player
        self.move = False
        self.id = Piece.id_counter
        Piece.id_counter += 1

    def __repr__(self) :
        return self.type

    def move_piece(self, nput, other) :
        position = (int(nput[-2]), int(nput[-1]))
        if type(self.board[position[0]][position[1]]) != type(Square()) :
            self.player.vict_list.append(self.board[position[0]][position[1]])
            other.list = [item for item in other.list if item.position != position]
        if (self.type == 'o') & ((position[0] == 7) | (position[0] == 0)) :
            self.type = 'Q'
        self.board[self.position[0]][self.position[1]] = Square()
        self.board[position[0]][position[1]] = self
        self.position = position
        self.move = True

    def piece_parser(self, position, other) :
        if (self.board[position[0]][position[1]].color == self.color) | (self.position == position) :
            return False
        elif self.type == "K" :
            if ((self.position[0] == position[0]) & ((self.position[1] - position[1]) ** 2 == 1)) | \
                    ((self.position[1] == position[1]) & ((self.position[0] - position[0]) ** 2 == 1)) | \
                    (((self.position[0] - position[0]) ** 2 == 1) & ((self.position[1] - position[1]) ** 2 == 1)) :
                return True
            else :
                return False
        elif self.type == "Q" :
            return self.rook_parser(position) | self.bishop_parser(position)
        elif self.type == "R" :
            return self.rook_parser(position)
        elif self.type == "B" :
            return self.bishop_parser(position)
        elif self.type == "N" :
            if ((((self.position[0] - position[0]) ** 2 == 4) & ((self.position[1] - position[1]) ** 2 == 1)) |
                    (((self.position[0] - position[0]) ** 2 == 1) & ((self.position[1] - position[1]) ** 2 == 4))) :
                return True
            else :
                return False
        else :
            one = 1
            if self.color == "white" :
                one -= 2
            if (self.position[1] == position[1]) & (type(self.board[position[0]][position[1]]) == type(Square())) :
                if (position[0] - self.position[0] == one) | (
                        (position[0] - self.position[0] == one + one) & (self.move == False)) :
                    return True
            elif (one == position[0] - self.position[0]) & (1 == (position[1] - self.position[1]) ** 2) & \
                    (type(self.board[position[0]][position[1]]) != type(Square())) :
                return True
            else :
                return False



    def rook_parser(self, position) :
        negate = 1
        if self.position[0] == position[0] :
            if self.position[1] > position[0] :
                negate = -1
            return all([((type(self.board[position[0]][square]) == type(Square())) | (self.board[position[0]][square] ==
                    self)) for square in range(self.position[1], position[1], negate)])
        elif self.position[1] == position[1] :
            if self.position[0] > position[0] :
                negate = -1
            return all(
                [((type(self.board[square][position[1]]) == type(Square())) | (self.board[square][position[1]] == self))
                 for square in
                 range(self.position[0], position[0], negate)])
        else :
            return False

    def bishop_parser(self, position) :
        if (self.position[0] - position[0]) ** 2 == (self.position[1] - position[1]) ** 2 :
            negative = 1
            if self.position[0] > position[0] :
                negative = -1
            bishlist = [x for x in range(self.position[0], position[0], negative)]
            bishdict = {}
            i = 0
            negative = 1
            if self.position[1] > position[1] :
                negative = -1
            for x in range(self.position[1], position[1], negative) :
                bishdict[bishlist[i]] = x
                i += 1
            if self.type == "B" :
                print()
            return all(
                [(type(self.board[key][bishdict[key]]) == type(Square())) | (self.board[key][bishdict[key]] == self) for
                 key in bishdict.keys()])
        else :
            return False


class Move() :
    def __init__(self, piece, position) :
        self.piece = piece
        self.position = position
        self.repr = str(self.piece.id) + str(self.position[0]) + str(self.position[1])

    def translate_numpy_to_chess(self, position) :
        return {0 : "a", 1 : "b", 2 : "c", 3 : "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}[position[1]] + str(
            8 - position[0])

    def __repr__(self) :
        return str(self.piece.id) + str(self.position[0]) + str(self.position[1])


def initiate_session() :
    colors = ["white", "black"]
    game = Game()
    players = []
    for i in range(2) :
        players.append(Player(colors[i], game.board, 15, 0))
        for num in range(0, 8) :
            players[-1].list.append(Piece(colors[i], (i * (-5) + 6, num), "o", game.board, players[-1]))
        for num in range(1, 3) :
            players[-1].list.append(Piece(colors[i], (i * (-7) + 7, (num * 7) - 7), "R", game.board, players[-1]))
            players[-1].list.append(Piece(colors[i], (i * (-7) + 7, (num * 5) - 4), "N", game.board, players[-1]))
            players[-1].list.append(Piece(colors[i], (i * (-7) + 7, (num ** 2) + 1), "B", game.board, players[-1]))
        king = Piece(colors[i], (i * (-7) + 7, 3 + i), "K", game.board, players[-1])
        players[-1].list.append(king)
        players[-1].king = king
        players[-1].list.append(Piece(colors[i], (i * (-7) + 7, 4 - i), "Q", game.board, players[-1]))
    players[0].legal_lister(players[1])
    players[0].delta = datetime.datetime.now()
    return players


def chess(players, form) :
    print(form)
    players[0].time -= (datetime.datetime.now() - players[0].delta)
    [move for move in players[0].legal_moves if form == str(move)][0].piece.move_piece(form,players[1])
    players[1].legal_lister(players[0])
    players[1].delta = datetime.datetime.now()
    players = [players[1], players[0]]
    return players
