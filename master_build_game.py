# Poke the Dots - Pygame Variation

import pygame, sys, string
from math import sqrt
from pygame import QUIT, MOUSEBUTTONDOWN, Color
from pygame.time import Clock, get_ticks, delay
from pygame.event import get as get_events
from pygame.draw import circle as draw_circle
from random import randint

# State

ctx = {
  "game_bg_color": Color('black'),
  "game_width": 500,
  "game_height": 400,
  "game_font_name": 'ariel',
  "game_font_size": 64,
  "game_font_color": Color('white'),
  "game_frame_rate": 90,
  "game_over_title": "GAME OVER",
  "game_title": "Poke the Dots",
  "small_dot_color": Color('red'),
  "small_dot_radius": 30,
  "small_dot_center": [50, 75],
  "small_dot_velocity": [2, 4],
  "big_dot_color": Color('blue'),
  "big_dot_radius": 40,
  "big_dot_center": [200, 100],
  "big_dot_velocity": [4, 2]
}

def main(ctx):
  # create game
  game = Game(ctx)
  game.play(ctx)

class Game:
  def __init__(self, ctx):
    # initiate pygame's display and font, and set the caption
    # create the window with the width and height attributes
    # set the font, and fill the window
    # create the clock
    # define the frame rate
    # set close selected to False
    # set continue game to True
    # create the small dot and big dot, then randomize their locations
    # set the score to 0
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption(ctx["game_title"])
    self._window = pygame.display.set_mode((ctx["game_width"], ctx["game_height"]), 0, 0)
    self._adjust_window(ctx)
    self._clock = Clock()
    self._frame_rate = ctx["game_frame_rate"]
    self._close_selected = False
    self._continue_game = True
    self._score = 0
    self._small_dot = Dot(self._window, ctx["small_dot_color"], ctx["small_dot_center"], ctx["small_dot_radius"], ctx["small_dot_velocity"])
    self._big_dot = Dot(self._window, ctx["big_dot_color"], ctx["big_dot_center"], ctx["big_dot_radius"], ctx["big_dot_velocity"])
    self._small_dot.randomize()
    self._big_dot.randomize()
    pygame.display.update()

  def _adjust_window(self, ctx):
    self._font = pygame.font.SysFont(ctx["game_font_name"], ctx["game_font_size"], True)
    self._window.fill(ctx["game_bg_color"])
    pygame.display.update()

  def play(self, ctx):
    while not self._close_selected:
      self._close_selected = self.handle_events()
      self.draw_game(ctx)
      self.update()
    pygame.quit()
    sys.exit()

  def draw_game(self, ctx):
    self._window.fill(ctx["game_bg_color"])
    self.draw_score(ctx)
    self._small_dot.draw()
    self._big_dot.draw()
    if not self._continue_game:
      self.draw_game_over(ctx)
    pygame.display.update()

  def draw_string(self, ctx, string, font_color, bg_color, x_pos, y_pos):
    self._window.blit(
      self._font.render(string, True, font_color, bg_color), 
      (x_pos, y_pos)
    )
    pygame.display.update()

  def draw_score(self, ctx):
    score_string = 'Score: ' + str(self._score)
    self.draw_string(ctx, score_string, ctx["game_font_color"], ctx["game_bg_color"], 0, 0)
    pygame.display.update()

  def update(self):
    if self._continue_game:
      for dot in [self._small_dot, self._big_dot]:
        dot.move()
      self._score = int(get_ticks() // 1000)
    self._clock.tick(self._frame_rate) 

    if self._small_dot.intersects(self._big_dot):
      self._continue_game = False

  def handle_inner_click(self):
    for dot in [self._small_dot, self._big_dot]:
      dot.randomize()

  def handle_events(self):
    event_list = pygame.event.get()
    for event in event_list:
      self.handle_one_event(event)

  def handle_one_event(self, event):
    if event.type == QUIT:
      self._close_selected = True
    elif self._continue_game and event.type == MOUSEBUTTONDOWN:
      self.handle_inner_click()

  def draw_game_over(self, ctx):
    font_color = self._small_dot.get_color()
    bg_color = self._big_dot.get_color()
    original_font_color = ctx["game_font_color"]
    original_bg_color = ctx["game_bg_color"]
    line_height = self._window.get_height() - self._font.get_height()
    self.draw_string(ctx, ctx["game_over_title"], original_font_color, original_bg_color, 0, line_height)
    for event in pygame.event.get():
      if event.type == MOUSEBUTTONDOWN:
        pygame.quit()
        sys.exit()

class Dot:
  # an object in this class represents a complete dot
  def __init__(self, window, color, center, radius, velocity):
    self._window = window
    self._color = color
    self._center = center
    self._radius = radius
    self._velocity = velocity

  def draw(self):
    pygame.draw.circle(self._window, self._color, self._center, self._radius)

  def randomize(self):
    window_size = [self._window.get_width(), self._window.get_height()]
    for index in range(0, 2):
      self._center[index] = randint(self._radius, window_size[index] - self._radius)

  def get_color(self):
    return self._color

  def intersects(self, other_dot):
    # distance formula = √2(x2 - x1) + 2(y2 - y1)

    # if the distance is less than the two radiuses combined, it intersects
    distance = sqrt((self._center[0] - other_dot._center[0])**2 + (self._center[1] - other_dot._center[1])**2)
    return distance <= self._radius + other_dot._radius

  def move(self):
    window_size = [self._window.get_width(), self._window.get_height()]
    # size[0] is the max width, size[1] is the max height
    for index in range(0, 2):
      # calculate the new center given the movement from velocity
      self._center[index] += self._velocity[index]
      # if the new center exceeds the max, invert the velocity
      if (self._center[index] + self._radius >= window_size[index]) or (self._center[index] - self._radius <= 0): 
        self._velocity[index] = -self._velocity[index]

main(ctx)