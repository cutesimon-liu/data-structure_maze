import time
import os
import random
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def generate_maze(rows=30, cols=30): 
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows-1 or j == 0 or j == cols-1:
                maze[i][j] = 1
            elif random.random() < 0.3:
                maze[i][j] = 1
            else:
                maze[i][j] = 0
    maze[rows-2][cols-2] = 0
    maze[1][1] = 0
    return maze

maze = generate_maze()
rows = len(maze)
cols = len(maze[0])
x = rows-2
y = cols-2
stack = []
stack.append((x, y))

# --- 影片設定 ---
CELL_SIZE = 40 
width = cols * CELL_SIZE
height = rows * CELL_SIZE
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('maze_video_emoji.avi', fourcc, 10.0, (width, height)) # FPS 10

# 設定字型 (嘗試讀取 Windows 的 Emoji 字型)
try:
    font_path = "C:\\Windows\\Fonts\\seguiemj.ttf" # Windows Emoji 字型
    font = ImageFont.truetype(font_path, 30)
except:
    print("找不到 Emoji 字型，使用預設字型 (可能無法顯示 Emoji)")
    font = ImageFont.load_default()

def draw_frame(maze, mouse_x, mouse_y):
    # 使用 PIL 建立圖片 (RGB)
    img_pil = Image.new("RGB", (width, height), (0, 0, 0)) # 黑色背景
    draw = ImageDraw.Draw(img_pil)
    
    for i in range(rows):
        for j in range(cols):
            # 計算文字位置 (置中)
            pos_x = j * CELL_SIZE + 5
            pos_y = i * CELL_SIZE + 5
            
            text = ""
            if i == mouse_x and j == mouse_y:
                text = "🐭"
            elif maze[i][j] == 1:
                text = "🧱"
            elif maze[i][j] == 2:
                text = "🐾"
            elif maze[i][j] == 3:
                text = "❌"
            else:
                text = "  "
            
            if text.strip() != "":
                draw.text((pos_x, pos_y), text, font=font, fill=(255, 255, 255))

    # 將 PIL 圖片轉回 OpenCV 格式 (RGB -> BGR)
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    return img_cv

print("開始錄製 Emoji 迷宮影片...")

while x != 1 or y != 1:
    maze[x][y] = 2
    
    frame = draw_frame(maze, x, y)
    out.write(frame)
    
    if maze[x-1][y] <= 0:      # 上
        x = x - 1
        stack.append((x, y))
    elif maze[x+1][y] <= 0:    # 下
        x = x + 1
        stack.append((x, y))
    elif maze[x][y-1] <= 0:    # 左
        y = y - 1
        stack.append((x, y))
    elif maze[x][y+1] <= 0:    # 右
        y = y + 1
        stack.append((x, y))
    elif maze[x-1][y+1] <= 0:  # 右上
        x = x - 1
        y = y + 1
        stack.append((x, y))
    elif maze[x+1][y+1] <= 0:  # 右下
        x = x + 1
        y = y + 1
        stack.append((x, y))
    elif maze[x-1][y-1] <= 0:  # 左上
        x = x - 1
        y = y - 1
        stack.append((x, y))
    elif maze[x+1][y-1] <= 0:  # 左下
        x = x + 1
        y = y - 1
        stack.append((x, y))
    else:
        maze[x][y] = 3
        stack.pop()
        if len(stack) > 0:
            x, y = stack[-1]
        else:
            print("迷宮無解！")
            break

if x == 1 and y == 1:
    maze[x][y] = 2
    print("抵達終點！正在儲存影片...")
    final_frame = draw_frame(maze, x, y)
    for _ in range(20):
        out.write(final_frame)

out.release()
print("影片已儲存為 maze_video_emoji.avi")

