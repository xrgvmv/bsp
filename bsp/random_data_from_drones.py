import random
from database import db
from bsp.models import RemoteID

def random_coordinate(base, variance):
    return base + random.uniform(-variance, variance)

def add_random_data_from_drone_to_db():
    base_latitude = 54.352025
    base_longitude = 18.646638

    new_remoteid = RemoteID(
        status=random.choice([0, 1]),
        direction=random.uniform(0, 360),
        speed_horizontal=random.uniform(0, 20), 
        speed_vertical=random.uniform(-5, 5),  
        latitude=random_coordinate(base_latitude, 0.01),
        longitude=random_coordinate(base_longitude, 0.01),
        altitude_baro=random.uniform(50, 200),   
        altitude_geo=random.uniform(45, 195),    
        height_type=random.choice([1, 2]),
        height=random.uniform(0, 100),          
        horiz_accuracy=random.randint(1, 3),    
        vert_accuracy=random.randint(1, 3),     
        baro_accuracy=random.randint(1, 3),     
        speed_accuracy=random.randint(1, 3),      
        ts_accuracy=random.randint(1, 3),        
        timestamp=random.uniform(1234567890.0, 1234567890.0 + 10000)  
    )

    db.session.add(new_remoteid)
    db.session.commit()
