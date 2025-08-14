import pygame
import sys


# class Piano:
#     def __init__(self):
        

class Game:
    """游戏主控制类"""
    def __init__(self, width=400, height=300, title="music play"):
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