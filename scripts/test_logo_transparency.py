from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes
import cv2

p = r'C:\Users\Dell\.gemini\antigravity\brain\95021a72-d85c-4ee6-ac3c-a5e236398f5e\.user_uploaded\media_1794408125084_74e4e35e.jpg'
img = Image.open(p)
arr = np.array(img)
h, w, _ = arr.shape

# Let's inspect the white building inside the purple pin:
# Where is the center of the purple pin?
# Let's find purple pixels
is_purple = (arr[:, :, 0] > 90) & (arr[:, :, 0] < 160) & (arr[:, :, 2] > 140) & (arr[:, :, 1] < 60)
y_p, x_p = np.where(is_purple)
if len(y_p) > 0:
    center_y, center_x = int(y_p.mean()), int(x_p.mean())
    print(f"Pin center approx: x={center_x}, y={center_y}")
    # Sample pixels inside the pin
    building_pixels = arr[center_y-20:center_y+20, center_x-20:center_x+20]
    print("Building pixel min/max:", building_pixels.min(), building_pixels.max())
