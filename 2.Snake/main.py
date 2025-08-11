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
        self.food_position = self.spawn_food()

        # 初始化蛇的属性
        self.body_color = (0, 255, 0)  # 蛇身颜色
        self.head_color = (0, 200, 0)  # 蛇头颜色
        self.head_position = self.spawn_head()  # 蛇头位置
        self.body = [self.head_position]
        self.direction = (1, 0)  # 初始方向向右


    def spawn_head(self):
        """生成蛇头位置,不允许在地图边界两行处"""
        while True:
            x = random.randint(1, self.map_size[0] - 2) 
            y = random.randint(1, self.map_size[1] - 2) 
            return (x, y)

    def spawn_food(self):
        """生成食物，读取map如果位置为0则生成食物"""
        while True:
            x = random.randint(0, self.map_size[0] - 1) 
            y = random.randint(0, self.map_size[1] - 1) 
            return (x, y)
        
        
    def move(self):
        # 移动蛇身
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    




class Game:
    """游戏主控制类"""
    def __init__(self, width=800, height=600, title="贪吃蛇"):
        """初始化游戏窗口"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.bg_color = (255, 255, 255)
    
    def handle_events(self):
        """处理系统事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        """更新游戏状态（此处可添加动画逻辑）"""
        
        pass
    
    def render(self):
        """渲染游戏画面"""
        self.screen.fill(self.bg_color)
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":

    game = Game()
    game.run()