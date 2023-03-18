import pygame
from pygame.locals import *
import random
import sys
from abc import ABC, abstractmethod

class AIStrategy(ABC):
    @abstractmethod
    def make_move(self, board, player):
        pass

class RandomStrategy(AIStrategy):
    def make_move(self, board, player):
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == '']
        if empty_cells:
            return random.choice(empty_cells)
        return None, None

class OptimalStrategy(AIStrategy):
    def make_move(self, board, player):
        opponent = 'O' if player == 'X' else 'X'

        def check_win(board, player):
            for i in range(3):
                if board[i][0] == board[i][1] == board[i][2] == player:
                    return True
                if board[0][i] == board[1][i] == board[2][i] == player:
                    return True
            if board[0][0] == board[1][1] == board[2][2] == player:
                return True
            if board[0][2] == board[1][1] == board[2][0] == player:
                return True
            return False

        def minimax(board, depth, is_maximizing):
            if check_win(board, player):
                return 1
            if check_win(board, opponent):
                return -1
            if all(board[row][col] != '' for row in range(3) for col in range(3)):
                return 0

            if is_maximizing:
                best_value = -float('inf')
                for row in range(3):
                    for col in range(3):
                        if board[row][col] == '':
                            board[row][col] = player
                            value = minimax(board, depth + 1, False)
                            board[row][col] = ''
                            best_value = max(best_value, value)
                return best_value
            else:
                best_value = float('inf')
                for row in range(3):
                    for col in range(3):
                        if board[row][col] == '':
                            board[row][col] = opponent
                            value = minimax(board, depth + 1, True)
                            board[row][col] = ''
                            best_value = min(best_value, value)
                return best_value

        best_move = None, None
        best_value = -float('inf')

        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = player
                    value = minimax(board, 0, False)
                    board[row][col] = ''
                    if value > best_value:
                        best_value = value
                        best_move = row, col

        return best_move

