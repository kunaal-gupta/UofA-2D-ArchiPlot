class RoomManager:
    def __init__(self, rooms, campus, building, floor):
        self.rooms = rooms  # rooms should be a list of room coordinates
        self.campus = campus
        self.building = building
        self.floor = floor

    def are_neighbouring_rooms(self, room1, room2):
        from FindingNeigbour import Neighbours
        neighbours = Neighbours()
        return neighbours.are_rooms_neighbors(room1, room2)

    def generating_neighbours(self):
        default_file_name = 'NeighboringRooms.txt'
        output_file = input(f'Enter File name to store neighbouring rooms data. Default {default_file_name}, otherwise press enter: ')
        if output_file == '':
            output_file = default_file_name

        with open(output_file, 'a') as file:
            if file.tell() == 0:
                print(f'Created {output_file} to store neighbouring rooms data')
            else:
                print(f'Appending data to {output_file}')

            for i in range(len(self.rooms)):
                for j in range(i + 1, len(self.rooms)):
                    room1_name = self.rooms[i][0][0]
                    room1 = self.rooms[i][1:]
                    room2_name = self.rooms[j][0][0]
                    room2 = self.rooms[j][1:]

                    if self.are_neighbouring_rooms(room1, room2):
                        file.write(f"Campus: {self.campus}, Building: {self.building}, Floor: {self.floor}, Neighbours: [{room1_name} & {room2_name}].\n")
            file.write("\n\n")

        print(f"Neighboring rooms have been written to {output_file}.")
