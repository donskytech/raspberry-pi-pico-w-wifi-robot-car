from machine import Pin
from machine import PWM
import utime

"""
Class to represent our robot car
"""


class RobotCar:
    MAX_DUTY_CYCLE = 65535
    MIN_DUTY_CYCLE = 0

    MAX_DUTY_CYCLE_SETTINGS = 30000
    MIN_DUTY_CYCLE_SETTINGS = 55000

    MAX_SPEED_VALUE = 100
    MIN_SPEED_VALUE = 0

    def __init__(self, motor_pins, frequency=20000):
        self.left_motor_pin1 = PWM(Pin(motor_pins[0], mode=Pin.OUT))
        self.left_motor_pin2 = PWM(Pin(motor_pins[1], mode=Pin.OUT))
        self.right_motor_pin1 = PWM(Pin(motor_pins[2], mode=Pin.OUT))
        self.right_motor_pin2 = PWM(Pin(motor_pins[3], mode=Pin.OUT))
        # set PWM frequency
        self.left_motor_pin1.freq(frequency)
        self.left_motor_pin2.freq(frequency)
        self.right_motor_pin1.freq(frequency)
        self.right_motor_pin2.freq(frequency)
        # Initialize the current speed to 100% or 30000 (the lower the PWM the faster the motor)
        self.current_speed = RobotCar.MAX_SPEED_VALUE
        self.current_duty_cycle = RobotCar.MAX_DUTY_CYCLE_SETTINGS

    def move_forward(self):
        print("Car is moving forward")
        self.left_motor_pin1.duty_u16(RobotCar.MAX_DUTY_CYCLE)
        self.left_motor_pin2.duty_u16(self.__get_current_duty_cycle())

        self.right_motor_pin1.duty_u16(RobotCar.MAX_DUTY_CYCLE)
        self.right_motor_pin2.duty_u16(self.__get_current_duty_cycle())

    def move_backward(self):
        print("Car is moving backward...")
        self.left_motor_pin1.duty_u16(self.__get_current_duty_cycle())
        self.left_motor_pin2.duty_u16(RobotCar.MAX_DUTY_CYCLE)

        self.right_motor_pin1.duty_u16(self.__get_current_duty_cycle())
        self.right_motor_pin2.duty_u16(RobotCar.MAX_DUTY_CYCLE)

    def turn_left(self):
        print("Car is moving left...")
        self.left_motor_pin1.duty_u16(RobotCar.MAX_DUTY_CYCLE)
        self.left_motor_pin2.duty_u16(self.__get_current_duty_cycle())

        self.right_motor_pin1.duty_u16(RobotCar.MAX_DUTY_CYCLE)
        self.right_motor_pin2.duty_u16(RobotCar.MAX_DUTY_CYCLE)

    def turn_right(self):
        print("Car is moving right...")
        self.left_motor_pin1.duty_u16(RobotCar.MAX_DUTY_CYCLE)
        self.left_motor_pin2.duty_u16(RobotCar.MAX_DUTY_CYCLE)

        self.right_motor_pin1.duty_u16(RobotCar.MAX_DUTY_CYCLE)
        self.right_motor_pin2.duty_u16(self.__get_current_duty_cycle())

    def stop(self):
        print("Stopping car...")
        self.left_motor_pin1.duty_u16(RobotCar.MAX_DUTY_CYCLE)
        self.left_motor_pin2.duty_u16(RobotCar.MAX_DUTY_CYCLE)

        self.right_motor_pin1.duty_u16(RobotCar.MAX_DUTY_CYCLE)
        self.right_motor_pin2.duty_u16(RobotCar.MAX_DUTY_CYCLE)

    """ 
        Map duty cycle values from 0-100 to duty cycle 30000-55000
        The lower the PWM, the faster the motor moves
        0 	- 	55000
        50 	- 	42500
        100 - 	30000
    """

    def __map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    """ new_speed is a value from 0% - 100% """

    def change_speed(self, new_speed):
        # Compute the current duty cyle based on the new_speed percentage
        self.current_duty_cycle = self.__map_range(
            int(new_speed),
            RobotCar.MIN_SPEED_VALUE,
            RobotCar.MAX_SPEED_VALUE,
            RobotCar.MIN_DUTY_CYCLE_SETTINGS,
            RobotCar.MAX_DUTY_CYCLE_SETTINGS,
        )
        self.current_speed = new_speed

    def get_current_speed(self):
        return self.current_speed

    def __get_current_duty_cycle(self):
        return self.current_duty_cycle

    def deinit(self):
        """deinit PWM Pins"""
        print("Deinitializing PWM Pins")
        self.stop()
        utime.sleep_us(1)
        self.left_motor_pin1.deinit()
        self.left_motor_pin2.deinit()
        self.right_motor_pin1.deinit()
        self.right_motor_pin2.deinit()
