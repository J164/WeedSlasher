from src import vehicle as vehicle_module
from typing import List
import time

if __name__ == '__main__':

    vehicle = vehicle_module.Vehicle(
        {
            "motors": {
                "left": {
                    "pins": {
                        "speed": 13,
                        "control1": 5,
                        "control2": 6
                    }
                },
                "right": {
                    "pins": {
                        "speed": 12,
                        "control1": 7,
                        "control2": 8
                    }
                }
            }
        }
    )

    # Example usage
    grid_test = [[0,1,1,0,0,0],
                 [0,1,1,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0]]
    grid = 6 #input n-foot square grid
    drive_speed = 1
    for i in range(2):
        print('Forward')
        vehicle.drive_forward(drive_speed)
        time.sleep(grid)

        print('Stop')
        vehicle.stop()
        time.sleep(1)

        print('Pivot right')
        vehicle.pivot_right(drive_speed)
        time.sleep(1)

        print('Forward')
        vehicle.drive_forward(drive_speed)
        time.sleep(.8)
        vehicle.stop()

        print('Pivot right')
        vehicle.pivot_right(drive_speed)
        time.sleep(1)

        print('Forward')
        vehicle.drive_forward(drive_speed)
        time.sleep(grid)

        print('Stop')
        vehicle.stop()
        time.sleep(1)

        print('Pivot left')
        vehicle.pivot_left(drive_speed)
        time.sleep(1)

        print('Forward')
        vehicle.drive_forward(drive_speed)
        time.sleep(.8)
        vehicle.stop()

        print('Pivot left')
        vehicle.pivot_left(drive_speed)
        time.sleep(1)
    vehicle.stop()

  




