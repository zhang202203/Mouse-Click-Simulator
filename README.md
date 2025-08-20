# Mouse Click Simulator 鼠标连点器

## English

A Python-based mouse auto-clicker with a graphical interface that allows you to automate mouse clicks at a customizable interval and count. The program can be controlled using configurable hotkeys (Ctrl+1-9 or Alt+1-9).

<img width="270" height="310" alt="image" src="https://github.com/user-attachments/assets/411e702e-b270-4dbd-babb-4c199821a891" />
<div align="center">
  <img width="270" height="310" alt="image" src="https://github.com/user-attachments/assets/411e702e-b270-4dbd-babb-4c199821a891" />
</div>

### Features

- **Customizable Click Settings**:
  - Adjustable click interval (in milliseconds)
  - Set number of clicks (0 for infinite)
  - Select mouse button (Left, Right, or Middle)

- **Flexible Hotkey Control**:
  - Configurable modifier key (Ctrl or Alt)
  - Configurable number key (1-9)
  - Supports multiple activation methods:
    - Press both keys simultaneously (e.g., Ctrl+1)
    - Press modifier key first, then number key (e.g., hold Ctrl, then press 1)
    - Press number key first, then modifier key

- **Persistent Configuration**:
  - Settings are automatically saved to `mouse_simulator_config.json`
  - Configuration is loaded on startup

- **User-Friendly Interface**:
  - Clean and intuitive GUI built with Tkinter
  - Real-time status updates
  - Settings applied automatically when changed

### Requirements

- Python 3.x
- `pynput` library
- `tkinter` (usually included with Python)

### Installation

1. Install required libraries:
   ```bash
   pip install pynput
   ```

2. Run the program:
   ```bash
   python mouse_click_simulator.py
   ```

### Usage

1. Configure your desired click settings:
   - Set click interval (milliseconds)
   - Set number of clicks (0 for infinite)
   - Select mouse button

2. Configure your hotkey:
   - Choose modifier key (Ctrl or Alt)
   - Choose number key (1-9)

3. Use the hotkey to start/stop clicking:
   - Press your configured hotkey combination to start clicking
   - Press the same combination again to stop

### Configuration File

Settings are saved to `mouse_simulator_config.json`:
```json
{
    "interval": 0.1,
    "count": 0,
    "button": "Left",
    "modifier": "Ctrl",
    "number": "1"
}
```

## 中文

一个基于Python的图形化鼠标连点器，允许您以可自定义的时间间隔和次数自动执行鼠标点击。该程序可以通过可配置的热键(Ctrl+1-9或Alt+1-9)进行控制。

### 功能特点

- **可自定义点击设置**：
  - 可调节的点击间隔（毫秒）
  - 设置点击次数（0为无限）
  - 选择鼠标按键（左键、右键或中键）

- **灵活的热键控制**：
  - 可配置的修饰键（Ctrl或Alt）
  - 可配置的数字键（1-9）
  - 支持多种激活方式：
    - 同时按下两个键（如Ctrl+1）
    - 先按修饰键，再按数字键（如按住Ctrl，再按1）
    - 先按数字键，再按修饰键

- **持久化配置**：
  - 设置会自动保存到`mouse_simulator_config.json`
  - 启动时加载配置

- **用户友好界面**：
  - 使用Tkinter构建的简洁直观的图形界面
  - 实时状态更新
  - 更改设置时自动应用

### 环境要求

- Python 3.x
- `pynput` 库
- `tkinter`（通常随Python一起安装）

### 安装方法

1. 安装所需库：
   ```bash
   pip install pynput
   ```

2. 运行程序：
   ```bash
   python mouse_click_simulator.py
   ```

### 使用方法

1. 配置所需的点击设置：
   - 设置点击间隔（毫秒）
   - 设置点击次数（0为无限）
   - 选择鼠标按键

2. 配置热键：
   - 选择修饰键（Ctrl或Alt）
   - 选择数字键（1-9）

3. 使用热键开始/停止点击：
   - 按下配置的热键组合开始点击
   - 再次按下相同组合停止点击

### 配置文件

设置保存在`mouse_simulator_config.json`中：
```json
{
    "interval": 0.1,
    "count": 0,
    "button": "Left",
    "modifier": "Ctrl",
    "number": "1"
}
```
