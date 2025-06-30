import turtle
import time
import random

# Game state
delay = 0.1
score = 0
high_score = 0
paused = False

# Screen setup
win = turtle.Screen()
win.title("🐍 Realistic Snake Game")
win.bgcolor("black")
win.setup(width=700, height=700)
win.tracer(0)

# Draw chessboard background
def draw_chessboard():
    block_size = 40
    board = turtle.Turtle()
    board.hideturtle()
    board.penup()
    colors = ["#2d2d2d", "#3e3e3e"]

    for row in range(-8, 9):
        for col in range(-8, 9):
            x = col * block_size
            y = row * block_size
            color = colors[(row + col) % 2]
            board.goto(x - 20, y - 20)
            board.fillcolor(color)
            board.begin_fill()
            for _ in range(4):
                board.forward(block_size)
                board.left(90)
            board.end_fill()

draw_chessboard()

# Snake head
head = turtle.Turtle()
head.shape("circle")
head.color("#00FF00")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 310)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 20, "bold"))

# Pause text
pause_text = turtle.Turtle()
pause_text.hideturtle()
pause_text.color("yellow")
pause_text.penup()

segments = []

# Movement
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

# Draw square buttons with arrows
def draw_arrow_button(t, x, y, label):
    t.penup()
    t.goto(x - 25, y - 25)
    t.pendown()
    t.fillcolor("#444")
    t.begin_fill()
    for _ in range(4):
        t.forward(50)
        t.left(90)
    t.end_fill()
    t.penup()
    t.goto(x, y - 10)
    t.color("white")
    t.write(label, align="center", font=("Arial", 20, "bold"))

btn_drawer = turtle.Turtle()
btn_drawer.hideturtle()
btn_drawer.speed(0)
draw_arrow_button(btn_drawer, -250, 0, "↑")
draw_arrow_button(btn_drawer, -250, -60, "↓")
draw_arrow_button(btn_drawer, -280, -30, "←")
draw_arrow_button(btn_drawer, -220, -30, "→")
draw_arrow_button(btn_drawer, 250, 270, "⏸")

# Button click handling
def button_click(x, y):
    global paused
    if -275 < x < -225 and -25 < y < 25:
        go_up()
    elif -275 < x < -225 and -85 < y < -35:
        go_down()
    elif -305 < x < -255 and -55 < y < -5:
        go_left()
    elif -225 < x < -175 and -55 < y < -5:
        go_right()
    elif 225 < x < 275 and 240 < y < 300:
        paused = not paused
        if paused:
            pause_text.goto(0, 0)
            pause_text.write("⏸ PAUSED", align="center", font=("Courier", 30, "bold"))
        else:
            pause_text.clear()

# Game loop
def run_game():
    global delay, score, high_score, segments

    delay = 0.1
    score = 0
    segments = []

    head.goto(0, 0)
    head.direction = "stop"
    food.goto(0, 100)
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 20, "bold"))
    pause_text.clear()

    while True:
        win.update()

        if paused:
            time.sleep(0.1)
            continue

        # Border collision
        if abs(head.xcor()) > 340 or abs(head.ycor()) > 340:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            delay = 0.1
            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 20, "bold"))

        # Food collision
        if head.distance(food) < 20:
            x = random.randint(-320, 320)
            y = random.randint(-320, 320)
            food.goto(x, y)

            new_segment = turtle.Turtle()
            new_segment.shape("square")
            new_segment.color("#77ff77")
            new_segment.penup()
            segments.append(new_segment)

            delay -= 0.001
            score += 10
            if score > high_score:
                high_score = score
            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 20, "bold"))

        # Move segments
        for i in range(len(segments) - 1, 0, -1):
            segments[i].goto(segments[i - 1].pos())
        if segments:
            segments[0].goto(head.pos())

        move()

        # Self collision
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()
                score = 0
                delay = 0.1
                pen.clear()
                pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 20, "bold"))

        time.sleep(delay)

# Menu
menu = turtle.Turtle()
menu.hideturtle()
menu.color("white")
menu.penup()
menu.goto(0, 50)
menu.write("🐍 Realistic Snake with Chessboard 🐍", align="center", font=("Courier", 22, "bold"))
menu.goto(0, 10)
menu.write("Click anywhere to start", align="center", font=("Courier", 16, "normal"))

# Start game on click
def start_game(x, y):
    menu.clear()
    win.onscreenclick(button_click)
    win.listen()
    win.onkey(go_up, "Up")
    win.onkey(go_down, "Down")
    win.onkey(go_left, "Left")
    win.onkey(go_right, "Right")
    run_game()

win.onscreenclick(start_game)
win.mainloop()
