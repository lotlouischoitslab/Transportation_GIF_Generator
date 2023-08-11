import imageio.v2 as imageio
import numpy as np
import os 
from collections import deque

class ImageTraversal:
    def __init__(self, image, start_point, tolerance=0.5):
        self.image = image
        self.start_point = start_point
        self.tolerance = tolerance
        self.visited = np.zeros(image.shape[:2], dtype=bool)
        self.traverse_order = self.get_traversal_order()

    def calculate_distance(self, p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def is_within_tolerance(self, point):
        start_color = self.image[self.start_point[1], self.start_point[0]]
        point_color = self.image[point[1], point[0]]
        return self.calculate_distance(start_color, point_color) <= self.tolerance

    def get_traversal_order(self):
        points = []
        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                if self.is_within_tolerance((x, y)):
                    points.append((x, y))
        return points
    
    def __iter__(self):
        return iter(self.traverse_order)


def create_gif_from_folder(folder_path, gif_name='output.gif'):
    frames = []

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            image_data = imageio.imread(image_path)
            
            bfs_image_data = image_data.copy()
            bfs_traversal = ImageTraversal(bfs_image_data, (0, 0))
            frame_count = 0
            for point in bfs_traversal:
                x, y = point
                if bfs_image_data.shape[2] == 4:  # Check for alpha channel
                    bfs_image_data[y][x] = [255, 0, 0, 255]  # Red color with full opacity
                else:
                    bfs_image_data[y][x] = [255, 0, 0]
                frame_count += 1
                
                frames.append(bfs_image_data.copy())

            # Similar for DFS traversal ...

    imageio.mimsave(gif_name, frames, duration=0.5)

def main():
    folder_path = "images"
    create_gif_from_folder(folder_path)

if __name__ =='__main__':
    main()