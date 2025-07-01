import tkinter as tk
from tkinter import messagebox
class Gomoku:
    def __init__(self, master):
        self.master = master
        self.board_size = 15
        self.cell_size = 40
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack()

        # 当前回合标识 ('black' or 'white')
        self.current_turn = 'black'

        # 添加显示当前回合的标签
        self.turn_label = tk.Label(master, text="轮到：黑方", font=("Arial", 14), fg="black")
        self.turn_label.pack(pady=10)

        self.ecom = []  # 黑子位置列表
        self.recor = []  # 白子位置列表
        self.total_moves = []  # 所有已落子的位置

        self.draw_board()
        self.bind_events()

    def draw_board(self):
        board_pixel_size = self.board_size * self.cell_size
        offset = self.cell_size // 2
        for i in range(self.board_size):
            x = i * self.cell_size + offset
            self.canvas.create_line(x, offset, x, board_pixel_size + offset)
            self.canvas.create_line(offset, x, board_pixel_size + offset, x)

        # 绘制星位和天元
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11)]
        tengen = (7, 7)

        for point in star_points + [tengen]:
            x = point[1] * self.cell_size + offset
            y = point[0] * self.cell_size + offset
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def bind_events(self):
        self.canvas.bind("<Button-1>", lambda e: self.handle_click(e, 'black'))  # 左键：黑子
        self.canvas.bind("<Button-3>", lambda e: self.handle_click(e, 'white'))  # 右键：白子

    def handle_click(self, event, color):
        if color != self.current_turn:
            return  # 不允许非当前玩家操作

        pos = self.get_grid_pos(event)
        if pos == -1 or pos in self.total_moves:
            return

        self.draw_piece(pos, color)
        if color == 'black':
            self.ecom.append(pos)
        else:
            self.recor.append(pos)
        self.total_moves.append(pos)

        # 切换回合
        self.current_turn = 'white' if color == 'black' else 'black'
        self.turn_label.config(text=f"轮到：{'白方' if self.current_turn == 'white' else '黑方'}", fg=self.current_turn)

        if self.check_win(pos, color):
            messagebox.showinfo("胜利", f"{color}方获胜！")
            self.reset_game()

    def get_grid_pos(self, event):
        offset = self.cell_size // 2
        x = event.x - offset
        y = event.y - offset

        col = round(x / self.cell_size)
        row = round(y / self.cell_size)

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return row * self.board_size + col
        return -1

    def draw_piece(self, pos, color):
        row, col = divmod(pos, self.board_size)
        offset = self.cell_size // 2
        x = col * self.cell_size + offset
        y = row * self.cell_size + offset
        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color)

    def callback(self, event):
        pos = self.get_grid_pos(event)
        if pos == -1 or pos in self.total_moves:
            return
        self.draw_piece(pos, "black")
        self.ecom.append(pos)
        self.total_moves.append(pos)
        if self.check_win(pos, "black"):
            messagebox.showinfo("胜利", "黑方获胜！")
            self.reset_game()

    def callback2(self, event):
        pos = self.get_grid_pos(event)
        if pos == -1 or pos in self.total_moves:
            return
        self.draw_piece(pos, "white")
        self.recor.append(pos)
        self.total_moves.append(pos)
        if self.check_win(pos, "white"):
            messagebox.showinfo("胜利", "白方获胜！")
            self.reset_game()

    def check_win(self, pos, color):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for step in [1, -1]:
                x, y = divmod(pos, self.board_size)
                while True:
                    x += dx * step
                    y += dy * step
                    if 0 <= x < self.board_size and 0 <= y < self.board_size:
                        neighbor = x * self.board_size + y
                        if neighbor in (self.ecom if color == "black" else self.recor):
                            count += 1
                        else:
                            break
                    else:
                        break
            if count >= 5:
                return True
        return False

    def reset_game(self):
        self.canvas.delete("all")
        self.draw_board()
        self.ecom.clear()
        self.recor.clear()
        self.total_moves.clear()
        self.current_turn = 'black'
        self.turn_label.config(text="轮到：黑方", fg="black")
        self.current_turn = 'white'
        self.turn_label.config(text="轮到：白方", fg="white")


def start_game():
    root = tk.Tk()
    game = Gomoku(root)
    root.mainloop()

def main():
    window = tk.Tk()
    window.title("五子棋游戏")

    btn_start = tk.Button(window, text="开始游戏", command=start_game)
    btn_exit = tk.Button(window, text="退出游戏", command=window.destroy)

    btn_start.pack(pady=20)
    btn_exit.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
