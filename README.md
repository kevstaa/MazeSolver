# MazeSolver

MazeSolver is a Python application that generates and solves mazes visually using the Tkinter library.

## What It Does

- Generates a random maze using depth-first search (DFS) with backtracking.
- Visualizes the maze generation and solving process step by step.
- Solves the maze from the top-left to the bottom-right cell, showing the pathfinding process.
- Provides a graphical window where you can watch the maze being built and solved in real time.

## How It Works

- When you run `window.py`, a Tkinter window opens and displays the maze grid.
- The maze is generated cell by cell, with walls being removed to create a solvable path.
- After generation, the solver uses DFS to find a path from the entrance to the exit, animating each move.
- The window remains open until you close it.

## Requirements

- Python 3.7 or higher
- Tkinter (usually included with standard Python installations)

## How to Run

1. Install Python if you haven't already.
2. Make sure Tkinter is available (it is included by default in most Python distributions).
3. Run the application with:

```bash
python3 window.py
```

A window will appear showing the maze generation and solving process.

## License

This project is for educational purposes.
