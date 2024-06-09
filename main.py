from matplotlib import pyplot as plt

import MapDesign
import XMLDataExtract

RoomPoints = []
EntrancePoints = []
ElevatorPoints = []
HallwayPoints = []
WashroomPoints = []
StairPoints = []
XPoints = []
BuildingPoints = []
All_GenderPoints = []


def fetchCoordinateMap(floorNumber):
    return XMLDataExtract.main(floorNumber=floorNumber)


def categorizesCoordinateMap(floorNumber: int):
    CoordinateMap = fetchCoordinateMap(floorNumber)

    global RoomPoints, EntrancePoints, ElevatorPoints, HallwayPoints, WashroomPoints, StairPoints, XPoints

    RoomPoints = CoordinateMap['Room']
    EntrancePoints = CoordinateMap['Entrance']
    ElevatorPoints = CoordinateMap['Elevator']
    HallwayPoints = CoordinateMap['Hallway']
    WashroomPoints = CoordinateMap['Washroom']
    StairPoints = CoordinateMap['Stairs']
    XPoints = CoordinateMap['X']


def plotFloorMap(i):
    title = f'Architectural Map of Floor {i}'
    app = MapDesign.Application(points_categories, category_names, title)
    app.mainloop()

floor = int(input('Which Floor: '))
if __name__ == '__main__':
    # for i in range(1, 5):
    categorizesCoordinateMap(floor)

    points_categories = [RoomPoints, EntrancePoints, ElevatorPoints, HallwayPoints, WashroomPoints, StairPoints,
                         XPoints, BuildingPoints, All_GenderPoints]
    category_names = ['RoomPoints', 'EntrancePoints', 'ElevatorPoints', 'HallwayPoints', 'WashroomPoints',
                      'StairPoints', 'XPoints', 'BuildingPoints', 'All_GenderPoints']
    plotFloorMap(floor)
