/*
  Commands resume, get using python command_helper.py -l :

-n        [ruf*:bool]
-ruf      [ruf:bool]
-s        [separator:str]
-dc       [character:str]
-mv       [max_values:int]
-aa       [rcp:int] [title*:str] [xlabel*:str] [ylabel*:str]
-aas      [row:int] [column:int]
-at       [axis:int] [title:str]
-albl     [axis:int] [xlabel:str] [ylabel:str]
-clra     [axis:int]
-ra       [axis:int]
-al       [axis:int] [color*:str]
-cl       [axis:int] [line:int] [color:str]
-ml       [axis:int] [line:int] [marker:str]  | See this to know more about marker: https://matplotlib.org/stable/api/markers_api.html
-sl       [axis:int] [line:int] [style:str]
-clrl     [axis:int] [line:int]
-rl       [axis:int] [line:int]
-h        [header1] [header2] [header3]  ... 
-w        [data1] [data2] [data3]  ... 
-ws       [data11] [data12] [data13] ; [data21] [data22] [data23] ; [data31] [data32] ; ... 
-l        [axis:int] [line:int] [xdata1:float] [ydata1:float] ; [xdata2:float] [ydata2:float] ; [xdata3:float] [ydata3:float] ; ... | The character used to indicate a new pair of data is ";" or a simple space " ".
-lw       [axis:int] [line:int] [xdata:float] [ydata:float]
-lws      [axis:int] [line:int] [xdata1:float] [ydata1:float] ; [xdata2:float] [ydata2:float] ; [xdata3:float] [ydata3:float] ; ...
-ld       [oriAxis:int] [oriLine:int] [derivedAxis:int] [derivedLine:int] [degree*:int]

*/

/*
 If data contains space, replace it by _ : Time (ms) => Time_(ms) ; my handsome title => my_handsome_title
 
 This exemple will send sinus values, showing several use cases.
*/

float timeElapsed;
float value;
unsigned int interval;

bool stopSending = false;
unsigned int duration = 10; // Examples: 4, 5, 9, 11

// To send many data in a row
byte packetSize;
byte packetCount;
String dataToSend;
String dataToSend2;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  timeElapsed = 0.0;
  value = 0.0;
  interval = 100; // change in example 4, 5, 7, 8, 10
  Serial.println("Initialized...");

  // For all the examples, only the Arduino board is needed. No specific installation is required.
  
  //init_1(); // Example 1: Write line by line into the save file.                                          New commands: -n, -ruf, -s, -dc, -h, -w
  //init_2(); // Example 2: Write many lines in a row into the save file.                                   New commands: -ws
  //init_3(); // Example 3: Create a GUI with one axis and one line                                         New commands: -aa, -at, -albl, -al, -cl, -ml, -sl, -l
  //init_4(); // Example 4: Create a GUI with two axis and one line in each axis, to draw Sine and Cosine   New commands: -aas
  //init_5(); // Example 5: Same as the 4th example, but using packet sending
  //init_6(); // Example 6: Write and draw data                                                             New commands: -lw
  //init_7(); // Example 7: Same as the 6th example, but using packet sending                               New commands: -lws
  //init_8(); // Example 8: Curve display with a maximum number of points                                   New commands: -mv
  //init_9(); // Example 9: Draw sine and show his derivative (Cosine)                                      New commands: -ld
  //init_10(); // Example 10: Draw 4 axes with Sine and its 3 first derived (Cosine, -Sine, -Cosine)
  init_11(); // Example 11: Same as the 10th example, but all in the same axis.
  //init_12(); // Example 12: Clear a line                                                                  New commands: -clrl
  //init_13(); // Example 13: Remove a line                                                                 New commands: -rl
  //init_14(); // Example 14: Clear an axis                                                                 New commands: -clra
  //init_15(); // Example 15: Remove an axis                                                                New commands: -ra

  /*
    You now have enough knowledges to build your own Visualizer.
    Of course, it is up to you to adapt according to the performance of your computer and your project.
    The delay in the display of the curves is most often due to the sending of long messages, to a high frequency of sending and to the request of the viewer (to display the derivative, draw many lines, or using a massive marker, ...).
    It is up to you to test the best interval for sending data, the size of the message, or the markers of the curves...
    For some laptops, charging the battery can improve performance. 
  */
}

