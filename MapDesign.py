import matplotlib.pyplot as plt


def draw_points(point_list):
    colors = ['red', 'blue', 'green', 'orange', 'black', 'grey', 'yellow', 'pink']  # Define colors for each set
    num_sets = len(point_list) // 4  # Calculate the number of sets
    i = 0
    for coordinatesList in point_list:
        print(coordinatesList)
        n = len(coordinatesList)
        x_coords = []
        y_coords = []

        for coordinates in coordinatesList:
            print('coordinates', coordinates)
            x_coords.append(coordinates[0])
            y_coords.append(coordinates[1])
            print(x_coords, y_coords)

        plt.scatter(x_coords, y_coords, color=colors[i])  # Plot points for each set
        plt.plot(x_coords + [x_coords[0]], y_coords + [y_coords[0]], color=colors[i])



    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Points')
    plt.grid(True)  # Add grid
    plt.show()


points = [

    [[255.5406941, -512.3851514], [214.7050109, -512.3851514], [214.7050109, -598.0542383], [340.6213337, -598.0542383],
     [340.6213337, -494.4147361], [255.5406941, -494.4147361]],
    [[340.6213337, -399.6321009], [214.7050109, -399.6321009], [214.7050109, -476.4443208], [255.5406941, -476.4443208],
     [255.5406941, -494.4147361], [340.6213337, -494.4147361]],
    [[214.7050109, -512.3851514], [148.6932796, -512.3851514], [148.6932796, -598.0542383],
     [214.7050109, -598.0542383]],
    [[214.7050109, -399.632101], [148.6932796, -399.632101], [148.6932796, -476.4443209], [214.7050109, -476.4443209]],
    [[82.6815484, -598.0542383], [148.6932797, -598.0542383], [148.6932797, -512.3851514], [82.6815484, -512.3851514]],
    [[148.6932797, -399.632101], [82.6815484, -399.632101], [82.6815484, -476.4443209], [148.6932797, -476.4443209]],
    [[82.6815484, -598.0542383], [82.6815484, -512.3851514], [20.6321581, -512.3851514], [20.6321581, -598.0542383]],
    [[20.6321581, -598.0542383], [20.6321581, -512.3851514], [-41.4172322, -512.3851514], [-41.4172322, -598.0542383]],
    [[-41.4172321, -449.8342254], [-140.2703208, -449.8342254], [-140.2703208, -598.0542383],
     [-41.4172321, -598.0542383]],
    [[-140.2703208, -382.0143266], [-140.2703208, -449.8342254], [-41.4172321, -449.8342254],
     [-41.4172321, -382.0143266]],
    [[-140.2703208, -318.5483283], [-140.2703208, -382.0143267], [-41.4172321, -382.0143267],
     [-41.4172321, -318.5483283]],
    [[67.3092877, -387.2523456], [67.3092877, -308.3447892], [-10.3567719, -308.3447892], [-10.3567719, -387.2523456]],
    [[-140.2703208, -258.9454801], [-140.2703208, -318.5483282], [-41.4172321, -318.5483282],
     [-41.4172321, -258.9454801]],
    [[-10.3567719, -246.6016095], [-10.3567719, -308.3447892], [67.3092877, -308.3447892], [67.3092877, -246.6016095]],
    [[-140.2703208, -200.4901816], [-140.2703208, -258.9454801], [-41.4172321, -258.9454801],
     [-41.4172321, -200.4901816]],
    [[-10.3567719, -182.2515306], [-10.3567719, -246.6016095], [67.3092877, -246.6016095], [67.3092877, -182.2515306]],
    [[-140.2703208, -132.8978871], [-140.2703208, -200.4901816], [-41.4172321, -200.4901816],
     [-41.4172321, -132.8978871]],
    [[-10.3567719, -137.3014595], [-10.3567719, -182.2515306], [67.3092877, -182.2515306], [67.3092877, -137.3014595]],
    [[87.9289516, -65.4515058], [67.3092878, -43.6886937], [-10.3567718, -43.6886937], [-10.3567718, -137.3014594],
     [67.3092878, -137.3014594], [87.9289516, -115.5386473]],
    [[87.9289516, 115.5386473], [67.3092878, 137.3014594], [-10.3567718, 137.3014594], [-10.3567718, 43.6886937],
     [67.3092878, 43.6886937], [87.9289516, 65.4515058]],
    [[-41.4172321, 138.8153014], [-41.4172321, 199.9136667], [-140.2703208, 199.9136667], [-140.2703208, 138.8153014]],
    [[67.3092877, 137.3014594], [67.3092877, 199.1567456], [-10.3567719, 199.1567456], [-10.3567719, 137.3014594]],
    [[-140.2703208, 261.0120319], [-140.2703208, 199.9136666], [-41.4172321, 199.9136666], [-41.4172321, 261.0120319]],
    [[-10.3567719, 261.0120319], [-10.3567719, 199.1567457], [67.3092877, 199.1567457], [67.3092877, 261.0120319]],
    [[-41.4172321, 261.0120319], [-41.4172321, 325.393846], [-140.2703208, 325.393846], [-140.2703208, 261.0120319]],
    [[67.3092877, 261.0120319], [67.3092877, 325.393846], [-10.3567719, 325.393846], [-10.3567719, 261.0120319]],
    [[-140.2703208, 389.7756601], [-140.2703208, 325.393846], [-41.4172321, 325.393846], [-41.4172321, 389.7756601]],
    [[-10.3567719, 389.7756601], [-10.3567719, 325.393846], [67.3092877, 325.393846], [67.3092877, 389.7756601]],
    [[-140.2703208, 454.359175], [-140.2703208, 389.7756601], [-41.4172321, 389.7756601], [-41.4172321, 454.359175]],
    [[-140.2703208, 598.0542383], [-140.2703208, 454.359175], [-41.4172321, 454.359175], [-41.4172321, 598.0542383]],
    [[15.8278114, 598.0542383], [-41.4172322, 598.0542383], [-41.4172322, 514.3500648], [15.8278114, 514.3500648]],
    [[82.718828, 483.2523249], [82.718828, 399.632101], [146.4922733, 399.632101], [146.4922733, 483.2523249]],
    [[146.4922733, 598.0542383], [93.6795068, 598.0542383], [93.6795068, 514.3500648], [146.4922733, 514.3500648]],
    [[146.4922733, 399.632101], [211.3541816, 399.632101], [211.3541816, 483.2523249], [146.4922733, 483.2523249]],
    [[146.4922733, 514.3500648], [211.3541816, 514.3500648], [211.3541816, 598.0542383], [146.4922733, 598.0542383]],
    [[255.5406941, 483.2523249], [211.3541815, 483.2523249], [211.3541815, 399.632101], [340.6213337, 399.632101],
     [340.6213337, 498.8011949], [255.5406941, 498.8011949]],
    [[340.6213337, 598.0542383], [211.3541815, 598.0542383], [211.3541815, 514.3500648], [255.5406941, 514.3500648],
     [255.5406941, 498.8011948], [340.6213337, 498.8011948]],
    [[110.7874636, 377.1426375], [89.9720077, 356.3271816], [88.4694058, 357.8297835], [109.2848617, 378.6452394]],
    [[90.30792, -357.9005308], [109.7533565, -377.3459673], [108.869473, -378.2298508], [89.4240365, -358.7844143]],
    [[-41.4172321, 61.9490356], [-41.4172321, 112.2615356], [-84.8547321, 112.2615356], [-84.8547321, 61.9490356]],
    [[-41.4172321, -32.2116576], [-140.2703208, -32.2116576], [-140.2703208, -58.0559076000001],
     [-41.4172321, -58.0559076000001], [-41.4172321, -512.3851514], [255.5406941, -512.3851514],
     [255.5406941, -476.4443208], [82.6815484, -476.4443208], [82.6815484, -485.6435555], [-10.3567718, -485.6435555],
     [-10.3567718, 492.1738077], [82.718828, 492.1738077], [82.718828, 483.2523249], [255.5406941, 483.2523249],
     [255.5406941, 514.3500648], [93.6795068, 514.3500648], [93.6795068, 542.6170882], [15.8278115, 542.6170882],
     [15.8278115, 514.3500648], [-41.4172321, 514.3500648]],
    [[82.6815484, -399.632101], [114.2659829, -399.632101], [104.409542, -389.7756601], [112.4124122, -381.7727899],
     [85.1685988, -354.5289765], [77.1657287, -362.5318467], [67.3092878, -352.6754058], [67.3092878, -387.2523456],
     [26.6036568, -387.2523456], [26.6036568, -485.6435555], [82.6815484, -485.6435555]],
    [[-41.4172321, -132.8978871], [-41.4172321, -58.0559076], [-140.2703208, -58.0559076],
     [-140.2703208, -132.8978871]],
    [[26.6036568, 389.77566], [67.3092878, 389.77566], [67.3092878, 352.6754058], [77.1657287, 362.5318467],
     [85.1685988, 354.5289765], [112.4124122, 381.7727899], [104.409542, 389.77566], [114.2659829, 399.6321009],
     [82.718828, 399.6321009], [82.718828, 492.1738076], [26.6036568, 492.1738076]],
    [[26.6036567, -485.6435555], [26.6036567, -436.4479506], [-10.3567719, -436.4479506], [-10.3567719, -485.6435555]],
    [[-10.3567719, 492.1738077], [-10.3567719, 432.8046146], [26.6036567, 432.8046146], [26.6036567, 492.1738077]],
    [[-10.3567719, -387.2523456], [-10.3567719, -436.4479505], [26.6036567, -436.4479505], [26.6036567, -387.2523456]],
    [[26.6036567, 389.7756601], [26.6036567, 432.8046146], [-10.3567719, 432.8046146], [-10.3567719, 389.7756601]],
    [[-140.2703208, -32.2116576], [-41.4172321, -32.2116576], [-41.4172321, 138.8153014], [-140.2703208, 138.8153014]],
    [[-140.2703208, -89.6895339], [-140.2703208, 94.8577095], [-229.4851484, 94.8577095], [-229.4851484, 277.1108574],
     [-340.6213337, 277.1108574], [-340.6213337, -89.6895339]],
    [[67.3092877, -43.6886937], [67.3092877, 43.6886937], [-10.3567719, 43.6886937], [-10.3567719, -43.6886937]],
    [[15.8278114, 598.0542383], [15.8278114, 542.6170882], [93.6795068, 542.6170882], [93.6795068, 598.0542383]],

]
draw_points(points)
