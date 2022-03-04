
class Game():
    def __init__(self):
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.pot=[
            ["--","--","--","--","--","--","--","--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.movefunctions= {
            'p': self.getpawnmoves, 'R': self.getrookmoves, 'Q': self.getqueenmoves, 'K': self.getkingmoves, 'N': self.getknightmoves,
            'B': self.getbishopmoves
        }
        self.pieceval={
            'p': 1, 'R': 5, 'Q': 9, 'K': 100,
            'N': 3,
            'B': 3, '-':0
        }
        self.boardval=0
        self.turn=True
        self.movelog=[]
    def select(self, r, c,scanmoves):
        piece = self.board[r][c][1]
        for cur in scanmoves:
            if cur.startrow==r and cur.startcol==c:
                self.pot[cur.endrow][cur.endcol]="."
    def diselect(self):
        for r in range(8):
            for c in range(8):
                if self.pot[r][c]==".":
                    self.pot[r][c]="--"
    def makemove(self, move,iscalc=False):
        self.movelog.append(move)
        piece = self.board[move.startrow][move.startcol][1]
        if self.turn:
            self.boardval -= self.pieceval[move.piececaptured[1]]
        else:
            self.boardval += self.pieceval[move.piececaptured[1]]
        if piece == 'K' and abs(move.startcol - move.endcol) == 2:
            if move.startcol - move.endcol > 0:
                self.board[move.startrow][3] = self.board[move.startrow][0]
                self.board[move.startrow][0] = '--'
            else:
                self.board[move.startrow][5] = self.board[move.startrow][7]
                self.board[move.startrow][7] = '--'
        if len(move.piecemove) == 3:
            if move.piecemove[2] == 'o':
                if iscalc==False:
                    print(move.piececaptured)
                if not self.turn:
                    self.board[move.startrow - 1][move.endcol] = "--"
                else:
                    self.board[move.startrow + 1][move.endcol] = "--"
                self.board[move.startrow][move.startcol] = "--"
                self.board[move.endrow][move.endcol] = move.piecemove[:2]
            else:
                print("PROMOTION!!!!!")
                self.board[move.endrow][move.endcol] = move.piecemove[:2]
                self.board[move.startrow][move.startcol] = "--"
                if self.turn:
                    self.boardval -= 1 - self.pieceval[move.piecemove[1]]
                else:
                    self.boardval += 1 - self.pieceval[move.piecemove[1]]
        else:
            if iscalc==False:
                print(move.piececaptured)
            self.board[move.startrow][move.startcol] = "--"
            self.board[move.endrow][move.endcol] = move.piecemove

        if self.turn:
            self.turn=False
        else:
            self.turn=True
    def undo(self):
        if len(self.movelog)>=1:
            move = self.movelog.pop()
            piece = move.piecemove[1]
            if self.turn:
                self.boardval -= self.pieceval[move.piececaptured[1]]
            else:
                self.boardval += self.pieceval[move.piececaptured[1]]
            if len(move.piecemove)==3:
                if move.piecemove[2]=='o':
                    if not self.turn:
                        self.board[move.startrow-1][move.endcol]=move.piececaptured
                    else:
                        self.board[move.startrow +1][move.endcol] = move.piececaptured
                    self.board[move.endrow][move.endcol]="--"
                    self.board[move.startrow][move.startcol]=move.piecemove[:2]
                else:
                    self.board[move.endrow][move.endcol] = move.piececaptured
                    self.board[move.startrow][move.startcol] = move.piecemove[0]+"p"
                    if self.turn:
                        self.boardval += 1 - self.pieceval[move.piecemove[1]]
                    else:
                        self.boardval -= 1 - self.pieceval[move.piecemove[1]]
            else:
                self.board[move.endrow][move.endcol]=move.piececaptured
                self.board[move.startrow][move.startcol]=move.piecemove
            if piece == 'K' and abs(move.startcol - move.endcol) == 2:
                if move.startcol - move.endcol > 0:
                    self.board[move.startrow][0] = self.board[move.startrow][3]
                    self.board[move.startrow][3] = '--'
                else:
                    self.board[move.startrow][7] = self.board[move.startrow][5]
                    self.board[move.startrow][5] = '--'
            if self.turn:
                self.turn = False
            else:
                self.turn = True
    def getvalidmoves(self):
        movelogs=self.getallpossiblemoves()
        res=[]
        for pos in range(len(movelogs)):
            self.makemove(movelogs[pos],iscalc=True)
            possiblemoves=self.getallpossiblemoves()
            good=True
            for cur in possiblemoves:
                if cur.piececaptured[1]=='K':
                    good=False
                    break
            if good==True:
                res.append(movelogs[pos])
            self.undo()
        return res
    def getifcastle(self):
        moves = []
        if self.turn:
            self.turn = False
        else:
            self.turn = True
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != '--' and self.board[r][c][1]!='K':
                    piece = self.board[r][c][1]
                    self.movefunctions[piece](r, c, moves)
        if self.turn:
            self.turn = False
        else:
            self.turn = True
        return moves

    def getallpossiblemoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                curcolor = self.board[r][c][0]
                if self.board[r][c][0]!='-':
                    piece=self.board[r][c][1]
                    self.movefunctions[piece](r, c, moves)
        return moves
    def getpawnmoves(self, r, c, moves):
        check=False
        prevmove=None
        if len(self.movelog)>=1:
            prevmove=self.movelog[len(self.movelog) - 1]
        if self.turn and self.board[r][c][0]=="w":
            if self.board[r-1][c] =="--":
                if r==1:
                    rook=move((r,c),(r-1,c),self.board)
                    rook.piecemove="wRp"
                    queen = move((r, c), (r - 1, c), self.board)
                    queen.piecemove = "wQp"
                    knight = move((r, c), (r - 1, c), self.board)
                    knight.piecemove = "wNp"
                    bishop = move((r, c), (r - 1, c), self.board)
                    bishop.piecemove = "wBp"
                    moves.append(rook)
                    moves.append(queen)
                    moves.append(knight)
                    moves.append(bishop)
                else:
                    moves.append(move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(move((r, c), (r - 2, c), self.board))
            if r!=0 and c>0 and self.board[r-1][c-1][0]=='b':
                if r==1:
                    rook = move((r, c), (r - 1, c-1), self.board)
                    rook.piecemove = "wRp"
                    queen = move((r, c), (r - 1, c-1), self.board)
                    queen.piecemove = "wQp"
                    knight = move((r, c), (r - 1, c-1), self.board)
                    knight.piecemove = "wNp"
                    bishop = move((r, c), (r - 1, c-1), self.board)
                    bishop.piecemove = "wBp"
                    moves.append(rook)
                    moves.append(queen)
                    moves.append(knight)
                    moves.append(bishop)
                else:
                    moves.append(move((r,c),(r-1,c-1),self.board))
            if r!=0 and c<7 and self.board[r-1][c + 1][0] == 'b':
                if r == 1:
                    rook = move((r, c), (r - 1, c + 1), self.board)
                    rook.piecemove = "wRp"
                    queen = move((r, c), (r - 1, c + 1), self.board)
                    queen.piecemove = "wQp"
                    knight = move((r, c), (r - 1, c + 1), self.board)
                    knight.piecemove = "wNp"
                    bishop = move((r, c), (r - 1, c + 1), self.board)
                    bishop.piecemove = "wBp"
                    moves.append(rook)
                    moves.append(queen)
                    moves.append(knight)
                    moves.append(bishop)
                else:
                    moves.append(move((r, c), (r - 1, c + 1), self.board))
            if r==3 and prevmove.piecemove=="bp" and prevmove.endrow==3 and prevmove.startrow==1:
                if prevmove.endcol == c+1:
                    onp=move((r, c), (r - 1, c + 1), self.board)
                    onp.piecemove = "wpo"
                    onp.piececaptured = "bp"
                    moves.append(onp)
                elif prevmove.endcol == c-1:
                    onp = move((r, c), (r - 1, c - 1), self.board)
                    onp.piecemove = "wpo"
                    onp.piececaptured = "bp"
                    moves.append(onp)
        elif not self.turn and self.board[r][c][0]=="b":
            if self.board[r+1][c] == "--":
                if r==6:
                    rook = move((r, c), (r + 1, c), self.board)
                    rook.piecemove = "bRp"
                    queen = move((r, c), (r + 1, c), self.board)
                    queen.piecemove = "bQp"
                    knight = move((r, c), (r + 1, c), self.board)
                    knight.piecemove = "bNp"
                    bishop = move((r, c), (r + 1, c), self.board)
                    bishop.piecemove = "bBp"
                    moves.append(rook)
                    moves.append(queen)
                    moves.append(knight)
                    moves.append(bishop)
                else:
                    moves.append(move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(move((r, c), (r + 2, c), self.board))
            if r!=7 and c>0 and self.board[r+1][c-1][0]=="w":
                if r==6:
                    rook = move((r, c), (r + 1, c-1), self.board)
                    rook.piecemove = "bRp"
                    queen = move((r, c), (r + 1, c-1), self.board)
                    queen.piecemove = "bQp"
                    knight = move((r, c), (r + 1, c-1), self.board)
                    knight.piecemove = "bNp"
                    bishop = move((r, c), (r + 1, c-1), self.board)
                    bishop.piecemove = "bBp"
                    moves.append(rook)
                    moves.append(queen)
                    moves.append(knight)
                    moves.append(bishop)
                else:
                    moves.append(move((r,c), (r+1,c-1), self.board))
            if r!=7 and c<7 and self.board[r+1][c + 1][0] == "w":
                if r == 6:
                    rook = move((r, c), (r + 1, c + 1), self.board)
                    rook.piecemove = "bRp"
                    queen = move((r, c), (r + 1, c + 1), self.board)
                    queen.piecemove = "bQp"
                    knight = move((r, c), (r + 1, c + 1), self.board)
                    knight.piecemove = "bNp"
                    bishop = move((r, c), (r + 1, c + 1), self.board)
                    bishop.piecemove = "bBp"
                    moves.append(rook)
                    moves.append(queen)
                    moves.append(knight)
                    moves.append(bishop)
                else:
                    moves.append(move((r, c), (r + 1, c + 1), self.board))
            if r==4 and prevmove.piecemove=='wp'and prevmove.endrow==4 and prevmove.startrow==6:
                if prevmove.endcol==c+1:
                    onp=move((r, c), (r + 1, c + 1), self.board)
                    onp.piecemove="bpo"
                    onp.piececaptured = "wp"
                    moves.append(onp)
                elif prevmove.endcol==c-1:
                    onp = move((r, c), (r + 1, c - 1), self.board)
                    onp.piecemove = "bpo"
                    onp.piececaptured = "wp"
                    moves.append(onp)
    def recur(self, do ,depth,ord):
        og=[[],[],[],[],[],[],[],[]]
        for i in range(8):
            for f in range(8):
                og[i].append(self.board[i][f])
        self.makemove(do,iscalc=True)
        if depth==0:
            temp=self.boardval
            self.undo()
            return temp
        best = None
        val = None
        possible=self.getallpossiblemoves()
        for cur in possible:
            temp=self.recur(cur,depth-1,ord)
            if ord==self.turn and (val==None or temp>val):
                best=cur
                val=temp
            elif ord!=self.turn and (val==None or temp<val):
                best=cur
                val=temp
        self.undo()
        good=1
        for i in range(8):
            for f in range (8):
                if og[i][f]!=self.board[i][f]:
                    print("retard")
                    break
            if good==0:
                break
    def getbestmove(self, moves,depth):
        best=None
        val=None
        for cur in moves:
            temp=self.recur(cur,depth,self.turn)
            if val==None or temp>val:
                val=temp
                best=cur
        return best
    def getrookmoves(self,r,c,moves):
        if self.turn and self.board[r][c][0]=="w":
            for inc in range(8-r-1):
                if self.board[r+inc+1][c]=="--":
                    moves.append(move((r, c), (r+inc+1, c), self.board))
                elif self.board[r+inc+1][c][0]=="b":
                    moves.append(move((r, c), (r+inc+1, c), self.board))
                    break
                else:
                    break
            for inc in range(8-c-1):
                if self.board[r][c+inc+1]=="--":
                    moves.append(move((r, c), (r, c+inc+1), self.board))
                elif self.board[r][c+inc+1][0]=="b":
                    moves.append(move((r, c), (r, c+inc+1), self.board))
                    break
                else:
                    break
            for inc in range(c):
                if self.board[r][c-inc-1]=="--":
                    moves.append(move((r, c), (r, c-inc-1), self.board))
                elif self.board[r][c-inc-1][0]=="b":
                    moves.append(move((r, c), (r, c-inc-1), self.board))
                    break
                else:
                    break
            for inc in range(r):
                if self.board[r-inc-1][c]=="--":
                    moves.append(move((r, c), (r-inc-1, c), self.board))
                elif self.board[r-inc-1][c][0]=="b":
                    moves.append(move((r, c), (r-inc-1, c), self.board))
                    break
                else:
                    break
        if not self.turn and self.board[r][c][0]=="b":
            for inc in range(8-r-1):
                if self.board[r+inc+1][c]=="--":
                    moves.append(move((r, c), (r+inc+1, c), self.board))
                elif self.board[r+inc+1][c][0]=="w":
                    moves.append(move((r, c), (r+inc+1, c), self.board))
                    break
                else:
                    break
            for inc in range(8-c-1):
                if self.board[r][c+inc+1]=="--":
                    moves.append(move((r, c), (r, c+inc+1), self.board))
                elif self.board[r][c+inc+1][0]=="w":
                    moves.append(move((r, c), (r, c+inc+1), self.board))
                    break
                else:
                    break
            for inc in range(c):
                if self.board[r][c-inc-1]=="--":
                    moves.append(move((r, c), (r, c-inc-1), self.board))
                elif self.board[r][c-inc-1][0]=="w":
                    moves.append(move((r, c), (r, c-inc-1), self.board))
                    break
                else:
                    break
            for inc in range(r):
                if self.board[r-inc-1][c]=="--":
                    moves.append(move((r, c), (r-inc-1, c), self.board))
                elif self.board[r-inc-1][c][0]=="w":
                    moves.append(move((r, c), (r-inc-1, c), self.board))
                    break
                else:
                    break
    def getbishopmoves(self, r, c, moves):
        if self.turn and self.board[r][c][0]=="w":
            for inc in range(min(r,c)):
                piece=self.board[r-inc-1][c-inc-1]
                if piece=="--":
                    moves.append(move((r, c),(r-inc-1,c-inc-1),self.board))
                elif piece[0]=="b":
                    moves.append(move((r, c), (r - inc - 1, c - inc - 1), self.board))
                    break
                else:
                    break
            for inc in range(min(8-r-1,8-c-1)):
                piece=self.board[r+inc+1][c+inc+1]
                curmove=move((r, c),(r+inc+1,c+inc+1),self.board)
                if piece=="--":
                    moves.append(curmove)
                elif piece[0]=="b":
                    moves.append(curmove)
                    break
                else:
                    break
            for inc in range(min(r,8-c-1)):
                piece=self.board[r-inc-1][c+inc+1]
                curmove=move((r, c),(r-inc-1,c+inc+1),self.board)
                if piece=="--":
                    moves.append(curmove)
                elif piece[0]=="b":
                    moves.append(curmove)
                    break
                else:
                    break
            for inc in range(min(8-r-1,c)):
                piece=self.board[r+inc+1][c-inc-1]
                curmove=move((r, c),(r+inc+1,c-inc-1),self.board)
                if piece=="--":
                    moves.append(curmove)
                elif piece[0]=="b":
                    moves.append(curmove)
                    break
                else:
                    break
        if not self.turn and self.board[r][c][0] == "b":
            for inc in range(min(r , c )):
                piece = self.board[r - inc - 1][c - inc - 1]
                if piece == "--":
                    moves.append(move((r, c), (r - inc - 1, c - inc - 1), self.board))
                elif piece[0] == "w":
                    moves.append(move((r, c), (r - inc - 1, c - inc - 1), self.board))
                    break
                else:
                    break
            for inc in range(min(8 - r - 1, 8 - c - 1)):
                piece = self.board[r + inc + 1][c + inc + 1]
                curmove = move((r, c), (r + inc + 1, c + inc + 1), self.board)
                if piece == "--":
                    moves.append(curmove)
                elif piece[0] == "w":
                    moves.append(curmove)
                    break
                else:
                    break
            for inc in range(min(r , 8 - c -1)):
                piece = self.board[r - inc - 1][c + inc + 1]
                curmove = move((r, c), (r - inc - 1, c + inc + 1), self.board)
                if piece == "--":
                    moves.append(curmove)
                elif piece[0] == "w":
                    moves.append(curmove)
                    break
                else:
                    break
            for inc in range(min(8 - r - 1, c )):
                piece = self.board[r + inc + 1][c - inc - 1]
                curmove = move((r, c), (r + inc + 1, c - inc - 1), self.board)
                if piece == "--":
                    moves.append(curmove)
                elif piece[0] == "w":
                    moves.append(curmove)
                    break
                else:
                    break
    def getqueenmoves(self, r, c, moves):
        self.getrookmoves(r,c,moves)
        self.getbishopmoves(r,c,moves)
    def getknightmoves(self,r,c,moves):
        list=[-1, -2, 1, 2]
        if self.turn and self.board[r][c][0]=="w":
            for i in range(len(list)):
                if r+list[i]<8 and r+list[i]>=0 and c+list[((i+1)%4)]<8 and c+list[((i+1)%4)]>=0:
                    piece=self.board[r+list[i]][c+list[((i+1)%4)]]
                    if piece[0]=="b" or piece=="--":
                        moves.append(move((r,c),(r+list[i], c+list[((i+1)%4)]), self.board))
                if r+list[i]<8 and r+list[i]>=0 and c+list[((i+3)%4)]<8 and c+list[((i+3)%4)]>=0:
                    piece = self.board[r + list[i]][c + list[((i + 3)%4)]]
                    if piece[0] == "b" or piece == "--":
                        moves.append(move((r, c), (r+list[i], c + list[((i + 3)%4)]), self.board))
        elif not self.turn and self.board[r][c][0]=="b":
            for i in range(len(list)):
                if r+list[i]<8 and r+list[i]>=0 and c+list[((i+1)%4)]<8 and c+list[((i+1)%4)]>=0:
                    piece=self.board[r+list[i]][c+list[((i+1)%4)]]
                    if piece[0]=="w" or piece=="--":
                        moves.append(move((r,c), (r+list[i], c+list[((i+1)%4)]), self.board))
                if r + list[i] < 8 and r + list[i] >= 0 and c + list[((i + 3) % 4)] < 8 and c + list[((i + 3) % 4)] >= 0:
                    piece = self.board[r + list[i]][c + list[((i + 3)%4)]]
                    if piece[0] == "w" or piece == "--":
                        moves.append(move((r, c), (r+list[i], c + list[((i + 3)%4)]), self.board))
    def getkingmoves(self,r,c,moves):
        if self.turn and self.board[r][c][0]=="w":
            possibleturns = []
            for tempr in range(-1,2):
                for tempc in range(-1,2):
                    if tempr!=0 or tempc!=0:
                        if r+tempr>=0 and r+tempr<8 and c+tempc>=0 and c+tempc<8:
                            piece=self.board[r+tempr][c+tempc]
                            if piece=="--" or piece[0]=="b":
                                curmove = (move((r, c), (r + tempr, c + tempc), self.board))
                                moves.append(curmove)
            good=1
            right=1
            left=1
            for cur in self.movelog:
                if cur.startrow==7 and cur.startcol==4:
                    good=0
                if cur.startrow==7 and cur.startcol==7:
                    right=0
                if cur.startrow==7 and cur.startcol==0:
                    left=0
            if good and (right or left):
                possibleturns = self.getifcastle()
            if good==1 and right==1:
                for inc in range(7-c-1):
                    if self.board[r][c+inc+1]!="--":
                        right=0
                        break
                    for cur in possibleturns:
                        if cur.endrow==r and cur.endcol==c+inc and cur.piecemove[0]=='b':
                            right=0
                            break
                    if right==0:
                        break

                if right==1:
                    moves.append(move((r,c), (r, c+2), self.board))
            if good==1 and left==1:
                for inc in range(c-2):
                    if self.board[r][c-inc-1]!="--":
                        left=0
                        break
                    for cur in possibleturns:
                        if cur.endrow==r and cur.endcol==c-inc-1 and cur.piecemove[0]=='b':
                            left=0
                            break
                    if left==0:
                        break
                if left==1:
                    moves.append(move((r,c), (r, c-2), self.board))
        if not self.turn and self.board[r][c][0]=="b":
            possibleturns = []
            for tempr in range(-1,2):
                for tempc in range(-1,2):
                    if tempr!=0 or tempc!=0:
                        if r + tempr >= 0 and r + tempr < 8 and c + tempc >= 0 and c + tempc < 8:
                            piece = self.board[r + tempr][c + tempc]
                            if piece == "--" or piece[0] == "w":
                                curmove=(move((r, c), (r + tempr, c + tempc), self.board))
                                moves.append(curmove)
            good = 1
            right = 1
            left = 1
            for cur in self.movelog:
                if cur.startrow == 0 and cur.startcol == 4:
                    good = 0
                if cur.startrow == 0 and cur.startcol == 7:
                    right = 0
                if cur.startrow == 0 and cur.startcol == 0:
                    left = 0
            if good and (right or left):
                possibleturns = self.getifcastle()
            if good == 1 and right == 1:
                for inc in range(7 - c - 1):
                    if self.board[r][c + inc + 1] != "--":
                        right = 0
                        break
                    for cur in possibleturns:
                        if cur.endrow == r and cur.endcol == c + inc and cur.piecemove[0]=='w':
                            right = 0
                            break
                    if right == 0:
                        break

                if right == 1:
                    moves.append(move((r, c), (r, c + 2), self.board))
            if good == 1 and left == 1:
                for inc in range(c - 2):
                    if self.board[r][c - inc - 1] != "--":
                        left = 0
                        break
                    for cur in possibleturns:
                        if cur.endrow == r and cur.endcol == c - inc - 1 and cur.piecemove[0]=='w':
                            left = 0
                            break
                    if left == 0:
                        break
                if left == 1:
                    moves.append(move((r, c), (r, c - 2), self.board))
class move():
    def eq(self, comp):
        if self.moveid==comp.moveid:
            return True
        return False
    def __init__(self, startsq, endsq, board):
        self.startrow=startsq[0]
        self.startcol=startsq[1]
        self.endrow=endsq[0]
        self.endcol=endsq[1]
        self.piecemove=board[self.startrow][self.startcol]
        self.piececaptured = board[self.endrow][self.endcol]
        self.moveid=self.startrow*1000+self.startcol*100+self.endrow*10+self.endcol