void loop() {
  //example_1();
  //example_2();
  //example_3();
  //example_4();
  //example_5();
  //example_6();
  //example_7();
  //example_8();
  //example_9();
  //example_10();
  example_11();
  //example_12();
  //example_13();
  //example_14();
  //example_15();
  delay(interval);
}

void init_1() {
  // Example 1: Write line by line into the save file
  
  // First command to send before writing or displaying a graphic:
  Serial.println("-n");
  // It will create the data folder, and the save file (YYYY_dd_mm-HH_MM_SS.txt)
  // If you don't, the main.py script will write "Not initialized".

  // To remove all unused files created at the end of the run, or containing only headers, you can set the RemoveUnusedFiles to true using:
  Serial.println("-ruf false"); // Can use a non-zero integer, true or True
  
  // The last two commands can be combined into one with :
  //Serial.println("-n 1");

  // All lines with 'Option' are not required and can be removed.
  
  // Option: You can specify the separator between the data in the save file. The default value is ';'.
  //Serial.println("-s ;");
  
  // Option: You can specify the decimal character used in the save file. The default value is '.'.
  //Serial.println("-dc ,"); // To use ',' instead of '.'
  
  // Option: If you want, you can also write the header in this new file.
  Serial.println("-h Time_(s) Sine");
  // If the sepatator is ';', the result in the save file will be: Time (s);Sine
}

void example_1() {
  // Write line by line into the save file : a time and a sine value with 6 digit of precision.
    
  timeElapsed = millis() / 1000.0;
  value = sin(timeElapsed);
  Serial.println("-w " + String(timeElapsed) + " " + String(value, 6));

  // If the decimal character is ',' and the sepatator is ';', the result in the save file will be:
  // 0,00;0,000000
  // 0,51;0,489922
  // ...
}


void init_2() {
  // Example 2: Write many lines in a row into the save file
  
  packetSize = 5; // Want to send 5 lines
  packetCount = 0;
  dataToSend = "";
  
  Serial.println("-n 1");
  Serial.println("-dc ,");
  Serial.println("-h Time_(s) Sine");
}

void example_2() {
  // Write many lines in a row into the save file : a time and a sine value with 6 digit of precision.

  timeElapsed = millis() / 1000.0;
  value = sin(timeElapsed);
  dataToSend += " " + String(timeElapsed) + " " + String(value, 6) + " ;"; // To indicate the end of the line, use ';'.
  packetCount++;
  if (packetCount >= packetSize) {
    // Send the command only when the number of packets is reached 
    packetCount = 0;
    Serial.println("-ws" + dataToSend);
    dataToSend = "";
  }
}


