# TouchCalibrate
Calibrate Touchscreen in X11 on Linux

Calibration helper, used to calibrate touchscreens and get calibration Matrix.
E.g. used for "silead_ts" driver calibration

Feel free to create pull requests.


## Howto
Before calibration reset the device to default matrix:
```
 xinput set-prop --type=float "silead_ts" "Coordinate Transformation Matrix" 1 0 0 0 1 0 0 0 1
```

This is a 9x9 matrix, where the first line is X, and the Second line is Y.
The input is X as the first column, Y at the second column.

Therefore the default matrix is:
```
 1 0 0
 0 1 0
 0 0 1
```

To swap X / Y axes simple exchange row 1 and 2, e.g.
```
 0 1 0
 1 0 0
 0 0 1
```

To inverse the X axes, e.g. write
```
 -1  0  1
  0  1  0
  0  0  1
```

This technical means: position * -1, e.g. if a touchscreen with 100px is touched at 20, the point is 20 * -1, means -20, which is outside the screen range, therefore 1 * 100 needs to be added, so it's 80. Therefore the 1 in the last column.


The device "silead_ts" need to replaced with your device, see
```
 xinput list
```

Calibrate with
```
 ./calibrate.py
```

## Check how the touchscreen with
```
 ./draw-test.py
```

