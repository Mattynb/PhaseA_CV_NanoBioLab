import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Original color ranges
original_ranges = {
    "Red": {"min": (122, 13, 34), "max": (208, 145, 160)},
    "Blue": {"min": (7, 19, 139), "max": (147, 148, 242)},
    "Green": {"min": (80, 117, 54), "max": (163, 181, 156)},
    "Purple": {"min": (83, 36, 143), "max": (148, 122, 206)}
}

# Adjusted color ranges
adjusted_ranges = {
    "Red": {"min": (122, 13, 34), "max": (208, 100, 130)},
    "Blue": {"min": (7, 19, 139), "max": (100, 130, 242)},
    "Green": {"min": (80, 117, 54), "max": (140, 181, 120)},
    "Purple": {"min": (100, 30, 143), "max": (160, 100, 206)}
}

fig = plt.figure(figsize=(14, 7))

# Plot for original ranges
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title('Original Color Ranges')
ax1.set_xlabel('R')
ax1.set_ylabel('G')
ax1.set_zlabel('B')

# Plot for adjusted ranges
ax2 = fig.add_subplot(122, projection='3d')
ax2.set_title('Adjusted Color Ranges')
ax2.set_xlabel('R')
ax2.set_ylabel('G')
ax2.set_zlabel('B')

# Helper function to plot ranges
def plot_ranges(ax, ranges, colors):
    for color, range in ranges.items():
        min_corner = range['min']
        max_corner = range['max']
        
        # Generate corners of the rectangle
        corners = [
            [min_corner[0], min_corner[1], min_corner[2]],  # Min corner
            [min_corner[0], min_corner[1], max_corner[2]],  # Min, min, max
            [min_corner[0], max_corner[1], min_corner[2]],  # Min, max, min
            [min_corner[0], max_corner[1], max_corner[2]],  # Min, max, max
            [max_corner[0], min_corner[1], min_corner[2]],  # Max, min, min
            [max_corner[0], min_corner[1], max_corner[2]],  # Max, min, max
            [max_corner[0], max_corner[1], min_corner[2]],  # Max, max, min
            [max_corner[0], max_corner[1], max_corner[2]]   # Max corner
        ]
        
        # Convert corners to XYZ format for plotting
        xs, ys, zs = zip(*corners)
        
        # Plot
        ax.scatter(xs, ys, zs, label=color, alpha=0.5)
        ax.legend()

# Plot original ranges
plot_ranges(ax1, original_ranges, ['r', 'g', 'b', 'm'])

# Plot adjusted ranges
plot_ranges(ax2, adjusted_ranges, ['r', 'g', 'b', 'm'])


def draw_cube(ax, min_corner, max_corner, color):
    # Generate corners of the cube
    corners = [
        [min_corner[0], min_corner[1], min_corner[2]],  # 0
        [max_corner[0], min_corner[1], min_corner[2]],  # 1
        [max_corner[0], max_corner[1], min_corner[2]],  # 2
        [min_corner[0], max_corner[1], min_corner[2]],  # 3
        [min_corner[0], min_corner[1], max_corner[2]],  # 4
        [max_corner[0], min_corner[1], max_corner[2]],  # 5
        [max_corner[0], max_corner[1], max_corner[2]],  # 6
        [min_corner[0], max_corner[1], max_corner[2]]   # 7
    ]

    # List of sides, each side is a list of 4 corners
    sides = [
        [0, 1, 2, 3],  # Bottom
        [4, 5, 6, 7],  # Top
        [0, 1, 5, 4],  # Side
        [1, 2, 6, 5],  # Side
        [2, 3, 7, 6],  # Side
        [3, 0, 4, 7]   # Side
    ]

    for side in sides:
        xs = [corners[corner][0] for corner in side]
        ys = [corners[corner][1] for corner in side]
        zs = [corners[corner][2] for corner in side]
        # Close the loop
        xs.append(xs[0])
        ys.append(ys[0])
        zs.append(zs[0])
        
        ax.plot(xs, ys, zs, color=color)

fig = plt.figure(figsize=(14, 7))

# Plot for original ranges with cube faces
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title('Original Color Ranges with Faces')
ax1.set_xlabel('R')
ax1.set_ylabel('G')
ax1.set_zlabel('B')

# Plot for adjusted ranges with cube faces
ax2 = fig.add_subplot(122, projection='3d')
ax2.set_title('Adjusted Color Ranges with Faces')
ax2.set_xlabel('R')
ax2.set_ylabel('G')
ax2.set_zlabel('B')

# Colors for drawing
colors = ['r', 'b', 'g', 'm']

# Draw original ranges with cube faces
for i, (color, range) in enumerate(original_ranges.items()):
    draw_cube(ax1, range['min'], range['max'], colors[i])

# Draw adjusted ranges with cube faces
for i, (color, range) in enumerate(adjusted_ranges.items()):
    draw_cube(ax2, range['min'], range['max'], colors[i])

plt.show()