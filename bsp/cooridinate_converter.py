import math
from geopy.distance import geodesic
from geopy.point import Point

def shifted_coords(latitude, longitude, x_change_meters, y_change_meters):

    distance = math.sqrt(x_change_meters**2 + y_change_meters**2)

    if distance == 0:
        return latitude, longitude

    angle_rad = math.atan2(x_change_meters,y_change_meters)
    bearing_degrees = (math.degrees(angle_rad) + 360) % 360

    start_point = Point(latitude=latitude, longitude=longitude)

    dist_object = geodesic(meters=distance)

    new_coords = dist_object.destination(point=start_point, bearing=bearing_degrees)

    return new_coords.latitude, new_coords.longitude


    