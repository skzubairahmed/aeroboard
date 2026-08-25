
# AeroBoard alpha-v0.1
---
[DOWNLOAD NOW!](https://github.com/skzubairahmed/aeroboard/releases/tag/v0.1-alpha)

This is a opencv based air-whiteboard, you can draw anything using 3 main colours(RED, GREEN, BLUE), you can also clear the screen.

---

What I used for doing what?

1. Tracking:
    
    This mainly used opencv and mediapipe(through cvzone) to track the fingertip positions
2. Filters:

    I used simple 2D Kalman filters to remove the micro jitters in the fingertip positions which occurs when fingers are moved, i made the data more precise so the strokes become smoother and less jagged.
3. Gestures:

    I used some of my own code to determine the gesture which the user was showing, I have mainly integrated two gestures now(PEN and POINTER)

4. Logger:

    I have made my own logger class to log sany errors in a logfile.

5. AirButtons:

    I have made some of my own code for the AirButtons used to change the pen color and to clear the screen.

That pretty much sums it all up.

The application is only available for windows(.exe)*
---

[DOWNLOAD NOW!](https://github.com/skzubairahmed/aeroboard/releases/tag/v0.1-alpha)

Thank you :)



