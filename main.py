from consts import *
import time
import sys
import pygame
screen = pygame.display.set_mode(size=(NB_COL* CELL_SIZE, NB_ROW * CELL_SIZE))
timer = pygame.time.Clock()
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

    def setNewPos(self,x:int,y:int):
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
    def getMoves(self): #pawns:list afin de verifier qu'il n'y est pas de pions a l'emplacement
        #on rappelle que les pions mangent en diagonal

        """
            flips positions where the pawn can go
        """ 
        moves_dict = {
            (False, COLOR_TAB[0]): [(0, -2), (0, -1)],
            (True, COLOR_TAB[0]): [(0, -1)],
            (False, COLOR_TAB[1]): [(0, 2), (0, 1)],
            (True, COLOR_TAB[1]): [(0, 1)],
         }
        pos = self.getPos()
        key = (self.alreadyPlayed, self.color)
        moves = [(pos[0] + m[0], pos[1] + m[1]) for m in moves_dict[key]]
        #verifier que le tableau moove ne contient pas des positions de pions 
        # sinon il faut les suprimer 
        # ensuite il faut verifier si le pions peut manger des piosn en diagonales

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
        self.actual_player  =  COLOR_TAB[0] # se sont les blancs qui commencent à jouer
        self.BLACK_PAWNS = [
            Rook(0,0,BLACK_ROOK_SPRITE,COLOR_TAB[1]),
            Rook(7,0,BLACK_ROOK_SPRITE,COLOR_TAB[1]),
            Knight(1,0,BLACK_KNGIHT_SPRITE,COLOR_TAB[1]),
            Knight(6,0,BLACK_KNGIHT_SPRITE,COLOR_TAB[1]),
            Bishop(2,0,BLACK_BISHOP_SPRITE,COLOR_TAB[1]),
            Bishop(5,0,BLACK_BISHOP_SPRITE,COLOR_TAB[1]),
            King(3,0,BLACK_KING_SPRITE,COLOR_TAB[1]),
            Queen(4,0,BLACK_QUEEN_SPRITE,COLOR_TAB[1]),
            ]
        self.WHITE_PAWNS = [
            Rook(0,7,WHITE_ROOK_SPRITE,COLOR_TAB[0]),
            Rook(7,7,WHITE_ROOK_SPRITE,COLOR_TAB[0]),
            Knight(1,7,WHITE_KNGIHT_SPRITE,COLOR_TAB[0]),
            Knight(6,7,WHITE_KNGIHT_SPRITE,COLOR_TAB[0]),
            Bishop(2,7,WHITE_BISHOP_SPRITE,COLOR_TAB[0]),
            Bishop(5,7,WHITE_BISHOP_SPRITE,COLOR_TAB[0]),
            King(3,7,WHITE_KING_SPRITE,COLOR_TAB[0]),
            Queen(4,7,WHITE_QUEEN_SPRITE,COLOR_TAB[0]),
        ]
        # ajouter les pions
        for i in range(8):
            self.WHITE_PAWNS.append(Pawn(i,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]))
            self.BLACK_PAWNS.append(Pawn(i,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]))    

    def setActualPlayer(self) -> None:
        """
           allows you to define the player who will play
        """
        if self.actual_player == COLOR_TAB[1]:
            self.actual_player =  COLOR_TAB[0]
        else:
            self.actual_player =  COLOR_TAB[1]
    def resetSelectedPawn(self) -> None:
        self.selected_pawn = None
    def handleClick(self) -> None:
        x = (( pygame.mouse.get_pos()[0]) // CELL_SIZE)#position x du click
        y = (( pygame.mouse.get_pos()[1])// CELL_SIZE)#position y du click
        print("click à la position" , (x,y))
        if self.actual_player == COLOR_TAB[0]:
            for whitePawn in  self.WHITE_PAWNS:
                if whitePawn.getPos() == (x,y):
                    self.selected_pawn = whitePawn
        else:
            for blackPawn in  self.BLACK_PAWNS:
                if blackPawn.getPos() == (x,y):
                    self.selected_pawn = blackPawn
        if self.selected_pawn != None:
            print(self.selected_pawn.getColor())
            possible_moves = self.selected_pawn.getMoves()
            print(possible_moves)
            if (x,y) in possible_moves:
                self.selected_pawn.setNewPos(x,y)
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
        for whitePawn in self.WHITE_PAWNS:
            screen.blit(whitePawn.getSprite(),(whitePawn.getPos()[0]*CELL_SIZE,whitePawn.getPos()[1]*CELL_SIZE))
        for blackPawn in self.BLACK_PAWNS:
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
      
        


    screen.fill(pygame.Color("white"))
    game.make_board()#afficher le plateau
    game.placePawns()#afficher les pions sur le plateau
    pygame.display.update()
    timer.tick(20)