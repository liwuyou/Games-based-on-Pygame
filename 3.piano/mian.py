import pygame
import sys
import os
import threading
from my_play import PianoMusic, PianoPlayer

class Game:
    """游戏主控制类"""
    def __init__(self, width=600, height=400, title="钢琴播放器"):
        """初始化游戏窗口"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.bg_color = (240, 240, 240)
        self.font = pygame.font.SysFont('simhei', 24)
        self.title_font = pygame.font.SysFont('simhei', 32, bold=True)
        
        # 音乐控制
        self.player = PianoPlayer()
        self.music = PianoMusic()
        self.songs = self.load_songs()
        self.current_song = 0
        self.is_playing = False
        
        # 按钮定义
        button_w, button_h = 100, 40
        self.play_btn = pygame.Rect(250, 300, button_w, button_h)
        self.prev_btn = pygame.Rect(130, 300, button_w, button_h)
        self.next_btn = pygame.Rect(370, 300, button_w, button_h)
        
    def load_songs(self):
        """加载yaml目录下的所有乐谱"""
        song_dir = os.path.join(os.path.dirname(__file__), 'yaml')
        return [f for f in os.listdir(song_dir) if f.endswith('.yaml')]
    
    def play_current(self):
        """播放当前选中乐曲"""
        if not self.songs:
            return False
        song_path = os.path.join(os.path.dirname(__file__), 'yaml', self.songs[self.current_song])
        if self.music.load_sheet_music(song_path):
            play_thread = threading.Thread(target=self.music.play, args=(self.player,))
            play_thread.daemon = True
            play_thread.start()
            return True
        return False
    
    def handle_events(self):
        """处理系统事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_btn.collidepoint(event.pos):
                    self.is_playing = not self.is_playing
                    if self.is_playing:
                        if not self.play_current():
                            self.is_playing = False
                elif self.prev_btn.collidepoint(event.pos):
                    self.current_song = max(0, self.current_song-1)
                elif self.next_btn.collidepoint(event.pos):
                    self.current_song = min(len(self.songs)-1, self.current_song+1)
        return True
    
    def update(self):
        """更新游戏状态"""
        pass
    
    def render(self):
        """渲染游戏画面"""
        self.screen.fill(self.bg_color)
        
        # 显示当前歌曲信息
        if self.songs and hasattr(self.music, 'sheet_music') and self.music.sheet_music:
            song_info = self.music.sheet_music
            title = self.title_font.render(f"当前播放: {song_info.get('title', '未知')}", True, (0, 0, 0))
            self.screen.blit(title, (50, 50))
        else:
            title = self.title_font.render("请选择歌曲", True, (0, 0, 0))
            self.screen.blit(title, (50, 50))
            
        # 显示歌曲列表
        if self.songs:
            for i, song in enumerate(self.songs):
                color = (0, 100, 200) if i == self.current_song else (0, 0, 0)
                text = self.font.render(f"{i+1}. {song.replace('.yaml', '')}", True, color)
                self.screen.blit(text, (50, 100 + i*30))
        
        # 绘制按钮
        pygame.draw.rect(self.screen, (0, 200, 0), self.play_btn)
        pygame.draw.rect(self.screen, (200, 0, 0), self.prev_btn)
        pygame.draw.rect(self.screen, (200, 0, 0), self.next_btn)
        
        # 按钮文字
        play_text = self.font.render("播放" if not self.is_playing else "暂停", True, (255, 255, 255))
        prev_text = self.font.render("上一首", True, (255, 255, 255))
        next_text = self.font.render("下一首", True, (255, 255, 255))
        
        self.screen.blit(play_text, (self.play_btn.x+30, self.play_btn.y+10))
        self.screen.blit(prev_text, (self.prev_btn.x+20, self.prev_btn.y+10))
        self.screen.blit(next_text, (self.next_btn.x+20, self.next_btn.y+10))
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        self.player.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
