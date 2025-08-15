import numpy as np
import pyaudio
import yaml
import time


class PianoPlayer:
    def __init__(self, SAMPLE_RATE=44100):
        self.SAMPLE_RATE = SAMPLE_RATE  # 采样率（Hz）
        self.FADE_DURATION = 0.02  # 20ms淡入淡出
        self.p = pyaudio.PyAudio()

        # 打开音频流
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.SAMPLE_RATE,
            output=True
        )

    def apply_fade(self, wave):
        fade_samples = int(self.FADE_DURATION * self.SAMPLE_RATE)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        wave[:fade_samples] *= fade_in
        wave[-fade_samples:] *= fade_out
        return wave

    def generate_sine_wave(self, freq, duration, sample_rate):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(2 * np.pi * freq * t) * 0.3  # 降低音量
        return self.apply_fade(wave)  # 应用淡入淡出

    def play_tone(self, frequency, duration):
        sine_wave = self.generate_sine_wave(frequency, duration, self.SAMPLE_RATE)
        self.stream.write(sine_wave.astype(np.float32).tobytes())
    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class PianoMusic:
    # 音符频率映射 (以A4=440Hz为基准)
    NOTE_FREQS = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
        'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
        'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88,
        'bB': 466.16, 'bA': 415.30, 'bG': 392.00, 'bE': 311.13
    }
    
    def get_note_freq(self, note_name):
        """根据音符名称获取频率，处理八度变化"""
        base_note = note_name.rstrip(",'")  # 移除所有八度标记
        octave_shift = note_name.count("'") - note_name.count(",")
        
        # 获取基准频率
        freq = self.NOTE_FREQS.get(base_note, 440.0)  # 默认A4
        
        # 应用八度变化 (每八度频率翻倍/减半)
        return freq * (2 ** octave_shift)

    def __init__(self):
        self.sheet_music = None
        self.parsed_notes = []

    def load_sheet_music(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.sheet_music = yaml.safe_load(file)
            return self.sheet_music
        except Exception as e:
            print(f"读取乐谱失败: {e}")
            return None

    def parse_sheet_music(self):
        """解析乐谱为可播放的音符序列"""
        if not self.sheet_music:
            return False
            
        tempo = self.sheet_music.get('tempo', 100)
        base_duration = 60 / tempo  # 四分音符的秒数
        
        sections = self.sheet_music.get('sections', '').split('|')
        for section in sections:
            notes = section.strip().split()
            for note in notes:
                if note == '-':  # 延音
                    self.parsed_notes.append(('rest', 0, base_duration))
                elif note.startswith('0'):  # 处理0/或0//等休止符
                    duration = base_duration
                    if '/' in note:  # 八分休止符
                        duration = base_duration / 2
                    if '//' in note:  # 十六分休止符
                        duration = base_duration / 4
                    if '.' in note:  # 附点休止符
                        duration *= 1.5
                    self.parsed_notes.append(('rest', 0, duration))
                else:
                    # 解析音符和时值
                    note_name = ''.join([c for c in note if c.isalpha() or c in (',', "'")])
                    duration = base_duration
                    
                    if '/' in note:  # 八分音符
                        duration = base_duration / 2
                    if '//' in note:  # 十六分音符
                        duration = base_duration / 4
                    if '.' in note:  # 附点音符
                        duration *= 1.5
                    
                    freq = self.get_note_freq(note_name)  # 处理八度变化
                    self.parsed_notes.append(('note', freq, duration))
        return True

    def play(self, piano_player):
        """使用PianoPlayer播放解析后的乐谱"""
        if not self.parsed_notes:
            if not self.parse_sheet_music():
                print("无法播放：乐谱未解析")
                return
                
        for note_type, freq, duration in self.parsed_notes:
            if note_type == 'note':
                piano_player.play_tone(freq, duration)
            else:  # rest
                time.sleep(duration)

    def print_sheet_music(self):
        if not self.sheet_music:
            print("没有可用的乐谱数据")
            return
            
        print("\n=== 乐谱信息 ===")
        print(f"标题: {self.sheet_music.get('title', '无')}")
        print(f"副标题: {self.sheet_music.get('subtitle', '无')}")
        print(f"作曲家: {self.sheet_music.get('composer', '无')}")
        print(f"编曲: {self.sheet_music.get('arranger', '无')}")
        print(f"速度: {self.sheet_music.get('tempo', '无')}")
        print(f"调号: {self.sheet_music.get('key', '无')}")
        print(f"节拍: {self.sheet_music.get('meter', '无')}")
        
        print("\n=== 乐谱内容 ===")
        sections = self.sheet_music.get('sections', '').split('|')
        for i, section in enumerate(sections, 1):
            print(f"小节 {i}: {section.strip()}")


if __name__ == "__main__":
    import time
    
    piano_music = PianoMusic()
    sheet_music = piano_music.load_sheet_music("C:\\Users\\33117\\Desktop\\Games based on Pygame\\3.piano\\yaml\\qianxun.yaml")
    
    if sheet_music:
        piano_music.print_sheet_music()
        if piano_music.parse_sheet_music():
            print("\n准备播放乐谱...")
            player = PianoPlayer()
            try:
                piano_music.play(player)
            finally:
                player.close()
    else:
        print("无法加载乐谱文件")