class OptimalStrategyAlphaBeta(AIStrategy):
    def make_move(self, board, player):
        opponent = 'O' if player == 'X' else 'X'

        def check_win(board, player):
            for i in range(3):
                if board[i][0] == board[i][1] == board[i][2] == player:
                    return True
                if board[0][i] == board[1][i] == board[2][i] == player:
                    return True
            if board[0][0] == board[1][1] == board[2][2] == player:
                return True
            if board[0][2] == board[1][1] == board[2][0] == player:
                return True
            return False

        def minimax(board, depth, alpha, beta, is_maximizing):
            if check_win(board, player):
                return 1
            if check_win(board, opponent):
                return -1
            if all(board[row][col] != '' for row in range(3) for col in range(3)):
                return 0

            if is_maximizing:
                best_value = -float('inf')
                for row in range(3):
                    for col in range(3):
                        if board[row][col] == '':
                            board[row][col] = player
                            value = minimax(board, depth + 1, alpha, beta, False)
                            board[row][col] = ''
                            best_value = max(best_value, value)
                            alpha = max(alpha, best_value)
                            if beta <= alpha:
                                return best_value
                return best_value
            else:
                best_value = float('inf')
                for row in range(3):
                    for col in range(3):
                        if board[row][col] == '':
                            board[row][col] = opponent
                            value = minimax(board, depth + 1, alpha, beta, True)
                            board[row][col] = ''
                            best_value = min(best_value, value)
                            beta = min(beta, best_value)
                            if beta <= alpha:
                                return best_value
                return best_value

        best_move = None, None
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = player
                    value = minimax(board, 0, alpha, beta, False)
                    board[row][col] = ''
                    if value > best_value:
                        best_value = value
                        best_move = row, col

        return best_move

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption('Tic-Tac-Toe')

        self.cell_size = 100
        self.line_color = (255, 255, 255)
        self.line_width = 3
        self.font = pygame.font.Font(None, 30)

        self.reset()

    def reset(self):
        self.board = [['', '', ''] for _ in range(3)]
        self.current_player = 'X'
        self.ai_strategy = None
        self.ai_player = 'O'
        self.game_over = False
        self.winner = None

    def draw_board(self):
        # Draw the game board
        self.screen.fill((0, 0, 0))

        for i in range(1, 3):
            pygame.draw.line(self.screen, self.line_color, (i * self.cell_size, 0), (i * self.cell_size, 300), self.line_width)
            pygame.draw.line(self.screen, self.line_color, (0, i * self.cell_size), (300, i * self.cell_size), self.line_width)

        for row in range(3):
            for col in range(3):
                if self.board[row][col] != '':
                    text = self.font.render(self.board[row][col], True, self.line_color)
                    position = ((col * self.cell_size) + (self.cell_size // 2) - (text.get_width() // 2),
                                (row * self.cell_size) + (self.cell_size // 2) - (text.get_height() // 2))
                    self.screen.blit(text, position)

        pygame.display.flip()

    def check_win(self):
        # Check if a player has won
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]

        return None

    def check_draw(self):
        # Check if the game is a draw
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    return False
        return True

    def update_board(self, row, col, player):
        # Update the game board with a player's move
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False

    def get_empty_cells(self):
        # Get a list of empty cells on the game board
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    empty_cells.append((row, col))
        return empty_cells

    def is_valid_move(self, row, col):
        # Check if the move is valid
        return self.board[row][col] == ''

    def make_ai_move(self):
        if self.ai_strategy and self.current_player == self.ai:
            row, col = self.ai_strategy.make_move(self.board, self.ai)
            if row is not None and col is not None:
                self.update_board(row, col, self.ai)
                self.winner = self.check_win()
                if not self.winner:
                    self.current_player = 'O' if self.current_player == 'X' else 'X'

    def handle_events(self):
        # Handle game events, such as mouse clicks or key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
                x, y = pygame.mouse.get_pos()
                row, col = y // self.cell_size, x // self.cell_size
                if self.update_board(row, col, self.current_player):
                    self.winner = self.check_win()
                    if not self.winner:
                        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def menu(self):
        menu_option = -1
        while menu_option not in ['0', '1', '2']:
            self.screen.fill((0, 0, 0))
            self.draw_text("1: One Player", (100, 100), (255, 255, 255))
            self.draw_text("2: Two Players", (100, 150), (255, 255, 255))
            self.draw_text("0: Exit", (100, 200), (255, 255, 255))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.unicode in ['0', '1', '2']:
                    menu_option = event.unicode

        if menu_option == '0':
            pygame.quit()
            sys.exit()
        elif menu_option == '1':
            self.select_ai_strategy()
        else:
            self.play_game(None)

    def select_ai_strategy(self):
        strategy_option = -1
        while strategy_option not in ['1', '2', '3', '0']:
            self.screen.fill((0, 0, 0))
            self.draw_text("1: Random Strategy", (60, 100), (255, 255, 255))
            self.draw_text("2: Optimal Strategy", (60, 150), (255, 255, 255))
            self.draw_text("3: Optimal AlphaBeta", (60, 200), (255, 255, 255))
            self.draw_text("0: Back", (60, 250), (255, 255, 255))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.unicode in ['0', '1', '2', '3']:
                    strategy_option = event.unicode

        if strategy_option == '0':
            self.menu()
        elif strategy_option == '1':
            self.play_game(RandomStrategy(), self.select_player_marker())
        elif strategy_option == '2':
            self.play_game(OptimalStrategy(), self.select_player_marker())
        else:
            self.play_game(OptimalStrategyAlphaBeta(), self.select_player_marker())

    def select_player_marker(self):
        marker_option = -1
        while marker_option not in ['1', '2', '0']:
            self.screen.fill((0, 0, 0))
            self.draw_text("1: X", (60, 100), (255, 255, 255))
            self.draw_text("2: O", (60, 150), (255, 255, 255))
            self.draw_text("0: Back", (60, 200), (255, 255, 255))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.unicode in ['0', '1', '2']:
                    marker_option = event.unicode

        if marker_option == '0':
            self.select_ai_strategy()
        elif marker_option == '1':
            return 'X'
        else:
            return 'O'

    def play_game(self, ai_strategy=None, ai_player=None):
        self.ai = ai_player
        self.main(ai_strategy)

    def show_results(self):
        self.screen.fill((0, 0, 0))
        if self.winner:
            self.draw_text(f"Player {self.winner} has won!", (60, 100), (255, 255, 255))
        else:
            self.draw_text("The game is a draw!", (60, 100), (255, 255, 255))
        self.draw_text("Press any key to continue", (30, 200), (255, 255, 255))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    self.menu()

    def draw_text(self, text, position, color):
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, position)

    def main(self, ai_strategy=None):
        # Main game loop
        self.reset()
        self.ai_strategy = ai_strategy
        while not self.game_over:
            if self.current_player == self.ai:
                self.make_ai_move()
            else:
                self.handle_events()
            self.draw_board()
            if self.winner or self.check_draw():
                self.game_over = True
            pygame.time.wait(50)

        if self.winner:
            print(f"Player {self.winner} has won the game!")
        else:
            print("The game is a draw!")

        self.show_results()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.menu()
    pygame.quit()
