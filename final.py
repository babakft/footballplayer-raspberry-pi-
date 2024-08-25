import threading
import RPi.GPIO as GPIO
from pyPS4Controller.controller import Controller
import cv2
import imutils
import numpy as np

FORWARD_IN_1 = 27
FORWARD_IN_2 = 17
BACKWARD_IN_1 = 20
BACKWARD_IN_2 = 21
SHOOTER = 16


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        ###########
        GPIO.setup(FORWARD_IN_1, GPIO.OUT)
        GPIO.setup(FORWARD_IN_2, GPIO.OUT)
        GPIO.setup(BACKWARD_IN_1, GPIO.OUT)
        GPIO.setup(BACKWARD_IN_2, GPIO.OUT)
        GPIO.setup(SHOOTER, GPIO.OUT)

        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)

        self.servo1 = GPIO.PWM(13, 50)
        self.servo2 = GPIO.PWM(12, 50)
        self.catcher = GPIO.PWM(19, 50)
        self.servo1.start(0)
        self.servo2.start(0)
        self.catcher.start(0)
        ###########

    def on_x_press(self):
        GPIO.output(SHOOTER, True)

    def on_triangle_press(self):
        GPIO.output(SHOOTER, False)

    def on_square_press(self):
        self.catcher.ChangeDutyCycle(11)

    def on_circle_press(self):
        self.catcher.ChangeDutyCycle(8)

    def cycle_number_calculator(value):
        res = 0
        if value == 0:
            res = 0
        if 0 < value <= 2500:
            res = 25
        if 2500 < value <= 5000:
            res = 50
        if 5000 < value <= 12000:
            res = 75
        if 12000 < value:
            res = 100
        return res

    def on_L3_up(self, value):
        value = abs(value)
        cycle_number = cycle_number_calculator(value)
        GPIO.output(FORWARD_IN_1, True)
        GPIO.output(FORWARD_IN_2, True)
        self.servo1.ChangeDutyCycle(cycle_number)
        self.servo2.ChangeDutyCycle(cycle_number)

    def on_L3_down(self, value):
        value = abs(value)
        cycle_number = cycle_number_calculator(value)
        GPIO.output(BACKWARD_IN_1, True)
        GPIO.output(BACKWARD_IN_2, True)
        self.servo1.ChangeDutyCycle(cycle_number)
        self.servo2.ChangeDutyCycle(cycle_number)

    def on_L3_right(self, value):
        value = abs(value)
        cycle_number = cycle_number_calculator(value)
        GPIO.output(FORWARD_IN_1, True)
        GPIO.output(BACKWARD_IN_2, True)
        self.servo1.ChangeDutyCycle(cycle_number)
        self.servo2.ChangeDutyCycle(cycle_number)

    def on_L3_left(self, value):
        value = abs(value)
        cycle_number = cycle_number_calculator(value)
        GPIO.output(FORWARD_IN_2, True)
        GPIO.output(BACKWARD_IN_1, True)
        self.servo1.ChangeDutyCycle(cycle_number)
        self.servo2.ChangeDutyCycle(cycle_number)

    def on_L3_x_at_rest(self):
        GPIO.output(FORWARD_IN_1, False)
        GPIO.output(FORWARD_IN_2, False)
        GPIO.output(BACKWARD_IN_1, False)
        GPIO.output(BACKWARD_IN_2, False)

    def on_L3_y_at_rest(self):
        GPIO.output(FORWARD_IN_1, False)
        GPIO.output(FORWARD_IN_2, False)
        GPIO.output(BACKWARD_IN_1, False)
        GPIO.output(BACKWARD_IN_2, False)


class BallDetector:
    def __init__(self, lower_ball, upper_ball, upper_gate, lower_gate):
        self.LOWER_HSV = lower_ball
        self.UPPER_HSV = upper_ball
        self.UPPER_HSV_GATE = upper_gate
        self.LOWER_HSV_GATE = lower_gate

    def detect_ball(self, frame):
        output = None
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (17, 17), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_HSV, self.UPPER_HSV)
        mask = cv2.erode(mask, None, iterations=0)
        mask = cv2.dilate(mask, None, iterations=0)
        cnts = cv2.findContours(mask.copy(),
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            output = center
            # print(center)
            if radius > 10 and radius < 170:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        cv2.imshow("Frame", frame)
        return output

    def detect_gate(self, frame):
        output = None

        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (17, 17), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_HSV_GATE, self.UPPER_HSV_GATE)
        mask = cv2.erode(mask, None, iterations=0)
        mask = cv2.dilate(mask, None, iterations=0)
        cnts = cv2.findContours(mask.copy(),
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)  # Draw rectangle around the gate
            output = rect[0]  # Return the center of the gate
        cv2.imshow("Frame", frame)
        return output


if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    
    def my_command():
        controller.listen()

    command_thread = threading.Thread(target=my_command)
    command_thread.start()
    ball_detector = BallDetector((13, 99, 132), (24, 255, 255),
                                 (107, 159, 192), (94, 89, 100))
    video = cv2.VideoCapture(0)
    address = 'http://192.168.1.102:8080/video'
    video.open(address)
    
    while True:
        ret, frame = video.read()
        if not ret:
            break

        print("searching for ball")
        output = ball_detector.detect_ball(frame=frame)
        print(output)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
