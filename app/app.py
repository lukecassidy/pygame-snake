#!/usr/bin/env python
"""
A simple snake game using pygame
"""


import random
from enum import Enum
import pygame
import sys


# TODO: move to classes
BLOCK_SIZE = 10
SCORE_PER_FOOD = 250
GROWTH_PER_FOOD = 2


class Colour:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 150, 0)
    BLUE = (0, 0, 255)


class Direction(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Game:
    caption = "Snake"
    fps = 20
    screen_width = 600
    screen_height = 400
    score_colour = Colour.RED

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font_small = pygame.font.SysFont(None, 25)
        self.font_med = pygame.font.SysFont(None, 30)
        self.font_large = pygame.font.SysFont(None, 40)


    def display_score(self):
        message = f"score: {self.score}"
        text_surface = self.font_small.render(message, True, self.score_colour)
        text_rect = text_surface.get_rect()
        self.surface.blit(text_surface, text_rect)

    def message_to_screen(self, message, colour, font_size, y_change=0, x_change=0):
        match font_size:
            case 'large':
                font = self.font_large
            case 'med':
                font = self.font_med
            case 'small' | _:
                font = self.font_small

        text_surface = font.render(message, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (
            (self.screen_width // 2) + x_change,
            (self.screen_height // 2) + y_change,
        )
        self.surface.blit(text_surface, text_rect)

    def get_score(self) -> int:
        return self.score

    def reset(self):
        self.score = 0

    def exit(self):
        pygame.quit()
        sys.exit()


class Snake:
    colour = Colour.GREEN
    block_size = BLOCK_SIZE

    def __init__(self):
        self.snake_list = []
        self.snake_head = []
        self.length = 1               # Increase when you eat food
        self.speed = self.block_size  # Move by one grid cell
        # Start centered on the grid
        self.head_x = (Game.screen_width // 2 // self.block_size) * self.block_size
        self.head_y = (Game.screen_height // 2 // self.block_size) * self.block_size
        self.x_change = 0
        self.y_change = 0
        self.direction = Direction.NONE

    def reset(self):
        self.length = 1
        self.snake_list = []
        self.snake_head = []
        self.head_x = (Game.screen_width // 2 // self.block_size) * self.block_size
        self.head_y = (Game.screen_height // 2 // self.block_size) * self.block_size
        self.x_change = 0
        self.y_change = 0
        self.direction = Direction.NONE

    def draw_snake(self, surface: pygame.Surface):
        for x, y in self.snake_list:
            pygame.draw.rect(
                surface, self.colour, [x, y, self.block_size, self.block_size]
            )

    def check_boundaries(self) -> bool:
        if self.head_x >= Game.screen_width:
            return True
        if self.head_x < 0:
            return True
        if self.head_y >= Game.screen_height:
            return True
        if self.head_y < 0:
            return True
        return False

    def check_self_collision(self) -> bool:
        # If the snake hits itself, game over
        for snake_point in self.snake_list[:-1]:
            if snake_point == self.snake_head:
                return True
        return False

    def remove_tail(self):
        # Delete the oldest snake position
        if len(self.snake_list) > self.length:
            del self.snake_list[0]


class Food:
    def __init__(self):
        self.colour = Colour.RED
        self.block_size = BLOCK_SIZE
        self.snake_body_list = []
        self.x = 0
        self.y = 0
        self.generate_food()

    def generate_food(self):
        while True:
            random_x = random.randrange(0, Game.screen_width, self.block_size)
            random_y = random.randrange(0, Game.screen_height, self.block_size)
            if [random_x, random_y] not in self.snake_body_list:
                self.x = random_x
                self.y = random_y
                return


def game_intro():
    display_intro = True
    while display_intro:
        game.surface.fill(Colour.BLACK)
        game.message_to_screen("Snake", Colour.RED, font_size='large', y_change=-100)
        game.message_to_screen("Press ENTER to Play", Colour.WHITE, font_size='med', y_change=+20)
        game.message_to_screen("Press ESC to Quit", Colour.WHITE, font_size='med', y_change=+100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.exit()
                elif event.key == pygame.K_RETURN:
                    display_intro = False

        game.clock.tick(game.fps)
        pygame.display.update()


def game_pause():
    display_pause = True
    while display_pause:
        game.surface.fill(Colour.BLACK)
        game.message_to_screen("Snake", Colour.RED, font_size='large', y_change=-100)
        game.message_to_screen("Press ENTER to Continue", Colour.WHITE, font_size='med', y_change=+20)
        game.message_to_screen("Press ESC to Quit", Colour.WHITE, font_size='med', y_change=+100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.exit()
                elif event.key == pygame.K_RETURN:
                    display_pause = False

        game.clock.tick(game.fps)
        pygame.display.update()


def game_loop():
    # TODO: rename, these are currently confusing 
    game_quit = False
    game_over = False

    while not game_quit:
        while game_over:
            game.surface.fill(Colour.BLACK)
            game.message_to_screen("Game Over", Colour.RED, font_size='large', y_change=-100)
            game.message_to_screen(
                f"Score {game.get_score()}", Colour.RED, font_size='large', y_change=-40
            )
            game.message_to_screen("Press ENTER to play", Colour.WHITE, font_size='med', y_change=+60)
            game.message_to_screen("Press ESC to Quit", Colour.WHITE, font_size='med', y_change=+100)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.exit()
                    elif event.key == pygame.K_RETURN:
                        game.reset()
                        snake.reset()
                        food.generate_food()
                        game_over = False
                if event.type == pygame.QUIT:
                    game.exit()

            pygame.display.update()
            game.clock.tick(game.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.exit()
                if event.key == pygame.K_LEFT and snake.direction != Direction.RIGHT:
                    snake.x_change = -snake.speed
                    snake.y_change = 0
                    snake.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != Direction.LEFT:
                    snake.x_change = snake.speed
                    snake.y_change = 0
                    snake.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and snake.direction != Direction.DOWN:
                    snake.x_change = 0
                    snake.y_change = -snake.speed
                    snake.direction = Direction.UP
                elif event.key == pygame.K_DOWN and snake.direction != Direction.UP:
                    snake.x_change = 0
                    snake.y_change = snake.speed
                    snake.direction = Direction.DOWN
                elif event.key == pygame.K_p:
                    game_pause()

        snake.head_x += snake.x_change
        snake.head_y += snake.y_change

        if snake.check_boundaries():
            game_over = True

        game.surface.fill(Colour.WHITE)

        pygame.draw.rect(game.surface, Colour.RED, [food.x, food.y, food.block_size, food.block_size])

        snake.snake_head = [snake.head_x, snake.head_y]
        snake.snake_list.append(snake.snake_head)

        snake.remove_tail()

        if snake.check_self_collision():
            game_over = True

        snake.draw_snake(game.surface)

        head_rect = pygame.Rect(snake.head_x, snake.head_y, snake.block_size, snake.block_size)
        food_rect = pygame.Rect(food.x, food.y, food.block_size, food.block_size)
        if head_rect.colliderect(food_rect):
           food.snake_body_list = snake.snake_list
           food.generate_food()
           pygame.draw.rect(game.surface, Colour.RED, [food.x, food.y, food.block_size, food.block_size])
           snake.length += GROWTH_PER_FOOD
           game.score += SCORE_PER_FOOD
        game.display_score()
        pygame.display.update()
        game.clock.tick(game.fps)


def main():
    pygame.init()
    game_display = pygame.display.set_mode((Game.screen_width, Game.screen_height))
    pygame.display.set_caption(Game.caption)

    global game, snake, food
    game = Game(game_display)
    snake = Snake()
    food = Food()

    game_intro()
    game_loop()
    game.exit()


if __name__ == "__main__":
    main()