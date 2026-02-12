import os
import time
import sys
from PIL import Image
import numpy as np
from threading import Thread

# Enable ANSI colors for Windows and hide cursor
os.system('')
sys.stdout.write("\033[?25l") # Hide cursor
sys.stdout.flush()

def play_webp_fullscreen(path):
    global stop
    img = Image.open(path)
    try:
        while not stop:
            for frame_num in range(getattr(img, "n_frames", 1)):
                if stop: break
                img.seek(frame_num)
                tw, th = os.get_terminal_size()
                frame = img.convert("RGB").resize((tw, th - 1))
                
                output = "\033[H"
                for y in range(th - 1):
                    for x in range(tw):
                        r, g, b = frame.getpixel((x, y))
                        output += f"\033[48;2;{r};{g};{b}m "
                    output += "\n"
                sys.stdout.write(output + "\033[0m")
                sys.stdout.flush()
                time.sleep(img.info.get('duration', 100) / 1000.0)
    finally:
        sys.stdout.write("\033[0m")

def play_webp_high_res(path):
    global stop
    img = Image.open(path)
    try:
        while not stop:
            for frame_num in range(getattr(img, "n_frames", 1)):
                if stop: break
                img.seek(frame_num)
                tw, th = os.get_terminal_size()
                target_h = (th - 1) * 2
                frame = img.convert("RGB").resize((tw, target_h))
                
                output = "\033[H"
                for y in range(0, target_h - 1, 2):
                    for x in range(tw):
                        r1, g1, b1 = frame.getpixel((x, y))
                        r2, g2, b2 = frame.getpixel((x, y + 1))
                        output += f"\033[38;2;{r1};{g1};{b1};48;2;{r2};{g2};{b2}m▀"
                    output += "\033[0m\n"
                sys.stdout.write(output)
                sys.stdout.flush()
                time.sleep(img.info.get('duration', 100) / 1000.0)
    finally:
        sys.stdout.write("\033[0m")

def play_webp_ultra_fast(path):
    global stop
    img = Image.open(path)
    frames = []
    durations = []
    
    print("Pre-loading frames for max FPS...")
    try:
        for f in range(getattr(img, "n_frames", 1)):
            img.seek(f)
            frames.append(np.array(img.convert("RGB")))
            durations.append(img.info.get('duration', 100) / 1000.0)
    except EOFError:
        pass

    try:
        while not stop:
            for i, frame_data in enumerate(frames):
                if stop: break
                start_time = time.perf_counter()
                tw, th = os.get_terminal_size()
                target_h = (th - 1) * 2
                
                frame_img = Image.fromarray(frame_data).resize((tw, target_h), Image.NEAREST)
                pix = np.array(frame_img)
                
                lines = ["\033[H"]
                for y in range(0, target_h - 1, 2):
                    line = [f"\033[38;2;{pix[y,x,0]};{pix[y,x,1]};{pix[y,x,2]};48;2;{pix[y+1,x,0]};{pix[y+1,x,1]};{pix[y+1,x,2]}m▀" for x in range(tw)]
                    lines.append("".join(line))
                
                sys.stdout.write("\n".join(lines) + "\033[0m")
                sys.stdout.flush()
                
                elapsed = time.perf_counter() - start_time
                time.sleep(max(0, durations[i] - elapsed))
    finally:
        sys.stdout.write("\033[0m")

def play(file_path="test.webp", res="high", fps="high", time_limit=3):
    file_path = f"ASCII\Animations\{file_path}"
    global stop
    stop = False
    
    if res == "high" and fps == "high":
        target_func = play_webp_ultra_fast
    elif res == "high" and fps == "low":
        target_func = play_webp_high_res
    elif res == "low" and fps == "low":
        target_func = play_webp_fullscreen
    else: 
        raise ValueError("Invalid Input")

    t = Thread(target=target_func, args=[file_path])
    t.daemon = True 
    t.start()
    
    start_timestamp = time.time()

    try:
        while t.is_alive():
            if (time.time() - start_timestamp) >= time_limit:
                stop = True
                break
            time.sleep(0.1) # Essential for CPU and Ctrl+C
    except KeyboardInterrupt:
        stop = True
    finally:
        stop = True # Ensure thread knows to stop
        t.join()
        sys.stdout.write("\033[?25h\033[0m\n") # Show cursor and reset colors
        sys.stdout.flush()
        print("Playback finished.")

def get_description(filename):
    with open("DB_VDATA.csv","r",encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            if filename in line:
                return line.split(",")[1]

def get_files():
    from pathlib import Path
    path = Path('ASCII\Animations')
    l = []
    for entry in path.iterdir():
        if entry.name.startswith("VData_"):
            l.append(entry.name)
    return l


if __name__ == "__main__":
    # Change "test2.webp" to your actual filename
    print(get_files())
    """ play("test2.webp", "high", "low", time_limit=3) """