import turtle
import math
import random

SCORES_FILE = "scores.txt"  # File pang store sa scores
font_style = ("Courier New", 24, "normal")  # Font style
player = None

# Player name
def get_player_name():
    global player_name
    player_name = input("Enter Player Name: ")
    return player_name

# The SCORES section hahaha
def update_score(name, score):
    with open(SCORES_FILE, "a") as file:
        file.write(f"{name},{score}\n")

def get_scores():
    scores = []
    with open(SCORES_FILE, "r") as file:
        for line in file:
            name, score = line.strip().split(",")
            scores.append((name, int(score)))
    return scores

def display_scores():
    scores = get_scores()
    print("Scores:")
    for name, score in scores:
        print(f"{name}: {score}")

# Movement / Spawning sa enemies
def anchor(t1, t2):
    x1 = t1.xcor()
    y1 = t1.ycor()
    x2 = t2.xcor()
    y2 = t2.ycor()
    alien = math.atan2(y1 - y2, x1 - x2)
    alien = alien * 180.0 / 3.14159
    return alien

# Character Creation
def create_players():
    global player, missiles, enemies

    # Shapes for the player and enemies
    turtle.register_shape("GIFs/earth_guard.gif")
    turtle.register_shape("GIFs/garbage_monster.gif")
    turtle.register_shape("GIFs/plastic_monster.gif")
    turtle.register_shape("GIFs/smoke_monster.gif")

    # The player
    player = turtle.Turtle()
    player.shape("GIFs/earth_guard.gif")
    player.penup()
    player.score = 0
    player.goto(0, 0)

    # The missiles
    missiles = [] # Storing sa enemies | instances
    for _ in range(3):
        missile = player.clone()
        missile.penup()
        missile.shape("arrow")
        missile.color('red')
        missile.speed = 1
        missile.state = "ready"
        missile.hideturtle()
        missiles.append(missile)

    # The enemies || Pollutant Monsters
    enemies = []
    for _ in range(5):
        enemy = player.clone()
        enemy.penup()
        enemy.shape(random.choice(["GIFs/garbage_monster.gif", "GIFs/plastic_monster.gif", "GIFs/smoke_monster.gif"]))
        enemy.speed = random.randint(2, 3) / 50
        enemy.goto(0, 0)
        alien = random.randint(0, 260)
        distance = random.randint(300, 400)
        enemy.setheading(alien)
        enemy.fd(distance)
        enemy.setheading(anchor(player, enemy))
        enemies.append(enemy)

    return player, missiles, enemies, player.score

# Player Movement and defence
def left_side():
    player.lt(20)

def right_side():
    player.rt(20)

def fire_missile():
    for missile in missiles:
        if missile.state == "ready":
            missile.goto(0, 0)
            missile.showturtle()
            missile.setheading(player.heading())
            missile.state = "fire"
            break

# Instructions function - dapat mo balik sa main_menu
def instructions():
    global instruction_turtle
    menu.hideturtle()

    turtle.register_shape("GIFs/instruc.gif")
    instruction_turtle = turtle.Turtle()
    instruction_turtle.shape("GIFs/instruc.gif")
    window.update()

    def back_to_menu():
        instruction_turtle.clear()  # Clear the instructions
        instruction_turtle.hideturtle() # E hide kay magpakita gihapon sa play
        window.onkey(None, 'q')  # Unbind the 'q' key press event
        window.update()
        title_screen()  # Go back to the main menu

    window.onkey(back_to_menu, 'q')  # Bind 'q' to back_to_menu function

    return instruction_turtle

# Literal bye sa skreen
def bye():
    turtle.bye()

def play():
    global player
    status = False # For the checking of player hit
    
    pen = turtle.Turtle() # Score keeper on the top while game is on
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 250)
    pen.write("Score: 0", False, align="center", font=font_style)

    # Update screen
    menu.hideturtle()

    # Call create_players() to initialize the player turtle
    create_players()

    # win keyz
    window.listen()
    window.onkey(left_side, "Left")
    window.onkey(left_side, "a")

    window.onkey(right_side, "Right")
    window.onkey(right_side, "d")

    window.onkey(fire_missile, "space")

    # Game logik
    while True:
        window.update()

        for missile in missiles:
            if missile.state == "fire":
                missile.fd(missile.speed)
                if missile.xcor() > 300 or missile.xcor() < -300 or missile.ycor() > 300 or missile.ycor() < -300:
                    missile.hideturtle()
                    missile.state = "ready"
        for enemy in enemies:
            enemy.fd(enemy.speed)
            for missile in missiles:
                if enemy.distance(missile) < 20:
                    # Collision checking
                    alien = random.randint(0, 260)
                    distance = random.randint(600, 800)
                    enemy.setheading(alien)
                    enemy.fd(distance)
                    enemy.setheading(anchor(player, enemy))
                    enemy.speed += 0.01
                    missile.goto(600, 600)
                    missile.hideturtle()
                    missile.state = "ready"
                    player.score += 10
                    pen.clear()
                    pen.write("Score: {}".format(player.score), False, align="center", font=font_style)

                # I am hit
                if enemy.distance(player) < 20:
                    alien = random.randint(0, 260)
                    distance = random.randint(600, 800)
                    enemy.setheading(alien)
                    enemy.fd(distance)
                    enemy.setheading(anchor(player, enemy))
                    enemy.speed += 0.005
                    status = True

        # Display better luk
        if status:
            write_pen = pen.clone()

            write_pen.goto(0, 150)
            write_pen.penup()
            write_pen.write("Better Luck Next Time!", False, align="center", font=font_style)

            write_pen.goto(0,100)
            write_pen.write("Press [Q] to exit game.", False, align="center", font=font_style)

            write_pen.goto(0, 50)
            write_pen.write("Press [S] to view scores.", False, align="center", font=font_style)
            update_score(player_name, player.score)
            break



def title_screen():
    global window, menu
    turtle.register_shape("GIFs/main_menu.gif")

    window = turtle.Screen()  # Create a turtle screen
    window.title("Galactic Eco-Guardians!")
    window.bgpic("GIFs/space.gif")
    window.setup(width=600, height=600)
    window.cv._rootwindow.resizable(False, False) # For disabling sa resizing
    window.tracer(0)

    # For the menu
    menu = turtle.Turtle()
    menu.shape("GIFs/main_menu.gif")
    menu.up()
    menu.goto(0, 0)
    window.update()

    # For the diff parts sa menu
    window.listen()
    window.onkey(play, "p")
    window.onkey(display_scores, "s")
    window.onkey(instructions, "h")
    window.onkey(bye, "q")

    turtle.mainloop()  # to start

def main():
    # global player_name
    player_name = get_player_name()
    title_screen()  # Pang initialize sa menu

if __name__ == "__main__":
    main()
