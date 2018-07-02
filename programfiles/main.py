#Garbagebot Raspberry Pi Program
import time
import sys
from AI import Watcher, Handler
from movement import DriveForward, Rotateto45, Rotateto180, Rotateto270, RotateBackto0, pickupGarbage, binGarbage
from vision import path_clear, JustDirt, GarbagePic, GarbageisThere

currentHeading = 0
PauseButtonClicked = False
PlayButtonClicked = False
Paused = False

w = Watcher()
w.run()

try:
    while Paused == False:
        if path_clear() == True:
            if currentHeading != 0:
                RotateBackto0()
        DriveForward()

    else:
        print('Path obstructed!')
        Rotateto45()
        currentHeading == 45
        if path_clear() == True:
            DriveForward()
        else:
            print('Path obstructed again!')
            Rotateto270()
            currentHeading == 270
            if path_clear() == True:
                DriveForward()
            else:
                print('Boxed in, retracing my steps...')
                Rotateto180()
                currentHeading == 180
                if path_clear() == True:
                    DriveForward()
                else:
                    print('Trapped!! AHHHHHH!!!')
                    Paused = True

        if JustDirt() == False:
            GarbagePic()
        if GarbageisThere == True:
            pickupGarbage()
            binGarbage()

    while PauseButtonClicked == True:
        print('Paused...')
        time.sleep(0.5)
        while PlayButtonClicked == False:
            Paused == True
            time.sleep(0.5)
        else:
            Paused == False
            time.sleep(0.5)
            print('Play Button Clicked - Resuming...')



except KeyboardInterrupt:
    sys.exit()
