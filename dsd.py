import matplotlib.pyplot as plt

# Input string with 3D coordinates separated by "|"
coordinate_string = "255.5406941,0,-512.3851514|214.7050109,0,-512.3851514|214.7050109,0,-598.0542383|340.6213337,0,-598.0542383|340.6213337,0,-494.4147361|255.5406941,0,-494.4147361"

# Split the string into individual coordinates
coordinates = coordinate_string.split("|")

# Extract the x and z coordinates
x_coords = []
z_coords = []

for coord in coordinates:
    x, y, z = map(float, coord.split(","))
    x_coords.append(x)
    z_coords.append(z)

# Plotting the coordinates
plt.figure(figsize=(8, 6))
plt.plot(x_coords, z_coords, 'bo-', label="Polygon")
plt.xlabel('X Coordinates')
plt.ylabel('Z Coordinates')
plt.title('2D Plot of Coordinates (X, Z)')
plt.grid(True)
plt.legend()
plt.show()
