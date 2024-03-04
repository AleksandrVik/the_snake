from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс."""

    def __init__(self, body_color=None):
        self.position = [SCREEN_WIDTH // 1, SCREEN_HEIGHT // 1]
        self.body_color = body_color

    def draw(self):
        """Функция отрисовки объекта на игровом поле."""


class Snake(GameObject):
    """Дочерний класс. Отвечает за свойства и отображение змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возврат головы змейки."""
        return self.positions[0]

    def move(self):
        """Логика и движение змейки."""
        new_position = (
            (self.positions[0][0] + self.direction[0]
             * GRID_SIZE) % SCREEN_WIDTH,
            (self.positions[0][1] + self.direction[1] * GRID_SIZE)
            % SCREEN_HEIGHT)

        if new_position in self.positions[1:]:
            self.reset()

        self.positions.insert(0, new_position)

        if self.length < len(self.positions):
            self.last = self.positions.pop()

        else:
            self.last = None

    def reset(self):
        """Перезапуск змейки при столкновении."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, LEFT, RIGHT, DOWN])
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self, surface):
        """Отрисовка объекта на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Дочерний класс. Отвечает за свойства и отображение яблока."""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.position = self.randomize_position()
        self.last = None

    def randomize_position(self):
        """Создание случайного расположения яблока."""
        return (randint(0, SCREEN_WIDTH // 20 - 1)
                * GRID_SIZE, randint(0, SCREEN_HEIGHT // 20 - 1) * GRID_SIZE)

    def draw(self, surface):
        """Отрисовка объекта на игровом поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка нажатия клавиш,
    изменение направления движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Обновление состояния объектов."""
    apple = Apple()
    snake = Snake()
    apple.randomize_position()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 0

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.position = apple.randomize_position()
            apple.draw(screen)
            pygame.display.update()

        handle_keys(snake)
        snake.move()
        snake.update_direction()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
