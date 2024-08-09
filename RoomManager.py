class RoomManager:
    def __init__(self, rooms):
        self.rooms = rooms  # rooms should be a list of room coordinates

    def are_neighbouring_rooms(self, room1, room2):
        """ Determine if two rooms are neighbors based on shared edges or vertices. """
        from FindingNeigbour import Neighbours
        neighbours = Neighbours()
        return neighbours.are_rooms_neighbors(room1, room2)

    def generating_neigbours(self):
        """ Generate a text file listing neighboring rooms. """
        output_file = 'neighboring_rooms.txt'

        with open(output_file, 'w') as file:
            # Loop through each pair of rooms
            for i in range(len(self.rooms)):
                for j in range(i + 1, len(self.rooms)):  # Ensure not to check the same pair twice
                    room1 = self.rooms[i]
                    room2 = self.rooms[j]
                    print(room1, room2)

                    if self.are_neighbouring_rooms(room1, room2):
                        file.write(f"Room {i} and Room {j} are neighbors.\n")

        print(f"Neighboring rooms have been written to {output_file}.")

# Example usage
rooms = [
    [(1, 2), (3, 4), (4, 4), (5, 2)],  # Room 1 coordinates
    [(3, 4), (6, 3), (6, 1), (3, 1)],  # Room 2 coordinates
    # Add more rooms as needed
]

room_manager = RoomManager(rooms)
room_manager.generating_neigbours()
