from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс."""

    def __init__(self, body_color=None):
        self.position = [SCREEN_WIDTH // 1, SCREEN_HEIGHT // 1]
        self.body_color = body_color

    def draw(self):
        """Функция отрисовки объекта на игровом поле."""
        raise NotImplementedError()


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
            (self.positions[0][1] + self.direction[1]
             * GRID_SIZE) % SCREEN_HEIGHT)

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
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Дочерний класс. Отвечает за свойства и отображение яблока."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.last = None

    def randomize_position(self, snake):
        """Создание случайного расположения яблока."""
        new_position = (randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                        randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
        while new_position in snake.position:
            new_position = (randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
                            * GRID_SIZE,
                            randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)
                            * GRID_SIZE)
        self.position = new_position

    def draw(self, surface):
        """Отрисовка объекта на игровом поле."""
        rect = pg.Rect(self.position[0],
                       self.position[1], GRID_SIZE, GRID_SIZE)
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)
        if self.last:
            last_rect = pg.Rect(
                self.last[0], self.last[1], GRID_SIZE, GRID_SIZE)
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка нажатия клавиш,
    изменение направления движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Обновление состояния объектов."""
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake)
            snake.length += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        handle_keys(snake)
        snake.move()
        snake.update_direction()
        apple.draw(screen)
        snake.draw(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
