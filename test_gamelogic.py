import elements

def test_score():
    assert elements.score == 0
    elements.score += 2
    assert elements.score == 2
    elements.score -= 1
    assert elements.score == 1

def test_tail():
    assert elements.ntail == 2 # because the snake starts initial with a width of 3, so ntail = 2 -> 0 1 2 

def test_wall_hit():
    snake = [[5,7],[5,6],[5,5]] # create a snake horizontal with 3 elements
    right_wall = []
    snake_hit = ""
    i = 0
    while i < 10:
        right_wall.insert(0,[i,7]) # right wall on x axes 7 with a length of 10
        i += 1
    
    if(snake[0] in right_wall[1:]): # if head of snake hits right_wall
        snake_hit = "right_wall"

    assert snake_hit == "right_wall"

def test_ball_hit():
    ball = [[5,5]] # create a ball
    right_wall = []
    elements.ball_hit = ""
    i = 0
    while i < 10:
        right_wall.insert(0,[i,8]) # right wall on x axes 8 with a length of 10
        i += 1
    ball.insert(0,[5,6])
    ball.pop(-1)
    if(ball[0] in right_wall[1:]):
        elements.ball_hit == "right_wall"

    assert elements.ball_hit == ""

    ball.insert(0,[5,7])
    ball.pop(-1)
    ball.insert(0,[5,8])
    ball.pop(-1)
    if(ball[0] in right_wall[1:]):
        elements.ball_hit = "right_wall"

    assert elements.ball_hit == "right_wall"
    
def test_tail_hit():
    elements.ntail = 10 # a snake with an tail of 10 width
    i = 0
    snake = []
    hits_snake = False
    while i < elements.ntail:
        snake.insert(0,[10,i]) # create snake with 10 elements
        i += 1
    
    snake.insert(0,[snake[0][0]-1,snake[0][1]]) # head of snake goes 1 tile up
    snake.pop(-1) # removes last tail of snake because there is a new head
    snake.insert(0,[snake[0][0],snake[0][1]-1]) # head of snake goes 1 tile to the left 
    snake.pop(-1)
    if(snake[0] in snake[1:]): # if head of snake hits own tail
        hits_snake = True
    assert hits_snake is not True

    snake.insert(0,[snake[0][0]+1, snake[0][1]]) # head of snake goes 1 tile down
    snake.pop(-1)
    if(snake[0] in snake[1:]): # if head of snake hits own tail
        hits_snake = True
    assert hits_snake

def test_direction_ball():
    elements.ntail = 10 # a snake with an tail of 10 width
    i = 0
    snake = []
    ball = [[5,0]] # ball is at the begin on y axis 5
    hits_snake = False
    while i < elements.ntail:
        snake.insert(0,[i,5]) # makes a snake that is vertical with a length of 10 on x axis 5
        i += 1

    if(ball[0][0] in snake[1:][0] and
        ball[0][1]+1 in snake[1:][1]): # if ball hits the snake, we do +1 on the ball because the ball doesnt go in the snake but bounces against it
        elements.directionball = "left" # if the ball hits snake -> direction of ball has to go left

    assert elements.directionball == "right" # the ball hasn't moved yet so this stays right
    i = 1
    while i < 5:
        ball.insert(0,[5,i]) # moves the ball to the right, straight through x axis
        ball.pop(-1)
        i += 1
        if(ball[0][0] in snake[1:][0] and
            ball[0][1]+1 in snake[1:][1]): # if ball hits the snake, we do +1 on the ball because the ball doesnt go in the snake but bounces against it
            elements.directionball = "left"

    assert elements.directionball == "left"

def test_prev_ball_hit():
    ball = [[5,5]] # create a ball
    right_wall = []
    upper_wall = []
    i = 0
    while i < 10:
        right_wall.insert(0,[i,8]) # right wall on x axes 8 with a length of 10
        upper_wall.insert(0,[0,i]) # upper wall on x axes 0 with a length of 10
        i += 1
    ball.insert(0,[5,6])
    ball.pop(-1)

    if(ball[0] in right_wall[1:]):
        elements.ball_hit == "right_wall"
    elif(ball[0] in upper_wall[1:]):
        elements.ball_hit == "upper_wall"
    else:
        elements.ball_hit = ""

    assert elements.ball_hit == ""

    ball.insert(0,[5,7])
    ball.pop(-1)
    ball.insert(0,[5,8])
    ball.pop(-1)
    if(ball[0] in right_wall[1:]):
        elements.ball_hit = "right_wall"

    assert elements.ball_hit == "right_wall"

    ball.insert(0,[1,6]) # ball goes up so it doesnt hit the right or upper wall
    ball.pop(-1)
    ball.insert(0,[0,6]) # ball goes against upper wall
    ball.pop(-1)
    if(ball[0] in right_wall[1:]):
        elements.ball_hit == "right_wall"
    elif(ball[0] in upper_wall[1:]):
        elements.prev_ball_hit = "right_wall"
        elements.ball_hit = "upper_wall"
    else:
        elements.ball_hit = ""

    assert elements.prev_ball_hit == "right_wall"
    assert elements.ball_hit == "upper_wall"
