from typing import Tuple
from typing import Optional

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib import pyplot as plot
from matplotlib import patches as patches
from matplotlib import figure as fig
from matplotlib import axes as ax
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Memory:
	"""
	This class simulates a memory architecture consisting of multiple chips, and visualizes its layout using Matplotlib.
	The memory system is defined by its capacity, word size, and chip configuration. The drawing functions provide
	a visual representation of the memory organization, with components like chips, addressing units, R/W lines, and decoders.

	Attributes:
		CHIP_WIDTH (float): The width of a single memory chip.
		CHIP_SPACING (float): The spacing between memory chips.
		CHIP_HEIGHT (float): The height of a single memory chip.
		CHIP_DECODER_WIDTH (float): The width of the decoder for the chips.
		MAR_WIDTH (float): The width of the Memory Address Register (MAR).
		RW_X_POS (float): The X position of the R/W lines.
		RW_Y_POS (float): The Y position of the R/W lines.
		RW_CONNECT_OFFSET (float): The offset for connecting the R/W lines to chips.
		DECODER_POS (float): The position of the decoder.
		DECODER_HEIGHT (float): The height of the decoder.
		DECODER_CONNECT_OFFSET (float): The offset for connecting the decoder.
		DATABUS_OFFSET (float): The offset for the data bus.

	Methods:
		__init__(self, memory_capacity: int, memory_wordsize: int, chip_capacity: int, chip_wordsize: int):
			Initializes the memory system with the given parameters and sets up the memory dimensions.
		
		setmemory(self) -> None:
			Sets up the memory configuration, calculating the number of rows and columns of chips, 
			and configuring the plot for visualization.
		
		calculate_dimensions(self) -> Tuple[int, int]:
			Calculates the number of chips in each row and column based on memory and chip capacities.
		
		draw_chips(self) -> None:
			Draws the individual memory chips in the visualization.
		
		draw_addressing_unit(self) -> None:
			Draws the addressing unit (MAR) for each chip in the visualization.
		
		draw_RW(self) -> None:
			Draws the Read/Write lines for the memory system.
		
		draw_decoder(self) -> None:
			Draws the decoder, responsible for addressing and selecting the appropriate chips.
		
		draw_address_lines(self) -> None:
			Draws the address lines connecting the decoder to the chips.
		
		draw_data_lines(self) -> None:
			Draws the data lines that connect the memory chips.
	"""
	CHIP_WIDTH = 1
	CHIP_SPACING = CHIP_WIDTH * 2 + 1
	CHIP_HEIGHT = 1.5
	CHIP_DECODER_WIDTH = 0.15
	MAR_WIDTH = 0.2
	RW_X_POS = -3
	RW_Y_POS = CHIP_HEIGHT + (CHIP_HEIGHT / 6)
	RW_CONNECT_OFFSET = 0.25
	DECODER_POS = -5
	DECODER_HEIGHT = 2
	DECODER_CONNECT_OFFSET = 0.6
	DATABUS_OFFSET = 0.25
	def __init__(
		self, 
		memory_capacity: int, 
		memory_wordsize: int,
		chip_capacity: int,
		chip_wordsize: int,
	):
		"""
		Initializes the memory system with the given parameters.

		Args:
			memory_capacity (int): The total capacity of the memory system (in bytes).
			memory_wordsize (int): The word size of the memory (in bytes).
			chip_capacity (int): The capacity of a single chip (in bytes).
			chip_wordsize (int): The word size of a single chip (in bytes).
		"""
		self.memory_capacity: int = memory_capacity
		self.memory_wordsize: int = memory_wordsize
		self.chip_capacity: int = chip_capacity
		self.chip_wordsize: int = chip_wordsize
		self.rows: Optional[int] = None
		self.columns: Optional[int] = None
		self.figure: Optional[fig.Figure] = None
		self.axis: Optional[ax.Axes] = None
		self.setmemory()


	def setmemory(self) -> None:
		"""
		Calculates the number of rows and columns needed for memory chips and sets up the plot.
		"""
		P, Q = self.calculate_dimensions
		self.rows = P
		self.columns = Q
		self.figure, self.axis = plot.subplots(constrained_layout = True, figsize = (15, 15))
		for spine in self.axis.spines.values():
			spine.set_visible(False)
		self.axis.set_xticks([])
		self.axis.set_yticks([])
		self.axis.set_aspect('equal')
	

	@property
	def calculate_dimensions(self) -> Tuple[int, int]:
		"""
		Calculates the number of chips in each row and column based on memory and chip parameters.

		Returns:
			Tuple[int, int]: A tuple containing the number of rows and columns.
		
		Raises:
			ValueError: If any of the parameters (memory_capacity, memory_wordsize, chip_capacity, chip_wordsize) is zero or less.
		"""
		if (self.memory_capacity == 0 or self.memory_wordsize == 0 or self.chip_capacity == 0 or self.chip_wordsize == 0):
			raise ValueError("All values must be greater than zero")
		P = self.memory_capacity // self.chip_capacity
		Q = self.memory_wordsize // self.chip_wordsize
		if P <= 0 or Q <= 0:
			raise ValueError("Memory must be greater than or equal to chip")
		return (P, Q)


	def draw_chips(self) -> None:
		"""
		Draws the individual memory chips in the plot. Each chip is represented as a rectangle with a label "CS".
		"""
		CS_offset = (9, -5)
		for col in range(self.columns):
			for row in range(self.rows):
				rectangle = patches.Rectangle((col * self.CHIP_SPACING, row * self.CHIP_SPACING), self.CHIP_WIDTH, self.CHIP_HEIGHT, edgecolor = 'black', facecolor = '#47c295', linewidth = 2)
				self.axis.add_patch(rectangle)
				self.axis.annotate("CS", (col * self.CHIP_SPACING + 1, row * self.CHIP_SPACING + 1.5), textcoords = 'offset points', xytext = CS_offset)
				

	def draw_addressing_unit(self) -> None:
		"""
		Draws the addressing unit (MAR) for each chip. This includes the Memory Address Register and its connection lines.
		"""
		for row in range(self.rows):
			for col in range(self.columns):
				x_start = col * self.CHIP_SPACING - self.CHIP_DECODER_WIDTH
				x_end = col * self.CHIP_SPACING
				chip_bottom = row * self.CHIP_SPACING
				chip_top = row * self.CHIP_SPACING + self.CHIP_HEIGHT
				y_bottom = chip_bottom + self.CHIP_DECODER_WIDTH
				y_top = chip_top - self.CHIP_DECODER_WIDTH
				self.axis.plot([x_start, x_end], [y_bottom, chip_bottom], color = 'black', linewidth = 2)
				self.axis.plot([x_start, x_end], [y_top, chip_top], color = 'black', linewidth = 2)
				self.axis.plot([x_start, x_start], [y_bottom, y_top], color = 'black', linewidth = 2)
				MAR = patches.Rectangle((x_start, y_bottom), -self.MAR_WIDTH, y_top - y_bottom, edgecolor = 'black', facecolor = 'brown', linewidth = 2)
				self.axis.add_patch(MAR)


	def draw_RW(self) -> None:
		"""
		Draws the Read/Write lines connecting the chips to the R/W unit.
		"""
		x_pos = [self.RW_X_POS, self.RW_X_POS]
		y_pos = [self.RW_Y_POS, self.rows * self.CHIP_SPACING if self.rows != 1 else self.RW_Y_POS]
		text_offset = (6, -15)
		self.axis.plot(x_pos, y_pos, color = 'red')
		self.axis.annotate("R/W", (x_pos[1], y_pos[1]), textcoords = 'offset points', xytext = text_offset, weight = 'extra bold', fontsize = 10)
		for col in range(self.columns):
			for row in range(self.rows):
				self.axis.plot([self.RW_X_POS, col * self.CHIP_SPACING + self.RW_CONNECT_OFFSET], [row * self.CHIP_SPACING + self.RW_Y_POS, row * self.CHIP_SPACING + self.RW_Y_POS], color = 'red')
				self.axis.plot([col * self.CHIP_SPACING + self.RW_CONNECT_OFFSET, col * self.CHIP_SPACING + self.RW_CONNECT_OFFSET], [row * self.CHIP_SPACING + self.RW_Y_POS, row * self.CHIP_SPACING + self.CHIP_HEIGHT], color = 'red')


	def draw_decoder(self) -> None:
		"""
		Draws the decoder, which is responsible for chip addressing and selection.
		"""
		x_end = self.DECODER_POS - 0.3
		decoder_bottom = ((self.rows * self.CHIP_SPACING) / 2) - self.DECODER_HEIGHT
		decoder_top = self.rows * self.CHIP_SPACING / 2
		decoder_bottom_l = decoder_bottom + 0.25
		decoder_top_l = decoder_top - 0.25
		if self.rows > 1:
			self.axis.plot([self.DECODER_POS, self.DECODER_POS], [decoder_bottom, decoder_top], color = 'black')
			self.axis.plot([x_end, x_end], [decoder_bottom_l, decoder_top_l], color = 'black')
			self.axis.plot([x_end, self.DECODER_POS], [decoder_bottom_l, decoder_bottom], color = 'black')
			self.axis.plot([x_end, self.DECODER_POS], [decoder_top_l, decoder_top], color = 'black')
			self.axis.plot([x_end - 0.5, x_end], [decoder_bottom_l + (decoder_top_l - decoder_bottom_l) / 2, decoder_bottom_l + (decoder_top_l - decoder_bottom_l) / 2], color = 'black', lw = 1.75)
		lines_space = (decoder_top - decoder_bottom) / (self.rows + 1)
		n = 0
		m = self.rows
		chip_y_pos = [i * self.CHIP_SPACING + self.CHIP_HEIGHT + 0.5 for i in range(self.rows)]
		while n < m:
			decoder_bottom += lines_space
			decoder_top -= lines_space
			n += 1
			m -= 1
			line_length = self.DECODER_POS + 0.2 * n
			if self.rows > 1:
				self.axis.plot(self.DECODER_POS, decoder_bottom, 'ko', ms = 7.5) 
				self.axis.plot(self.DECODER_POS, decoder_top, 'ko', ms = 7.5) 
				self.axis.plot([self.DECODER_POS, line_length], [decoder_bottom, decoder_bottom], color = 'black', lw = 1.75)
				self.axis.plot([self.DECODER_POS, line_length], [decoder_top, decoder_top], color = 'black', lw = 1.75)
				self.axis.plot([line_length, line_length], [decoder_bottom, chip_y_pos[n - 1]], color = 'black', lw = 1.75)
				self.axis.plot([line_length, line_length], [decoder_top, chip_y_pos[m]], color = 'black', lw = 1.75)
			self.axis.plot([line_length, (self.columns - 1) * self.CHIP_SPACING + self.DECODER_CONNECT_OFFSET], [chip_y_pos[n - 1], chip_y_pos[n - 1]], color = 'black', lw = 1.75)
			self.axis.plot([line_length, (self.columns - 1) * self.CHIP_SPACING + self.DECODER_CONNECT_OFFSET], [chip_y_pos[m], chip_y_pos[m]], color = 'black', lw = 1.75)
			for col in range(self.columns):
				self.axis.plot([col * self.CHIP_SPACING + self.DECODER_CONNECT_OFFSET, col * self.CHIP_SPACING + self.DECODER_CONNECT_OFFSET], [chip_y_pos[n - 1], chip_y_pos[n - 1] - 0.5], color = 'black', lw = 1.75)
				self.axis.plot([col * self.CHIP_SPACING + self.DECODER_CONNECT_OFFSET, col * self.CHIP_SPACING + self.DECODER_CONNECT_OFFSET], [chip_y_pos[m], chip_y_pos[m] - 0.5], color = 'black', lw = 1.75)
				self.axis.plot(col * self.CHIP_SPACING + self.DECODER_CONNECT_OFFSET, chip_y_pos[n - 1] - 0.5, 'ko', ms = 7.5) 
				self.axis.plot(col * self.CHIP_SPACING + self.DECODER_CONNECT_OFFSET, chip_y_pos[m] - 0.5, 'ko', ms = 7.5) 


	def draw_address_lines(self) -> None:
		"""
		Draws the address lines that connect the decoder to each memory chip.
		"""
		self.axis.plot([self.DECODER_POS - 0.3, -self.CHIP_DECODER_WIDTH - self.MAR_WIDTH], [self.CHIP_HEIGHT / 2, self.CHIP_HEIGHT / 2], color = 'black', lw = 1.75)
		self.axis.plot([self.DECODER_POS / 2, self.DECODER_POS / 2], [self.CHIP_HEIGHT / 2, ((self.rows - 1) * self.CHIP_SPACING + self.CHIP_HEIGHT / 2) if self.rows != 1 else self.CHIP_HEIGHT / 2], color = 'black', lw = 1.75)
		for row in range(self.rows):
			self.axis.plot([self.DECODER_POS / 2, -self.CHIP_DECODER_WIDTH - self.MAR_WIDTH], [row * self.CHIP_SPACING + self.CHIP_HEIGHT / 2, row * self.CHIP_SPACING + self.CHIP_HEIGHT / 2], color = 'black')
			if self.columns > 1:
				self.axis.plot([(self.DECODER_POS / 2 + (-self.CHIP_DECODER_WIDTH - self.MAR_WIDTH)) / 2, (self.columns - 1) * self.CHIP_SPACING + (self.DECODER_POS / 2 + (-self.CHIP_DECODER_WIDTH - self.MAR_WIDTH)) / 2], [row * self.CHIP_SPACING + self.CHIP_HEIGHT / 2 - (self.CHIP_HEIGHT / 2 + 0.5), row * self.CHIP_SPACING + self.CHIP_HEIGHT / 2 - (self.CHIP_HEIGHT / 2 + 0.5)], color = 'black')
				for col in range(self.columns):
					self.axis.plot([col * self.CHIP_SPACING + (self.DECODER_POS / 2 + (-self.CHIP_DECODER_WIDTH - self.MAR_WIDTH)) / 2, col * self.CHIP_SPACING + (self.DECODER_POS / 2 + (-self.CHIP_DECODER_WIDTH - self.MAR_WIDTH)) / 2], [row * self.CHIP_SPACING + self.CHIP_HEIGHT / 2, row * self.CHIP_SPACING + self.CHIP_HEIGHT / 2 - (self.CHIP_HEIGHT / 2 + 0.5)], color = 'black')
					self.axis.plot([col * self.CHIP_SPACING + (self.DECODER_POS / 2 + (-self.CHIP_DECODER_WIDTH - self.MAR_WIDTH)) / 2, col * self.CHIP_SPACING -self.CHIP_DECODER_WIDTH -self.MAR_WIDTH], [row * self.CHIP_SPACING + self.CHIP_HEIGHT / 2, row * self.CHIP_SPACING + self.CHIP_HEIGHT / 2], color = 'black')
					

	def draw_data_lines(self) -> None:
		"""
		Draws the data lines connecting the chips to the data bus.
		"""
		self.axis.arrow(self.columns * self.CHIP_SPACING, -1, dx = 0, dy = self.rows * self.CHIP_SPACING, head_width = 0.1, head_length = 0.1, color = 'black')
		self.axis.arrow(self.columns * self.CHIP_SPACING, self.rows * self.CHIP_SPACING - 1, dx=0, dy= - self.rows * self.CHIP_SPACING, head_width=0.1, head_length=0.1, color='black')
		for row in range(self.rows):
			self.axis.plot([0, self.columns * self.CHIP_SPACING], [row * self.CHIP_SPACING - (self.CHIP_SPACING / 10), row * self.CHIP_SPACING - (self.CHIP_SPACING / 10)], color = 'black', lw = 1.5)
			for col in range(self.columns):
				self.axis.arrow(col * self.CHIP_SPACING + self.DATABUS_OFFSET, row * self.CHIP_SPACING - (self.CHIP_SPACING / 10), dx = 0, dy = self.CHIP_SPACING / 15, head_width = 0.1, head_length = 0.1, color = 'black', lw = 1.5)
				self.axis.arrow(col * self.CHIP_SPACING + self.DATABUS_OFFSET, row * self.CHIP_SPACING, dx = 0, dy = self.CHIP_SPACING / 15 * -1, head_width = 0.1, head_length = 0.1, color='black', lw = 1.5)


