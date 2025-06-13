import curses
import random

# Set up window
screen = curses.initscr()
curses.curs_set(0)
height, width = screen.getmaxyx()
window = curses.newwin(height, width, 0, 0)
window.keypad(True)
window.timeout(100)

# Initial snake coordinates and food
snake = [
    [height//2, width//4],
    [height//2, width//4 - 1],
    [height//2, width//4 - 2]
]
food = [height//2, width//2]
window.addch(food[0], food[1], 'O')

# Initial movement direction
key = curses.KEY_RIGHT

score = 0

try:
    while True:
        next_key = window.getch()
        key = key if next_key == -1 else next_key

        # Calculate new head position
        head = snake[0].copy()
        if key == curses.KEY_DOWN:
            head[0] += 1
        if key == curses.KEY_UP:
            head[0] -= 1
        if key == curses.KEY_LEFT:
            head[1] -= 1
        if key == curses.KEY_RIGHT:
            head[1] += 1

        # Check for collision with boundaries or self
        if (
            head[0] in [0, height] or
            head[1] in [0, width] or
            head in snake
        ):
            msg = f'Game Over! Score: {score}'
            window.addstr(height//2, width//2 - len(msg)//2, msg)
            window.refresh()
            window.timeout(-1)
            window.getch()
            break

        snake.insert(0, head)

        # Check if snake got food
        if head == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, height - 2),
                    random.randint(1, width - 2)
                ]
                if nf not in snake:
                    food = nf
            window.addch(food[0], food[1], 'O')
        else:
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        window.addch(snake[0][0], snake[0][1], '#')
finally:
    curses.endwin()

