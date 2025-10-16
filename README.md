# Sphero Interactive Robot Project / Sphero 互动机器人项目

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

### 📖 Project Overview

This is an interactive robot project based on the Sphero Bolt platform, featuring multimodal human-robot interaction capabilities including vision, voice, touch, and motion sensing. The robot has an interactive character named "Ishmael" who can express emotions through LED patterns and respond to various user inputs.

### ✨ Key Features

- **🛌 Sleep/Wake Mechanism**: Robot enters sleep mode and wakes up when picked up or shaken
- **👁️ Computer Vision Tracking**: Uses OpenCV to track red objects, enabling the robot to chase targets
- **🎤 Voice Recognition**: Recognizes the phrase "your fault" to trigger angry mode
- **😊 Emotion Expression**: Displays different facial expressions (happy, angry, sad, etc.) through 8x8 LED matrix
- **🎮 Keyboard Control**: Real-time control via keyboard shortcuts
- **🌊 Dynamic LED Effects**: Including heartbeat, wave, and other animations

### 📁 Project Structure

#### Main Programs

- **`Sphero_Interaction.py`** - Main interaction control program
  - Implements complete sleep/wake cycle
  - Integrates vision tracking, voice recognition, and LED display
  - State management (sleeping → awake → tracking)
  - Keyboard event handling (press 's' to start tracking, 'ESC' to quit)
  - Angry mode triggered by voice commands (7-second duration)

- **`Sphero_Pattern.py`** - LED pattern display module
  - Defines various emotional expressions for Ishmael character:
    - `ishmael` - Neutral/idle expression
    - `smile` - Happy expression
    - `frown` - Sad/worried expression
    - `angry` - Angry expression (red eyes)
    - `tear` - Crying expression (blue tear)
  - Manages color palettes and matrix rendering
  - Controls front/back LED synchronization

- **`Sphero_Vision.py`** - Computer vision module
  - Red object detection (target tracking)
  - Green LED detection (Sphero position identification)
  - Real-time calculation of relative angle and distance
  - OpenCV-based image processing and contour detection
  - Visualization window with debug information

- **`Sphero_Voice.py`** - Voice recognition module
  - Continuous background listening
  - Google Speech Recognition API integration
  - Detects specific phrase "your fault"
  - Callback-based event notification

#### Auxiliary Directories

- **`FirstMove/`** - Basic movement and control demos
  - `FirstMove.py` - Basic Sphero connection test
  - `Control_intro.py` - Wave animation demo
  - `Sphero_Movement.py` - Manual control via arrow keys
  - `Sphero_Programmed_Movement.py` - Pre-programmed movement sequences

- **`LED_Heart_Wave/`** - LED lighting effects
  - `Sphero_Heartbeat.py` - Heartbeat and wave LED effects with smooth transitions

- **`sphero/`** - Early interactive versions
  - `Interactive_Sphero.py` - Earlier version of interactive control
  - `Connect_test.py` - Connection testing utilities
  - Other movement control modules

#### Configuration Files

- **`requirements.txt`** - Python dependencies list
- **`activate.sh`** - Virtual environment activation script
- **`run_interaction.sh`** - Launch script for main program

### 🚀 Quick Start

#### 1. Environment Setup

```bash
# Create virtual environment
python3 -m venv sphero_env

# Activate virtual environment
source activate.sh

# Install dependencies
pip install -r requirements.txt
```

#### 2. Running the Program

```bash
# Method 1: Use launch script
bash run_interaction.sh

# Method 2: Run directly
source sphero_env/bin/activate
python3 Sphero_Interaction.py
```

#### 3. Usage Instructions

1. **Waking Up**: When program starts, Sphero enters sleep mode. Pick it up or shake it to wake it up
2. **Starting Tracking**: Press 's' key to activate vision tracking mode (front/back LEDs turn green)
3. **Voice Control**: Say "your fault" to trigger angry mode (Sphero spins 720°)
4. **Exit Program**: Press 'ESC' key to exit

### 🔧 Technical Details

#### Hardware Requirements
- Sphero Bolt robot (model: SB-D96A)
- Computer with camera (for vision tracking)
- Microphone (for voice recognition)
- Bluetooth connectivity

#### Software Dependencies
- `spherov2` - Sphero control library
- `opencv-python` - Computer vision
- `speech_recognition` - Voice recognition
- `pynput` - Keyboard input monitoring
- `numpy` - Numerical computation
- macOS specific: PyObjC frameworks (for Bluetooth and system integration)

#### State Flow
```
Sleeping Mode → (shake/pickup) → Awake Mode → (press 's') → Tracking Mode
                                      ↓
                              (voice: "your fault")
                                      ↓
                                 Angry Mode (7s)
                                      ↓
                              Return to previous state
```

### 📝 Notes

- Ensure Sphero Bolt is powered on and Bluetooth is enabled
- For vision tracking, a red target object is required
- Voice recognition requires internet connection (Google API)
- Run on macOS for best compatibility

### 🎯 Future Development

- [ ] Add more interactive modes
- [ ] Support custom LED patterns
- [ ] Multi-robot collaboration
- [ ] More complex emotion state machine
- [ ] Mobile app control interface

---

<a name="chinese"></a>
## 中文

### 📖 项目简介

