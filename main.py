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
    
    def isAlliesPos(aliesPawns, pos)->bool:
        for aliesPawn in aliesPawns:
            if (aliesPawn.getPos() == pos):
                return (1);
        return (0);

    def getMoves(self): #pawns:list afin de verifier qu'il n'y est pas de pions a l'emplacement
        """
            flips positions where the pawn can go
        """ 
        pawns = []
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

        #il faut ajouter les mouvement de manger
        #il faut retirer les emplacements ou des pions de notre couleur existe deja

        return moves
        
    

class King(Pawn):
    def __init__(self,x: int ,y: int, sprite: pygame.Surface,color: str) -> None:
        super().__init__(x, y, sprite,color) 
    def getMoves():
        pass
class Queen(Pawn):
    def __init__(self, x: int, y: int, sprite: pygame.Surface,color: str) -> None:
        super().__init__(x, y, sprite,color) 
class Bishop(Pawn):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str) -> None:
        super().__init__(x, y, sprite,color) 
class Rook(Pawn):
    def __init__(self, x: int, y: int, sprite: pygame.Surface, color: str) -> None:
        super().__init__(x, y, sprite,color)
class Knight(Pawn):
    def __init__(self,x: int, y: int, sprite: pygame.Surface, color:str) -> None:
        super().__init__(x, y, sprite,color)  

game_on = True
class Audio():
    def __init__(self,file: str) -> None:
        self.playlist = [] #on enregistrera tout les musique de la playlist ici
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.

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
    def handleClick(self) -> None:
        x = (( pygame.mouse.get_pos()[0]) // CELL_SIZE)  #position x du click
        y = (( pygame.mouse.get_pos()[1])// CELL_SIZE) #position y du click
        print("click à la position" , (x,y))
        for pawn in  self.actual_player.getPawns():
            if pawn.getPos() == (x,y):
                self.selected_pawn = pawn
        if self.selected_pawn != None:
            print(self.selected_pawn.getColor())
            possible_moves = self.selected_pawn.getMoves()
            print(possible_moves)
            if (x, y) in possible_moves:
                #if (self.actual_player == COLOR_TAB[0]):
                 #   for blackPawn in  self.BLACK_PAWNS:
                  #      if (x, y) == blackPawn.getPos():
                   #         self.BLACK_PAWNS.remove(blackPawn);
                self.selected_pawn.setNewPos(x, y)
                self.setActualPlayer()
                self.selected_pawn = None
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
      
        
    screen.fill(pygame.Color("white"))
    game.make_board()#afficher le plateau
    game.placePawns()#afficher les pions sur le plateau
    pygame.display.update()
    timer.tick(20)