from src import vehicle as vehicle_module
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

    vehicle.drive_forward(3)
    time.sleep(6)
    vehicle.drive_backward(3)
    time.sleep(6)
    vehicle.stop()