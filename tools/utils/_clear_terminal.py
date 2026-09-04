import os

def clear():
    # 'cls' for Windows, 'clear' for macOS/Linux
    os.system('cls' if os.name == 'nt' else 'clear')