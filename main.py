from consts import *
import time
import sys
import pygame
screen = pygame.display.set_mode(size=(NB_COL* CELL_SIZE, NB_ROW * CELL_SIZE))
timer = pygame.time.Clock()
class Pawn():
    def __init__(self, x: int, y : int,sprite,color:str) -> None:
       self.alreadyPlayed = False #False par default
       self.color = color
       self.x = x 
       self.y = y
       self.sprite = sprite
    def setAlreadyPlayed(self):
        """
            une fois appelé elle met a true l'attribut AlreadyPlayed
        """
        self.alreadyPlayed = True

    def setNewPos(self,x:int,y:int):
        self.x = x 
        self.y = y
        # si la fonction est appelé on considere que le pion a jouer uen fois
        self.setAlreadyPlayed()
    def getSprite(self):
        return self.sprite
    def getColor(self) -> str:
        return self.color
    def getPos(self):
        return (self.x,self.y)
    def getMoves(self): #pawns:list afin de verifier qu'il n'y est pas de pions a l'emplacement
        #on rappelle que les pions mangent en diagonal 
        moves_dict = {
            (False, COLOR_TAB[0]): [(0, -2), (0, -1)],
            (True, COLOR_TAB[0]): [(0, -1)],
            (False, COLOR_TAB[1]): [(0, 2), (0, 1)],
            (True, COLOR_TAB[1]): [(0, 1)],
         }
        pos = self.getPos()
        key = (self.alreadyPlayed, self.color)
        moves = [(pos[0] + m[0], pos[1] + m[1]) for m in moves_dict[key]]
        return moves
        
    

class King(Pawn):
    def __init__(self,x: int ,y: int, sprite,color:str) -> None:
        super().__init__(x, y, sprite,color) 
    def getMoves():
        pass
class Queen(Pawn):
    def __init__(self, x, y, sprite,color) -> None:
        super().__init__(x, y, sprite,color) 
class Bishop(Pawn):
    def __init__(self,x ,y ,sprite,color) -> None:
        super().__init__(x, y, sprite,color) 
class Rook(Pawn):
    def __init__(self,x,y,sprite,color) -> None:
        super().__init__(x, y, sprite,color)
class Knight(Pawn):
    def __init__(self,x,y,sprite,color) -> None:
        super().__init__(x, y, sprite,color)  





game_on = True
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
            Pawn(0,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]),
            Pawn(1,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]),
            Pawn(2,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]),
            Pawn(3,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]),
            Pawn(4,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]),
            Pawn(5,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]),
            Pawn(6,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]),
            Pawn(7,1,BLACK_PAWN_SPRITE,COLOR_TAB[1]),
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

            Pawn(0,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]),
            Pawn(1,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]),
            Pawn(2,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]),
            Pawn(3,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]),
            Pawn(4,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]),
            Pawn(5,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]),
            Pawn(6,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]),
            Pawn(7,6,WHITE_PAWN_SPRITE,COLOR_TAB[0]),
        ]
    def setActualPlayer(self):
        if self.actual_player == COLOR_TAB[1]:
            self.actual_player =  COLOR_TAB[0]
        else:
            self.actual_player =  COLOR_TAB[1]
    def resetSelectedPawn(self):
        self.selected_pawn = None
    def handleClick(self):
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
    def make_plate(self) -> None:
        for ligne in range(0,NB_COL):
            for colonne in range(0,NB_COL):
                rect = pygame.Rect(ligne*CELL_SIZE,colonne*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                x = ( ligne % 2 == 0 ) ^ ( colonne % 2 == 0 )
                pygame.draw.rect(screen,pygame.Color(COLOR_TAB[x]),rect)
    def placePawns(self):
        for whitePawn in self.WHITE_PAWNS:
            screen.blit(whitePawn.getSprite(),(whitePawn.getPos()[0]*CELL_SIZE,whitePawn.getPos()[1]*CELL_SIZE))
        for blackPawn in self.BLACK_PAWNS:
            screen.blit(blackPawn.getSprite(),(blackPawn.getPos()[0]*CELL_SIZE,blackPawn.getPos()[1]*CELL_SIZE))

game = Game()
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 1 == left button
                game.handleClick()

    screen.fill(pygame.Color("white"))

    game.make_plate()#afficher le plateau
    game.placePawns()#afficher les pions sur le plateau
    pygame.display.update()
    timer.tick(20)