void init_3() {
  // Example 3: Create a GUI with one axis and one line
  
  Serial.println("-n 1");
  // Add an axis : The window is composed from 1 row, 1 column and the axis is placed to the position 1 => 111
  // The title is 'my new graph', the xlabel is 'X' and the ylabel is 'Y'
  Serial.println("-aa 111 my_new_graph X Y");

  // Option: You can rename the title of the first axis.
  //Serial.println("-at 1 new_title");
  
  // Option: You can rename the labels of an first axis.
  //Serial.println("-albl 1 new_x new_y");

  // Add a line to the first axis with a specific color
  //Serial.println("-al 1 #E0E000");

   // Add a line to the first axis (the color is chosen by the GUI)
  Serial.println("-al 1");
  
  // Option: You can set the color of the first line in the first axis
  // Serial.println("-cl 1 1 #FFD700");  // using a hexadecimal code
  // Serial.println("-cl 1 1 gold");     // using a color name

  /*
    Default line color:
    
    #E24A33 : red
    #348ABD : blue
    #988ED5 : purple
    #777777 : gray
    #FBC15E : orange
    #8EBA42 : green
    #FFB5B8 : pink

    If you have several lines in a chart, when you add a line without a specific color, the program will choose the color automatically following the order of the list.
    If the last color is taken, it returns to the first color and so on.
  */
  
  // Option: You can set the marker of the first line in the first axis. Default value is "o". // See this to know more about marker: https://matplotlib.org/stable/api/markers_api.html
  // Serial.println("-ml 1 1 *"); // Use "*" instead of "o".

  // Option: You can set the style of the first line in the first axis. Default value is "-".
  // Serial.println("-sl 1 1 -."); // Use "-." instead of "-".

  /*
  Available styles:
  ==========================================  =================
  linestyle                                   description
  ==========================================  =================
  '-'    or 'solid'                           solid line
  '--'   or 'dashed'                          dashed line
  '-.'   or 'dash-dot'                        dash-dotted line
  ':'    or 'dotted'                          dotted line
  'none' or 'None'                            draw nothing
  ==========================================  =================
  */

  // Add many values to the first line in the first axis
  // Serial.println("-l 1 1 0 0 1 2 2 6");
  Serial.println("-l 1 1 0 0 ; 1 2 ; 2 6"); // You can also use ";" to separate data pairs.
}

void example_3() {
  // Do noting in this example
}


void init_4() {
  // Example 4: Create a GUI with two axis and one line in each axis, to draw Sine and Cosine for 10 seconds
  
  Serial.println("-n 1");

  // Add axes ine by one
  Serial.println("-aa 211 Sine X Y"); // row: 2, column: 1, place: 1
  Serial.println("-aa 212 Cosine X Y"); // row: 2, column: 1, place: 1
  // Add 2 axes in a row
  /*
  Serial.println("-aas 2 1"); // 2 rows and 1 column => build 2 * 1 = 2 axes
  Serial.println("-at 1 Sine");
  Serial.println("-at 2 Cosine");
  Serial.println("-albl 1 X Y");
  Serial.println("-albl 2 X Y");
  */
  Serial.println("-al 1");
  Serial.println("-ml 1 1 *");
  Serial.println("-al 2 #1F85DE");

  /*
    Tips:
    The default interval is 100ms.
    
    If the data sending frequency is low, such as every 100ms, 250ms, 500ms or 1000s, drawing line by line is sufficient.
    If the frequency is high, such as every 1ms, 10ms or 20ms, it may be better to use packet sending, as shown in example 5.
    Especially if the curve display is active.
    If there is only writing in the save file, there may be no need to send it by packet.

    You can use a stopwatch to check that the curve continues to be displayed after the 10s.  
    Comment or uncomment the following line to observe the delay of the display.
  */
  // interval = 10; // 10 ms of interval => too fast
}

void example_4() {
  // Example 4: Draw Sine and Cosine
  if (stopSending) {
    return;
  }
  timeElapsed = millis() / 1000.0;
  if (timeElapsed > duration) {
    stopSending = true;
    Serial.println("10 seconds! Stop");
  }
  Serial.println("-l 1 1 " + String(timeElapsed) + " " + String(sin(timeElapsed), 6));
  Serial.println("-l 2 1 " + String(timeElapsed) + " " + String(cos(timeElapsed), 6));
}


void init_5() {
  // Example 5: Same as the 4th example, but using packet sending.
  // You can easy see that sendind message is a bigger process.
  
  packetSize = 5; // Want to send 5 lines
  packetCount = 0;
  dataToSend = "";
  dataToSend2 = "";
  interval = 10; // Even if the interval is short, the display is now in real time.
    
  Serial.println("-n 1");
  Serial.println("-aa 211 Sine X Y"); // row: 2, column: 1, place: 1
  Serial.println("-aa 212 Cosine X Y"); // row: 2, column: 1, place: 1
  Serial.println("-al 1");
  Serial.println("-ml 1 1 *");
  Serial.println("-al 2 #1F85DE");
}

