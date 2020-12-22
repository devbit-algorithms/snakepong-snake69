import curses
from curses import textpad

def print_score(stdscr, score):
    sh, sw = stdscr.getmaxyx()
    score_text = "Score: {}".format(score)
    stdscr.addstr(0, sw//2 - len(score_text)//2, score_text)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0) # disable cursor blinking
    stdscr.nodelay(1) # so that the app dont wait till the user presses a key -> getch() function is now non blocking
    stdscr.timeout(150) # 150 ms timeout, how long we wait till the user can press something

    sh, sw = stdscr.getmaxyx()
    box = [[3,3],[sh-3,sw-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1]) # makes rectangle

    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]] # initial body of snake -> ###
    direction = curses.KEY_RIGHT # goes to right
    
    for y,x in snake:
        stdscr.addstr(y, x, '#') # print initial snake in terminal

    score = 0
    print_score(stdscr, score)

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

        if (snake[0][0] in [box[0][0], box[1][0]] or
            snake[0][1] in [box[0][1], box[1][1]] or
            snake[0] in snake[1:]): # if snake hits wall or his tail
            msg= "Game Over!"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg) # print message in center of screen
            stdscr.nodelay(0) # makes getch blocking again, so the user has to press a key to exit game
            stdscr.getch()
            break

        stdscr.refresh()

curses.wrapper(main)