class MemoryApp:
	"""
    MemoryApp is a Tkinter-based application that visualizes the layout of memory and chips
    based on user input. The user provides memory and chip parameters, and the app generates
    a visual representation of the memory structure.

    Methods:
    ----------
    __init__(self, window): Initializes the MemoryApp with a Tkinter window.
    create_menu(self): Creates the menu bar with options to start a new layout or exit the application.
    create_input_frame(self): Creates the input frame where the user enters memory and chip details.
    generate_layout(self): Processes the user input to generate the memory layout and visualize it.
    show_layout(self, figure): Displays the generated memory layout figure in the window.
    show_input_frame(self): Resets the window to show the input frame again.
    """

	def __init__(self, window):
		"""
        Initializes the MemoryApp instance, setting up the window size and title, 
        creating the menu, and displaying the input frame.
        
        Parameters:
        -----------
        window : tkinter.Tk
            The Tkinter window object representing the application window.
        """
		self.window = window
		self.window.title("Memory Layout Visualizer")
		self.window.protocol("WM_DELETE_WINDOW", self.window.quit)
		screen_width = window.winfo_screenwidth()
		screen_height = window.winfo_screenheight()
		self.window.geometry(f"{screen_width}x{screen_height}")
		self.create_menu()
		self.canvas = None
		self.create_input_frame()


	def create_menu(self):
		"""
        Creates the menu bar with options for generating a new layout or exiting the application.
        """
		menu_bar = tk.Menu(self.window)
		menu_bar.add_command(label = "New", command = self.show_input_frame)
		menu_bar.add_command(label = "Exit", command = self.window.quit)
		self.window.config(menu = menu_bar)


	def create_input_frame(self):
		"""
        Creates the frame where the user can input memory and chip parameters for generating the layout.
        Displays input fields for memory capacity, memory word size, chip capacity, and chip word size.
        Also includes a button to generate the layout.
        """
		self.input_frame = tk.Frame(self.window)
		self.input_frame.place(relx = 0.5, rely = 0.5, anchor = "center")
		tk.Label(self.input_frame, text = "Memory Capacity:").grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "e")
		tk.Label(self.input_frame, text = "Memory Word Size:").grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "e")
		tk.Label(self.input_frame, text = "Chip Capacity:").grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "e")
		tk.Label(self.input_frame, text = "Chip Word Size:").grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "e")

		self.memory_capacity_entry = ttk.Entry(self.input_frame)
		self.memory_wordsize_entry = ttk.Entry(self.input_frame)
		self.chip_capacity_entry = ttk.Entry(self.input_frame)
		self.chip_wordsize_entry = ttk.Entry(self.input_frame)

		self.memory_capacity_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
		self.memory_wordsize_entry.grid(row = 1, column = 1, padx = 10, pady = 10)
		self.chip_capacity_entry.grid(row = 2, column = 1, padx = 10, pady = 10)
		self.chip_wordsize_entry.grid(row = 3, column = 1, padx = 10, pady = 10)

		generate_button = ttk.Button(self.input_frame, text = "Generate Layout", command = self.generate_layout)
		generate_button.grid(row = 4, column = 0, columnspan = 2, pady = 20)


	def generate_layout(self):
		"""
        Generates the memory layout based on the user inputs, and displays the generated layout in the window.
        The method creates a Memory object using the input parameters and calls methods to draw various
        components of the memory layout. If any error occurs (e.g., invalid input), an error message is shown.
        """
		try:
			memory_capacity = int(self.memory_capacity_entry.get())
			memory_wordsize = int(self.memory_wordsize_entry.get())
			chip_capacity = int(self.chip_capacity_entry.get())
			chip_wordsize = int(self.chip_wordsize_entry.get())
			memory = Memory(
				memory_capacity=memory_capacity,
				memory_wordsize=memory_wordsize,
				chip_capacity=chip_capacity,
				chip_wordsize=chip_wordsize
			)
			memory.draw_chips()
			memory.draw_addressing_unit()
			memory.draw_RW()
			memory.draw_decoder()
			memory.draw_address_lines()
			memory.draw_data_lines()
			self.input_frame.destroy()
			self.show_layout(memory.figure)
		except ValueError as e:
			messagebox.showerror("Input Error", str(e))
		except Exception as e:
			messagebox.showerror("Error", f"An error occurred: {e}")


	def show_layout(self, figure):
		"""
        Displays the generated memory layout figure in the application window.
        
        Parameters:
        -----------
        figure : matplotlib.figure.Figure
            The figure object containing the visualized memory layout.
        """
		if self.canvas:
			self.canvas.get_tk_widget().destroy()
		layout_frame = tk.Frame(self.window)
		layout_frame.grid(row = 0, column = 0, sticky = "nsew")
		figure.set_size_inches(self.window.winfo_width() / 50, self.window.winfo_height() / 50)
		self.canvas = FigureCanvasTkAgg(figure, master = layout_frame)
		self.canvas.get_tk_widget().pack(fill = "both", expand = True)
		self.canvas.draw()
		self.window.columnconfigure(0, weight = 1)
		self.window.rowconfigure(0, weight = 1)


	def show_input_frame(self):
		"""
        Resets the window to show the input frame for entering memory and chip parameters again.
        """
		for widget in self.window.winfo_children():
			widget.destroy()
		self.create_menu()
		self.create_input_frame()


if __name__ == "__main__":
	window = tk.Tk()
	app = MemoryApp(window)
	window.mainloop()