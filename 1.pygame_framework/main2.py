import pygame
import math
import sys

class Star:
    """五角星类，封装绘制逻辑"""
    def __init__(self, center, outer_radius=100, inner_radius=40, color=(255, 0, 0)):
        """
        初始化五角星
        :param center: 中心点坐标 (x, y)
        :param outer_radius: 外接圆半径
        :param inner_radius: 内接圆半径
        :param color: 颜色 (R, G, B)
        """
        self.center = center
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.color = color
        self.points = self._calculate_points()
    
    def _calculate_points(self):
        """计算五角星的10个顶点坐标"""
        points = []
        for i in range(10):
            angle = math.pi / 2 - i * 2 * math.pi / 10  # 从12点钟方向开始
            radius = self.outer_radius if i % 2 == 0 else self.inner_radius
            x = self.center[0] + radius * math.cos(angle)
            y = self.center[1] - radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def draw(self, surface):
        """在指定surface上绘制五角星"""
        pygame.draw.polygon(surface, self.color, self.points)
    
    def move(self, new_center):
        """移动五角星到新位置"""
        self.center = new_center
        self.points = self._calculate_points()
    
    def resize(self, new_outer_radius, new_inner_radius=None):
        """调整五角星大小"""
        self.outer_radius = new_outer_radius
        if new_inner_radius is not None:
            self.inner_radius = new_inner_radius
        self.points = self._calculate_points()

class Game:
    """游戏主控制类"""
    def __init__(self, width=800, height=600, title="五角星示例"):
        """初始化游戏窗口"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.bg_color = (255, 255, 255)
        
        # 创建五角星实例
        self.star = Star(
            center=(width // 2, height // 2),
            outer_radius=100,
            inner_radius=40,
            color=(255, 0, 0)
        )
    
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
        self.star.draw(self.screen)
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