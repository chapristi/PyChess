import pygame

NB_COL = 8
NB_ROW = 8
CELL_SIZE = 120

COLOR_TAB = ["WHITE","GRAY"]
#PAWNS
BLACK_PAWN_SPRITE  = pygame.transform.scale(pygame.image.load('images/black-pawn.png'),(100,100))
WHITE_PAWN_SPRITE  = pygame.transform.scale(pygame.image.load('images/white-pawn.png'),(100,100))

#BISHOP
BLACK_BISHOP_SPRITE  = pygame.transform.scale(pygame.image.load('images/black-bishop.png'),(100,100))
WHITE_BISHOP_SPRITE  = pygame.transform.scale(pygame.image.load('images/white-bishop.png'),(125,125))

#KNGIHT 
BLACK_KNGIHT_SPRITE  = pygame.transform.scale(pygame.image.load('images/black-knight.png'),(100,100))
WHITE_KNGIHT_SPRITE  = pygame.transform.scale(pygame.image.load('images/white-knight.png'),(100,100))

#ROOK

BLACK_ROOK_SPRITE  = pygame.transform.scale(pygame.image.load('images/black-rook.png'),(100,100))
WHITE_ROOK_SPRITE  = pygame.transform.scale(pygame.image.load('images/white-rook.png'),(100,100))
#QUEEN

BLACK_QUEEN_SPRITE  = pygame.transform.scale(pygame.image.load('images/black-queen.png'),(100,100))
WHITE_QUEEN_SPRITE  = pygame.transform.scale(pygame.image.load('images/white-queen.png'),(100,100))

#KING
BLACK_KING_SPRITE  = pygame.transform.scale(pygame.image.load('images/black-king.png'),(100,100))
WHITE_KING_SPRITE  = pygame.transform.scale(pygame.image.load('images/white-king.png'),(100,100))