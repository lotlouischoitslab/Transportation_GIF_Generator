import os
from PIL import Image, ImageDraw
import imageio.v2 as imageio
from collections import deque

# Utility function to check if the given cell is valid
def is_valid(x, y, width, height, visited):
    return 0 <= x < width and 0 <= y < height and not visited[y][x]

def bfs_traversal(img):
    width, height = img.size
    visited = [[False for _ in range(width)] for _ in range(height)]

    # Directions for up, down, left, right
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    frames = []

    queue = deque([(0, 0)])
    visited[0][0] = True

    while queue:
        x, y = queue.popleft()
        frame = Image.new('RGB', img.size, color=(255, 255, 255))
        frame.paste(img.crop((0, 0, x + 1, y + 1)), (0, 0))
        frames.append(frame)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y, width, height, visited):
                visited[new_y][new_x] = True
                queue.append((new_x, new_y))

    return frames

def dfs_traversal(img, x, y, frames, visited):
    width, height = img.size

    # Base case
    if not is_valid(x, y, width, height, visited):
        return

    visited[y][x] = True
    frame = Image.new('RGB', img.size, color=(255, 255, 255))
    frame.paste(img.crop((0, 0, x + 1, y + 1)), (0, 0))
    frames.append(frame)

    # Directions for up, down, left, right
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for dx, dy in directions:
        dfs_traversal(img, x + dx, y + dy, frames, visited)

def save_gif(frames, output_gif_path):
    imageio.mimsave(output_gif_path, [frame.convert('P', dither=Image.NONE, palette=Palette.ADAPTIVE) for frame in frames], duration=0.1)

def create_image_row_or_column(image_path, num, direction='horizontal'):
    """ 
    Create a row or column of the same image.
    direction: 'horizontal' or 'vertical'
    """
    img = Image.open(image_path)
    width, height = img.size
    
    if direction == 'horizontal':
        canvas = Image.new('RGB', (width*num, height))
        for i in range(num):
            canvas.paste(img, (i*width, 0))
    else:  # 'vertical'
        canvas = Image.new('RGB', (width, height*num))
        for i in range(num):
            canvas.paste(img, (0, i*height))
    
    return canvas

def bfs_traversal_linear(img, num, direction='horizontal'):
    if direction == 'horizontal':
        cell_width, cell_height = img.size[0] // num, img.size[1]
        directions = [(1, 0), (-1, 0)]
    else:
        cell_width, cell_height = img.size[0], img.size[1] // num
        directions = [(0, 1), (0, -1)]

    visited = [[False for _ in range(num)]]
    frames = []

    queue = deque([(0, 0)])
    visited[0][0] = True

    while queue:
        x, y = queue.popleft()
        frame = Image.new('RGB', img.size, color=(255, 255, 255))
        if direction == 'horizontal':
            frame.paste(img.crop((0, 0, (x+1)*cell_width, cell_height)), (0, 0))
        else:
            frame.paste(img.crop((0, 0, cell_width, (y+1)*cell_height)), (0, 0))
        frames.append(frame)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y, num, 1, visited):
                visited[new_y][new_x] = True
                queue.append((new_x, new_y))

    return frames


# Example usage:
image_path = 'path_to_your_image.jpg'
output_folder_path = 'path_for_output_gifs'
os.makedirs(output_folder_path, exist_ok=True)

# Horizontal Row
row_img = create_image_row_or_column(image_path, 3, 'horizontal')
bfs_frames_row = bfs_traversal_linear(row_img, 3, 'horizontal')
save_gif(bfs_frames_row, os.path.join(output_folder_path, 'bfs_row_traversal.gif'))

# Vertical Column
col_img = create_image_row_or_column(image_path, 3, 'vertical')
bfs_frames_col = bfs_traversal_linear(col_img, 3, 'vertical')
save_gif(bfs_frames_col, os.path.join(output_folder_path, 'bfs_col_traversal.gif'))