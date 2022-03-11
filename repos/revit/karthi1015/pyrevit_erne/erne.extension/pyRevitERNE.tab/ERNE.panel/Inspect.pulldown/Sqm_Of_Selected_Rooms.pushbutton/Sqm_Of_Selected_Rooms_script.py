"""
Square meters of selected rooms
"""
from rpw import doc, uidoc

selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]

total_area = 0.0

for elem in selection:
    if elem.Category.Name == "Rooms":
        room = elem
        room_area = room.Area
        total_area += room_area

convert_sftsqm = 10.764
print("Total sqm of selected rooms: ")
print(total_area / convert_sftsqm)
