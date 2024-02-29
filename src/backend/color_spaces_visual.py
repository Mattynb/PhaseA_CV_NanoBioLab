import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Original color ranges
"""
original_ranges = {
    "Red": {"min": (122, 13, 34), "max": (208, 145, 160)},
    "Blue": {"min": (7, 19, 139s), "max": (147, 148, 242)},
    "Green": {"min": (80, 117, 54), "max": (163, 181, 156)},
    "Purple": {"min": (83, 36, 143), "max": (148, 122, 206)}
}
"""
# Adjusted color ranges
adjusted_ranges = {
    "Red": {"min": (150,0,0), "max": (255,150,87+40)},
    "Blue": {"min": (49-40,77-40,150), "max": (110,77+40+50,255)},
    "Green": {"min": (50,100,0), "max": (149,255,125)},
    "Purple": {"min": (111,78-40,150), "max": (255+25,78+40+50,255)},
    #"Red2": {"min" : (161,101,100), "max" : (200,125,150)},    
}

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

fig = plt.figure()

"""
# Plot for original ranges with cube faces
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title('Original Color Ranges with Faces')
ax1.set_xlabel('R')
ax1.set_ylabel('G')
ax1.set_zlabel('B')
"""
# Plot for adjusted ranges with cube faces
ax2 = fig.add_subplot(projection='3d')
ax2.set_title('Adjusted Color Ranges with Faces')
ax2.set_xlabel('R')
ax2.set_ylabel('G')
ax2.set_zlabel('B')

# Colors for drawing
colors = ['r', 'b', 'g', 'm', 'r']

"""
# Draw original ranges with cube faces
for i, (color, range) in enumerate(original_ranges.items()):
    draw_cube(ax1, range['min'], range['max'], colors[i])
"""

# Draw adjusted ranges with cube faces
for i, (color, range) in enumerate(adjusted_ranges.items()):
    draw_cube(ax2, range['min'], range['max'], colors[i])

# Add other custom points to the plot
customs = [
{      
    "Red": [114, 159, 80],
    "1":  [123, 77, 188],
    "2": [125, 75, 195],
    "3": [125, 70, 200]
},
]

i =3
for custom in customs:
    for color, point in custom.items():
        #ax1.scatter(*point, color=colors[i], s=100, label=colors[i])
        ax2.scatter(*point, color=colors[i], s=100, label=colors[i])
        
    i += 1

plt.show()