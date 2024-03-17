import random
import pygame
from pygame.math import Vector2
import sys
from copy import deepcopy

obs_dim = 30
min_obs_num = 1
max_obs_num = 100
screen_size = (1128, 634)
map_area_padding = 50
screen_bg = (200, 180, 255)
max_points = 6000

unit = 20

class Node:
  def __init__(self, v: Vector2):
    self.pos = v
    self.radius = 2
    self.color = (128, 128, 128)
    self.parent_node = None
    self.path_length = 0
  
  def add_parent_node(self, node):
    self.parent_node = node
    self.path_length = node.path_length + (self.pos - node.pos).length()

  def step_to_point(self, point: Vector2):
    unit_step = (point - self.pos)/(point - self.pos).magnitude() * unit
    new_node = Node(self.pos + unit_step)
    new_node.add_parent_node(self)
    return new_node

  def draw_node(self):
    pygame.draw.circle(screen, self.color, self.pos, self.radius)
    
class StartNode(Node):
  def __init__(self, v: Vector2):
    super().__init__(v)
    self.radius = 15
    self.color = (0, 150, 0)
    
class GoalNode(Node):
  def __init__(self, v: Vector2):
    super().__init__(v)
    self.radius = 15
    self.color = (240, 50, 0)

class Obstacle:
  def __init__(self, c: Vector2, w, h):
    self.width = w
    self.height = h
    self.center = c
    self.body = pygame.Rect((self.center.x - self.width//2), (self.center.y - self.height//2),
                            self.width, self.height)
    self.color = (0, 0, 0)
    
  def draw_obs(self):
      pygame.draw.rect(screen, self.color, self.body)

def draw_map():
  start_x = random.randint(map_area_padding + 15, screen_size[0] - map_area_padding - 15)
  start_y = random.randint(map_area_padding + 15, screen_size[1] - map_area_padding - 15)
  start = StartNode(Vector2(start_x, start_y))
  goal_node_not_formed = True
  while goal_node_not_formed:
    goal_x = random.randint(map_area_padding + 15, screen_size[0] - map_area_padding - 15)
    goal_y = random.randint(map_area_padding + 15, screen_size[1] - map_area_padding - 15)
    goal_center = Vector2(goal_x, goal_y)
    if (goal_center - start.pos).length_squared() <= 900:
      continue
    else:
      goal = GoalNode(goal_center)
      goal_node_not_formed = False
  obs_num = random.randint(min_obs_num, max_obs_num)
  obstacles = []
  while obs_num >= 0:
    obs_not_formed = True
    while obs_not_formed:
      obs_width = obs_dim
      obs_height = obs_dim
      obs_x = random.randint(map_area_padding + obs_width//2, screen_size[0] - map_area_padding - obs_width//2)
      obs_y = random.randint(map_area_padding + obs_height//2, screen_size[1] - map_area_padding - obs_height//2)
      obs_center = Vector2(obs_x, obs_y)
      if (obs_center - start.pos).length_squared() <= 1024 or (obs_center - goal.pos).length_squared() <= 1024:
        continue
      else:
        obs = Obstacle(obs_center, obs_width, obs_height)
        obs_not_formed = False
    obstacles.append(obs)
    obs_num -= 1
  
  start.draw_node()
  goal.draw_node()
  for obstacle in obstacles:
    obstacle.draw_obs()
  
  return start, goal, obstacles

def erase_path(path):
  for i in range(len(path) - 1):
    pygame.draw.line(screen, (240, 240, 240), path[i].pos, path[i+1].pos, width=3)
    pygame.draw.line(screen, (70, 70, 70), path[i].pos, path[i+1].pos)
    path[i].draw_node()
  path[-1].draw_node()
  pygame.display.update()

def record_and_draw_path():
  path = []
  child_node = goal
  path.append(goal)
  while child_node.parent_node is not None:
    path.append(child_node.parent_node)
    child_node = child_node.parent_node
        
  path.reverse()
  for i in range(len(path) - 1):
    pygame.draw.line(screen, (70, 255, 255), path[i].pos, path[i+1].pos, width=3)
    pygame.draw.circle(screen, (255, 255, 0), path[i].pos, 2)
    pygame.display.update()
    clock.tick(60)
  pygame.draw.circle(screen, (0, 70, 255), path[-1].pos, 2)
  return path

if __name__ == '__main__':
  pygame.init()
  pygame.display.set_caption("Motion Planning: RRT Implementation")
  screen = pygame.display.set_mode(screen_size)
  clock = pygame.time.Clock()
  
  nodes = []
  reached_point = False
  
  running = True
  path_recorded = False
  previous_path = []
  
  screen.fill(screen_bg)
  
  start, goal, obstacles = draw_map()
  nodes.append(start)
  
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        sys.exit()
    
    root_node = start
    while len(nodes) < max_points:
      random_point_x = random.randint(0, screen_size[0])
      random_point_y = random.randint(0, screen_size[1])
      random_point = Vector2(random_point_x, random_point_y)
      new_node = root_node.step_to_point(random_point)
      for obstacle in obstacles:
        if obstacle.body.collidepoint(new_node.pos) or obstacle.body.clipline(new_node.parent_node.pos, new_node.pos):
          branch_node = deepcopy(new_node.parent_node)
          clipped_line = obstacle.body.clipline(new_node.parent_node.pos, new_node.pos)
          new_node = Node(Vector2(clipped_line[0]))
          new_node.add_parent_node(branch_node)
      nodes.append(new_node)
      for node in nodes:
        if node.parent_node:
          node.draw_node()
          pygame.draw.line(screen, (70, 70, 70), node.parent_node.pos, node.pos)
      if previous_path:
        for i in range(len(previous_path) - 1):
          pygame.draw.line(screen, (70, 255, 255), previous_path[i].pos, previous_path[i+1].pos, width=3)
          pygame.draw.circle(screen, (255, 255, 0), previous_path[i].pos, 2)
      if (new_node.pos - goal.pos).length() < 1.5 * unit:
        reached_point = True
        pygame.draw.line(screen, (70, 70, 70), new_node.pos, goal.pos)
        goal.add_parent_node(new_node)
        if previous_path:
          erase_path(previous_path)
        path = record_and_draw_path()
        previous_path = path
        print(f'Number of nodes: {len(path)}')
        print(f'Length of path taken: {goal.path_length:.2f} units (1 unit = {unit} pixels)')
      min_dist = 5000
      for node in nodes:
        dist = (node.pos - random_point).length()
        if min_dist > dist:
          min_dist = dist
          closest_node = node
      root_node = closest_node
      pygame.display.update()
      clock.tick(144)
    print(f'Maximum points ({max_points}) reached.')
