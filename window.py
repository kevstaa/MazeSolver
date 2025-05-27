from tkinter import Tk, BOTH, Canvas
import time
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y,
            self.p2.x, self.p2.y,
            fill=fill_color, width=2
        )

class Window:
    def __init__(self, width, height):
        # Create the root Tk widget
        self.__root = Tk()
        self.__root.title("Tkinter Window")
        self.width = width
        self.height = height
        # Create the canvas widget
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        # Running state for the window loop
        self.running = False
        # Ensure window cloase uses our close method
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        # Redraw graphics
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.__root.destroy()

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1
        self.__win = win
        
    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.__win is None:
            return
        
        bg = "#d9d9d9"
        left_color = "black" if self.has_left_wall else bg
        top_color = "black" if self.has_top_wall else bg
        right_color = "black" if self.has_right_wall else bg
        bottom_color = "black" if self.has_bottom_wall else bg

        Line(Point(x1, y1), Point(x1, y2)).draw(self.__win.canvas, left_color)
        Line(Point(x1, y1), Point(x2, y1)).draw(self.__win.canvas, top_color)
        Line(Point(x2, y1), Point(x2, y2)).draw(self.__win.canvas, right_color)
        Line(Point(x1, y2), Point(x2, y2)).draw(self.__win.canvas, bottom_color)

    def center(self):
        # Returns the center point of the cell (current position)
        if min(self.__x1, self.__y1, self.__x2, self.__y2) < 0:
            # Not yet drawn or coordinates not set
            return None
        return Point((self.__x1 + self.__x2) // 2, (self.__y1 + self.__y2) // 2)
    
    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return
        color = "gray" if undo else "red"
        from_center = self.center()
        to_center = to_cell.center()
        move_line = Line(from_center, to_center)
        move_line.draw(self.__win.canvas, color)
    

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        if seed is not None:
            random.seed(seed)
        self.__create_cells()

    def __create_cells(self):
        self.__cells = []
        for i in range(self.__num_cols):
            col = []
            for j in range(self.__num_rows):
                cell = Cell(self.__win)
                col.append(cell)
            self.__cells.append(col)
        # draw all cells
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        cell = self.__cells[i][j]
        cell.draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        if self.__win is not None:
            self.__win.redraw()
            time.sleep(0.05)

    def __break_entrance_and_exit(self):
        self._Maze__cells[0][0].has_top_wall = False
        self._Maze__draw_cell(0, 0)
        last_col = self._Maze__num_cols - 1
        last_row = self._Maze__num_rows - 1
        self._Maze__cells[last_col][last_row].has_bottom_wall = False
        self._Maze__draw_cell(last_col, last_row)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            directions = []
            # Check left
            if i > 0 and not self.__cells[i - 1][j].visited:
                directions.append(('L', i - 1, j))
            # Check right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                directions.append(('R', i + 1, j))
            # Check up
            if j > 0 and not self.__cells[i][j - 1].visited:
                directions.append(('U', i, j - 1))
            # Check down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                directions.append(('D', i, j + 1))
            if not directions:
                self._Maze__draw_cell(i, j)
                return
            dir, ni, nj = random.choice(directions)
            # Knock down walls between (i,j) and (ni,nj)
            if dir == 'L':
                self.__cells[i][j].has_left_wall = False
                self.__cells[ni][nj].has_right_wall = False
            elif dir == 'R':
                self.__cells[i][j].has_right_wall = False
                self.__cells[ni][nj].has_left_wall = False
            elif dir == 'U':
                self.__cells[i][j].has_top_wall = False
                self.__cells[ni][nj].has_bottom_wall = False
            elif dir == 'D':
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[ni][nj].has_top_wall = False
            self._Maze__draw_cell(i, j)
            self._Maze__draw_cell(ni, nj)
            self.__break_walls_r(ni, nj)

    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False


    def solve(self):
        """Intenta resolver el laberinto desde la celda (0,0) usando DFS."""
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        cell = self.__cells[i][j]
        cell.visited = True

        # ¿Estamos en la meta?
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        # Direcciones: (dx, dy, pared_actual, pared_vecino)
        directions = [
            (-1, 0, "has_left_wall", "has_right_wall"),   # izquierda
            (1, 0, "has_right_wall", "has_left_wall"),    # derecha
            (0, -1, "has_top_wall", "has_bottom_wall"),   # arriba
            (0, 1, "has_bottom_wall", "has_top_wall"),    # abajo
        ]

        for dx, dy, wall, neighbor_wall in directions:
            ni, nj = i + dx, j + dy
            # ¿Está dentro del rango?
            if 0 <= ni < self.__num_cols and 0 <= nj < self.__num_rows:
                neighbor = self.__cells[ni][nj]
                # ¿Hay paso y no visitado?
                if not getattr(cell, wall) and not neighbor.visited:
                    cell.draw_move(neighbor)
                    if self._solve_r(ni, nj):
                        return True
                    cell.draw_move(neighbor, undo=True)
        return False
    
    def _animate(self):
        if self.__win is not None:
            self.__win.redraw()
            import time; time.sleep(0.05)


def main():
    win = Window(800, 600)
    # Small Maze
    maze = Maze(50, 50, 10, 12, 40, 40, win, seed=0)
    maze._Maze__break_walls_r(0, 0)
    maze._Maze__break_entrance_and_exit()
    maze._Maze__reset_cells_visited()
    maze.solve()
    win.wait_for_close()

if __name__ == '__main__':
    main()