void example_5() {
  if (stopSending) {
    return;
  }
  timeElapsed = millis() / 1000.0;
  if (timeElapsed > duration) {
    stopSending = true;
    Serial.println("10 seconds! Stop");
  }
  
  dataToSend  += " " + String(timeElapsed) + " " + String(sin(timeElapsed), 6);
  dataToSend2 += " " + String(timeElapsed) + " " + String(cos(timeElapsed), 6);
  packetCount++;
  if (packetCount >= packetSize) {
    packetCount = 0;
    Serial.println("-l 1 1" + dataToSend);
    Serial.println("-l 2 1" + dataToSend2);
    dataToSend = "";
    dataToSend2 = "";
  }
}


void init_6() {
  // Example 6: Write and draw data
  Serial.println("-n 1");
  Serial.println("-dc ,");
  Serial.println("-h Time_(s) Sine");
  Serial.println("-aa 111 Sine X Y");
  Serial.println("-al 1");
  Serial.println("-ml 1 1 None");
  Serial.println("-sl 1 1 -.");
}

void example_6() {
  timeElapsed = millis() / 1000.0;
  value = sin(timeElapsed);
  dataToSend = String(timeElapsed) + " " + String(value, 6);
  // Send two commands
  //Serial.println("-w " + dataToSend); // write one line
  //Serial.println("-l 1 1 " + dataToSend); // add this value to the line 1 in axis 1
  // Send both commands in one
  Serial.println("-lw 1 1 " + dataToSend);
}


void init_7() {
  // Example 7: Write several lines and draw data
  packetSize = 5; // Want to send 5 lines
  packetCount = 0;
  dataToSend = "";
  interval = 100; // Try with 10, 100 and 1000 to see the differencies

  Serial.println("-n 1");
  Serial.println("-dc ,");
  Serial.println("-h Time_(s) Sine");
  Serial.println("-aa 111 Sine X Y");
  Serial.println("-al 1");
}

void example_7() {
  timeElapsed = millis() / 1000.0;
  value = sin(timeElapsed);
  dataToSend += " " + String(timeElapsed) + " " + String(value, 6) + " ;";
  packetCount++;
  
  if (packetCount >= packetSize) {
    packetCount = 0;
    Serial.println("-lws 1 1" + dataToSend);
    dataToSend = "";
  }
}


void init_8() {
  // Example 8: Curve display with a maximum number of points
  packetSize = 5; // Want to send 5 lines
  packetCount = 0;
  dataToSend = "";
  interval = 10; // Try with 10, 100 and 1000 to see the differencies
  
  Serial.println("-n 1");
  // Set the maximum values to display
  Serial.println("-mv 200");
  Serial.println("-aa 111");
  Serial.println("-al 1");
  Serial.println("-ml 1 1 None");
}

void example_8() {
  timeElapsed = millis() / 1000.0;
  value = sin(timeElapsed);

  // Replace true or false to test the maximum values using normal mode or packet sending.
  if (true) {
    Serial.println("-l 1 1 " + String(timeElapsed) + " " + String(value, 6));
  }
  else {
    dataToSend += " " + String(timeElapsed) + " " + String(value, 6) + " ;";
    packetCount++;
    
    if (packetCount >= packetSize) {
      packetCount = 0;
      Serial.println("-l 1 1" + dataToSend);
      dataToSend = "";
    }
  }
}


void init_9() {
  // Example 9: Draw sine and show its first derived (Cosine)
  packetSize = 5; // Want to send 5 lines
  packetCount = 0;
  dataToSend = "";
  
  Serial.println("-n 1");
  Serial.println("-aa 111 Sine X Y");
  Serial.println("-al 1");
  Serial.println("-al 1 #1F85DE");

  // Can also set a max values.
  //Serial.println("-mv 50"); // Comment or uncomment this line to see the difference.

  // Can also enable the derived after a duration, and see that all the missing points are computed
  duration = 0; // 0 second => enable at the begining. 10 seconds => Enable after 10 seconds
}

