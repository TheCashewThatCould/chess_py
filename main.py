import pygame as p
import engine
WIDTH=HEIGHT=512
dimension = 8
SQ_SIZE=HEIGHT //dimension
MAX_FPS=15
IMAGES={}


def load_images():
    pieces=['wp', 'wK', 'wN', 'wB', 'wQ', 'wR', 'bp', 'bK', 'bN', 'bB', 'bQ', 'bR', '.']
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("image/"+piece+".png"), (SQ_SIZE, SQ_SIZE))
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs=engine.Game()
    load_images()
    running = True
    sqSelected=()
    playerClicks=[]
    validmoves = gs.getvalidmoves()
    movemade=False
    while running:
        if len(validmoves)==0:
            if gs.turn:
                gs.turn = False
                iswin = False
                possible = gs.getallpossiblemoves()
                for cur in possible:
                    if cur.piececaptured == "wK":
                        iswin = True
                        break
                if iswin:
                    print("Black wins")
                else:
                    print("Draw")
            else:
                gs.turn = True
                iswin = False
                possible = gs.getallpossiblemoves()
                for cur in possible:
                    if cur.piececaptured == "bK":
                        iswin = True
                        break
                if iswin:
                    print("White wins")
                else:
                    print("Draw")
            running = False
            break

      ##  if gs.turn==False:
        ##    do=gs.getbestmove(validmoves, 2)
          ##  gs.makemove(do)
            ##validmoves.clear()
            ##validmoves=gs.getvalidmoves()
            ##movemade=True
            ##gs.turn=True
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if gs.board[row][col]!="--":
                    gs.select(row, col,validmoves)
                    drawGameState(screen, gs)
                    clock.tick(MAX_FPS)
                    p.display.flip()
                if sqSelected== (row, col):
                    sqSelected=()
                    playerClicks=[]
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks)==2:
                    move=engine.move(playerClicks[0], playerClicks[1], gs.board)
                    for cur in validmoves:
                        if move.eq(cur):
                            gs.makemove(move)
                            movemade = True
                            break
                    sqSelected=()
                    playerClicks=[]
                    gs.diselect()
            elif e.type==p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo()
                    validmoves=gs.getvalidmoves()

        if movemade:
            validmoves=gs.getvalidmoves()
            movemade=False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board,gs.pot)
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color=colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board, pot):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            dot=pot[r][c]
            if dot!="--":
                screen.blit(IMAGES["."], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if piece!= "--":
                screen.blit(IMAGES[piece[0]+piece[1]], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
main()