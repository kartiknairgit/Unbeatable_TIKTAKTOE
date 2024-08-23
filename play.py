import tkinter as tk
from tkinter import messagebox
import random
import time
import pickle
import json
import os

class QAgent:
    def __init__(self, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.q_table = {}
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, available_actions):
        if random.random() < self.epsilon:
            return random.choice(available_actions)
        else:
            q_values = [self.get_q_value(state, a) for a in available_actions]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(available_actions, q_values) if q == max_q]
            return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        old_q = self.get_q_value(state, action)
        next_max_q = max([self.get_q_value(next_state, a) for a in range(9) if next_state[a] == ''])
        new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)
        self.q_table[(state, action)] = new_q

    def save_q_table(self, filename='q_table.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename='q_table.pkl'):
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print("Q-table file not found. Starting with an empty Q-table.")

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

        self.agent = QAgent()
        self.agent.load_q_table()

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
                                     bg="#0F3460", fg="white", activebackground="#E94560")
        self.mode_button.pack(pady=5)

        self.reset_button = tk.Button(self.master, text="Reset Game", font=("Roboto", 12), command=self.reset_game,
                                      bg="#0F3460", fg="white", activebackground="#E94560")
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
            if self.against_ai:
                reward = 1 if self.current_player == "O" else -1
                self.agent.learn(tuple(self.board), move, reward, tuple(self.board))
            self.save_game_history()
        elif "" not in self.board:
            self.game_over = True
            self.status_label.config(text="It's a tie!")
            messagebox.showinfo("Game Over", "It's a tie!")
            self.stop_timer()
            if self.against_ai:
                self.agent.learn(tuple(self.board), move, 0, tuple(self.board))
            self.save_game_history()
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s turn")
            self.reset_timer()

    def ai_move(self):
        state = tuple(self.board)
        available_actions = [i for i, v in enumerate(self.board) if v == ""]
        action = self.agent.choose_action(state, available_actions)
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
        self.mode_button.config(text="Mode: vs AI" if self.against_ai else "Mode: 2 Players")
        self.reset_game()

    def reset_game(self):
        self.stop_timer()
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        for button in self.buttons:
            button.config(text="", bg="#0F3460", fg="black")
        self.status_label.config(text="Player X's turn")
        self.reset_timer()
        self.start_timer()
        self.agent.save_q_table()  # Save the Q-table after each game

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
    game = TicTacToe(root)
    root.mainloop()