void example_9() {
  timeElapsed = millis() / 1000.0;
  value = sin(timeElapsed);
  
  // Replace true or false to test the maximum values using normal mode or packet sending.
  if (true) {
    Serial.println("-l 1 1 " + String(timeElapsed, 3) + " " + String(value, 6));
    
    if (timeElapsed >= duration) {
      // Draw in the axis 1 line 2, the derived of the axis 1 line 1
      Serial.println("-ld 1 1 1 2");
      //Serial.println("-ld 1 1 1 2 1"); // Degree can be set optionnaly. Default is 1. 0 Return the original curve. Under will return an error. The degree can be 1, 2, 3, ...
    }
  }
  else {
    dataToSend += " " + String(timeElapsed, 3) + " " + String(value, 6) + " ;";
    packetCount++;
    
    if (packetCount >= packetSize) {
      packetCount = 0;
      Serial.println("-l 1 1" + dataToSend);
      dataToSend = "";
      
      if (timeElapsed >= duration) {
        // Draw in the axis 1 line 2, the derived of the axis 1 line 1
        Serial.println("-ld 1 1 1 2");
        //Serial.println("-ld 1 1 1 2 1"); // Degree can be set optionnaly. Default is 1. 0 Return the original curve. Under will return an error. The degree can be 1, 2, 3, ...
      }
    }
  }
}


void init_10() {
  // Example 10: Draw 4 axes with Sine and its 3 first derived (Cosine, -Sine, -Cosine)
  
  interval = 100;
  Serial.println("-n 1");
  // Try each desgin
  
  // Desing: 2 x 2
  /*
  Serial.println("-aas 2 2");
  Serial.println("-at 1 Sine");
  Serial.println("-at 2 d/dx_Sine_(Cosine)");
  Serial.println("-at 3 d2/dx2_Sine_(-Sine)");
  Serial.println("-at 4 d3/dx3_Sine_(-Cosine)");
  */
  // Desing: 4 x 1
  
  Serial.println("-aa 411 Sine X Y");
  Serial.println("-aa 412 d/dx_Sine_(Cosine) X Y");
  Serial.println("-aa 413 d2/dx2_Sine_(-Sine) X Y");
  Serial.println("-aa 414 d3/dx3_Sine_(-Cosine) X Y");
  
  // Add lines
  for (int i = 1; i <= 4; i++) {
    // Serial.println("-albl " + String(i) + " X Y");  // Set label, If design 2 x 2
    Serial.println("-al " + String(i));
  }
  // Set colors
  Serial.println("-cl 2 1 #348ABD");
  Serial.println("-cl 3 1 #988ED5");
  Serial.println("-cl 4 1 #FBC15E");
}

void example_10() {
  timeElapsed = millis() / 1000.0;
  value = sin(timeElapsed);
  Serial.println("-l 1 1 " + String(timeElapsed, 5) + " " + String(value, 6));
  
  // first way to draw derivative lines
  Serial.println("-ld 1 1 2 1 1"); // compute the first derivative
  Serial.println("-ld 1 1 3 1 2"); // compute the first derivative and a second time to get the second derivative
  Serial.println("-ld 1 1 4 1 3"); // compute the first derivative, then the second, and finally compute the third derivative 
  /*
    This method is working but can be optimized.
    The algorithm used to calculate a derivative uses recursion to calculate when the degree is greater than 1.
    Here, when we ask for the second derivative, we recalculate the first derivative to calculate the second. 
    But the first one has already been calculated in the previous line. So we make calculations that have already been done. Same thing for the third derivative.
    
    To optimize this, we can use the derivative lines to calculate only first derivatives.
    Of course this optimization is possible because each derivative is displayed. 
    If you only need the main line and its second derivative, without displaying the first derivative, you can use the above method.
  */
  // second way to draw derivative lines
  //Serial.println("-ld 1 1 2 1");
  //Serial.println("-ld 2 1 3 1");
  //Serial.println("-ld 3 1 4 1");
}

