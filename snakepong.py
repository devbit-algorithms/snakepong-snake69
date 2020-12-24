import curses
from curses import textpad
import elements
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
    if i % 2 == 1: # if paddle hits upper wall, paddle needs to go down
        paddle.insert(0, [paddle[0][0]+1,paddle[0][1]])
        stdscr.addstr(paddle[0][0], paddle[0][1], '|')
        stdscr.addstr(paddle[-1][0], paddle[-1][1], ' ')
        paddle.pop()

    if i % 2 == 0: # if paddle hits lower wall
        paddle.reverse() # need to reverse because paddle has to go up instead of down
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

def game_logic(stdscr):
    curses.curs_set(0) # disable cursor blinking
    stdscr.nodelay(1) # so that the app dont wait till the user presses a key -> getch() function is now non blocking
    stdscr.timeout(150) # 150 ms timeout, how long we wait till the user can press something

    sh, sw = stdscr.getmaxyx() # get max height and width of terminal screen
    box = [[3,3],[sh-3,sw/2-3]] # create a box to play the game in
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1]) # makes rectangle with values of box


    snake = [[sh//3, sw//3+1], [sh//3, sw//3], [sh//3, sw//3-1]] # initial body of snake -> ###
    direction = curses.KEY_RIGHT # goes to right

    for y,x in snake:
        stdscr.addstr(y, x, '#') # print initial snake in terminal
    
    paddle = [[8,4],[7,4],[6,4],[5,4],[4,4]]
    for y,x in paddle:
        stdscr.addstr(y, x, '|')

    ball = [[sh/2,5]]
    stdscr.addstr(ball[0][0], ball[0][1], '*')
    print_score(stdscr, elements.score)

    while 1:
        key = stdscr.getch() # get user keyboard input

        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            direction = key # if key is one of these, change it to that value

        head = snake[0] # head of snake is first element -> snake[0]

        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1] # if arrow key right is pressed, x axis will be incremented
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1] # if arrow key left is pressed, x axis will be decremented
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]] # if arrow key up is pressed, y axis will be decremented
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]] # if arrow key down is pressed, y axis will be incremented

        if (paddle[0][0] in [box[0][0]+1, box[1][0]-1] or
            paddle[-1][0] in [box[0][0]+1, box[0][0]+1]):
            elements.i += 1 # if paddle hits wall increment i with 1

        if ball[0][0] in [box[1][0]-1]: # if ball hits lower wall
            elements.prev_ball_hit = elements.ball_hit
            elements.ball_hit = "lower_wall"
        elif ball[0][0] in [box[0][0]+1]: # if ball hits upper wall
            elements.prev_ball_hit = elements.ball_hit
            elements.ball_hit = "upper_wall"
        elif ball[0][1] in [box[1][1]-1]: # if ball hits right wall
            elements.prev_ball_hit = elements.ball_hit
            elements.ball_hit = "right_wall"
        elif ball[0][1] in [box[0][1]+1]: # if ball hits left wall
            elements.prev_ball_hit = elements.ball_hit
            elements.ball_hit = "left_wall"

        j = 0

        while j < elements.ntail:
            if(ball[0][1] in [snake[j][1]-1] and
                ball[0][0] in [snake[j][0]]): # if ball hits left part of snake
                elements.prev_ball_hit = elements.ball_hit
                elements.ball_hit = "snakeleft"
            elif(ball[0][1] in [snake[j][1]+1] and
                ball[0][0] in [snake[j][0]]): # if ball hits right part of snake
                elements.prev_ball_hit = elements.ball_hit
                elements.ball_hit = "snakeright"
            j+=1

        j = 0
        while j < 4:
            if(ball[0][1] in [paddle[j][1]+1] and
                ball[0][0] in [paddle[j][0]]): # if ball hits paddle
                elements.prev_ball_hit = elements.ball_hit
                elements.ball_hit = "paddle"
            j+=1

        # moves ball inside the walls with an algoritm
        if elements.ball_hit == "paddle":
            elements.directionball = "right"
            if elements.prev_ball_hit == "upper_wall":
                ball.insert(0, [ball[0][0]+1, ball[0][1]+1])
            elif elements.prev_ball_hit == "lower_wall":
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
        elif elements.ball_hit == "lower_wall":
            if elements.directionball == "left":
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
        elif elements.ball_hit == "snakeleft":
            elements.directionball = "left"
            if elements.prev_ball_hit == "upper_wall":
                ball.insert(0, [ball[0][0]+1, ball[0][1]-1])
            elif elements.prev_ball_hit == "lower_wall":
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
        elif elements.ball_hit == "upper_wall":
            if elements.directionball == "left":
                ball.insert(0, [ball[0][0]+1, ball[0][1]-1])
            else:
                ball.insert(0, [ball[0][0]+1, ball[0][1]+1])
        elif elements.ball_hit == "right_wall":
            elements.directionball = "left"
            if elements.prev_ball_hit == "lower_wall":
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
            elif elements.prev_ball_hit == "upper_wall":
                ball.insert(0, [ball[0][0]+1, ball[0][1]-1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
        elif elements.ball_hit == "snakeright":
            elements.directionball = "left"
            if elements.prev_ball_hit == "upper_wall":
                ball.insert(0, [ball[0][0]+1, ball[0][1]+1])
            elif elements.prev_ball_hit == "lower_wall":
                ball.insert(0, [ball[0][0]-1, ball[0][1]+1])
            else:
                ball.insert(0, [ball[0][0]-1, ball[0][1]-1])
        elif elements.ball_hit == "left_wall":
            elements.directionball = "right"
            ball.insert(0, [ball[0][0], ball[0][1]+2])
            elements.score += 1
            elements.ntail += 1
        
        # prints snake, paddle and ball in terminal
        print_terminal(stdscr, elements.score, snake, new_head, elements.ball_hit, ball, paddle, elements.i)

        if(elements.ball_hit == "left_wall"):
            elements.ball_hit = "paddle"
            
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

curses.wrapper(game_logic)


def main(stdscr):
    game_logic(stdscr)
