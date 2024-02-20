import math
import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
from statistics import mean


# Use the rotation matrices for each axis
# Formula is v_new = Tx * Ty * Tz * v
def rotated_cube(cube, angle_x, angle_y, angle_z):
    # Get the rotation matrices for each axis based on angle of rotation in that angle
    Tx = get_tx(angle_x)
    Ty = get_ty(angle_y)
    Tz = get_tz(angle_z)

    rotatedcube = [Tx @ Ty @ Tz @ point for point in cube]

    return rotatedcube


# The projection takes the x and y coordinates from each (x,y,z)
def get_projection(rotatedcube):
    p = np.matrix([[1, 0, 0], [0, 1, 0]])
    two_d_projection = [(p @ point).transpose().tolist()[0] for point in rotatedcube]
    return two_d_projection


# Get the convex hull and then the area of the perimeter
def get_area_of_convex_hull(two_d_projection):
    hull = ConvexHull(two_d_projection).vertices
    hull_points = tuple([tuple(two_d_projection[i]) for i in hull.tolist()])
    polygon = Polygon(hull_points)
    return polygon.area


# Putting all of them together
def rotate_and_get_projected_area(cube, angle_x, angle_y, angle_z):
    new_cube = rotated_cube(cube, angle_x, angle_y, angle_z)
    projection = get_projection(new_cube)
    area = get_area_of_convex_hull(projection)
    return area


# Variables to save intermediate results for the translation matrices
matrices_x = [None] * 45
matrices_y = [None] * 45
matrices_z = [None] * 45


# Get translation matrix for the x axis
def get_tx(angle_x):
    if matrices_x[angle_x] is None:
        matrices_x[angle_x] = np.matrix([[1, 0, 0],
                                         [0, math.cos(math.radians(angle_x)), -math.sin(math.radians(angle_x))],
                                         [0, math.sin(math.radians(angle_x)), math.cos(math.radians(angle_x))]])

    return matrices_x[angle_x]


# Get translation matrix for the y axis
def get_ty(angle_y):
    if matrices_y[angle_y] is None:
        matrices_y[angle_y] = np.matrix([[math.cos(math.radians(angle_y)), 0, math.sin(math.radians(angle_y))],
                                         [0, 1, 0],
                                         [-math.sin(math.radians(angle_y)), 0, math.cos(math.radians(angle_y))]])

    return matrices_y[angle_y]


# Get translation matrix for the z axis
def get_tz(angle_z):
    if matrices_z[angle_z] is None:
        matrices_z[angle_z] = np.matrix([[math.cos(math.radians(angle_z)), -math.sin(math.radians(angle_z)), 0],
                                         [math.sin(math.radians(angle_z)), math.cos(math.radians(angle_z)), 0],
                                         [0, 0, 1]])

    return matrices_z[angle_z]


# Define the default cube
cube = [np.matrix([[0], [0], [0]]), np.matrix([[0], [0], [1]]), np.matrix([[0], [1], [0]]), np.matrix([[0], [1], [1]]),
        np.matrix([[1], [0], [0]]), np.matrix([[1], [0], [1]]), np.matrix([[1], [1], [0]]), np.matrix([[1], [1], [1]])]

# Rotate the cube and log the area
areas = []
for x in range(45):
    for y in range(45):
        for z in range(45):
            areas.append(rotate_and_get_projected_area(cube, x, y, z))

print(mean(areas))