from consts import *
import time
import sys
import pygame
from enum import Enum
 
screen = pygame.display.set_mode(size=(NB_COL* CELL_SIZE, NB_ROW * CELL_SIZE))
timer = pygame.time.Clock()


class Colors(Enum):
    BLACK = "GRAY"
    WHITE = "WHITE"

class Player:
    def __init__(self, couleur):
        self.color = couleur
        self.pawns = []
    def add_pawns(self, pawns):
        self.pawns = pawns
    def getPawns(self):
        return self.pawns
    def rm_pawns(self, piece):
        self.pieces.remove(piece)
 
class Pawn():
    def __init__(self, x: int, y : int,sprite:pygame.Surface,color:str) -> None:
       self.alreadyPlayed = False #False par default
       self.color = color #la couleur de la piece
       self.x = x #position x de la piece
       self.y = y #position y de la piece
       self.sprite = sprite #sprite de la piece

    def clone(self):
        return Pawn(self.x, self.y, self.sprite, self.color)
    def setAlreadyPlayed(self):
        """
            once called it sets the AlreadyPlayed attribute to true
        """
        self.alreadyPlayed = True

    def setNewPos(self,x :int,y :int):
        """
            Allows you to define a new position x and y to the piece and already
            passes Player to True to say that the piece is played at least Once.
        """
        self.x = x 
        self.y = y
        # si la fonction est appelé on considere que le pion a jouer uen fois
        self.setAlreadyPlayed()
    def getSprite(self)->pygame.Surface:
        """
            returns the sprite of the pawn
        """
        return self.sprite
    def getColor(self) -> str:
        """
            returns the color of the pawn
        """
        return self.color
    def getPos(self):
        """
             Returns the position of the pawn as a tuple (x,y)
        """
        return (self.x,self.y)
    def isOutOfBoard(self, x: int, y: int) -> bool:
        """
            renvoie True si les coordonnées sont en dehors du plateau de jeu sinon False
        """
        return not (0 <= x <= 7 and 0 <= y <= 7)
    
    def isAlliesPos(self, aliesPawns, pos)->bool:
        for aliesPawn in aliesPawns:
            if (aliesPawn.getPos() == pos):
                return (1);
        return (0);

    def isEnnemiesPos(self, ennemiesPawns, pos)->bool:
        for ennemiesPawn in ennemiesPawns:
            if (ennemiesPawn.getPos() == pos):
                return (1);
        return (0);
    def is_king_in_check_after_move(self, move, player_pawns, opponent_pawns):
        copied_player_pawns = [pawn.clone() for pawn in player_pawns]
        copied_opponent_pawns = [pawn.clone() for pawn in opponent_pawns]
        print(len(copied_player_pawns),len(player_pawns))
        for cop_player_pawn in copied_player_pawns:
            #print("hitle")
            if self.getPos() == cop_player_pawn.getPos():
                cop_player_pawn.setNewPos(move[0],move[1])
        king_pos = ()
        for pawn in copied_player_pawns:
            if isinstance(pawn, King):
                print("test")
                king_pos = pawn.getPos()
        for enemy_pawn in copied_opponent_pawns:
            possible_moves = enemy_pawn.getMoves(copied_opponent_pawns,copied_player_pawns)
            if king_pos in possible_moves:
                return True
        return False
        
    def getMoves(self, aliesPawns, ennemiesPawns): #pawns:list afin de verifier qu'il n'y est pas de pions a l'emplacement
        """
            flips positions where the pawn can go
        """ 
        moves_dict = {
            (False, Colors.WHITE.value): [(0, -2), (0, -1)],
            (True, Colors.WHITE.value): [(0, -1)],
            (False, Colors.BLACK.value): [(0, 2), (0, 1)],
            (True, Colors.BLACK.value): [(0, 1)],
         }
        x,y = self.getPos()
        key = (self.alreadyPlayed, self.color)
        #on ajout les mouvements possibles en fonction du moves_dict
        moves = [(x + m[0], y + m[1]) for m in moves_dict[key]]
        for move in moves:
            if(self.isAlliesPos(aliesPawns,move)):
                moves.remove(move)
        for move in moves:
            if(self.isEnnemiesPos(ennemiesPawns,move)):
                moves.remove(move)
                
        if self.color == Colors.BLACK.value:
            target_positions = [((x + 1), (y + 1)), ((x - 1), (y + 1))]
        elif self.color == Colors.WHITE.value:
            target_positions = [((x - 1), (y - 1)), ((x + 1), (y - 1))]
        for ennemiesPawn in ennemiesPawns:
            for target_pos in target_positions:
                if ennemiesPawn.getPos() == target_pos:
                    moves.append(target_pos)
        return moves
    
