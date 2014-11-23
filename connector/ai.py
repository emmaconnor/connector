inf = 100000000000000000000000

class AI(object):
    """An AI for playing Connect Four-like games."""

    def __init__(self, my_t, depth=4):
        self.t = my_t
        if my_t == 'X':
            self.other_t = 'O'
        else:
            self.other_t = 'X'
        self.depth = depth

    def get_move(self, board):
        """Get the best possible move."""
        move, score = self.neg_max(board, self.depth, True, -inf, inf)
        return move, self.t

    def neg_max(self, board, depth, my_turn, alpha, beta):
        """Recursively search for the best move."""
        wg = board.get_winning_group()

        if depth == 0 or wg is not None:
            score = self.score_state(board, self.t)
            if not my_turn:
                score = -score
            return None, score

        possible_moves = board.get_valid_moves()

        def order_move(m):
            board.drop_piece(m, self.t if my_turn else self.other_t)
            score = self.score_state(board, self.t)
            board.remove_piece(m)
            if my_turn:
                score = -score
            return score
        possible_moves = sorted(possible_moves, key=order_move)

        max_score = None
        max_move = None
        for m in possible_moves:
            board.drop_piece(m, self.t if my_turn else self.other_t)
            move, score = self.neg_max(board, depth-1, not my_turn, -beta, -alpha)
            score = -score
            board.remove_piece(m)
            if max_score is None or score > max_score:
                max_score = score
                max_move = m
            alpha = max(alpha, score)
            if alpha >= beta:
                break

        if max_score is None:
            return None, self.score_state(board, self.t)

        return max_move, max_score

    def score_state(self, board, to_play):
        """Score a board's state as-is. A higher score represents a more favorable position."""
        score = 0
        def score_group(start, dir, t):
            r, c = start
            dr, dc = dir
            changes = 0
            for i in range(board.win_size):
                if board[r, c] == '.':
                    dist = 0
                    tr = r
                    while board.in_bounds(tr, c) and board[tr, c] == '.':
                        dist += 1
                        tr -= 1
                    changes += dist
                elif board[r, c] == t:
                    pass
                else:
                    return 0

                r, c = r + dr, c + dc

            #print "STARTING AT %s, %s MOVING %s, %s (TYPE: %s) CHANGES: %s" % (start+dir+(t,changes))
            if changes == 0:
                return inf

            return 2**max(10 - changes, 0) / 100.0

        # Get all horizontal groups
        for sr in range(board.rows):
            for sc in range(board.cols - board.win_size + 1):
                score += score_group((sr, sc), (0, 1), self.t)
                score -= score_group((sr, sc), (0, 1), self.other_t)

        # Get all vertical groups
        for sc in range(board.cols):
            for sr in range(board.rows - board.win_size + 1):
                score += score_group((sr, sc), (1, 0), self.t)
                score -= score_group((sr, sc), (1, 0), self.other_t)

        # Get all ascending diagonal groups
        for sr in range(board.rows - board.win_size + 1):
            for sc in range(board.cols - board.win_size + 1):
                score += score_group((sr, sc), (1, 1), self.t)
                score -= score_group((sr, sc), (1, 1), self.other_t)

        # Get all descending diagonal groups
        for sr in range(board.rows-1, board.win_size-1, -1):
            for sc in range(board.cols - board.win_size + 1):
                score += score_group((sr, sc), (-1, 1), self.t)
                score -= score_group((sr, sc), (-1, 1), self.other_t)

        return score
