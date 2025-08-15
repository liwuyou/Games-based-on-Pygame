import numpy as np
import pyaudio
import time

# 音频参数
SAMPLE_RATE = 44100  # 采样率（Hz）
DURATION = 2.0      # 播放时长（秒）
FREQUENCY = 440.0    # 频率（Hz，A4音符）
FADE_DURATION = 0.05  # 淡入淡出时长（秒）

# 生成正弦波音频数据
def generate_sine_wave(freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(2 * np.pi * freq * t)
    return wave * 0.3  # 降低音量避免爆音

# 添加淡入淡出效果
def apply_fade(wave, fade_duration=FADE_DURATION, sample_rate=SAMPLE_RATE):
    fade_samples = int(fade_duration * sample_rate)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    wave[:fade_samples] *= fade_in
    wave[-fade_samples:] *= fade_out
    return wave

# 初始化PyAudio
p = pyaudio.PyAudio()

# 打开音频流
stream = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=SAMPLE_RATE,
    output=True
)

# 生成并播放音频
print(f"正在播放正弦波序列...")
sine_wave = apply_fade(generate_sine_wave(261.63, DURATION, SAMPLE_RATE))
sine_wave2 = apply_fade(generate_sine_wave(329.63, DURATION, SAMPLE_RATE))
sine_wave3 = apply_fade(generate_sine_wave(392.00, DURATION, SAMPLE_RATE))

stream.write(sine_wave.astype(np.float32).tobytes())
time.sleep(0.02)  # 添加短暂间隔
stream.write(sine_wave2.astype(np.float32).tobytes())
time.sleep(0.02)
stream.write(sine_wave3.astype(np.float32).tobytes())

# 关闭流和PyAudio
stream.stop_stream()
stream.close()
p.terminate()
print("播放结束")
