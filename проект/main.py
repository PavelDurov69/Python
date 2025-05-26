"""
Проект MiniPaint
Клон графического редактора Microsoft Paint

Версия 1.0 (2025)
Автор: Свистунов Александр, ИБС235, КАИТ № 20
г. Москва, 2025
"""


import tkinter as tk
from tkinter import ttk  # Для виджетов с современным стилем
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageGrab
import os

# --- Константы ---
DEFAULT_COLOR = "black"
DEFAULT_BG_COLOR = "white"
DEFAULT_WIDTH = 4
MAX_WIDTH = 30
CANVAS_WIDTH = 900  # Сделаем холст шире
CANVAS_HEIGHT = 650 # И выше

# Классическая палитра Paint (приближённо)
COLOR_PALETTE = [
    "black", "gray50", "maroon", "red",
    "green", "lime", "navy", "blue",
    "purple", "magenta", "teal", "aqua",
    "silver", "gray80", "olive", "yellow",
    "white", "#FFC0CB", "#FFD700", "#E6E6FA",
    "#ADFF2F", "#ADD8E6", "#FFA07A", "#FFFACD"
]

class Paint31CloneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniPaint")
        self.root.minsize(1000, 750)
        self.root.configure(bg="#f3f3f3")
        # --- Установка иконки приложения ---
        try:
            icon_img = tk.PhotoImage(file="assets/minipaintlogo_100.png")
            self.root.iconphoto(False, icon_img)
            self._icon_img_ref = icon_img  # Сохраняем ссылку, чтобы не удалялось GC
        except Exception as e:
            pass  # Если не удалось загрузить иконку, продолжаем без неё
        self.fg_color = DEFAULT_COLOR
        self.bg_color = DEFAULT_BG_COLOR
        self.line_width = DEFAULT_WIDTH
        self.current_tool = "pencil"  # карандаш, линия, прямоугольник, овал, ластик
        self.start_x = None
        self.start_y = None
        self.temp_shape_id = None # Для предпросмотра фигур
        self.setup_ui()
        self.canvas.bind("<Button-1>", self.on_press)        # Нажатие ЛКМ
        self.canvas.bind("<B1-Motion>", self.on_drag)       # Перемещение ЛКМ
        self.canvas.bind("<ButtonRelease-1>", self.on_release) # Отпускание ЛКМ

    def setup_ui(self):
        """Создаёт основное окно приложения."""
        # --- Верхняя панель действий ---
        action_bar = tk.Frame(self.root, bd=0, relief=tk.FLAT, bg="#e0e0e0")
        action_bar.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        save_btn = ttk.Button(action_bar, text="Сохранить", style='Modern.TButton', command=self.save_canvas)
        save_btn.pack(side=tk.LEFT, padx=8, pady=6)
        clear_btn = ttk.Button(action_bar, text="Очистить", style='Modern.TButton', command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=8, pady=6)
        about_btn = ttk.Button(action_bar, text="О программе", style='Modern.TButton', command=self.show_about)
        about_btn.pack(side=tk.RIGHT, padx=8, pady=6)
        exit_btn = ttk.Button(action_bar, text="Выход", style='Modern.TButton', command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT, padx=8, pady=6)

        # --- Основная область ---
        main_area = tk.Frame(self.root, bg="#f3f3f3")
        main_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Панель инструментов (слева) ---
        toolbox_frame = tk.Frame(main_area, bd=0, relief=tk.FLAT, width=90, bg="#eaeaea")
        toolbox_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
        toolbox_frame.pack_propagate(False)
        tools = [
            ("Карандаш", "pencil"),
            ("Линия", "line"),
            ("Прямоуг.", "rect"),
            ("Овал", "oval"),
            ("Ластик", "eraser"),
        ]
        self.tool_buttons = {}
        for name, tool_id in tools:
            btn = ttk.Button(
                toolbox_frame,
                text=name,
                style='Modern.TButton',
                command=lambda t=tool_id: self.select_tool(t)
            )
            btn.pack(pady=6, padx=8, fill=tk.X)
            self.tool_buttons[tool_id] = btn
        self.select_tool("pencil")
        # --- Толщина линии ---
        thickness_frame = tk.LabelFrame(toolbox_frame, text="Толщина", bg="#eaeaea", font=('Segoe UI', 9))
        thickness_frame.pack(pady=(30, 10), padx=6)
        # Метка создаётся до слайдера, чтобы избежать AttributeError
        self.thickness_label_val = tk.Label(thickness_frame, text=str(self.line_width), width=3, bg="#eaeaea")
        self.thickness_label_val.pack(pady=2)
        self.thickness_slider = ttk.Scale(
            thickness_frame,
            from_=1,
            to=MAX_WIDTH,
            orient=tk.HORIZONTAL,
            length=70,
            command=self.update_thickness
        )
        self.thickness_slider.set(self.line_width)
        self.thickness_slider.pack(padx=8, pady=4)
        self.update_thickness(self.line_width)

        # --- Холст (центр) ---
        self.canvas = tk.Canvas(
            main_area,
            bg=self.bg_color,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bd=0,
            highlightthickness=2,
            highlightbackground="#b0b0b0"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Нижняя панель (палитра и индикаторы) ---
        bottom_frame = tk.Frame(self.root, bd=0, relief=tk.FLAT, bg="#e0e0e0")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        indicator_frame = tk.Frame(bottom_frame, bg="#e0e0e0")
        indicator_frame.pack(side=tk.LEFT, padx=12, pady=8)
        self.bg_indicator = tk.Frame(indicator_frame, width=30, height=30, relief=tk.SOLID, bd=1, bg=self.bg_color)
        self.bg_indicator.pack(side=tk.LEFT)
        tk.Label(indicator_frame, text="  Передний:", anchor='w', bg="#e0e0e0", font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(5,0))
        self.fg_indicator = tk.Frame(indicator_frame, width=25, height=25, relief=tk.SOLID, bd=1, bg=self.fg_color)
        self.fg_indicator.pack(side=tk.LEFT, padx=(0,5))
        tk.Label(indicator_frame, text="  Фон:", anchor='w', bg="#e0e0e0", font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(5,0))
        self.bg_indicator_label = tk.Frame(indicator_frame, width=25, height=25, relief=tk.SOLID, bd=1, bg=self.bg_color)
        self.bg_indicator_label.pack(side=tk.LEFT)
        # --- Палитра цветов ---
        palette_frame = tk.Frame(bottom_frame, bg="#e0e0e0")
        palette_frame.pack(side=tk.LEFT, padx=10, pady=8)
        cols = 14
        row_num = 0
        col_num = 0
        for i, color in enumerate(COLOR_PALETTE):
            color_btn = tk.Button(
                palette_frame,
                bg=color,
                width=2,
                height=1,
                relief=tk.RAISED,
                bd=1,
                command=lambda c=color: self.set_color(c)
            )
            color_btn.bind("<Button-3>", lambda e, c=color: self.set_color(c, target='bg'))
            color_btn.bind("<Button-2>", lambda e, c=color: self.set_color(c, target='bg'))
            color_btn.grid(row=row_num, column=col_num, padx=1, pady=1)
            col_num += 1
            if col_num >= cols:
                col_num = 0
                row_num += 1
        chooser_btn = ttk.Button(bottom_frame, text="Другие цвета...", style='Modern.TButton', command=self.choose_more_color)
        chooser_btn.pack(side=tk.LEFT, padx=16, pady=8)

    # --- Методы инструментов и параметров ---
    def select_tool(self, tool):
        """Выбор текущего инструмента и обновление внешнего вида кнопок."""
        self.current_tool = tool
        for t, btn in self.tool_buttons.items():
            btn.state(['pressed'] if t == tool else ['!pressed'])

    def set_color(self, color, target='fg'):
        """Установка цвета переднего плана или фона."""
        if target == 'fg':
            self.fg_color = color
            self.fg_indicator.config(bg=color)
        elif target == 'bg':
            self.bg_color = color
            self.bg_indicator_label.config(bg=color)
            self.canvas.config(bg=self.bg_color)

    def choose_more_color(self):
        """Открыть системный выбор цвета."""
        color_code = colorchooser.askcolor(title="Выберите цвет", initialcolor=self.fg_color)
        if color_code and color_code[1]:
            self.set_color(color_code[1], target='fg')

    def update_thickness(self, value):
        """Обновить толщину линии по слайдеру."""
        self.line_width = int(float(value))
        self.thickness_label_val.config(text=str(self.line_width))

    # --- Обработчики событий холста ---
    def on_press(self, event):
        """Обработка нажатия мыши на холсте."""
        self.start_x = event.x
        self.start_y = event.y
        self.temp_shape_id = None
        if self.current_tool == "eraser":
            self._draw_eraser_mark(event.x, event.y)

    def on_drag(self, event):
        """Обработка перемещения мыши с зажатой кнопкой на холсте."""
        if self.start_x is None or self.start_y is None:
            return
        x, y = event.x, event.y
        if self.current_tool == "pencil":
            self.canvas.create_line(
                self.start_x, self.start_y, x, y,
                fill=self.fg_color,
                width=self.line_width,
                capstyle=tk.ROUND,
                smooth=tk.TRUE
            )
            self.start_x = x
            self.start_y = y
        elif self.current_tool == "eraser":
            self._draw_eraser_mark(x, y, drag=True)
            self.start_x = x
            self.start_y = y
        elif self.current_tool in ["line", "rect", "oval"]:
            if self.temp_shape_id:
                self.canvas.delete(self.temp_shape_id)
            if self.current_tool == "line":
                self.temp_shape_id = self.canvas.create_line(
                    self.start_x, self.start_y, x, y,
                    fill=self.fg_color,
                    width=self.line_width,
                    dash=(4, 4)
                )
            elif self.current_tool == "rect":
                self.temp_shape_id = self.canvas.create_rectangle(
                    self.start_x, self.start_y, x, y,
                    outline=self.fg_color,
                    width=1,
                    dash=(4, 4)
                )
            elif self.current_tool == "oval":
                self.temp_shape_id = self.canvas.create_oval(
                    self.start_x, self.start_y, x, y,
                    outline=self.fg_color,
                    width=1,
                    dash=(4, 4)
                )

    def on_release(self, event):
        """Обработка отпускания кнопки мыши на холсте."""
        if self.start_x is None or self.start_y is None:
            return
        x, y = event.x, event.y
        if self.temp_shape_id:
            self.canvas.delete(self.temp_shape_id)
            self.temp_shape_id = None
        if self.current_tool == "line":
            self.canvas.create_line(
                self.start_x, self.start_y, x, y,
                fill=self.fg_color,
                width=self.line_width,
                capstyle=tk.ROUND
            )
        elif self.current_tool == "rect":
            self.canvas.create_rectangle(
                self.start_x, self.start_y, x, y,
                outline=self.fg_color,
                width=self.line_width
            )
        elif self.current_tool == "oval":
            self.canvas.create_oval(
                self.start_x, self.start_y, x, y,
                outline=self.fg_color,
                width=self.line_width
            )
        self.start_x = None
        self.start_y = None

    def _draw_eraser_mark(self, x, y, drag=False):
        """Вспомогательный метод для рисования ластиком."""
        eraser_size = max(2, self.line_width)
        if drag and self.start_x is not None:
            self.canvas.create_line(
                self.start_x, self.start_y, x, y,
                fill=self.bg_color,
                width=eraser_size,
                capstyle=tk.ROUND
            )
        else:
            self.canvas.create_rectangle(
                x - eraser_size // 2, y - eraser_size // 2,
                x + eraser_size // 2, y + eraser_size // 2,
                fill=self.bg_color,
                outline=self.bg_color
            )

    # --- Действия ---
    def clear_canvas(self):
        """Очистить весь холст."""
        if messagebox.askyesno("Очистить холст", "Вы уверены, что хотите очистить холст?"):
            self.canvas.delete("all")

    def save_canvas(self):
        """Сохранить только содержимое холста в PNG/JPG файл (без панелей, без postscript/ghostscript)."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG файлы", "*.png"), ("JPEG файлы", "*.jpg"), ("Все файлы", "*.*")],
                title="Сохранить рисунок как..."
            )
            if not file_path:
                return
            # Получаем координаты холста относительно экрана
            self.root.update_idletasks()
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            # Захватываем только область холста
            img = ImageGrab.grab(bbox=(x, y, x1, y1)).convert("RGB")
            file_ext = os.path.splitext(file_path)[1].lower()
            img_format = 'png'
            if file_ext == '.jpg' or file_ext == '.jpeg':
                img_format = 'jpeg'
            elif file_ext == '.gif':
                img_format = 'gif'
            img.save(file_path, format=img_format)
            messagebox.showinfo("Сохранено", f"Рисунок сохранён в:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить рисунок.\nОшибка: {e}")

    def show_about(self):
        """Показать окно 'О программе' в стиле winver."""
        about = tk.Toplevel(self.root)
        about.title("О программе")
        about.geometry("500x400")
        about.resizable(False, False)
        about.configure(bg="#f3f3f3")
        logo_img = tk.PhotoImage(file="assets/minipaintlogo_100.png")
        logo = tk.Label(about, image=logo_img, bg="#f3f3f3", height=100, width=100)
        logo.image = logo_img  # Keep a reference to avoid garbage collection
        logo.pack(pady=(18, 0))
        title = tk.Label(about, text="MiniPaint", font=("Segoe UI", 18, "bold"), bg="#f3f3f3")
        title.pack(pady=(8, 0))
        ver = tk.Label(about, text="Версия 1.0 (2025)", font=("Segoe UI", 11), bg="#f3f3f3")
        ver.pack(pady=(2, 0))
        sep = ttk.Separator(about, orient='horizontal')
        sep.pack(fill=tk.X, padx=30, pady=12)
        info = tk.Label(about, text="Простой графический редактор\nв стиле Microsoft Paint образца 1995 года\n\nАвтор: Свистунов Александр, ИБС235\nг. Москва, 2025", font=("Segoe UI", 10), bg="#f3f3f3", justify=tk.CENTER)
        info.pack(pady=(0, 10))
        ok_btn = ttk.Button(about, text="Закрыть", command=about.destroy)
        ok_btn.pack(pady=6)
        about.transient(self.root)
        about.grab_set()
        self.root.wait_window(about)

# --- Точка входа ---
if __name__ == "__main__":
    try:
        from PIL import Image, ImageGrab
    except ImportError:
        print("Ошибка: библиотека Pillow не найдена.")
        print("Установите её командой: pip install pillow")
        exit()
    root = tk.Tk()
    app = Paint31CloneApp(root)
    root.mainloop()