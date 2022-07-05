# Real Time Data Visualizer

**Python Projet using Python 3.10.5**

**************

## Environnement
- Python 3.10.5 is required.

## Run
- At first launch, use `pip install -r requirements.txt` to install all the dependencies.
- Use `python main.py` to run the script.

## Scripts

### `main.py`
The `main.py` script allows communication between the computer and the Arduino board.

### `pyplot_utils.py`
The `pyplot_utils.py` script contains some functions helping to build the GUI. Used by `main.py`.

### `command_helper.py`
The `command_helper.py` script is used to parse a new command line received. Used by `main.py`.
- Use `python command_helper.py -h` to get help.
- Use `python command_helper.py -l` to get the command list.
- Use `python command_helper.py -e filename.txt` to extract the commands list to a file.
  You can also use the `full` option with: `python command_helper.py -e filename.txt -f` 
- Use `python command_helper.py -d [cmd]` to get the details of a command.

**************

### `Contact`
roman.clavier.2001@gmail.com