void init_11() {
  // Example 11: Same as the 10th example, but all in the same axis.
  Serial.println("-n");
  // Serial.println("-mv 50");
  Serial.println("-aa 111");
  for (int i = 0; i < 4; i++) {
    Serial.println("-al 1");
    Serial.println("-ml 1 " + String(i + 1) + " none");
  }
  Serial.println("-cl 1 4 #FBC15E");
}

void example_11() {
  timeElapsed = millis() / 1000.0;
  value = sin(timeElapsed);
  Serial.println("-l 1 1 " + String(timeElapsed, 3) + " " + String(value, 6));
  Serial.println("-ld 1 1 1 2");
  Serial.println("-ld 1 2 1 3");
  Serial.println("-ld 1 3 1 4");
}


void init_12() {
  // Example 12: Clear a line
  duration = 3; // Clear the line every 3 seconds
  Serial.println("-n 1");
  Serial.println("-aa 111");
  Serial.println("-al 1");
}

void example_12() {
  timeElapsed = millis() / 1000.0;
  if (int(timeElapsed) % duration == 0) {
    Serial.println("-clrl 1 1"); // Clear the first line in the first axis
  }
  else {
    Serial.println("-l 1 1 " + String(timeElapsed) + " " + String(2 * timeElapsed));
  }
}


void init_13() {
  // Example 13: Remove a line
  Serial.println("-n 1");
  Serial.println("-aa 111");
  Serial.println("-al 1");
  Serial.println("-al 1");
  Serial.println("-al 1");
  Serial.println("-l 1 1 0  1 1 2 2 6 3 -1.25");
  Serial.println("-l 1 2 0  0 1 1 2 5 3 -2.25");
  Serial.println("-l 1 3 0 -1 1 0 2 4 3 -3.25");
  // Normally, this code shows 3 lines
  
  Serial.println("-rl 1 2"); // Comment or uncomment to remove the line 2 in the first axis
  // Warning: If you remove line 2, line 3 will be line 2, line 4 will be 3, and so on... !
  // If we now add to line 2 (previously line 3), the purple line will be longer.
  Serial.println("-l 1 2 4 3.25");
}

void example_13() {
  // do nothing
}


void init_14() {
  // Example 14: Clear an axis
  Serial.println("-n 1");
  Serial.println("-aa 111");
  Serial.println("-al 1");
  Serial.println("-al 1");
  Serial.println("-al 1");
  Serial.println("-l 1 1 0  1 1 2 2 6 3 -1.25");
  Serial.println("-l 1 2 0  0 1 1 2 5 3 -2.25");
  Serial.println("-l 1 3 0 -1 1 0 2 4 3 -3.25");
  // Normally, this code shows 3 lines
  
  Serial.println("-clra 1"); // Comment or uncomment to clear the first axis, so removing all the lines

  // Warning: If no new line is added, asking to add values to a line will raise an error.
  
  //Serial.println("-l 1 1 4 3.25"); // If it's uncommented, it will raise an error
  //Serial.println("-al 1"); // Add a new line
  //Serial.println("-l 1 1 0 0"); // Now, it will not raise any error
}

void example_14() {
  // do nothing
}


void init_15() {
  // Example 15: Remove an axis
  Serial.println("-n 1");
  Serial.println("-aas 2 2");
  for (int i = 1; i <= 4; i++) {
    Serial.println("-at " + String(i) + " Axis_" + String(i));
    Serial.println("-al " + String(i));
    Serial.println("-l " + String(i) + " 1 0 0 5 2");
  }
  // Normally, this code shows 4 axes with one line each
  
  // Warning: If you remove axis 1, axis 2 will be axis 1, axis 3 will be axis 2, and so on...!
  //Serial.println("-ra 1");
  //Serial.println("-l 1 1 6 10"); // We can notice that Axis 2 is now Axis 1
}

void example_15() {
  // do nothing
}
