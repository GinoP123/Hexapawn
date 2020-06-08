import turtle
import time
import random

'''Initializes variables'''
screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.register_shape("blackPawn.gif")
screen.register_shape("whitePawn.gif")
screen.register_shape("board.gif")
screen.bgpic("board.gif")

turtle.hideturtle()
turtle.penup()
turtle.speed(0)

point = []
turtle.goto(300, 300)
point.append(turtle.pos())

counter = 0

for r in range(0, 3, 1):
    for c in range(0, 3, 1):
        counter += 1
        xcor = -170 + (170 * c)
        ycor = 170 - (170 * r)
        turtle.goto(xcor, ycor)
        p = turtle.pos()
        point.append(p)
        turtle.goto((xcor - 50), (ycor + 30))
        turtle.write(counter, move=False, align="left", font=("Arial", 40, "bold"))

'''Asks for color'''
color = turtle.textinput("BoW?", "b or w?")

'''defines 6 pawns'''
p = [0]
c = [0]
playerpos = [0]
cpupos = [0]

for num in range(1, 4, 1):

    '''Inializes the player and cpu objects'''

    newp = turtle.Turtle()
    p.append(newp)
    p[num].penup()
    p[num].hideturtle()
    p[num].speed(0)
    p[num].goto(point[(6 + num)])
    p[num].speed(1)

    playerpos.append((point[(6 + num)]))

    newc = turtle.Turtle()
    c.append(newc)
    c[num].penup()
    c[num].hideturtle()
    c[num].speed(0)
    c[num].goto(point[num])
    c[num].speed(1)

    cpupos.append(point[num])

    '''Defines the colors'''
    if color == "b":
        p[num].shape("blackPawn.gif")
        c[num].shape("whitePawn.gif")

        p[num].showturtle()
        c[num].showturtle()
    else:
        p[num].shape("whitePawn.gif")
        c[num].shape("blackPawn.gif")

        p[num].showturtle()
        c[num].showturtle()


def updatePos():  # Updates the position of the pieces
    for pp in range(1, 4, 1):
        playerpos[pp] = p[pp].pos()
        cpupos[pp] = c[pp].pos()


def straight(f, t, poc):  # Checks to see if the move is straight or not
    tof = False

    for fNum in range(1, 10, 1):
        if poc == "player" and f == fNum and t == (f - 3):
            tof = True
        elif poc == "cpu" and f == fNum and t == (f + 3):
            tof = True

    return tof


def check(f, t, poc):  # Checks if a potential move is valid

    # Converts the points number into turtle coordinates
    fpos = point[f]
    tpos = point[t]

    updatePos()  # updates the position

    fval = False
    tval = True
    attacking = False
    attackpiece = -1
    pnum = 0

    sb = straight(f, t, poc)  # Checks if the move is straight
    if not sb:
        tval = sb

    if poc == "player":  # Checks if the player move is from a player piece
        for n in range(1, 4, 1):
            if fpos == playerpos[n]:
                pnum = n
                fval = True
    if poc == "cpu":  # Checks if the cpu move is from a cpu piece
        for n in range(1, 4, 1):
            if fpos == cpupos[n]:
                pnum = n
                fval = True

    for n in range(1, 4, 1):
        if poc == "player":  # Checks if the player is moving toward another piece
            if tpos == playerpos[n]:
                tval = False
            elif tpos == cpupos[n]:
                attacking = True
                attackpiece = n
                tval = attackCheck(poc, f, t)  # Checks whether the attack is valid
        elif poc == "cpu":  # Checks if the cpu is moving toward another piece
            if tpos == cpupos[n]:
                tval = False
            elif tpos == playerpos[n]:
                attacking = True
                attackpiece = n
                tval = attackCheck(poc, f, t)  # Checks whether the attack is valid

    # Returns values
    if not fval or not tval:
        return False, pnum, attacking, attackpiece

    else:
        return True, pnum, attacking, attackpiece


def attackCheck(poc, f, t):  # Checks whether an attack is valid
    up = [0]
    dp = [0]

    tof = False

    for u in range(4, 12, 1):  # Creates a list of acceptable moves

        ooe = u % 2

        if u > 5:
            u -= 1
            if u > 8:
                u -= 1

        up.append(u)

        if ooe == 0:
            dp.append((u - 2))
        else:
            dp.append((u - 4))

    for c in range(1, 9, 1):  # Checks if the move is in the list
        if poc == "player" and f == up[c] and t == dp[c]:
            tof = True
        elif poc == "cpu" and f == dp[c] and t == up[c]:
            tof = True

    return tof  # Returns Values


def goto(f, t, poc):  # Checks potential coordinates and moves the piece there
    val, pnum, attacking, attackpiece = check(f, t, poc)  # Checks if the move is valid
    tpos = point[t]
    if val:  # Hides the attacked piece if attacking and moves the piece to the coordinates
        if poc == "player":
            if attacking:
                c[attackpiece].hideturtle()
                c[attackpiece].goto(point[0])
            p[pnum].goto(tpos)
        elif poc == "cpu":
            if attacking:
                p[attackpiece].hideturtle()
                p[attackpiece].goto(point[0])
            c[pnum].goto(tpos)
        return True
    else:
        print("Move not possible")
        return False


def playerMove():  # Asks for player input until the player enters a valid coordinate
    valmov = False

    while not valmov:
        movefrom = int(turtle.numinput("From where?", "From where?", default=None, minval=1, maxval=9))
        moveto = int(turtle.numinput("To where?", "To where?", default=None, minval=1, maxval=9))

        valmov = goto(movefrom, moveto, "player")


def cpuMove():  # Generates a list of potential valid moves and randomly selects a move
    posmovef = []
    posmovet = []

    for fR in range(1, 10, 1):
        for tR in range(1, 10, 1):
            testGoto, u, q, r = check(fR, tR, "cpu")  # Checks whether the move is valid
            if testGoto:
                posmovef.append(fR)
                posmovet.append(tR)
                print(fR, tR)
    numPos = len(posmovef)

    randomMovement = random.randint(0, (numPos - 1))  # Selects a random element

    goto(posmovef[randomMovement], posmovet[randomMovement], "cpu")  # moves the cpu piece to the coordinates


def gameover(poc):  # Checks whether the game is over
    tof = True

    updatePos()

    for fR in range(1, 10, 1):  # If there is a potential move by the player or computer, the game is not over
        for tR in range(1, 10, 1):
            testGoto, u, q, r = check(fR, tR, poc)

            if testGoto:
                tof = False

    for num in range(1, 4, 1):  # Checks whether the player or cpu has reached the last row
        if playerpos[num] == point[1] or playerpos[num] == point[2] or playerpos[num] == point[3] or \
                cpupos[num] == point[7] or cpupos[num] == point[8] or cpupos[num] == point[9]:
            tof = True

    return tof


def gameFlow():  # Flow of the game
    gover = False
    moveNum = 0
    winner = " "

    while not gover:  # Loops the process until its game over

        moveNum += 1

        playerMove()  # Moves the player piece

        gover = gameover("cpu")
        if gover:
            winner = "Player"
            break

        if not gover:
            cpuMove()  # Moves the cpu piece

        gover = gameover("player")
        if gover:
            winner = "Cpu"

    turtle.goto(300, 280)
    turtle.write((winner + " wins!"), move=False, align="left", font=("Arial", 40, "bold"))

    turtle.goto(-300, 280)
    turtle.write("Game Over!", move=False, align="left", font=("Arial", 40, "bold"))
    print(winner)
    time.sleep(10)


gameFlow()  # Runs the game
