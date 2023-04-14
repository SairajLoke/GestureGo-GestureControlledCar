

class CarKeyboardController:
    def __init__(self):
        pass
        
        

    def control(self, key):
        if key == ord('w'):
            self.move_forward(30)
        elif key == ord('s'):
            self.move_back(30)
        elif key == ord('a'):
            self.move_left(30)
        elif key == ord('d'):
            self.move_right(30)
        elif key == ord('e'):
            self.rotate_clockwise(30)
        elif key == ord('q'):
            self.rotate_counter_clockwise(30)
        elif key == ord('r'):
            self.move_up(30)
        elif key == ord('f'):
            self.move_down(30)



