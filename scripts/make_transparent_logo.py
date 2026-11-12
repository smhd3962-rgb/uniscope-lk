import cv2
import numpy as np
from PIL import Image
import os

src_path = r'C:\Users\Dell\.gemini\antigravity\brain\95021a72-d85c-4ee6-ac3c-a5e236398f5e\.user_uploaded\media_1794408125084_74e4e35e.jpg'
out_dir = 'public/static/home/images'

img_bgr = cv2.imread(src_path)
h, w = img_bgr.shape[:2]

# Light gray checkerboard check (values > 220, diff < 20)
diff = np.max(img_bgr, axis=2).astype(int) - np.min(img_bgr, axis=2).astype(int)
is_light_gray = (img_bgr[:, :, 0] > 220) & (img_bgr[:, :, 1] > 220) & (img_bgr[:, :, 2] > 220) & (diff < 20)

# Protect the white university building inside the purple pin:
# Pin is roughly between y: 150..290, x: 80..260
# More precisely, let's detect the purple pin outline
hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
purple_mask = (hsv[:, :, 0] >= 115) & (hsv[:, :, 0] <= 170) & (hsv[:, :, 1] > 60)
pin_contours, _ = cv2.findContours(purple_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
protected = np.zeros((h, w), dtype=np.uint8)
for cnt in pin_contours:
    if cv2.contourArea(cnt) > 3000:
        cv2.drawContours(protected, [cnt], -1, 1, thickness=-1)

# Any light gray that is NOT protected is background
bg = np.where(is_light_gray & (protected == 0), 1, 0).astype(np.uint8)

# Floodfill from all 4 borders to get outer background
flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
# We fill with value 2
for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
    if bg[seed[1], seed[0]] == 1:
        cv2.floodFill(bg, flood_mask, seed, 2)

# In the text region (x > 325), any light-gray island (like inside 'O', 'e', 'P', 'p') is also background
is_text_counterspace = (np.arange(w) > 325) & (bg == 1)
bg[is_text_counterspace] = 2

# Also in the emblem: between the mortarboard tassel and the pin/cap, any light gray that connects to exterior is 2.
# External background is exactly where bg == 2
is_exterior = (bg == 2)

# Build alpha channel
alpha = np.where(is_exterior, 0, 255).astype(np.uint8)

# Refine alpha edges: antialias
# Feather the transition pixels slightly
alpha_blur = cv2.GaussianBlur(alpha, (3, 3), 0)

# Build RGBA
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
rgba = np.dstack([img_rgb, alpha_blur])

# Trim bounding box
y_indices, x_indices = np.where(alpha > 10)
min_y, max_y = max(0, y_indices.min() - 4), min(h, y_indices.max() + 4)
min_x, max_x = max(0, x_indices.min() - 6), min(w, x_indices.max() + 6)

trimmed_rgba = rgba[min_y:max_y, min_x:max_x]
Image.fromarray(trimmed_rgba).save(os.path.join(out_dir, 'uniscope_logo_full.png'), 'PNG')
Image.fromarray(trimmed_rgba).save(os.path.join(out_dir, 'uniscope_logo_full.webp'), 'WEBP', quality=95)
print(f"[OK] Full logo saved: {trimmed_rgba.shape[1]}x{trimmed_rgba.shape[0]}px, corner alpha = {trimmed_rgba[0, 0, 3]}")

# Standalone Emblem Mark (left side)
emblem_x_max = 330 - min_x
emblem_rgba = trimmed_rgba[:, :emblem_x_max]
# Trim emblem tightly
ey_ind, ex_ind = np.where(emblem_rgba[:, :, 3] > 10)
emblem_trimmed = emblem_rgba[ey_ind.min():ey_ind.max()+1, ex_ind.min():ex_ind.max()+1]
# Add small 6px padding around emblem
pad = 6
emblem_padded = np.zeros((emblem_trimmed.shape[0] + 2*pad, emblem_trimmed.shape[1] + 2*pad, 4), dtype=np.uint8)
emblem_padded[pad:pad+emblem_trimmed.shape[0], pad:pad+emblem_trimmed.shape[1]] = emblem_trimmed
Image.fromarray(emblem_padded).save(os.path.join(out_dir, 'uniscope_logo_mark.png'), 'PNG')
Image.fromarray(emblem_padded).save(os.path.join(out_dir, 'uniscope_logo_mark.webp'), 'WEBP', quality=95)
print(f"[OK] Emblem mark saved: {emblem_padded.shape[1]}x{emblem_padded.shape[0]}px")

# Dark Mode Logo:
# In dark mode, replace the dark navy text "UniScope" (from x=emblem_x_max onwards) with crisp white (#FFFFFF)
dark_rgba = trimmed_rgba.copy()
text_region_mask = np.zeros(dark_rgba.shape[:2], dtype=bool)
text_region_mask[:, emblem_x_max:] = True
is_navy_text = text_region_mask & (dark_rgba[:, :, 0] < 55) & (dark_rgba[:, :, 1] < 65) & (dark_rgba[:, :, 2] < 95) & (dark_rgba[:, :, 3] > 80)
dark_rgba[is_navy_text, 0] = 255
dark_rgba[is_navy_text, 1] = 255
dark_rgba[is_navy_text, 2] = 255
Image.fromarray(dark_rgba).save(os.path.join(out_dir, 'uniscope_logo_dark.png'), 'PNG')
Image.fromarray(dark_rgba).save(os.path.join(out_dir, 'uniscope_logo_dark.webp'), 'WEBP', quality=95)
print(f"[OK] Dark logo saved: {dark_rgba.shape[1]}x{dark_rgba.shape[0]}px")

# Favicon 64x64
fav = Image.fromarray(emblem_padded)
fav.thumbnail((64, 64), Image.Resampling.LANCZOS)
fav.save(os.path.join(out_dir, 'favicon.png'), 'PNG')
print("[OK] Favicon saved: 64x64px")
