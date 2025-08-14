import numpy as np
import pyaudio
import time

# 音频参数
SAMPLE_RATE = 44100  # 采样率（Hz）
DURATION = 2.0      # 播放时长（秒）
FREQUENCY = 440.0    # 频率（Hz，A4音符）

# 生成正弦波音频数据
def generate_sine_wave(freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(2 * np.pi * freq * t)
    return wave * 0.3  # 降低音量避免爆音

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
print(f"正在播放 {FREQUENCY}Hz 的正弦波...")
sine_wave = generate_sine_wave(FREQUENCY, DURATION, SAMPLE_RATE)
sine_wave2 = generate_sine_wave(500.0, DURATION, SAMPLE_RATE)
sine_wave3 = generate_sine_wave(300.0, DURATION, SAMPLE_RATE)

stream.write(sine_wave.astype(np.float32).tobytes())
stream.write(sine_wave2.astype(np.float32).tobytes())
stream.write(sine_wave3.astype(np.float32).tobytes())

# 关闭流和PyAudio
stream.stop_stream()
stream.close()
p.terminate()
print("播放结束")