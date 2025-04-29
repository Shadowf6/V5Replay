<h2>How to setup the replay system for your robot: </h2>


Make sure to include stdio in your header file, under the C++ specific definitions.<br>

```c
#include <stdio.h>
```

Create a .txt file within your robot's SD card.
Then, add this to your code, around the beginning where you set up your variables.

```c
FILE* fileName = fopen("usd/fileName.txt", "w")
``` 
<br>(And make sure to change the file name to what you named it)

Make you sure you have a chassis object set up and add this code to the loop of your opcontrol() function.

```c
fprintf(fileName, "%.3f %.3f %.3f\n", chassis.getPose().x, chassis.getPose().y, chassis.getPose().theta);
```
<br>You can modify the decimal point if you want it to round to less or more digits.

Finally, add this code to your disabled() function.
```c
fprintf(replay, "DONE\n");
fclose(replay);
```

And you're done! You can add switches to record or not. Just add if statements. Ideally you want to record position every 50 ms or so, so you can customize that to match the delay of your controller.

Once you've finished driving, simply upload the txt file from the SD, and install a Python IDE if you haven't yet (PyCharm or VSCode works fine). Go to the terminal and type <code>pip install arcade</code>. (If you don't have pip or python installed, please do so.)

Now, just add the file path of the txt file and main.py onto your Python project, and you're done setting it up.
