from src import vehicle as vehicle_module
from src import distance_sensor as distance_sensor_module
from typing import List
import time
import numpy as np
import detection.script as model

isStopped = False

distance_sensor1 = distance_sensor_module.DistanceSensor({
        "pins": {
            "echo": 23,
            "trigger": 24
        }
    })

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
    grid = 6 #input n x m-foot square grid
    drive_speed = 3
    def turn90right():
        vehicle.pivot_right(3)
        time.sleep(0.61)
        vehicle.stop()
        time.sleep(0.5)
        vehicle.stop()
        
    def turn90left():
        vehicle.pivot_left(3)
        time.sleep(0.61)
        vehicle.stop()
        time.sleep(0.5)
        vehicle.stop()
        
    def forwardN(tiles):
        for i in range (tiles*12):
            vehicle.drive_forward(3)
            time.sleep(0.1)
            distance = distance_sensor1.distance
            print (distance)
            if (distance <= 0.23):
                vehicle.stop()
                #model.classify('build/model')
                return True
        vehicle.stop()
        time.sleep(0.5)
        vehicle.stop()
        return False
        


    test = np.array([[1,0,0,0,0],
                     [1,0,0,0,0],
                     [1,0,0,0,0]

    ])

    def swerve():
        turn90right()
        

    def navigate(array):
        for i in range (array[0].size):
        
            if (forwardN(len(array))):
                break

            if (i%2 == 0):
                turn90right()
                forwardN(1)
                turn90right()

            if (i%2 == 1):
                turn90left()
                forwardN(1)
                turn90left()
    
    def navigate2(length, width):
        for i in range (width):
            if (forwardN(length)):
                break

            if (i%2 == 0):
                turn90right()
                forwardN(1)
                turn90right()

            if (i%2 == 1):
                turn90left()
                forwardN(1)
                turn90left()

    
    navigate2(2,2)