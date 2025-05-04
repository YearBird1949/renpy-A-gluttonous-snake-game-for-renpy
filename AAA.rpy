# 游戏参数设置
define CELL_SIZE = 30           
define GRID_WIDTH = 15           
define GRID_HEIGHT = 15           
define INITIAL_SPEED = 0.3       
define SNAKE_COLOR = "#00FF00"   
define HEAD_COLOR = "#FF0000"   
define FOOD_COLOR = "#FFFF00"     

init python:
    class SnakeGame:
        def __init__(self):
            self.reset_game()
        
        def reset_game(self):
            self.snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
            self.direction = (0, -1)  
            self.food = self.generate_food()
            self.game_over = False
            self.score = 0
            self.paused = False
        
        def generate_food(self):
            while True:
                x = renpy.random.randint(0, GRID_WIDTH-1)
                y = renpy.random.randint(0, GRID_HEIGHT-1)
                if (x, y) not in self.snake:
                    return (x, y)
        
        def update(self):
            if self.game_over or self.paused:
                return
            
            head_x = self.snake[0][0] + self.direction[0]
            head_y = self.snake[0][1] + self.direction[1]
            
            if (head_x < 0 or head_x >= GRID_WIDTH or
                head_y < 0 or head_y >= GRID_HEIGHT or
                (head_x, head_y) in self.snake):
                self.game_over = True
                return
            
            self.snake.insert(0, (head_x, head_y))
            
            if self.snake[0] == self.food:
                self.score += 1
                self.food = self.generate_food()
            else:
                self.snake.pop()
        
        def change_direction(self, new_dir):
            if (new_dir[0] + self.direction[0], new_dir[1] + self.direction[1]) != (0, 0):
                self.direction = new_dir

default snake_game = SnakeGame()

screen snake_game():
    tag game
    zorder 100
    
    frame:
        xalign 0.5
        yalign 0.3
        background "#404040"
        padding (10, 10)
        
        grid GRID_WIDTH GRID_HEIGHT:
            spacing 1
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    $ pos = (x, y)
                    if pos == snake_game.snake[0]:
                        add Solid(HEAD_COLOR, xsize=CELL_SIZE, ysize=CELL_SIZE)
                    elif pos in snake_game.snake:
                        add Solid(SNAKE_COLOR, xsize=CELL_SIZE, ysize=CELL_SIZE)
                    elif pos == snake_game.food:
                        add Solid(FOOD_COLOR, xsize=CELL_SIZE, ysize=CELL_SIZE)
                    else:
                        add Solid("#808080", xsize=CELL_SIZE, ysize=CELL_SIZE)
    
    vbox:
        xalign 0.5
        yalign 0.8
        spacing 10
        
        text "得分: [snake_game.score]" size 24 color "#FFFFFF"
        
        if snake_game.game_over:
            text "游戏结束！按R重新开始" size 24 color "#FF0000"
        elif snake_game.paused:
            text "游戏暂停" size 24 color "#FFFF00"
    
    if not snake_game.game_over and not snake_game.paused:
        timer INITIAL_SPEED repeat True action Function(snake_game.update)
    
    key "K_UP" action Function(snake_game.change_direction, (0, -1))
    key "K_DOWN" action Function(snake_game.change_direction, (0, 1))
    key "K_LEFT" action Function(snake_game.change_direction, (-1, 0))
    key "K_RIGHT" action Function(snake_game.change_direction, (1, 0))
    key "p" action ToggleDict(snake_game, "paused")
    key "r" action Function(snake_game.reset_game)

label start_snake_game:
    call screen snake_game
    return