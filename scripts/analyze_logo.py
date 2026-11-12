from PIL import Image
import numpy as np

p = r'C:\Users\Dell\.gemini\antigravity\brain\95021a72-d85c-4ee6-ac3c-a5e236398f5e\.user_uploaded\media_1794408125084_74e4e35e.jpg'
img = Image.open(p)
arr = np.array(img)

# Let's find pixels that are noticeably non-gray/non-white (i.e. foreground logo content)
# Check saturation or difference from light background
# Background is (R, G, B) where all channels are > 235 and max(R,G,B) - min(R,G,B) < 15
is_bg = (arr[:, :, 0] > 232) & (arr[:, :, 1] > 232) & (arr[:, :, 2] > 232) & (np.ptp(arr, axis=2) < 16)
fg_mask = ~is_bg

# Find bounding box of foreground
y_indices, x_indices = np.where(fg_mask)
min_y, max_y = y_indices.min(), y_indices.max()
min_x, max_x = x_indices.min(), x_indices.max()

print(f"Foreground bounding box: x=[{min_x}, {max_x}] ({max_x-min_x+1}px), y=[{min_y}, {max_y}] ({max_y-min_y+1}px)")

# What is the divider between the icon emblem (left) and the text "UniScope LK" (right)?
# Let's find column sums of foreground pixels
col_fg = fg_mask.sum(axis=0)
# Look at columns between x=280 and 360
for x in range(300, 350, 5):
    print(f"x={x}: fg_count={col_fg[x]}")
