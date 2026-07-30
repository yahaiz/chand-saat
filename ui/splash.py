import os
import time
import urllib.request
from core.config import BASE_DIR, logger

def show_splash(server_port: int = 28475):
    splash_path = os.path.join(BASE_DIR, "splash.png")
    if not os.path.exists(splash_path):
        return

    try:
        import tkinter as tk
        from PIL import Image, ImageTk

        splash_root = tk.Tk()
        splash_root.overrideredirect(True)
        splash_root.attributes('-topmost', True)

        TRANS_COLOR = '#010203'
        splash_root.config(bg=TRANS_COLOR)
        try:
            splash_root.wm_attributes('-transparentcolor', TRANS_COLOR)
        except Exception:
            pass

        img = Image.open(splash_path)

        target_w = 680
        w_percent = target_w / float(img.size[0])
        target_h = int(float(img.size[1]) * float(w_percent))

        img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        if img_resized.mode in ('RGBA', 'LA') or (img_resized.mode == 'P' and 'transparency' in img_resized.info):
            bg_img = Image.new('RGBA', img_resized.size, (1, 2, 3, 255))
            bg_img.paste(img_resized, (0, 0), img_resized)
            img_final = bg_img.convert('RGB')
        else:
            img_final = img_resized

        tk_img = ImageTk.PhotoImage(img_final)
        w, h = tk_img.width(), tk_img.height()

        sw = splash_root.winfo_screenwidth()
        sh = splash_root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        splash_root.geometry(f'{w}x{h}+{x}+{y}')

        label = tk.Label(splash_root, image=tk_img, bg=TRANS_COLOR, bd=0, highlightthickness=0)
        label.pack(fill='both', expand=True)

        start_time = time.time()

        def check_ready():
            is_ready = False
            try:
                req = urllib.request.Request(f"http://127.0.0.1:{server_port}/", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=0.3) as resp:
                    if resp.status == 200:
                        is_ready = True
            except Exception:
                pass

            elapsed = time.time() - start_time
            if (is_ready and elapsed >= 1.5) or elapsed > 10.0:
                splash_root.destroy()
            else:
                splash_root.after(100, check_ready)

        splash_root.after(100, check_ready)
        splash_root.mainloop()
    except Exception as e:
        logger.error(f"Splash screen display error: {e}")
