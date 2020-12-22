import curses
from curses import textpad

def print_score(stdscr, score):
    sh, sw = stdscr.getmaxyx()
    score_text = "Score: {}".format(score)
    stdscr.addstr(0, sw//4 - len(score_text)//4, score_text)
    stdscr.refresh()

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
    
    paddle = [[10,4],[9,4],[8,4],[7,4],[6,4],[5,4],[4,4]]
    for y,x in paddle:
        stdscr.addstr(y, x, '|')

    score = 0
    print_score(stdscr, score)
    i = 0

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

        snake.insert(0, new_head)
        stdscr.addstr(new_head[0], new_head[1], '#') # snake would move but will add body -> ####

        stdscr.addstr(snake[-1][0], snake[-1][1], ' ') # removes snake last body so original body still remains -> ###
        snake.pop() # removes last element of array

        if (paddle[0][0] in [box[0][0]+1, box[1][0]-1] or
            paddle[-1][0] in [box[0][0]+1, box[0][0]+1]):
            i += 1
        
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


        if (snake[0][0] in [box[0][0], box[1][0]] or
            snake[0][1] in [box[0][1], box[1][1]] or
            snake[0] in snake[1:]): # if snake hits wall or his tail
            msg= "Game Over!"
            stdscr.addstr(sh//2, sw//4 - len(msg)//4, msg) # print message in center of screen
            stdscr.nodelay(0) # makes getch blocking again, so the user has to press a key to exit game
            stdscr.getch()
            break

        





        stdscr.refresh()

curses.wrapper(main)