
## 这是一个蜂鸣器演示
## V1.0 piano
预期功能实现
- 播放曲目
- 选择谱子

前期使用蜂鸣器效果

play.py是一个废弃的，使用import winsound会出现问题
play2.py的import pyaudio，没有问题，nice,用这个

测试谱子
![20250814123301](https://liwuyou66.oss-cn-beijing.aliyuncs.com/img/20250814123301.png)

## V1.2 piano
问题1，爆音
问题2，会黏音，如"C/ A,/ A, B,",两个A的音就黏在一起了

## V1.4 piano
爆音解决，频率切换时，相位不对，增加淡入淡出
but 延音处理方面还是有问题