import pygame
from pygame.draw import *
from random import randint, choice
import os.path as path

pygame.init()

FPS = 30
A, B = 1200, 650  # screen width and height
sc = pygame.display.set_mode((A, B))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def generate_new_ball() -> list:
    """
    генерирует псевдослучайные параметры круга
    :return: цвет, координаты, радиус, вектор скорости круга
    """
    x = randint(101, A - 101)
    y = randint(101, B - 101)
    r = choice(range(10, 101, 10))
    color = choice(COLORS)
    mutation = randint(1, 2)
    if mutation == 1:
        speed = [-1, 1]
        Vx, Vy = choice(speed), choice(speed)
        cost = 110 - r
        mutation = mutation, None
    else:
        speed = [-1, 1]
        Vx = choice(speed)
        Vy = 0
        cost = (110 - r) // 2
        if Vx == 1:
            mut_params = x - r, randint(x + r, A)
        else:
            mut_params = randint(0, x - r), x + r
        mutation = mutation, mut_params
    return [color, x, y, r, [Vx, Vy], cost, mutation]


def draw_ball(screen, params) -> None:
    """
    рисует круг в заданном месте холста с заданными параметрами
    :param screen: холст, на котором рисуются круг
    :param params: параметры круга (color, x, y, r)
    :return: None
    """
    color, x, y, r, *needless = params
    circle(screen, color, (x, y), r)


def move_ball(params) -> list:
    """
    пересчитывает координаты круга, в соответствии с заданным вектором скорости
    :param params: параметры круга и его скорости (color, x, y, r, velocity)
    :return параметры круга с пересчитанными координатами (color, x, y, r, velocity)
    """
    x, y, r, [Vx, Vy] = params[1:5]
    params[1] = x + Vx
    params[2] = y + Vy
    return params


def check_collision(params, a, b) -> list:
    """
    проверяет столкновение круга с другим кругом или границами холста
    :param params: параметры круга (color, x, y, r, velocity)
    :param a: ширина холста
    :param b: высота холста
    :return: параметры круга с пересчитанным вектором скорости
    """
    x, y, r, [Vx, Vy], cost, mutation = params[1:]
    num_of_mutation, mut_params = mutation
    zero = 0
    if num_of_mutation == 2:
        zero = mut_params[0]
        a = mut_params[1]

    if x - r == zero or x + r == a:
        Vx = -Vx
    if y - r == 0 or y + r == b:
        Vy = -Vy
    params[4] = [Vx, Vy]
    return params


def check_hit(params, event) -> bool:
    """
    проверяет попадание клика мыши в круг
    :param params: пармаметры круга (color, x, y, r)
    :param event: событие = клик мыши по холсту
    :return: есть попадание: True; нет попадания: False
    """
    x_ball, y_ball, r = params[1:4]
    x_clk, y_clk = event.pos
    distance = ((x_clk - x_ball) ** 2 + (y_clk - y_ball) ** 2) ** 0.5
    if distance <= r:
        return True
    else:
        return False


def print_score_canvas(screen, score, diff) -> None:
    """
    печатает текущее количество очков (счёт) на холст
    :param screen: холст, на который будет напечатан счёт
    :param score: текущий счёт
    :param diff:  разница между пред и тек счётом
    :return:
    """
    color = (255, 255, 255)
    background = (100, 50, 100)
    fontObj = pygame.font.Font(None, 50)
    textSurfaceObj = fontObj.render(f'Your score: {score} (+{diff})', True, color, background)
    screen.blit(textSurfaceObj, [10, 10])


def mouse_button_down(balls, game_score, game_diff) -> tuple:
    """
    обрабатывает нажатия кнопок мышки
    :return:
    """
    for i, ball_params in enumerate(balls):
        if check_hit(ball_params, event):
            game_score += ball_params[5]
            game_diff = ball_params[5]
            del balls[i]
    return balls, game_score, game_diff


def print_score_to_file(game_score):
    """
    добавляет текущий счёт в файл с таблицей лидеров
    :param game_score: счёт в игре
    :return:
    """
    leaderboard = [game_score]
    if path.exists('leader_board.txt'):
        leaderboard = append_leaderboard(leaderboard)
        leaderboard.sort(reverse=True)

    with open('leader_board.txt', 'w') as f:
        number = 1
        for score in leaderboard:
            f.write(f'{number}. {score}\n')
            number += 1


def append_leaderboard(leader_list):
    """
    добавляет прошлую таблицу лидеров из файла  leader_board.txt в текущий список лидеров
    :param leader_list: текущий список лидеров
    :return: возвращает новый список лидеров
    """
    with open('leader_board.txt', 'r') as f:
        strings = f.readlines()

    for string in strings:
        score = int(string.split('. ')[1])
        leader_list.append(score)
    return leader_list


pygame.display.update()
clock = pygame.time.Clock()
finished = False
ball_params = None
game_score = game_diff = spawn_time = 0
balls = []

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls, game_score, game_diff = mouse_button_down(balls, game_score, game_diff)

    sc.fill(BLACK)
    if len(balls) < 10:
        spawn_time += 1
        if spawn_time > 99:
            balls.append(generate_new_ball())
            spawn_time = 0

    for i, ball_params in enumerate(balls):
        draw_ball(sc, ball_params)
        balls[i] = move_ball(ball_params)
        balls[i] = check_collision(balls[i], A, B)

    print_score_canvas(sc, game_score, game_diff)
    pygame.display.flip()


print_score_to_file(game_score)
pygame.quit()
