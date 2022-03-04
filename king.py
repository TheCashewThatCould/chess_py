import rook
class king:
    has_moved=False
    team=True
    def __init__(self,tteam):
        team=tteam
    def can_castle_long(board, self):
        if not self.has_moved:
            if not self.team:
                if isinstance(board[0][7],rook)and not board[0][7].hasmoved:
                    return True
            else:
                if isinstance(board[7][7], rook) and not board[7][7].hasmoved:
                    return True