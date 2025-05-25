<h1>How to setup the replay system for your robot:</h1>


Make sure to include stdio in your header file, under the C++ specific definitions.<br>

```c
#include <stdio.h>
```

Create a .txt file within your robot's SD card.
Then, add this to your code, around the beginning where you set up your variables.

```c
FILE *replay = fopen("usd/replay.txt", "w")
``` 
<br>(And make sure to change the file name to what you named it)

Inside your initialization() function, add this code to the Task that prints out your chassis onto the brain screen.

```c
Task screen_task([&]() {
  while (true) {
    pros::lcd::print(0, "X: %f", chassis.getPose().x);
    pros::lcd::print(1, "Y: %f", chassis.getPose().y);
    pros::lcd::print(2, "Theta: %f", chassis.getPose().theta);

    // New code:
    fprintf(replay, "%.3f %.3f %.3f\n", chassis.getPose().x, chassis.getPose().y, chassis.getPose().theta);

    pros::delay(25);
  }
});
```

Once you're done driving with the robot, upload the .txt file from the SD.<br> 
Install Python itself, an IDE, and pip by using the command <code>python -m ensurepip --upgrade</code> in the terminal. Make a python project, go to its terminal, and type in <code>pip install arcade</code>.

Configure the file path on <code>main.py</code> and other variables. And you're done!

<h1>How to use the replay</h1>

There are some variables in all uppercase that you can change to suit your situation.

<code>VIEWSCALE</code>: Changes size of your window<br>
<code>INITX</code>, <code>INITY</code>, <code>INITD</code>: Starting position of your robot<br>
<code>ROBOTWIDTH</code>, <code>ROBOTLENGTH</code>: Dimensions of your robot<br>
<code>DELAY</code>: How often you write to the replay file<br>
<code>REPLAYID</code>: Name of the text file<br>

Keys:

SPACE - Play/Pause<br>
LEFT - Go back 1 second<br>
RIGHT - Go forward 1 second<br>
, - Previous frame<br>
. - Next frame<br>
Left click - Mouse position/pose
Right click - Pose given mouse position is facing right click position
