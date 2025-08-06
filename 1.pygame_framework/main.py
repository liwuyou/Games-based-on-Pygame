import pygame
import math

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("红色五角星")

# 五角星的属性
star_color = (255, 0, 0)  # 红色 (RGB)
star_center = (screen_width // 2, screen_height // 2)  # 屏幕中心
outer_radius = 100  # 外接圆半径
inner_radius = 40   # 内接圆半径

# 计算五角星的顶点坐标
def calculate_star_points(center, outer_radius, inner_radius):
    points = []
    for i in range(10):  # 五角星有 10 个顶点（5 外 + 5 内）
        angle = math.pi / 2 - i * 2 * math.pi / 10  # 从 12 点钟方向开始
        if i % 2 == 0:
            # 外顶点
            x = center[0] + outer_radius * math.cos(angle)
            y = center[1] - outer_radius * math.sin(angle)
        else:
            # 内顶点
            x = center[0] + inner_radius * math.cos(angle)
            y = center[1] - inner_radius * math.sin(angle)
        points.append((x, y))
    return points

# 计算五角星顶点
star_points = calculate_star_points(star_center, outer_radius, inner_radius)

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 填充背景色（白色）
    screen.fill((255, 255, 255))
    
    # 绘制五角星
    pygame.draw.polygon(screen, star_color, star_points)
    
    # 更新屏幕显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()