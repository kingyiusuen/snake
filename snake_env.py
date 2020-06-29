import random
from collections import deque
import numpy as np
import pygame

RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

# find the new moving direction given the original direction and the chosen action 
# 3 possible actions - 0: go straight, 1: go left, 2: go right
action_to_direction = {
    "UP":    {0: "UP",    1: "LEFT",  2: "RIGHT"},
    "DOWN":  {0: "DOWN",  1: "RIGHT", 2: "LEFT"},
    "LEFT":  {0: "LEFT",  1: "DOWN",  2: "UP"},
    "RIGHT": {0: "RIGHT", 1: "UP",    2: "DOWN"}
}

class SnakeEnv():
    def __init__(self):
        pygame.display.set_caption("Snake")
        self.window_width = 440
        self.window_height = 440
        self.screen = None
        self.square_size = 20
        self.margin = 20
        self.speed = 50
        self.snake = deque()
        self.action_space = list(range(3))
        self.state_size = 5
        self.reset()

    def step(self, action):
        """ Take an action as an input, return the resulting game state, reward receivedand whether the game is over """
        self.direction = action_to_direction[self.direction][action]
        new_coord = self._get_new_coord(self.snake[0], self.direction)
        self.snake.appendleft(new_coord)

        result = self._is_collided(self.snake[0])
        done = False

        if result == 1:
            # increment score and generate new food if food is eaten
            self.score += 1
            self._generate_food()
        elif result == 2:
            # game over if snake eats itself or hits a wall
            done = True
        else:
            # doesn't hit anything
            self.snake.pop()

        state = self._get_game_state()
        reward = self._get_reward(result)
        return state, reward, done

    def reset(self):
        """ Reset the game environment, use to start a new game """
        self.score = 0
        self.snake.clear()
        self.snake.append((self.window_width // 2, self.window_height // 2)) # starts at the center of the screen
        self.direction = "UP"
        self._generate_food()
        return self._get_game_state()

    def render(self):
        """ Display the graphics (background, snake, food and score) """
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        clock = pygame.time.Clock()

        # draw the black background
        self.screen.fill(BLACK)

        # draw four borders
        top_left = (self.square_size, self.square_size)
        top_right = (self.window_width - self.square_size, self.square_size)
        bottom_left = (self.square_size, self.window_height - self.square_size)
        bottom_right = (self.window_width - self.square_size, self.window_height - self.square_size)
        pygame.draw.line(self.screen, WHITE, top_left, top_right) # top horizontal line
        pygame.draw.line(self.screen, WHITE, top_left, bottom_left) # left vertical line
        pygame.draw.line(self.screen, WHITE, bottom_left, bottom_right) # bottom horizontal
        pygame.draw.line(self.screen, WHITE, top_right, bottom_right) # right vertical

        # display score
        font = pygame.font.SysFont("Courier New", 18)
        score_text = font.render("SCORE: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, [self.window_width // 2 - 40, 0])

        # draw snake
        for square in self.snake:
            pygame.draw.rect(self.screen, GREEN, (square[0], square[1], self.square_size, self.square_size), 2)
            
        # draw food
        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], self.square_size, self.square_size))
            
        clock.tick(self.speed)
        pygame.display.update()

    def _generate_food(self):
        """ Generate coordinates for the food"""
        in_snake_body = True
        while in_snake_body: 
            rand_x = random.randint(self.margin, self.window_width - self.square_size - self.margin) // self.square_size * self.square_size
            rand_y = random.randint(self.margin, self.window_height - self.square_size - self.margin) // self.square_size * self.square_size
            in_snake_body = any(rand_x == x and rand_y == y for x, y in self.snake) # check if the generated position is in the snake body
        self.food = (rand_x, rand_y)

    def _is_collided(self, coord):
        """ 
        Check if any object is located in a given set of coordinates
        Returns 0 if nothing
                1 if it is occupied by the food
                2 if it is occupied by the snake body (excluding the head)
        """
        x, y = coord
        if (x, y) == self.food: 
            return 1 # collide with food
        if any(x == square[0] and y == square[1] for i, square in enumerate(self.snake) if i > 0) or \
                x < self.margin or x > self.window_width - self.square_size - self.margin or \
                y < self.margin or y > self.window_height - self.square_size - self.margin:
            return 2 # collide with the snake body or a wall
        return 0 # nothing

    def _get_reward(self, result):
        """ Return the reward for a given result  """
        rewards = {
            0:  -1, # nothing happens
            1:  50, # food is eaten
            2: -30, # eat itself or hit a wall
        }
        return rewards[result]

    def _get_new_coord(self, coord, direction):
        """ Return the coordinates of the snake head had the snake moved in the given direction """
        x, y = coord
        if direction == "UP":
            return (x, y - self.square_size)
        elif direction == "DOWN":
            return (x, y + self.square_size)
        elif direction == "LEFT":
            return (x - self.square_size, y)
        elif direction == "RIGHT":
            return (x + self.square_size, y)

    def _transform_coord(self, coord, direction):
        """ Transform coordinates relative to snake head based on moving direction """
        # if snake is moving up, no transformation is needed
        x, y = coord
        if direction == "LEFT": 
            return (-y, x)
        elif direction == "RIGHT": 
            return (y, -x)
        elif direction == "DOWN": 
            return (-x, -y)
        return (x, y)

    def _get_quadrant(self, coord):
        """ 
        Compute where (x, y) is, relative to the origin 
        Returns a tuple where
        qx: 1 if (x, y) is on the left of the origin, 2 if right, 0 otherwise
        qy: 1 if (x, y) is above the origin, 2 if below, 0 otherwise
        """
        def sign(n):
            if n < 0:
                return 1
            if n > 0:
                return 2
            return 0
        x, y = coord
        qx, qy = sign(x), sign(y)
        return (qx, qy)

    def _get_game_state(self):
        """
        Return a 5-dimensional tuple that represents the state space
        1. the kind of object the snake will encounter if it goes straight
        2. the kind of object the snake will encounter if it goes left
        3. the kind of object the snake will encounter if it goes right
        4. the x-position of food relative to snake head
        5. the y-position of food relative to snake head
        """
        state = []

        # check if there is any object adjacent to snake head in straight, 
        # left and right directions (relative to the moving direction)
        for new_direction in action_to_direction[self.direction].values():
            new_x, new_y = self._get_new_coord(self.snake[0], new_direction)
            state.append(self._is_collided((new_x, new_y)))

        # compute which quadrant the food is in, relative to the snake head and moving direction
        trans_coord = self._transform_coord((self.food[0] - self.snake[0][0], self.food[1] - self.snake[0][1]), self.direction)
        qx, qy = self._get_quadrant(trans_coord)
        state.append(qx)
        state.append(qy)
        return tuple(state) # have to use convert to tuple as list is not hashable
