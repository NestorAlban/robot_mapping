import pygame
import math
from queue import PriorityQueue
from image_mapping import ImageMapping

WIDTH = 720
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

image_mapping = ImageMapping()

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
		
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])
			
	def __lt__(self, other):
		return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def main(win, width):
	image_to_mapp_data = image_mapping.main_image_to_map()
	color_image_with_rob = image_to_mapp_data[0]
	rows = color_image_with_rob.shape[0]
	cols = color_image_with_rob.shape[1]
	interest_zone = image_to_mapp_data[1]
	rectangle_sizes = image_to_mapp_data[2]
	l_size = rectangle_sizes[5]
	l_size_mid = int(l_size/2)
	print(l_size_mid)

	print(WIDTH/l_size)
	dimensions = image_to_mapp_data[3]
	surface = pygame.Surface(dimensions)
	for row in range(rows):
		for col in range(cols):
			pixelBGR = color_image_with_rob[row, col]
			color = [pixelBGR[2],pixelBGR[1],pixelBGR[0]]
			rectangulo = pygame.Rect(col, row, 1, 1)
			pygame.draw.rect(surface, color, rectangulo)

	grid = make_grid(rows, width)
	start = None
	end = None
	pygame.init()

	screen = pygame.display.set_mode(dimensions)
	pygame.display.set_caption('Grid de colores')
	run = True
	screen.blit(surface, (0, 0))
	pygame.display.flip()

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			grid = make_grid(rows, width)
			for x in range(0,WIDTH, 5):
				pygame.draw.line(screen, RED, (1,x), (WIDTH, x), 2)
				pygame.draw.line(screen, RED, (x,1), (x,WIDTH), 2)
				pygame.display.update()
	



main(WIN, WIDTH)