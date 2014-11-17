#!/usr/bin/env python

#from sys.stdout import write
import sys
import StringIO

class Board:
    BLANK = ' '
    BORDER_HOR = '-------------\n'
    BORDER_VER = '|'
    WIDTH = 9
    HEIGHT = 9

    def __init__(self, board=[]):
        self.board = board
        if not board:
            B = self.BLANK
            self.board = [[B, 4, B, B, B, 5, B, 1, B],
                          [B, B, B, B, 1, B, 6, B, 9],
                          [6, B, 1, 9, 3, B, B, B, 4],
                          [5, B, 2, 6, 9, B, B, 7, B],
                          [B, 3, B, 7, B, 1, B, 9, B],
                          [B, 9, B, B, 4, 8, 1, B, 5],
                          [1, B, B, B, 7, 9, 8, B, 2],
                          [9, B, 3, B, 8, B, B, B, B],
                          [B, 7, B, 1, B, B, B, 4, B]]

    def __str__(self):
        s = StringIO.StringIO()
        for i in range(self.HEIGHT):
            if i == 0:
                s.write(self.BORDER_HOR)
            for j in range(self.WIDTH):
                if j == 0:
                    s.write(self.BORDER_VER)
                s.write(str(self.board[i][j]))
                if j % 3 == 2:
                    s.write(self.BORDER_VER)
            s.write('\n')
            if i % 3 == 2:
                s.write(self.BORDER_HOR)
        return s.getvalue()

def solve_init(board):
    solve(0, 0, board)

def solve(row, col, board):
    # are we finished
    if row == board.HEIGHT:
        row = 0
        col += 1
        if col == board.WIDTH:
            return True
        
    # skip if we're on a filled spot
    if board.board[row][col] != board.BLANK:
        return solve(row+1, col, board)

    # try solutions until we've got one (1-9 are only choices)
    for val in range(1, 10):
        if ok_placement(row, col, board, val):
            board.board[row][col] = val
            if solve(row+1, col, board):
                return True

    # Back track if no solution is found
    board.board[row][col] = board.BLANK
    
    return False

def ok_placement(row, col, board, attempt):
    # check row
    for check in range(board.WIDTH):
        if attempt == board.board[check][col]: return False

    # check column
    for check in range(board.HEIGHT):
        if attempt == board.board[row][check]: return False

    xBox = row / 3 * 3
    yBox = col / 3 * 3
    for x in range(3):
        for y in range(3):
            if attempt == board.board[(xBox+x)][(yBox+y)]:
                return False

    return True

if __name__ == "__main__":
    b = Board()
    print "Before solution:"
    print b
    solve_init(b)
    print "Solution:"
    print b
    