这是一个基于 Sphero Bolt 平台的交互式机器人项目，具有视觉、语音、触觉和运动感知等多模态人机交互能力。机器人拥有名为"Ishmael"的交互角色，可以通过 LED 图案表达情绪，并对各种用户输入做出响应。

### ✨ 主要功能

- **🛌 睡眠/唤醒机制**：机器人进入睡眠模式，被拾起或摇晃时唤醒
- **👁️ 计算机视觉追踪**：使用 OpenCV 追踪红色物体，实现目标追逐
- **🎤 语音识别**：识别"your fault"短语触发愤怒模式
- **😊 情绪表达**：通过 8x8 LED 矩阵显示不同表情（开心、生气、难过等）
- **🎮 键盘控制**：通过键盘快捷键实时控制
- **🌊 动态 LED 效果**：包括心跳、波浪等动画效果

### 📁 项目结构

#### 核心程序

- **`Sphero_Interaction.py`** - 主交互控制程序
  - 实现完整的睡眠/唤醒循环
  - 整合视觉追踪、语音识别、LED 显示
  - 状态管理（睡眠 → 清醒 → 追踪）
  - 键盘事件处理（按's'启动追踪，'ESC'退出）
  - 语音触发的愤怒模式（持续7秒）

- **`Sphero_Pattern.py`** - LED 图案显示模块
  - 定义 Ishmael 角色的各种情绪表情：
    - `ishmael` - 中性/待机表情
    - `smile` - 开心表情
    - `frown` - 难过/担忧表情
    - `angry` - 愤怒表情（红色眼睛）
    - `tear` - 哭泣表情（蓝色眼泪）
  - 管理颜色调色板和矩阵渲染
  - 控制前后 LED 同步

- **`Sphero_Vision.py`** - 计算机视觉模块
  - 红色物体检测（目标追踪）
  - 绿色 LED 检测（Sphero 位置识别）
  - 实时计算相对角度和距离
  - 基于 OpenCV 的图像处理和轮廓检测
  - 可视化窗口显示调试信息

- **`Sphero_Voice.py`** - 语音识别模块
  - 持续后台监听
  - Google 语音识别 API 集成
  - 检测特定短语"your fault"
  - 基于回调的事件通知

#### 辅助目录

- **`FirstMove/`** - 基础移动和控制演示
  - `FirstMove.py` - 基础 Sphero 连接测试
  - `Control_intro.py` - 波浪动画演示
  - `Sphero_Movement.py` - 方向键手动控制
  - `Sphero_Programmed_Movement.py` - 预编程运动序列

- **`LED_Heart_Wave/`** - LED 灯光效果
  - `Sphero_Heartbeat.py` - 心跳和波浪 LED 效果，带平滑过渡

- **`sphero/`** - 早期交互版本
  - `Interactive_Sphero.py` - 早期版本的交互控制
  - `Connect_test.py` - 连接测试工具
  - 其他移动控制模块

#### 配置文件

- **`requirements.txt`** - Python 依赖列表
- **`activate.sh`** - 虚拟环境激活脚本
- **`run_interaction.sh`** - 主程序启动脚本

### 🚀 快速开始

#### 1. 环境配置

```bash
# 创建虚拟环境
python3 -m venv sphero_env

# 激活虚拟环境
source activate.sh

# 安装依赖
pip install -r requirements.txt
```

#### 2. 运行程序

```bash
# 方式1：使用启动脚本
bash run_interaction.sh

# 方式2：直接运行
source sphero_env/bin/activate
python3 Sphero_Interaction.py
```

#### 3. 使用说明

1. **唤醒**：程序启动后，Sphero 进入睡眠模式，拾起或摇晃它以唤醒
2. **启动追踪**：按 's' 键激活视觉追踪模式（前后 LED 变绿）
3. **语音控制**：说"your fault"触发愤怒模式（Sphero 旋转720度）
4. **退出程序**：按 'ESC' 键退出

### 🔧 技术细节

#### 硬件要求
- Sphero Bolt 机器人（型号：SB-D96A）
- 带摄像头的计算机（用于视觉追踪）
- 麦克风（用于语音识别）
- 蓝牙连接

#### 软件依赖
- `spherov2` - Sphero 控制库
- `opencv-python` - 计算机视觉
- `speech_recognition` - 语音识别
- `pynput` - 键盘输入监控
- `numpy` - 数值计算
- macOS 特定：PyObjC 框架（用于蓝牙和系统集成）

#### 状态流转
```
睡眠模式 → (摇晃/拾起) → 清醒模式 → (按's'键) → 追踪模式
                            ↓
                    (语音："your fault")
                            ↓
                        愤怒模式(7秒)
                            ↓
                        返回之前状态
```

### 📝 注意事项

- 确保 Sphero Bolt 已开机且蓝牙已启用
- 视觉追踪需要准备一个红色目标物体
- 语音识别需要互联网连接（Google API）
- 在 macOS 上运行以获得最佳兼容性

### 🎯 未来开发方向

- [ ] 增加更多交互模式
- [ ] 支持自定义 LED 图案
- [ ] 多机器人协作
- [ ] 更复杂的情绪状态机
- [ ] 移动应用控制界面

---

## 📄 License / 许可证

This project is for educational and research purposes.

本项目用于教育和研究目的。

## 👥 Contact / 联系方式

For questions or collaboration, please open an issue on GitHub.

如有问题或合作意向，请在 GitHub 上提交 issue。

