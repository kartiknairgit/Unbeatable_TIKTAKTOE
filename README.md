# Unbeatable Tic-Tac-Toe

A Python-based Tic-Tac-Toe game with a graphical interface using Tkinter. This project implements a basic Tic-Tac-Toe game with both two-player and single-player modes. The AI opponent is based on the Minimax algorithm, making it unbeatable.

## Features

- **Two-player mode**: Play against another player locally.
- **AI mode**: Play against an AI opponent using the Minimax algorithm.
- **Game timer**: Players have a 10-second time limit for each move.
- **Game history**: Tracks and stores game history for both AI and two-player modes.


## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/unbeatable-tictactoe.git
    ```
   
2. **Navigate to the project directory**:
    ```bash
    cd unbeatable-tictactoe
    ```

3. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv tictactoe_env
    source tictactoe_env/bin/activate   # On Windows: tictactoe_env\Scripts\activate
    ```

4. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the game**:
    ```bash
    python play.py
    ```

## Usage

- **Mode Selection**: You can switch between "vs AI" and "2 Players" mode using the "Mode" button.
- **Reset Game**: Use the "Reset Game" button to start a new game.
- **Timer**: Each player has 10 seconds to make their move. If the time runs out, the turn automatically switches to the other player.

## Minimax Algorithm

The AI opponent utilizes the Minimax algorithm, making it unbeatable. The algorithm explores all possible moves and selects the optimal move to either win or prevent the player from winning.

## Game History

The game history is saved in JSON format in the following files:
- `AI_game_history.json` for AI matches.
- `TwoPlayer_game_history.json` for two-player matches.

These files track the moves made by each player, which can be used for analyzing gameplay or further development.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature/YourFeature
    ```
3. **Make your changes** and commit them:
    ```bash
    git commit -m "Add some feature"
    ```
4. **Push to the branch**:
    ```bash
    git push origin feature/YourFeature
    ```
5. **Open a pull request** to the `main` branch.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.



