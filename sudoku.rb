#!/usr/bin/env ruby
class Solver
  B = " " 
  attr_reader :sudoku_board
  
  def initialize
    @sudoku_board = [[B, 4, B, B, B, 5, B, 1, B],
                     [B, B, B, B, 1, B, 6, B, 9],
                     [6, B, 1, 9, 3, B, B, B, 4],
                     [5, B, 2, 6, 9, B, B, 7, B],
                     [B, 3, B, 7, B, 1, B, 9, B],
                     [B, 9, B, B, 4, 8, 1, B, 5],
                     [1, B, B, B, 7, 9, 8, B, 2],
                     [9, B, 3, B, 8, B, B, B, B],
                     [B, 7, B, 1, B, B, B, 4, B]]
  end
  
  def solve_init
    return solve(0, 0, sudoku_board)
  end

  def solve(row, col, board)
    # are we finished  ?
    if row == 9
      row = 0
      col += 1
      if col == 9: return true end
    end

    # are we on a spot that's filled already. skip.
    if board[row][col] != B: return solve(row + 1, col, board) end

    # loop over remaining cells (here is where we recurse)
    for val in 1..9
      # is the placement ok?
      if ok_placement(row, col, board, val)
        # set that cell and call solve on next space
        board[row][col] = val
        # if this solve is ok, return true
        if solve(row + 1, col, board): return true end
      end
    end

    board[row][col] = B
    return false
    # return false because loop ended with no solution
  end

  def ok_placement(row, col, board, attempt)
    # check row
    for check in 0..8
      if attempt == board[check][col].to_i: return false end
    end

    # check vertical
    for check in 0..8
      if attempt == board[row][check].to_i: return false end
    end

    # check boxes
    xBox = row / 3 * 3 # thanks to remainder chop off
    yBox = col / 3 * 3
    for x in 0..2
      for y in 0..2
        if attempt == board[ (xBox + x) ][ (yBox + y) ].to_i
          return false
        end
      end
    end

    return true
  end

  def print_board
    i = j = 0
    9.times do
      # draw horizontal line
      if i == 0
        print "-" * 13
        puts ""
      end
      9.times do
        # start box
        if j == 0: print "|" end

        print sudoku_board[i][j]

        # put box after 3, 6 and 9th number
        if j.modulo(3) == 2: print "|" end
        j += 1
      end
      puts ""
      # draw remaining horizontal lines
      if i.modulo(3) == 2
        print "-" * 13
        puts ""
      end
      j = 0
      i += 1
    end
  end
end

s = Solver.new
puts "Before solving"
s.print_board
puts "Solving..."
solved = s.solve_init
puts "Finished!"
if solved
  s.print_board
else
  puts "No solution..."
end
