# Othello AI Game (Python + Tkinter)

A fully playable **Othello (Reversi) board game** built using Python Tkinter with an AI opponent powered by the Minimax algorithm.

---

## Features

- 8×8 interactive game board
- Classic Othello rules implemented
- Valid move highlighting
- Turn-based gameplay (Black vs AI White)
- AI opponent using Minimax algorithm
- Score tracking system
- Game over detection with winner announcement
- Restart game option

---

## AI Logic

The AI uses the **Minimax algorithm** to evaluate moves and choose the best possible action.  
It simulates future game states to maximize its advantage.

---

## Technologies Used

- Python 3
- Tkinter (GUI)
- Minimax Algorithm
- Object-free procedural game design

---

## Project Structure
othello_game/
│
├── gui.py # Main game (run this file)
├── othello.py # Game logic + AI

---

## How to Run

```bash
git clone https://github.com/YOUR_USERNAME/othello-ai-game.git
cd othello-ai-game
python3 gui.py
```
