class TicTacToe:
    def __init__(self, board_2d):
        self.board = [cell[2] for row in board_2d for cell in row]
        self.human_player = "x"
        self.ai_player = "o"
        self.size=len(board_2d)

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ""]

    def make_move(self, position, player):
        if self.board[position] == "":
            self.board[position] = player
            return True
        return False

    def is_board_full(self):
        return "" not in self.board

    def check_winner(self):
        # Check rows
        for i in range(0, self.size**2, self.size):
            points = 0 
            for j in range(self.size):
                if self.board[i+j] == 'x':
                    points += 1
                elif self.board[i+j] == 'o':
                    points -= 1
                if points == self.size:
                    return 'x'
                elif points == -self.size:
                    return 'o'

        for i in range(self.size):
            points = 0
            for j in range(self.size):
                if self.board[i+j*self.size] == 'x':
                    points += 1
                elif self.board[i+j*self.size] == 'o':
                    points -= 1
                if points == self.size:
                    return 'x'
                elif points == -self.size:
                    return 'o'

        # Check diagonals
        points = 0
        for i in range(self.size):
            if self.board[i*(self.size+1)] == 'x':
                points += 1
            elif self.board[i*(self.size+1)] == 'o':
                points -= 1
            if points == self.size:
                return 'x'
            elif points == -self.size:
                return 'o'
        points = 0
        for i in range(1, self.size+1):
            if self.board[i*(self.size-1)] == 'x':
                points += 1
            elif self.board[i*(self.size-1)] == 'o':
                points -= 1
            if points == self.size:
                return 'x'
            elif points == -self.size:
                return 'o'
        return None

    def minimax(self, depth, is_maximizing, alpha=float("-inf"), beta=float("inf")):
        print(f"Depth: {depth}, Board: {self.board}, Is Maximizing: {is_maximizing}, Alpha: {alpha}, Beta: {beta}")
        # Base cases
        winner = self.check_winner()
        if winner == self.ai_player:
            return 1
        elif winner == self.human_player:
            return -1
        elif self.is_board_full() or depth >= 4:  # Add a depth limit
            return 0

        # Maximizing player's turn (AI)
        if is_maximizing:
            best_score = float("-inf")
            for move in self.available_moves():
                self.board[move] = self.ai_player
                score = self.minimax(depth + 1, False, alpha, beta)
                self.board[move] = ""  # Undo the move
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:  # Prune the branch
                    break
            return best_score

        # Minimizing player's turn (Human)
        else:
            best_score = float("inf")
            for move in self.available_moves():
                self.board[move] = self.human_player
                score = self.minimax(depth + 1, True, alpha, beta)
                self.board[move] = ""  # Undo the move
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:  # Prune the branch
                    break
            return best_score

    def get_best_move(self):
        best_score = float("-inf")
        best_move = None

        for move in self.available_moves():
            # Make a calculating move
            self.board[move] = self.ai_player
            # Recursively call minimax with alpha-beta pruning
            score = self.minimax(0, False, float("-inf"), float("inf"))
            # Reset the move
            self.board[move] = ""

            # Update the best score
            if score > best_score:
                best_score = score
                best_move = (move // self.size, move % self.size)

        return best_move