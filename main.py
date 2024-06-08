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


def plotFloorMap():
    MapDesign.draw_points(points_categories, category_names)


if __name__ == '__main__':
    # for i in range(1, 5):

    categorizesCoordinateMap(4)

    points_categories = [RoomPoints, EntrancePoints, ElevatorPoints, HallwayPoints, WashroomPoints, StairPoints,
                         XPoints, BuildingPoints, All_GenderPoints]
    category_names = ['RoomPoints', 'EntrancePoints', 'ElevatorPoints', 'HallwayPoints', 'WashroomPoints',
                      'StairPoints', 'XPoints', 'BuildingPoints', 'All_GenderPoints']
    plotFloorMap()
