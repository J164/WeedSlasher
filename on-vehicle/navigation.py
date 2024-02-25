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
        time.sleep(0.47)
        vehicle.stop()
        time.sleep(0.5)
        vehicle.stop()
        
    def turn90left():
        vehicle.pivot_left(3)
        time.sleep(0.48)
        vehicle.stop()
        time.sleep(0.5)
        vehicle.stop()
        
        #Drives forwards and detects
    def forwardN(tiles):
        for i in range (tiles*12):
            vehicle.drive_forward(3)
            time.sleep(0.1)
            distance = distance_sensor1.distance
            print (distance)

            #Checks distance sensor and checks if weed if object is close

            if (distance <= 0.25):
                vehicle.stop()
                classify = model.classify('build/model')
                
                print(classify)
                if(classify):
                    cut()
                else:
                    swerve()
                return True


        vehicle.stop()
        time.sleep(0.5)
        vehicle.stop()
        return False

    #drives forward but does not detect
    def forward1():
        vehicle.drive_forward(3)
        time.sleep(2.3)
        vehicle.stop()
        time.sleep(0.5)

    def forward2():
        vehicle.drive_forward(3)
        time.sleep(1.3)
        vehicle.stop()
        time.sleep(0.7)

    def cut():
        forward1()

    def swerve():
        turn90right()
        forward2()
        turn90left()
        forward1()
        turn90left()
        forward2()
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

    
    test = np.array([[1,0,0,0,0],
                     [1,0,0,0,0],
                     [1,0,0,0,0]

    ])

    navigate2(1,4)
    forwardN(2)