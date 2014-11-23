try:
    import colorama
except ImportError:
    colors = {
        'X': '',
        'O': '',
        '.': '',
    }
    color_reset = ''
else:
    colorama.init()
    colors = {
        'X': colorama.Fore.RED,
        'O': colorama.Fore.YELLOW,
        '.': '',
    }
    color_reset = colorama.Fore.RESET

class Board:
    """The game board."""
    
    def __init__(self, size, win_size):
        self.rows, self.cols = size
        self.win_size = win_size
        self.board = [[] for x in xrange(self.cols)]

    def print_board(self):
        """Print the board"""
        for r in range(self.rows-1, -1, -1):
            line = ''
            for c in range(self.cols):
                t = self[r, c]
                line += colors[t] + t + color_reset + ' '
            print line

        line = ''
        maxlen = len(str(self.cols))
        fstr = "%%%dd" % maxlen
        colstrs = [(fstr%c)[::-1] for c in range(self.cols)]
        for l in zip(*colstrs):
            print ' '.join(l)

    def is_playable(self, c):
        """Check if a given column is playable (i.e, not full)."""
        if not (0 <= c < self.cols):
            return False
        if len(self.board[c]) >= self.rows:
            return False
        return True

    def get_valid_moves(self):
        """Return all playable columns"""
        moves = []
        for c in range(self.cols):
            if self.is_playable(c):
                moves.append(c)
        return moves

    def is_full(self):
        """Return whether the board is completely full or not."""
        return len(self.get_valid_moves()) == 0

    def drop_piece(self, c, t):
        """Add a piece to the given column."""
        if self.is_playable(c):
            self.board[c].append(t)
        else:
            print "ERROR"

    def remove_piece(self, c):
        """Remove the top piece in the given column."""
        self.board[c].pop()

    def in_bounds(self, r, c):
        """Check if the given row and column are within the board bounds."""
        if not (0 <= r < self.rows):
            return False
        if not (0 <= c < self.cols):
            return False
        return True

    def __getitem__(self, coords):
        """Return the piece type at the given coords, or '.' if empty."""
        r, c = coords
        col = self.board[c]
        if r < len(col):
            return col[r]
        else:
            return '.'

    def get_winning_group(self):
        """Get the winning group, if there is one. Otherwise return None."""
        seqs = self.get_seqs()
        for seq in seqs:
            if len(seq) >= self.win_size:
                return seq
        return None

    def get_seqs(self):
        """Return all consecutive sequences of pieces of the same type of size greater than one."""
        seqs = []

        def get_consecutive(start, d):
            r, c = start
            dr, dc = d
            runs = []
            run = []
            last_t = None
            while self.in_bounds(r, c):
                t = self[r, c]
                if t == '.' or (t != last_t and last_t is not None):
                    if len(run) > 1:
                        runs.append(run)
                    run = []
                    if t != '.':
                        run.append((r, c))                    
                else:
                    run.append((r, c))
                last_t = t
                r, c = r + dr, c + dc
            if len(run) > 1:
                runs.append(run)
            return runs

        # Get all horizontal groups
        for sr in range(self.rows):
            seqs += get_consecutive((sr, 0), (0, 1))

        # Get all vertical groups
        for sc in range(self.cols):
            seqs += get_consecutive((0, sc), (1, 0))

        # Get all ascending diagonal groups
        for sr in range(self.rows):
            seqs += get_consecutive((sr, 0), (1, 1))
        for sc in range(1, self.cols):
            seqs += get_consecutive((0, sc), (1, 1))

        # Get all descending diagonal groups
        for sr in range(self.rows):
            seqs += get_consecutive((sr, 0), (-1, 1))
        for sc in range(1, self.cols):
            seqs += get_consecutive((self.rows - 1, sc), (-1, 1))

        return seqs