import sys


def bingo(nums, boards):
    # idea: since boards should contain unique elements, keep elements
    # hashed to their respecive row and column idxs. Looking up a number
    # is then constant, and decrementing the row/col count is constant

    # assuming all boards are square and equal size
    N = len(boards[0][0])

    class Board:
        def __init__(self, board):
            self.board = board
            self.row_counts = [0] * N  # i
            self.col_counts = [0] * N  # j
            self.called = [[False for _ in board[0]] for _ in board]
            self.nums = {
                board[i][j]: (i, j)
                for i in range(len(board))
                for j in range(len(board[0]))
            }
            self.winner = False

        def check_num(self, n):
            # check if a number results in a bingo
            if n not in self.nums:
                return False

            row_idx, col_idx = self.nums[n]
            self.row_counts[row_idx] += 1
            self.col_counts[col_idx] += 1
            self.called[row_idx][col_idx] = True

            if self.row_counts[row_idx] == N or self.col_counts[col_idx] == N:
                self.winner = True
                return True

            return False

        def sum_unmarked(self):
            res = 0
            for i in range(N):
                for j in range(N):
                    if not self.called[i][j]:
                        res += self.board[i][j]
            return res

    boards = [Board(board) for board in boards]
    part1 = None
    part2 = None
    has_won = [False] * len(boards)

    for num in nums:
        for i, board in enumerate(boards):
            if board.check_num(num):
                # bingo!
                if part1 is None:
                    # first winner
                    part1 = board.sum_unmarked() * num
                elif not has_won[i] and sum(has_won) == len(boards) - 1:
                    # final winner
                    part2 = board.sum_unmarked() * num
                has_won[i] = True
        if part1 is not None and part2 is not None:
            break

    return part1, part2


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read()

    nums, *boards = content.split('\n\n')
    nums = [int(n) for n in nums.split(',')]

    boards = [
        [[int(n) for n in row.split(' ') if n]
         for row in board.split('\n') if row]
        for board in boards
    ]

    val1, val2 = bingo(nums, boards)
    print('Part 1:', val1)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
