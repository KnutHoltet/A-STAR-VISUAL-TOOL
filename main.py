import pygame
import math
from queue import PriorityQueue


#Setter opp displayet for pygame, bredde er width witdh
WIDTH = 800
WIN =  pygame.display.set_mode((WIDTH, WIDTH))
#Overskrift program
pygame.display.set_caption("A* algoritme")

#Farger
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 244, 208)

#lager gride
class Spot:
  def __init__(self, rad, kol, width, totale_rader):
    self._rad = rad
    self._kol = kol
    self.x = rad * width
    self.y = kol * width
    self.farge = WHITE
    self.naboer = []
    self.width = width
    self._totale_rader = totale_rader

  def hent_posisjon(self):
    return self._rad, self._kol

  #Har vi sett paa denne posisjonen  
  #Oppdaterer fargen hvis algoritmen har gaatt igjennom denne ruten
  def is_closed(self):
    return self.farge == RED

  def is_open(self):
    return self.farge == GREEN

  def is_barrier(self):
    return self.farge == BLACK
  
  def is_start(self):
    return self.farge == ORANGE
  
  def is_end(self):
    return self.farge == TURQUOISE 

  def reset(self):
    self.farge = WHITE

  def make_closed(self):
    self.farge = RED
  
  def make_start(self):
    self.farge = ORANGE

  def make_open(self):
    self.farge = GREEN
  
  def make_barrier(self):
    self.farge = BLACK
  
  def make_end(self):
    self.farge = TURQUOISE

  def make_path(self):
    self.farge = PURPLE

  def tegn(self, win):
    #Denne tegner bare en kube i fargen den er under den oppdateringen
    pygame.draw.rect(win, self.farge, (self.x, self.y, self.width, self.width))
  
  def update_naboer(self, grid):
    #legge til alle de gyldige naboene til
    self.naboer = []
    #foest sjekke om jeg kan gaa ned, ved and, 
    #append den neste raden ned
    if self._rad < self._totale_rader - 1 and not grid[self._rad + 1][self._kol].is_barrier(): #Ned
      self.naboer.append(grid[self._rad + 1][self._kol])

    if self._rad > 0 and not grid[self._rad - 1][self._kol].is_barrier(): #Opp
      self.naboer.append(grid[self._rad - 1][self._kol])

    if self._kol < self._totale_rader - 1 and not grid[self._rad][self._kol - 1].is_barrier(): #Hoeyre
      self.naboer.append(grid[self._rad][self._kol + 1])

    if self._kol > 0 and not grid[self._rad][self._kol - 1 ].is_barrier(): #Venstre
      self.naboer.append(grid[self._rad - 1][self._kol - 1])

  def __lt__(self, other):
    return False
  

#node a og node b, eller punkt 1 og punkt 2
def h(p1, p2):
  #Her tar vi mer eller mindre, delta x, delta y, derfor lager vi to punkter
  x1, y1 = p1
  x2, y2 = p2
  return abs( x1 - x2) + abs(y1 - y2)

def algorithm(draw, grid, start, end):
  count = 0 #fscore
  open_set = PriorityQueue
  open_set.put((0, count, start))
  came_from = {}
  g_score = {spot: float("inf") for rad in grid for spot in rad} #noekkel for hver sp
  g_score[start] = 0
  f_score = {spot: float("inf") for rad in grid for spot in rad} #noekkel for hver sp
  f_score[start] = 0

#liste som holder alle punktene i griden min
#Lager gridden
def make_grid(rader, width):
  grid = []
  gap = width // rader
  for rad in range(rader):
    #Her legger vi til en rad
    grid.append([])
    for kol in range(rader):
      spot = Spot(rad, kol, gap, rader)
      #Ogsaa legger vi til den pikselen
      grid[rad].append(spot)

  # print(grid[0])
  return grid 

#saa maa vi tegne griden
#win er hvilket vindu altsaa pygame vindu
def draw_grid(win, rade, width):
  gap = width // rade
  # print(type(width), type(rade), end="\n")
  for i in range(rade):
    #for hver rad, skal vi tegne en horisontal linje
    pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) 
    #ogsaa bare tegner vi de samme linjene men vertikalt
    for j in range(rade):
      pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rade, width):
  win.fill(WHITE)

  # spot er pikselen
  for rad in grid:
    for spot in rad:
      spot.tegn(win)
  
  draw_grid(win, rade, width)
  pygame.display.update()

def get_clicked_pos(pos, rad, width):
  gap = width // rad
  #pos = posisjon
  y, x = pos

  #tar pos, x og y, og deler paa bredden paa kuben
  rad = y // gap
  kol = x // gap

  return rad, kol

def main(win, width):
  RAD = 50 
  grid = make_grid(RAD, width)

  start = None
  end = None

  run = True
  started = False
  while run:
    draw(win, grid, RAD, WIDTH)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if started:
        continue
  
      # if pygame.mouse.get_pressed()[0]: #venstre klikk
      if pygame.mouse.get_pressed()[0]: #venstre klikk
        # print("hei")
        pos = pygame.mouse.get_pos()
        rad, kol = get_clicked_pos(pos, RAD, width)
        spot = grid[rad][kol]
        if not start and spot != end:
          start = spot
          start.make_start()

        elif not end and spot != start:
          end = spot
          end.make_end()
        
        elif spot != end and spot != start:
          spot.make_barrier()

      elif pygame.mouse.get_pressed()[2]: #hoeyre klikk
        pos = pygame.mouse.get_pos()
        rad, kol = get_clicked_pos(pos, RAD, width)
        spot = grid[rad][kol]
        spot.reset()
        if spot == start:
          start = None
        
        if spot == end:
          end = None

      if event.type == pygame.KEYDOWN: #spacebar
        if event.key == pygame.K_SPACE and not started:
          for rad in grid:
            for spot in rad:
              spot.update_naboer()
            
          algorithm(lambda: draw(win, grid, RAD, width), grid, start, end)
  
  pygame.quit()

main(WIN, WIDTH)