class SlidingPieceSingle(Pawn):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str, starting_moves: list) -> None:
        super().__init__(x, y, sprite, color)
        self.starting_moves = starting_moves
    def getMoves(self, aliesPawns, ennemiesPawns) -> list:
        x,y = super().getPos()
        return [(mx + x, my + y) for mx, my in self.starting_moves if not self.isOutOfBoard(mx+x, my+y) and not self.isAlliesPos(aliesPawns, (mx + x, my + y)) and not self.is_king_in_check_after_move((mx + x, my + y),aliesPawns,ennemiesPawns)]
class SlidingPieceMult(Pawn):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str, starting_moves: list) -> None:
        super().__init__(x, y, sprite, color)
        self.starting_moves = starting_moves
    def getMoves(self, aliesPawns, ennemiesPawns) -> list:
        moves = []
        x,y = super().getPos()
        for move in self.starting_moves:
            curr_x,curr_y = (x + move[0]), (y + move[1])
            stop_loop = False
            while(not super().isOutOfBoard(curr_x, curr_y) and not super().isAlliesPos(aliesPawns,(curr_x,curr_y)) and not stop_loop and not self.is_king_in_check_after_move((curr_x, curr_y),aliesPawns,ennemiesPawns)):
                if super().isEnnemiesPos(ennemiesPawns,(curr_x,curr_y)):
                    moves.append((curr_x, curr_y))
                    stop_loop = True
                    continue
                moves.append((curr_x, curr_y))
                curr_x,curr_y = (curr_x + move[0]), (curr_y + move[1])
            curr_x,curr_y = super().getPos()
        return moves

class King(SlidingPieceSingle):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str) -> None:
        starting_moves = [
            (0, 1),(0, -1),(1, 0),
            (-1, 0),(-1, 1),(1, 1),
            (-1, -1),(1, -1),
        ]
        super().__init__(x, y, sprite,color,starting_moves)

class Queen(SlidingPieceMult):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str) -> None:
            starting_moves =[
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (-1, 1),
                (1, 1),
                (-1, -1),
                (1, -1),
            ]
            super().__init__(x, y, sprite,color,starting_moves)
    #def clone(self):
    #    return Queen(self.x, self.y, self.sprite, self.color)

class Bishop(SlidingPieceMult):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str) -> None:
        starting_moves =[
            (-1, 1),
            (1, 1),
            (-1, -1),
            (1, -1),
        ]
        super().__init__(x, y, sprite,color,starting_moves)
    #def clone(self):
    #    return Bishop(self.x, self.y, self.sprite, self.color)
   
class Rook(SlidingPieceMult):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str) -> None:
            starting_moves =[
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
            ]
            super().__init__(x, y, sprite,color,starting_moves)
    #def clone(self):
     #   return Rook(self.x, self.y, self.sprite, self.color)

class Knight(SlidingPieceSingle):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str) -> None:
        starting_moves = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ] 
        super().__init__(x, y, sprite,color,starting_moves)
    #def clone(self):
    #    return Rook(self.x, self.y, self.sprite, self.color)

game_on = True
class Audio():
    def __init__(self) -> None:
        pygame.mixer.init()
    def play(self, file: str):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play() 
audio = Audio()
     
