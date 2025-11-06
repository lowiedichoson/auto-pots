import threading
import time
import tkinter as tk
from pynput import mouse, keyboard as kb
import keyboard  # for global hotkey

# Global states
holding_right_click = False
macro_enabled = False

# Keyboard controller
kb_controller = kb.Controller()

# GUI update function
def update_label():
    status_label.config(text=f"Toggle: {'ON' if macro_enabled else 'OFF'}")

# Toggle macro function
def toggle_macro():
    global macro_enabled
    macro_enabled = not macro_enabled
    update_label()

# Spam keys function
def spam_keys():
    global holding_right_click, macro_enabled
    keys = ['q', 'w', 'e', 'r']
    while holding_right_click and macro_enabled:
        for key in keys:
            if not holding_right_click or not macro_enabled:
                break
            kb_controller.press(key)
            kb_controller.release(key)
            time.sleep(0.1)  # Adjust delay between key presses

# Mouse click handler
def on_click(x, y, button, pressed):
    global holding_right_click
    if button == mouse.Button.right:
        if pressed and macro_enabled:
            holding_right_click = True
            threading.Thread(target=spam_keys, daemon=True).start()
        else:
            holding_right_click = False

# Set up mouse listener in background
def start_mouse_listener():
    listener = mouse.Listener(on_click=on_click)
    listener.start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Macro Toggler")
root.geometry("200x80")
root.resizable(False, False)

status_label = tk.Label(root, text="Toggle: OFF", font=("Arial", 14))
status_label.pack(pady=10)

toggle_button = tk.Button(root, text="Toggle", command=toggle_macro)
toggle_button.pack()

# Start mouse listener
start_mouse_listener()

# Bind F8 as a global hotkey
keyboard.add_hotkey("F8", toggle_macro)

# Run GUI
root.mainloop()
