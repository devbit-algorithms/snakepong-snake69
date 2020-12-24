import elements

def test_score():
    assert elements.score == 0
    elements.score += 2
    assert elements.score == 2
    elements.score -= 1
    assert elements.score == 1

def test_tail():
    assert elements.ntail == 2 # because the snake starts initial with a width of 3, so ntail = 2 -> 0 1 2 

def test_ball_hit():
    snake = [[5,7],[5,6],[5,5]]
    right_wall = []
    i = 0
    hits_wall = False
    while i < 10:
        right_wall.insert(0,[i,7]) # right wall on x axes 7 with a length of 10
        i += 1
    
    if(snake[0] in right_wall[1:]):
        hits_wall = True

    assert hits_wall

def test_tail_hit():
    elements.ntail = 10 # a snake with an tail of 10 width
    i = 0
    snake = []
    hits_snake = False
    while i < elements.ntail:
        snake.insert(0,[10,i])
        i += 1
    
    snake.insert(0,[snake[0][0]-1,snake[0][1]]) # head of snake goes 1 tile up
    snake.pop(-1) # removes last tail of snake because there is a new head
    snake.insert(0,[snake[0][0],snake[0][1]-1]) # head of snake goes 1 tile to the left 
    snake.pop(-1)
    if(snake[0] in snake[1:]):
        hits_snake = True
    assert hits_snake is not True

    snake.insert(0,[snake[0][0]+1, snake[0][1]]) # head of snake goes 1 tile down
    snake.pop(-1)
    if(snake[0] in snake[1:]):
        hits_snake = True
    assert hits_snake
