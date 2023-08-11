import imageio.v2 as imageio
import numpy as np
import os 
from collections import deque

class ImageTraversal:
    def __init__(self, image, start_point, tolerance=0.5):
        self.image = image
        self.start_point = start_point
        self.tolerance = tolerance
        self.visited = [[False for _ in range(image.shape[1])] for _ in range(image.shape[0])]
        self.to_visit = deque([start_point])
        self.width, self.height = image.shape[1], image.shape[0]

    # Inside ImageTraversal class
    def calculate_delta(self, p1, p2):
        return sum(abs(int(p1[i]) - int(p2[i])) for i in range(3))  # Cast to int to handle overflow

    def is_valid(self, point):
        x, y = point
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        if self.visited[y][x]:
            return False
        if self.calculate_delta(self.image[self.start_point[1], self.start_point[0]], self.image[y, x]) >= self.tolerance:
            return False
        return True

    def add(self, point):
        if self.is_valid(point):
            self.to_visit.append(point)

    def pop(self):
        return self.to_visit.popleft()
    
    def begin(self):
        return self.Iterator(self)

    def end(self):
        return None

    class Iterator:
        def __init__(self, traversal):
            self.traversal = traversal
            self.current = traversal.start_point

        def __next__(self):
            if not self.traversal.to_visit:
                raise StopIteration

            self.current = self.traversal.pop()

            x, y = self.current

            # Add neighbors
            neighbors = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
            for n in neighbors:
                self.traversal.add(n)

            return self.current

        def __iter__(self):
            return self


def create_gif_from_folder(folder_path, gif_name='output.gif'):
    frames = []

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            
            # BFS traversal
            image_data_bfs = imageio.imread(image_path)
            bfs_traversal = ImageTraversal(image_data_bfs, (0, 0))
            for point in bfs_traversal.begin():
                x, y = point
                if image_data_bfs.shape[2] == 4:  # Check for alpha channel
                    image_data_bfs[y][x] = [255, 0, 0, 255]  # Red color with full opacity
                else:
                    image_data_bfs[y][x] = [255, 0, 0]
            frames.append(image_data_bfs)  # Append the frame from BFS traversal
            
            # Reload the image data for DFS
            # image_data_dfs = imageio.imread(image_path)
            
            # # DFS traversal
            # dfs_traversal = ImageTraversal(image_data_dfs, (0, 0))
            # for point in dfs_traversal.begin():
            #     x, y = point
            #     if image_data_dfs.shape[2] == 4:  # Check for alpha channel
            #         image_data_dfs[y][x] = [255, 0, 0, 255]  # Red color with full opacity
            #     else:
            #         image_data_dfs[y][x] = [255, 0, 0]
            # frames.append(image_data_dfs)  # Append the frame from DFS traversal

    # Save all the frames as a GIF
    imageio.mimsave(gif_name, frames, duration=0.5)

def main():
    folder_path = "images"
    create_gif_from_folder(folder_path)

if __name__ =='__main__':
    main()