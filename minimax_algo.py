class TicTacToe:
    def __init__(self, board_2d):
        self.board = [cell[2] for row in board_2d for cell in row]
        self.human_player = "x"
        self.ai_player = "o"

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
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != "":
                return self.board[i]

        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != "":
                return self.board[i]

        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != "":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != "":
            return self.board[2]

        return None

    def minimax(self, depth, is_maximizing):
        # Base cases
        winner = self.check_winner()
        if winner == self.ai_player:
            return 1
        if winner == self.human_player:
            return -1
        if self.is_board_full():
            return 0
        
        # if it is the maximizing player's turn (AI), we want to maximize the score
        if is_maximizing:
            best_score = float("-inf")
            for move in self.available_moves():
                # Make a calculating move
                self.board[move] = self.ai_player
                # Recursively call minimax with the next depth and the minimizing player
                score = self.minimax(depth + 1, False)
                # Reset the move
                self.board[move] = ""
                # Update the best score
                best_score = max(score, best_score)
            return best_score
        
        else:
            # if it is the minimizing player's turn (human), we want to minimize the score
            best_score = float("inf")
            for move in self.available_moves():
                # Make a calculating move
                self.board[move] = self.human_player
                # Recursively call minimax with the next depth and the maximizing player
                score = self.minimax(depth + 1, True)
                # Reset the move
                self.board[move] = ""
                # Update the best score
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        best_score = float("-inf")
        best_move = None

        for move in self.available_moves():
            # Make a calculating move
            self.board[move] = self.ai_player
            # Recursively call minimax with the next depth and the minimizing player
            score = self.minimax(0, False)
            # Reset the move
            self.board[move] = ""

            # Update the best score
            if score > best_score:
                best_score = score

                # move is a val from 0-8
                best_move = (move//3, move % 3)

        return best_move