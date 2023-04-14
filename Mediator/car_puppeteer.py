
import configargparse
import cv2 as cv

from gestures.car_gesture_controller import CarGestureController
from gestures.car_keyboard_controller import CarKeyboardController
from gestures.gesture_recognition import GestureBuffer
from gestures.gesture_recognition import GestureRecognition
from utils import CvFpsCalc 

import threading

import socket





def get_args():
    print('## Reading configuration ##')
    parser = configargparse.ArgParser(default_config_files=['config.txt'])

    parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    parser.add("--device", type=int, default=0)
    parser.add("--width", help='cap width', type=int, default=960)
    parser.add("--height", help='cap height', type=int, default=540)

    parser.add("--is_keyboard", help='To use Keyboard control by default', type=bool, default=False)
    # parser.add('--use_static_image_mode', action='store_true', help='True if running on photos')
    parser.add("--min_detection_confidence",
               help='min_detection_confidence',
               type=float,
               default=0.7)
    parser.add("--min_tracking_confidence",
               help='min_tracking_confidence',
               type=float,
               default=0.7)
    parser.add("--buffer_len",
               help='Length of gesture buffer',
               type=int,
               default=10)

    args = parser.parse_args()

    return args


def select_mode(key, mode):
    number = -1
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1
    if key == 104:  # h
        mode = 2
    return number, mode


def main():
    # init global vars
    global gesture_buffer
    global gesture_id

    # Argument parsing
    args = get_args()

    KEYBOARD_CONTROL = args.is_keyboard
    # WRITE_CONTROL = False
    in_motion = False


#-------------------------------------
    # HOST = '10.202.3.68'
    # HOST = '10.202.5.30'
    # PORT = 80
        
    # Carsock = socket.socket()
    # Carsock.connect((HOST,PORT))
    
                                        
    Car_gesture_controller = CarGestureController()
    keyboard_controller = CarKeyboardController()

    gesture_detector = GestureRecognition( args.min_detection_confidence,
                                          args.min_tracking_confidence)
    gesture_buffer = GestureBuffer(buffer_len=10)

    def car_control(key, keyboard_controller, gesture_controller):
        global gesture_buffer

        if KEYBOARD_CONTROL:
            print("shifted to keyboard")
            # keyboard_controller.control(key)
        else:
            # print("\ngesture controller: ")
            gesture_controller.gesture_control(gesture_buffer)

    # def battery():
    #     global battery_status
    #     try:
    #         battery_status = 100
    #         # battery_status = 
    #     except:
    #         battery_status = -1

    # FPS Measurement
    cv_fps_calc = CvFpsCalc(buffer_len=10)

    mode = 0
    number = -1


    
    # Camera preparation ###############################################################
    
    cap = cv.VideoCapture(0)

    while True:
        fps = cv_fps_calc.get()

        # Process Key (ESC: end)
        key = cv.waitKey(1) & 0xff
        if key == 27:  # ESC
            break
        elif key == 32:  # Space
            if not in_motion:
                # start 
                print("\nkey: 32 , Start Quick Toff")
                
                in_motion = True

            elif in_motion:
                # stop
                print("\n key elif, Stop Quick (L)")
                
                in_motion = False

        elif key == ord('k'):
            mode = 0
            KEYBOARD_CONTROL = True
            WRITE_CONTROL = False
            print("rc control 0 0 0 0")

        elif key == ord('g'):
            KEYBOARD_CONTROL = False
        elif key == ord('n'):
            mode = 1
            WRITE_CONTROL = True
            KEYBOARD_CONTROL = True

        # if WRITE_CONTROL:
        #     number = -1
        #     if 48 <= key <= 57:  # 0 ~ 9
        #         number = key - 48

        # Camera capture

        ret , image = cap.read()

        debug_image, gesture_id = gesture_detector.recognize(image, number, mode)
        gesture_buffer.add_gesture(gesture_id)

        

        # Start control thread
        threading.Thread(target=car_control, args=(key, keyboard_controller, Car_gesture_controller,)).start()
        # threading.Thread(target=tello_battery, args=()).start()

        # to avoid threading  # make sure not to run both cmds together
        # Car_gesture_controller.gesture_control(gesture_buffer)

        debug_image = gesture_detector.draw_info(debug_image, fps, mode, number)

        # Battery status and image rendering
        cv.putText(debug_image, "Battery: {}", (5, 720 - 5),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv.imshow('Gesture Recognition', debug_image)

    Car_gesture_controller.sock.close()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()