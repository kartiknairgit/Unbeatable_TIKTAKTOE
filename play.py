import tkinter as tk
from tkinter import messagebox
import random
import time
import json
import os

class MinimaxAgent:
    def __init__(self):
        pass

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner(board)
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif "" not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def choose_action(self, board):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = self.minimax(board, 0, False)
                board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def check_winner(self, board):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in win_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
                return board[combo[0]]
        return None

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.master.geometry("400x550")
        self.master.configure(bg="#1A1A2E")

        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.against_ai = True
        self.timer = None
        self.time_left = 10

        self.agent = MinimaxAgent()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Tic-Tac-Toe", font=("Roboto", 28, "bold"), bg="#1A1A2E", fg="#E94560")
        self.title_label.pack(pady=10)

        self.game_frame = tk.Frame(self.master, bg="#16213E")
        self.game_frame.pack(pady=10)

        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.game_frame, text="", font=("Roboto", 24, "bold"), width=3, height=1,
                                command=lambda row=i, col=j: self.on_click(row, col),
                                bg="#0F3460", fg="black", activebackground="#E94560")
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

        self.status_label = tk.Label(self.master, text="Player X's turn", font=("Roboto", 16), bg="#1A1A2E", fg="#E94560")
        self.status_label.pack(pady=10)

        self.timer_label = tk.Label(self.master, text="Time left: 10", font=("Roboto", 14), bg="#1A1A2E", fg="#E94560")
        self.timer_label.pack()

        self.mode_button = tk.Button(self.master, text="Mode: vs AI", font=("Roboto", 12), command=self.toggle_mode,
                                     bg="#0F3460", fg="black", activebackground="#E94560")
        self.mode_button.pack(pady=5)

        self.reset_button = tk.Button(self.master, text="Reset Game", font=("Roboto", 12), command=self.reset_game,
                                      bg="#0F3460", fg="black", activebackground="#E94560")
        self.reset_button.pack(pady=5)

        self.start_timer()

    def on_click(self, row, col):
        if not self.game_over and self.board[3 * row + col] == "":
            self.make_move(3 * row + col)
            
            if self.against_ai and self.current_player == "O" and not self.game_over:
                self.master.after(1000, self.ai_move)

    def make_move(self, move):
        self.board[move] = self.current_player
        self.buttons[move].config(text=self.current_player, 
                                  bg="#E94560" if self.current_player == "X" else "#0F3460",
                                  fg="black")

        if self.check_winner():
            self.game_over = True
            self.status_label.config(text=f"Player {self.current_player} wins!")
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.stop_timer()
            self.save_game_history()
        elif "" not in self.board:
            self.game_over = True
            self.status_label.config(text="It's a tie!")
            messagebox.showinfo("Game Over", "It's a tie!")
            self.stop_timer()
            self.save_game_history()
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s turn")
            self.reset_timer()

    def ai_move(self):
        action = self.agent.choose_action(self.board)
        self.make_move(action)

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(self.board[i] == self.board[j] == self.board[k] != "" for i, j, k in win_combinations)

    def toggle_mode(self):
        self.against_ai = not self.against_ai
        new_text = "Mode: vs AI" if self.against_ai else "Mode: 2 Players"

        # Micro transition effect
        self.mode_button.config(fg="white")
        self.master.after(100, lambda: self.mode_button.config(fg="black", text=new_text))
        
        self.reset_game()

    def reset_game(self):
        # Micro transition effect
        self.reset_button.config(fg="white")
        self.master.after(100, lambda: self.reset_button.config(fg="black"))
        
        self.stop_timer()
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        for button in self.buttons:
            button.config(text="", bg="#0F3460", fg="black")
        self.status_label.config(text="Player X's turn")
        self.reset_timer()
        self.start_timer()

    def start_timer(self):
        self.time_left = 10
        self.update_timer()

    def stop_timer(self):
        if self.timer is not None:
            self.master.after_cancel(self.timer)
            self.timer = None

    def reset_timer(self):
        self.stop_timer()
        self.start_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer = self.master.after(1000, self.update_timer)
        else:
            self.time_out()

    def time_out(self):
        if not self.game_over:
            messagebox.showinfo("Time's up!", f"Player {self.current_player} ran out of time!")
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s turn")
            self.reset_timer()
            if self.against_ai and self.current_player == "O":
                self.master.after(1000, self.ai_move())

    def save_game_history(self):
        game_data = {
            "player_moves": [i for i, p in enumerate(self.board) if p == "X"],
            "ai_moves": [i for i, p in enumerate(self.board) if p == "O"]
        }

        filename = "AI_game_history.json" if self.against_ai else "TwoPlayer_game_history.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
        else:
            data = []
        
        data.append(game_data)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
