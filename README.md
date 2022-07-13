# Real Time Data Visualizer

**Python Project using Python 3.10.5**

***

## Environment
- Python 3.10.5 is required.

***

## Run
- At first launch, use `python pip install -r requirements.txt` to install all the dependencies.
- Use `python main.py` to run the script.

***

## Scripts

### `main.py`
The `main.py` script allows communication between the computer and the Arduino board.

To communicate with the Arduino board, a communication port is required.
You can add all ports you want in the `ports.txt` file.
The program will try to connect until it succeeds.
You can also use two options to specify ports using the CLI.
- Use `python main.py -h` to get help.
- Use `python main.py -p PORT1 PORT2 ...` to specify the available ports.
- Use `python main.py -f myports.txt` to specify a file containing the available ports.

Both commands can be used at the same time to combine the ports contained in a file, and additional ports.
- Use `python main.py -p PORT1 PORT2 ... -f myports.txt`

### Find your Port:
To find out which port your board is using, run the `Arduino Software > Tools > Port`.

It is possible that several ports are available. 

If you don't know which one is the right one, 
you can use the delay option, in order to change the port automatically (even if the connection has been established),
if no data is received within a certain time period.

Use `python main.py -d 10` to wait 10 seconds (once a connection is established). 

Make sure the card is sending data at this time. 
If no data is received, the card will try to connect to the next port.

This way you can find out which ports are available and with which your card is communicating.

You can modify the `ports.txt` file as you wish to keep only the ports that are useful to you.

### `pyplot_utils.py`
The `pyplot_utils.py` script contains some functions helping to build the GUI. Used by `main.py`.

### `command_helper.py`
The `command_helper.py` script is used to parse a new command line received. Used by `main.py`.
- Use `python command_helper.py -h` to get help.
- Use `python command_helper.py -l` to get the command list.
- Use `python command_helper.py -e filename.txt` to extract the commands list to a file.
  You can also use the `full` option with: `python command_helper.py -e filename.txt -f` 
- Use `python command_helper.py -d CMD` to get the details of a command.

***

## Contact
roman.clavier.2001@gmail.com
