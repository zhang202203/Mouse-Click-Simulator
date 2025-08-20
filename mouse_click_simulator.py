# Mouse Click Simulator 鼠标连点器
import tkinter as tk
from tkinter import ttk, messagebox
from pynput import mouse, keyboard
import threading
import time
import json
import os

CONFIG_FILE = 'mouse_simulator_config.json'

class MouseClickSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("鼠标连点器")

        # --- State Variables ---
        self.is_clicking = False
        self.click_thread = None
        self.state_lock = threading.Lock()
        self.currently_pressed = set()
        self.hotkey_fired_on_press = False

        # --- Settings ---
        self.click_interval = tk.DoubleVar(value=0.1)
        self.click_count = tk.IntVar(value=0)
        self.mouse_button = tk.StringVar(value='Left')
        self.modifier_key = tk.StringVar(value='Ctrl')
        self.number_key = tk.StringVar(value='1')

        self.setup_gui()
        self.load_settings()

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=False)
        self.listener.start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        settings_frame = ttk.LabelFrame(main_frame, text="设置 (选择后自动保存)", padding="10")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Click Settings
        ttk.Label(settings_frame, text="点击间隔 (毫秒):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.interval_entry = ttk.Entry(settings_frame, width=15)
        self.interval_entry.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(settings_frame, text="点击次数 (0为无限):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.count_entry = ttk.Entry(settings_frame, width=15)
        self.count_entry.grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Label(settings_frame, text="鼠标按键:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.button_combo = ttk.Combobox(settings_frame, values=['Left', 'Right', 'Middle'], state='readonly', width=13)
        self.button_combo.grid(row=2, column=1, sticky=tk.W, pady=2)

        # Hotkey Settings
        ttk.Label(settings_frame, text="修饰键:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.modifier_combo = ttk.Combobox(settings_frame, values=['Ctrl', 'Alt'], state='readonly', width=13)
        self.modifier_combo.grid(row=3, column=1, sticky=tk.W, pady=2)

        ttk.Label(settings_frame, text="数字键:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.number_combo = ttk.Combobox(settings_frame, values=[str(i) for i in range(1, 10)], state='readonly', width=13)
        self.number_combo.grid(row=4, column=1, sticky=tk.W, pady=2)

        # Status
        status_frame = ttk.LabelFrame(main_frame, text="状态", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        self.status_label = ttk.Label(status_frame, text="状态：已就绪")
        self.status_label.pack(anchor='w')

        # Bindings
        for widget in [self.interval_entry, self.count_entry]:
            widget.bind("<FocusOut>", self._apply_and_save_settings)
            widget.bind("<Return>", self._apply_and_save_settings)
        for combo in [self.button_combo, self.modifier_combo, self.number_combo]:
            combo.bind("<<ComboboxSelected>>", self._apply_and_save_settings)

    def _apply_and_save_settings(self, event=None):
        try:
            # defensive check for empty entry
            interval_val = self.interval_entry.get()
            count_val = self.count_entry.get()
            if interval_val:
                self.click_interval.set(int(interval_val) / 1000.0)
            if count_val:
                self.click_count.set(int(count_val))

            self.mouse_button.set(self.button_combo.get())
            self.modifier_key.set(self.modifier_combo.get())
            self.number_key.set(self.number_combo.get())
            self.status_label.config(text=f"就绪: 使用 {self.modifier_key.get()} + {self.number_key.get()} 启动")
            self.save_settings()
        except (ValueError, TypeError): pass

    def on_press(self, key):
        self.currently_pressed.add(key)

        mod_str = self.modifier_key.get()
        num_char = self.number_key.get()

        # --- 更稳健的修饰键检查 ---
        mod_key_pressed = False
        ctrl_keys = {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl}
        alt_keys = {keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt}

        if mod_str == 'Ctrl':
            if any(k in ctrl_keys for k in self.currently_pressed):
                mod_key_pressed = True
        elif mod_str == 'Alt':
            if any(k in alt_keys for k in self.currently_pressed):
                mod_key_pressed = True

        # --- 更稳健的数字键检查 ---
        # 我们遍历当前所有按下的键，而不是创建一个新的去比较
        num_key_pressed = False
        for pressed_key in self.currently_pressed:
            # 检查按键的 .char 属性
            if hasattr(pressed_key, 'char') and pressed_key.char == num_char:
                num_key_pressed = True
                break
            # 作为备用方案，检查按键的虚拟键码 (vk)
            if hasattr(pressed_key, 'vk') and pressed_key.vk is not None and pressed_key.vk == ord(num_char):
                num_key_pressed = True
                break

        # 触发器逻辑保持不变
        if mod_key_pressed and num_key_pressed and not self.hotkey_fired_on_press:
            self.hotkey_fired_on_press = True
            self.toggle_clicking()

    def on_release(self, key):
        mod_str = self.modifier_key.get()
        num_char = self.number_key.get()

        key_was_part_of_combo = False
        
        # 检查是否是修饰键被释放
        if mod_str == 'Ctrl' and key in {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl}:
            key_was_part_of_combo = True
        elif mod_str == 'Alt' and key in {keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt}:
            key_was_part_of_combo = True
        
        # 检查是否是数字键被释放 (同样使用更稳健的方式)
        if not key_was_part_of_combo:
            if hasattr(key, 'char') and key.char == num_char:
                key_was_part_of_combo = True
            elif hasattr(key, 'vk') and key.vk is not None and key.vk == ord(num_char):
                key_was_part_of_combo = True

        if key_was_part_of_combo:
            self.hotkey_fired_on_press = False

        # 从集合中移除被释放的键
        if key in self.currently_pressed:
            try:
                self.currently_pressed.remove(key)
            except KeyError:
                pass # Key might have already been removed, ignore

    def toggle_clicking(self):
        with self.state_lock:
            self.is_clicking = not self.is_clicking
            if self.is_clicking:
                if self.click_thread is None or not self.click_thread.is_alive():
                    self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
                    self.click_thread.start()
                    self.status_label.config(text="状态：点击中...")
            else:
                self.status_label.config(text=f"状态：已停止。使用 {self.modifier_key.get()} + {self.number_key.get()} 再次启动")

    def click_loop(self):
        try:
            interval = self.click_interval.get()
            button_str = self.mouse_button.get()
            total_clicks = self.click_count.get()
        except tk.TclError: # Handle cases where GUI is destroyed mid-operation
            return
            
        button = {'Left': mouse.Button.left, 'Right': mouse.Button.right, 'Middle': mouse.Button.middle}[button_str]
        mouse_controller = mouse.Controller()
        clicks_done = 0
        
        while True:
            with self.state_lock:
                if not self.is_clicking:
                    break
            
            mouse_controller.click(button)
            
            if total_clicks > 0:
                clicks_done += 1
                if clicks_done >= total_clicks:
                    self.root.after(0, self.stop_clicking_after_count, total_clicks)
                    break
            
            time.sleep(interval)
    
    def stop_clicking_after_count(self, total_clicks):
        with self.state_lock:
            self.is_clicking = False
        self.status_label.config(text=f"状态：完成 {total_clicks} 次点击。")


    def save_settings(self):
        settings = {
            'interval': self.click_interval.get(),
            'count': self.click_count.get(),
            'button': self.mouse_button.get(),
            'modifier': self.modifier_key.get(),
            'number': self.number_key.get()
        }
        with open(CONFIG_FILE, 'w') as f: json.dump(settings, f, indent=4)

    def load_settings(self):
        if not os.path.exists(CONFIG_FILE): 
            self.set_defaults()
            return
        try:
            with open(CONFIG_FILE, 'r') as f: settings = json.load(f)
            self.interval_entry.insert(0, str(int(settings.get('interval', 0.1) * 1000)))
            self.count_entry.insert(0, str(settings.get('count', 0)))
            self.button_combo.set(settings.get('button', 'Left'))
            self.modifier_combo.set(settings.get('modifier', 'Ctrl'))
            self.number_combo.set(settings.get('number', '1'))
            self._apply_and_save_settings()
        except Exception:
            self.set_defaults()

    def set_defaults(self):
        self.interval_entry.insert(0, "100")
        self.count_entry.insert(0, "0")
        self.button_combo.set("Left")
        self.modifier_combo.set("Ctrl")
        self.number_combo.set("1")
        self._apply_and_save_settings()

    def on_closing(self):
        self.save_settings()
        self.is_clicking = False # Ensure clicking thread stops
        self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseClickSimulator(root)
    root.mainloop()