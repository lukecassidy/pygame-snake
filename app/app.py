#!/usr/bin/env python
"""
A simple snake game using pygame
"""

import random
from enum import Enum
import pygame
import sys


class COLOURS:
    WHITE = (255, 255, 255)
    NAVY = (10, 0, 40)
    PINK  = (255, 0, 128)
    TEAL = (0, 255, 214)
    BLUE  = (35, 0, 75)


class CONFIG:
    BLOCK_SIZE      = 10
    SCORE_PER_FOOD  = 250
    GROWTH_PER_FOOD = 2
    FPS             = 20
    SCREEN_WIDTH    = 600
    SCREEN_HEIGHT   = 400
    CAPTION         = "Snake"
    SCORE_COLOUR    = COLOURS.WHITE


class Direction(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Game:
    caption = CONFIG.CAPTION
    fps = CONFIG.FPS
    screen_width = CONFIG.SCREEN_WIDTH
    screen_height = CONFIG.SCREEN_HEIGHT
    score_colour = CONFIG.SCORE_COLOUR

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font_small = pygame.font.SysFont(None, 25)
        self.font_med = pygame.font.SysFont(None, 30)
        self.font_large = pygame.font.SysFont(None, 40)

    def display_score(self):
        message = f"SCORE: {self.score}"
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

    def get_score(self):
        return self.score

    def reset(self):
        self.score = 0

    def exit(self):
        pygame.quit()
        sys.exit()


class Snake:
    colour = COLOURS.TEAL
    block_size = CONFIG.BLOCK_SIZE

    def __init__(self):
        self.snake_list = []
        self.length = 1               # Increase when you eat food
        self.speed = self.block_size  # Move by one grid cell
        # Start centered on the grid
        self.head_x = (CONFIG.SCREEN_WIDTH // 2 // self.block_size) * self.block_size
        self.head_y = (CONFIG.SCREEN_HEIGHT // 2 // self.block_size) * self.block_size
        self.x_change = 0
        self.y_change = 0
        self.direction = Direction.NONE

    def reset(self):
        self.length = 1
        self.snake_list = []
        self.head_x = (CONFIG.SCREEN_WIDTH // 2 // self.block_size) * self.block_size
        self.head_y = (CONFIG.SCREEN_HEIGHT // 2 // self.block_size) * self.block_size
        self.x_change = 0
        self.y_change = 0
        self.direction = Direction.NONE

    def draw_snake(self, surface: pygame.Surface):
        for x, y in self.snake_list:
            pygame.draw.rect(surface, self.colour, [x, y, self.block_size, self.block_size])

    def check_boundaries(self):
        if self.head_x >= CONFIG.SCREEN_WIDTH:
            return True
        if self.head_x < 0:
            return True
        if self.head_y >= CONFIG.SCREEN_HEIGHT:
            return True
        if self.head_y < 0:
            return True
        return False

    def check_self_collision(self):
        # If the snake hits itself, game over
        head = [self.head_x, self.head_y]
        for snake_point in self.snake_list[:-1]:
            if snake_point == head:
                return True
        return False

    def remove_tail(self):
        # Delete the oldest snake position
        if len(self.snake_list) > self.length:
            del self.snake_list[0]


class Food:
    colour = COLOURS.PINK
    block_size = CONFIG.BLOCK_SIZE

    def __init__(self):
        self.snake_body_list = []
        self.x = 0
        self.y = 0
        self.generate_food()

    def generate_food(self):
        while True:
            random_x = random.randrange(0, CONFIG.SCREEN_WIDTH, self.block_size)
            random_y = random.randrange(0, CONFIG.SCREEN_HEIGHT, self.block_size)
            if [random_x, random_y] not in self.snake_body_list:
                self.x = random_x
                self.y = random_y
                return


def game_intro():
    display_intro = True
    while display_intro:
        game.surface.fill(COLOURS.NAVY)
        game.message_to_screen("Snake", COLOURS.PINK, font_size='large', y_change=-100)
        game.message_to_screen("Press ENTER to Play", COLOURS.WHITE, font_size='med', y_change=+20)
        game.message_to_screen("Press ESC to Quit", COLOURS.WHITE, font_size='med', y_change=+100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.exit()
                elif event.key == pygame.K_RETURN:
                    display_intro = False

        game.clock.tick(CONFIG.FPS)
        pygame.display.update()


def game_pause():
    display_pause = True
    while display_pause:
        game.surface.fill(COLOURS.NAVY)
        game.message_to_screen("Snake", COLOURS.PINK, font_size='large', y_change=-100)
        game.message_to_screen("Press ENTER to Continue", COLOURS.WHITE, font_size='med', y_change=+20)
        game.message_to_screen("Press ESC to Quit", COLOURS.WHITE, font_size='med', y_change=+100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.exit()
                elif event.key == pygame.K_RETURN:
                    display_pause = False

        game.clock.tick(CONFIG.FPS)
        pygame.display.update()


def game_loop():
    running = True
    is_game_over = False

    while running:
        while is_game_over:
            game.surface.fill(COLOURS.NAVY)
            game.message_to_screen("Game Over", COLOURS.PINK, font_size='large', y_change=-100)
            game.message_to_screen(
                f"Score {game.get_score()}", COLOURS.PINK, font_size='large', y_change=-40
            )
            game.message_to_screen("Press ENTER to play", COLOURS.WHITE, font_size='med', y_change=+60)
            game.message_to_screen("Press ESC to Quit", COLOURS.WHITE, font_size='med', y_change=+100)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.exit()
                    elif event.key == pygame.K_RETURN:
                        game.reset()
                        snake.reset()
                        food.generate_food()
                        is_game_over = False
                if event.type == pygame.QUIT:
                    game.exit()

            pygame.display.update()
            game.clock.tick(CONFIG.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
            is_game_over = True

        game.surface.fill(COLOURS.NAVY)

        pygame.draw.rect(game.surface, COLOURS.PINK, [food.x, food.y, food.block_size, food.block_size])

        snake.snake_list.append([snake.head_x, snake.head_y])

        snake.remove_tail()

        if snake.check_self_collision():
            is_game_over = True

        snake.draw_snake(game.surface)

        head_rect = pygame.Rect(snake.head_x, snake.head_y, snake.block_size, snake.block_size)
        food_rect = pygame.Rect(food.x, food.y, food.block_size, food.block_size)
        if head_rect.colliderect(food_rect):
            food.snake_body_list = snake.snake_list
            food.generate_food()
            pygame.draw.rect(game.surface, COLOURS.PINK, [food.x, food.y, food.block_size, food.block_size])
            snake.length += CONFIG.GROWTH_PER_FOOD
            game.score += CONFIG.SCORE_PER_FOOD

        game.display_score()
        pygame.display.update()
        game.clock.tick(CONFIG.FPS)


def main():
    pygame.init()
    game_display = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
    pygame.display.set_caption(CONFIG.CAPTION)

    global game, snake, food
    game = Game(game_display)
    snake = Snake()
    food = Food()

    game_intro()
    game_loop()
    game.exit()


if __name__ == "__main__":
    main()
