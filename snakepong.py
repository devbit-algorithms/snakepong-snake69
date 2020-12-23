import curses
from curses import textpad

def print_score(stdscr, score):
    sh, sw = stdscr.getmaxyx()
    score_text = "Score: {}".format(score)
    stdscr.addstr(0, sw//4 - len(score_text)//4, score_text)
    stdscr.refresh()

def print_snake(stdscr, snake, new_head, ball_hit):
    snake.insert(0, new_head)
    stdscr.addstr(new_head[0], new_head[1], '#') # snake would move but will add body -> ####
    if ball_hit != "left_wall":
        stdscr.addstr(snake[-1][0], snake[-1][1], ' ') # removes snake last body so original body still remains -> ###
        snake.pop() # removes last element of array

def print_ball(stdscr, ball):
    stdscr.addstr(ball[0][0], ball[0][1], '*')
    stdscr.addstr(ball[-1][0], ball[-1][1], ' ')
    ball.pop()

def print_paddle(stdscr, paddle, i):
    if i % 2 == 1:
        paddle.insert(0, [paddle[0][0]+1,paddle[0][1]])
        stdscr.addstr(paddle[0][0], paddle[0][1], '|')
        stdscr.addstr(paddle[-1][0], paddle[-1][1], ' ')
        paddle.pop()

    if i % 2 == 0:
        paddle.reverse()
        paddle.insert(0, [paddle[0][0]-1,paddle[0][1]])
        stdscr.addstr(paddle[0][0], paddle[0][1], '|')
        stdscr.addstr(paddle[-1][0], paddle[-1][1], ' ')
        paddle.pop()
        paddle.reverse()

def print_terminal(stdscr, score, snake, new_head, ball_hit, ball, paddle, i):
    print_score(stdscr, score)
    print_ball(stdscr, ball)
    print_snake(stdscr, snake, new_head, ball_hit)
    print_paddle(stdscr, paddle, i)

def main(stdscr):
    curses.curs_set(0) # disable cursor blinking
    stdscr.nodelay(1) # so that the app dont wait till the user presses a key -> getch() function is now non blocking
    stdscr.timeout(150) # 150 ms timeout, how long we wait till the user can press something

    sh, sw = stdscr.getmaxyx()
    box = [[3,3],[sh-3,sw/2-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1]) # makes rectangle

    snake = [[sh//4, sw//4+1], [sh//4, sw//4], [sh//4, sw//4-1]] # initial body of snake -> ###
    direction = curses.KEY_RIGHT # goes to right

    for y,x in snake:
        stdscr.addstr(y, x, '#') # print initial snake in terminal
    
    paddle = [[8,4],[7,4],[6,4],[5,4],[4,4]]
    for y,x in paddle:
        stdscr.addstr(y, x, '|')

    ball = [[sh/2,5]]
    stdscr.addstr(ball[0][0], ball[0][1], '*')

    score = 0
    print_score(stdscr, score)
    i = 0
    ball_hit = "paddle"
    prev_ball_hit = ""
    directionball = "right"
    ntail = 2
    while 1:
        key = stdscr.getch() # get user keyboard input

        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            direction = key # if key is one of these, change it to that value

        head = snake[0]

        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]

        if (paddle[0][0] in [box[0][0]+1, box[1][0]-1] or
            paddle[-1][0] in [box[0][0]+1, box[0][0]+1]):
            i += 1    

        if ball[0][0] in [box[1][0]-1]:
            prev_ball_hit = ball_hit
            ball_hit = "lower_wall"
        elif ball[0][0] in [box[0][0]+1]:
            prev_ball_hit = ball_hit
            ball_hit = "upper_wall"
        elif ball[0][1] in [box[1][1]-1]:
            prev_ball_hit = ball_hit
            ball_hit = "right_wall"
        elif ball[0][1] in [box[0][1]+1]:
            prev_ball_hit = ball_hit
            ball_hit = "left_wall"

        j = 0

        while j < ntail:
            if(ball[0][1] in [snake[j][1]-1] and
                ball[0][0] in [snake[j][0]]):
                prev_ball_hit = ball_hit
                ball_hit = "snakeleft"
            elif(ball[0][1] in [snake[j][1]+1] and
                ball[0][0] in [snake[j][0]]):
                prev_ball_hit = ball_hit
                ball_hit = "snakeright"
            j+=1

        j = 0
        while j < 4:
            if(ball[0][1] in [paddle[j][1]+1] and
                ball[0][0] in [paddle[j][0]]):
                prev_ball_hit = ball_hit
                ball_hit = "paddle"
            j+=1

        if ball_hit == "paddle":
            directionball = "right"
            if prev_ball_hit == "upper_wall":
                ball.insert(0, [ball[0][0]+1, ball[0][1]+1])
            elif prev_ball_hit == "lower_wall":
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
        elif ball_hit == "lower_wall":
            if directionball == "left":
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
        elif ball_hit == "snakeleft":
            directionball = "left"
            if prev_ball_hit == "upper_wall":
                ball.insert(0, [ball[0][0]+1, ball[0][1]-1])
            elif prev_ball_hit == "lower_wall":
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
        elif ball_hit == "upper_wall":
            if directionball == "left":
                ball.insert(0, [ball[0][0]+1, ball[0][1]-1])
            else:
                ball.insert(0, [ball[0][0]+1, ball[0][1]+1])
        elif ball_hit == "right_wall":
            directionball = "left"
            if prev_ball_hit == "lower_wall":
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
            elif prev_ball_hit == "upper_wall":
                ball.insert(0, [ball[0][0]+1, ball[0][1]-1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
        elif ball_hit == "snakeright":
            directionball = "left"
            if prev_ball_hit == "upper_wall":
                ball.insert(0, [ball[0][0]+1, ball[0][1]+1])
            elif prev_ball_hit == "lower_wall":
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
        elif ball_hit == "left_wall":
            directionball = "right"
            ball.insert(0, [ball[0][0], ball[0][1]+2])
            score += 1
            ntail += 1
            
        print_terminal(stdscr, score, snake, new_head, ball_hit, ball, paddle, i)

        if(ball_hit == "left_wall"):
            ball_hit = "paddle"
            

        if (snake[0][0] in [box[0][0], box[1][0]] or
            snake[0][1] in [box[0][1], box[1][1]] or
            snake[0] in snake[1:] or # if snake hits wall or his tail
            snake[0] in paddle[1:]): # if snake hits paddle
            msg= "Game Over!"
            stdscr.addstr(sh//2, sw//4 - len(msg)//4, msg) # print message in center of screen
            stdscr.nodelay(0) # makes getch blocking again, so the user has to press a key to exit game
            stdscr.getch()
            break

        stdscr.refresh()

curses.wrapper(main)