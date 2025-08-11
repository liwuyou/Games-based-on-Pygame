import pygame
import math
import sys
import random

class Snake:
    def __init__(self):
        """初始化地图"""
        self.map_size = [80, 60] # 地图大小
        self.map = [[0 for _ in range(self.map_size[0])] for _ in range(self.map_size[1])] # 二维数组存储位置
        self.tile_size = 10 # 每个格子的大小
        self.map_color = (200, 200, 200)  # 地图颜色
        self.food_color = (255, 0, 0)  # 食物颜色
        

        # 初始化蛇的属性
        self.body_color = (0, 255, 0)  # 蛇身颜色
        self.head_color = (0, 200, 0)  # 蛇头颜色
        self.head_position = self.spawn_head()  # 蛇头位置
        self.body = [self.head_position]
        self.direction = (1, 0)  # 初始方向向右
        self.food_position = self.spawn_food()   # 生成食物

    def spawn_head(self):
        """生成蛇头位置,不允许在地图边界两行处"""
        while True:
            x = random.randint(1, self.map_size[0] - 2) 
            y = random.randint(1, self.map_size[1] - 2) 
            print(f"head_position: ({x}, {y})")
            return (x, y)

    def spawn_food(self):
        """生成不在蛇身上的食物位置"""
        while True:
            x = random.randint(0, self.map_size[0]-1)
            y = random.randint(0, self.map_size[1]-1)
            if (x,y) not in self.body:  # 确保位置不在蛇身上
                return (x,y)

    def move(self):
        # 移动蛇身
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def dead(self):
        """判断蛇是否死亡"""
        head_x, head_y = self.body[0]
        # 撞墙
        if head_x < 0 or head_x >= self.map_size[0] or head_y < 0 or head_y >= self.map_size[1]:
            return True
        # 撞自己
        if self.body[0] in self.body[2:]:
            # print(f"Snake position: {self.body}")
            return True
        return False




class Game:
    """游戏主控制类"""
    def __init__(self, width=800, height=600, title="贪吃蛇"):
        """初始化游戏窗口"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.bg_color = (255, 255, 255)

        # 初始化贪吃蛇
        self.snake = Snake()
        
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                # 处理方向键输入
                elif event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.direction = (0, -1)  # 上
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.direction = (0, 1)   # 下
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.direction = (-1, 0)  # 左
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.direction = (1, 0)   # 右
        return True

    
    def update(self):
        """更新游戏状态（此处可添加控制逻辑）"""
        # 检查蛇是否死亡
        if self.snake.dead():
            # 游戏结束处理
            # 屏幕显示game over，显示分数
            font = pygame.font.SysFont(None, 55)
            text = font.render(f"Game Over, score: {len(self.snake.body) - 1}", True, (255, 0, 0))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(1000)
            return

        # 移动蛇
        
        self.snake.move()
        if self.snake.body[0] == self.snake.food_position:
            self.snake.body.append(self.snake.body[-1])
            self.snake.food_position = self.snake.spawn_food()



    def render(self):
        """渲染游戏画面"""
        self.screen.fill(self.bg_color)        
        # 绘画snake和食物
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, self.snake.body_color, (segment[0] * self.snake.tile_size, segment[1] * self.snake.tile_size, self.snake.tile_size, self.snake.tile_size))
        pygame.draw.rect(self.screen, self.snake.food_color, (self.snake.food_position[0] * self.snake.tile_size, self.snake.food_position[1] * self.snake.tile_size, self.snake.tile_size, self.snake.tile_size), 2)
        print(f"Food position: {self.snake.food_position}")

        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(10)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":

    game = Game()
    game.run()