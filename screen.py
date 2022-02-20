from tkinter import *
from tkinter import ttk
from random import randrange
from typing import List
import logging
from logging import config
from bubblesort import bubble_sort
from quicksort import quicksort
from mergesort import merge_sort
# TODO UI


class Screen:
    WINDOW_HEIGHT = 900
    WINDOW_WIDTH = 600
    BLUE = "#A2CDCD"
    RED = "#D57E7E"
    GREEN = "#C6D57E"
    YELLOW = "#FFE1AF"
    BACKGROUND_COLOR = BLUE
    HEADER_HEIGHT = 200
    HEADER_WIDTH = WINDOW_WIDTH
    CANVAS_HEIGHT = 380
    CANVAS_WIDTH = WINDOW_WIDTH
    SPACING = 5
    ALGORITHMS = ["Bubble Sort", "Merge Sort", "Quicksort"]

    def __init__(self) -> None:
        logging.config.fileConfig("logging.conf")  # Use logger config
        self.logger = logging.getLogger(__name__)  # Create logger

        self.logger.debug("Setting up screen...")
        self.data = []
        self.window = Tk()
        self.window.title("Sorting Algorithms Visualization")
        self.window.maxsize(self.WINDOW_HEIGHT, self.WINDOW_WIDTH)
        self.window.config(bg=self.BACKGROUND_COLOR)
        self.algorithm = StringVar()

        self.frame = Frame(self.window, width=600, height=200, bg=self.BACKGROUND_COLOR)
        self.frame.grid(row=0, column=0, padx=10, pady=5)

        self.canvas = Canvas(self.window, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg="#FFE1AF")
        self.canvas.grid(row=1, column=0, padx=10, pady=5)

        alg_label = Label(self.frame, text="Algorithm: ", bg=self.BACKGROUND_COLOR)
        alg_label.grid(row=0, column=0, padx=5, pady=5)

        self.alg_menu = ttk.Combobox(self.frame, textvariable=self.algorithm, values=self.ALGORITHMS)
        self.alg_menu.grid(row=0, column=1, padx=5, pady=5)
        self.alg_menu.current(0)

        self.speed_scale = Scale(self.frame, from_=0.1, to=2.0, length=200, digits=2, resolution=0.1, orient=HORIZONTAL,
                                 label="Speed selection")
        self.speed_scale.grid(row=0, column=2, padx=5, pady=5)
        self.start_but = Button(self.frame, text="Start", command=self.start_algorithm, bg=self.RED)
        self.start_but.grid(row=0, column=3, padx=5, pady=5)

        self.size_scale = Scale(self.frame, from_=3, to=30, resolution=1, orient=HORIZONTAL, label="Data Size")
        self.size_scale.grid(row=1, column=0, padx=5, pady=5)

        self.min_scale = Scale(self.frame, from_=0, to=10, resolution=1, orient=HORIZONTAL, label="Min Value")
        self.min_scale.grid(row=1, column=1, padx=5, pady=5)

        self.max_scale = Scale(self.frame, from_=10, to=100, resolution=1, orient=HORIZONTAL, label="Max Value")
        self.max_scale.grid(row=1, column=2, padx=5, pady=5)

        self.generate_but = Button(self.frame, text="Generate", command=self.generate_arr, bg='white')
        self.generate_but.grid(row=1, column=3, padx=5, pady=5)

        self.logger.info("Screen set. Maintaining...")
        self.window.mainloop()

        self.logger.info("Program closed.")

    def generate_arr(self) -> None:
        """Generate random array with set limits"""
        self.logger.debug("Generating random array...")
        min_val = int(self.min_scale.get())
        max_val = int(self.max_scale.get())
        size = int(self.size_scale.get())
        self.data = [randrange(min_val, max_val) for _ in range(size)]      # generate random array

        self.logger.debug("Random array generated.")
        self.data_visualize([self.BLUE for _ in self.data])

    def data_visualize(self, colors: List, data: None | List = None) -> None:
        """Redraw columns"""
        self.logger.debug("Redrawing columns...")
        if data is not None:
            self.data = data
        self.canvas.delete("all")
        x_width = self.CANVAS_WIDTH / (len(self.data) + 0)
        current_max = max(self.data)
        normalized_data = [i / current_max for i in self.data]
        for index, (value, height, color) in enumerate(zip(self.data, normalized_data, colors)):
            x0 = index * x_width + self.SPACING     # columns x positions
            x1 = (index + 1) * x_width

            y0 = self.CANVAS_HEIGHT - height * (self.CANVAS_HEIGHT - 40)        # columns y positions
            y1 = self.CANVAS_HEIGHT

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)        # create column
            text_pos = x0 + ((x1 - x0) // 2)
            self.canvas.create_text(text_pos, y0 - 7, anchor=CENTER, text=value)
        self.logger.debug("Columns redrawn.")

        self.window.update_idletasks()      # update drawing

    def start_algorithm(self) -> None:
        """Starting algorithm"""
        if self.alg_menu.get() == "Bubble Sort":
            self.logger.debug("Start bubble sort...")
            bubble_sort(self.data, self.data_visualize, self.speed_scale.get())
            self.data_visualize(["#C6D57E" for _ in range(len(self.data))], self.data)
            self.logger.debug("Bubble sort complete.")
        elif self.alg_menu.get() == "Quicksort":
            self.logger.debug("Start quicksort...")
            quicksort(self.data, 0, len(self.data) - 1, self.data_visualize, self.speed_scale.get())
            self.data_visualize(["#C6D57E" for _ in range(len(self.data))], self.data)
            self.logger.debug("Quicksort complete.")