class Game():
    def __init__(self) -> None:
        self.selected_pawn = None #verifier a chaque fois que le pions soit de la couleur du joeur actuelle 
        self.player1 = Player(Colors.WHITE.value)
        self.player2  = Player(Colors.BLACK.value)
        black_pawns = [
            Rook(0,0,BLACK_ROOK_SPRITE,Colors.BLACK.value),
            Rook(7,0,BLACK_ROOK_SPRITE,Colors.BLACK.value),
            Knight(1,0,BLACK_KNGIHT_SPRITE,Colors.BLACK.value),
            Knight(6,0,BLACK_KNGIHT_SPRITE,Colors.BLACK.value),
            Bishop(2,0,BLACK_BISHOP_SPRITE,Colors.BLACK.value),
            Bishop(5,0,BLACK_BISHOP_SPRITE,Colors.BLACK.value),
            King(3,0,BLACK_KING_SPRITE,Colors.BLACK.value),
            Queen(4,0,BLACK_QUEEN_SPRITE,Colors.BLACK.value),
            ]
        white_pawns = [
            Rook(0,7,WHITE_ROOK_SPRITE, Colors.WHITE.value),
            Rook(7,7,WHITE_ROOK_SPRITE, Colors.WHITE.value),
            Knight(1,7,WHITE_KNGIHT_SPRITE, Colors.WHITE.value),
            Knight(6,7,WHITE_KNGIHT_SPRITE, Colors.WHITE.value),
            Bishop(2,7,WHITE_BISHOP_SPRITE, Colors.WHITE.value),
            Bishop(5,7,WHITE_BISHOP_SPRITE, Colors.WHITE.value),
            King(3,7,WHITE_KING_SPRITE, Colors.WHITE.value),
            Queen(4,7,WHITE_QUEEN_SPRITE,Colors.WHITE.value),
        ]
        # ajouter les pions
        for i in range(8):
            white_pawns.append(Pawn(i,6,WHITE_PAWN_SPRITE,Colors.WHITE.value))
            black_pawns.append(Pawn(i,1,BLACK_PAWN_SPRITE,Colors.BLACK.value))
        self.player1.add_pawns(white_pawns)
        self.player2.add_pawns(black_pawns)
        self.actual_player  = self.player1 # se sont les blancs qui commencent à jouer

    def setActualPlayer(self) -> None:
        """
           allows you to define the player who will play
        """
        if self.actual_player == self.player1:
            self.actual_player =  self.player2
        else:
            self.actual_player =  self.player1
    def resetSelectedPawn(self) -> None:
        self.selected_pawn = None
    def eatPawn(self)->None:
        enemies_pawns = self.player2.getPawns() if (self.actual_player.getPawns() == self.player1.getPawns()) else self.player1.getPawns()
        for enemies_pawn in enemies_pawns:
            for current_player_pawn in self.actual_player.getPawns():
                if enemies_pawn.getPos() == current_player_pawn.getPos():
                    enemies_pawns.remove(enemies_pawn)
                    return
                
    def king_is_check(self):
        king_pos = ()
        enemy_pawns = self.player2.getPawns() if (self.actual_player.getPawns() == self.player1.getPawns()) else self.player1.getPawns()
        for pawn in self.actual_player.getPawns():
            if isinstance(pawn, King):
                king_pos = pawn.getPos()
        for enemy_pawn in enemy_pawns:
            possible_moves = enemy_pawn.getMoves(enemy_pawns, self.actual_player.getPawns())
            if king_pos in possible_moves:
                return True
        return False
    
    def is_valid_move(x, y, possible_moves):
        if (x, y) in possible_moves:
            return True
        #verifier si le deplacement se trouve dans le tableau des moves
        #et verifier si le roi est en echec si oui ne pas autoriser
        #un deplacment qui l'eneleve pas de echec
        #ensuite faire fonction isend et passer toutes les postions de touit les piosn dans is_valid
        #si y a rien un joueur a gagne 
        pass
    def handleClick(self) -> None:
        #if self.king_is_check():
            #print("check")
            #audio.play("check.mp3")
        x = (( pygame.mouse.get_pos()[0]) // CELL_SIZE)  #position x du click
        y = (( pygame.mouse.get_pos()[1])// CELL_SIZE) #position y du click
        print("click à la position" , (x,y))
        for pawn in  self.actual_player.getPawns():
            if pawn.getPos() == (x,y):
                self.selected_pawn = pawn

        if self.selected_pawn != None:
            #print(self.selected_pawn.getColor())
            enemies_pawns = self.player2.getPawns() if (self.actual_player.getPawns() == self.player1.getPawns()) else self.player1.getPawns()
            possible_moves = self.selected_pawn.getMoves(self.actual_player.getPawns(), enemies_pawns)
            print("moves clicked pawn", possible_moves)

            if (x, y) in possible_moves:
                audio.play("pawn_move.wav")
                self.selected_pawn.setNewPos(x, y)
                self.eatPawn()
                self.setActualPlayer()
                self.selected_pawn = None
                if(self.king_is_check()):
                    print("f")
                    audio.play("check.mp3")
               
        return
        
    # pour atteindre la bonne case on multiplie la case qu'on veut par CELL_SIZE
    def make_board(self) -> None:
        """
             allows you to create the game board
        """
        for ligne in range(0,NB_COL):
            for colonne in range(0,NB_COL):
                rect = pygame.Rect(ligne*CELL_SIZE,colonne*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                x = ( ligne % 2 == 0 ) ^ ( colonne % 2 == 0 )
                pygame.draw.rect(screen,pygame.Color(COLOR_TAB[x]),rect)
    def placePawns(self) -> None:
        """
            allows you to position the pieces on the game board
        """
        for whitePawn in self.player1.getPawns():
            screen.blit(whitePawn.getSprite(),(whitePawn.getPos()[0]*CELL_SIZE,whitePawn.getPos()[1]*CELL_SIZE))
        for blackPawn in self.player2.getPawns():
            screen.blit(blackPawn.getSprite(),(blackPawn.getPos()[0]*CELL_SIZE,blackPawn.getPos()[1]*CELL_SIZE))

game = Game()
#Audio("BJCODE.mp3")#lance la musique
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 1 == left button
                game.handleClick()
                pass
      
    screen.fill(pygame.Color(Colors.WHITE.value))
    game.make_board()#afficher le plateau
    game.placePawns()#afficher les pions sur le plateau
    pygame.display.update()
    timer.tick(20)