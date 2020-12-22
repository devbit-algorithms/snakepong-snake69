import curses
from curses import textpad

def main(stdscr):
    curses.curs_set(0) # disable cursor blinking

    sh, sw = stdscr.getmaxyx()
    box = [[3,3],[sh-3,sw-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1]) # makes rectangle

    snake = [[sh//2, sw//2+1], [sh//2, sw//2-1], [sh//2, sw//2-1]] # initial body of snake -> ###
    direction = curses.KEY_RIGHT # goes to right
    
    for y,x in snake:
        stdscr.addstr(y, x, '#') # print initial snake in terminal

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

        stdscr.refresh()

curses.wrapper(main)