import MapDesign


if __name__ == '__main__':
    # campus = input('Enter Campus Name: ').title()
    # building = input('Enter Building Name: ').title()
    campus = 'North Campus'
    building = 'Athabasca Hall'

    print()
    print("Building User interface.....")
    print('Fetching data....')

    app = MapDesign.Application(building, campus)
    app.mainloop()
#
# import os
#
# def find_xml_file(root_folder, file_name):
#     for root, _, files in os.walk(root_folder):
#         if file_name in files:
#             print(os.path.join(root, file_name))
#             return os.path.join(root, file_name)
#     return None
#
# print(find_xml_file('Buildings Data', 'xml'))