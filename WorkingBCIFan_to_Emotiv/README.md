# Emotiv BCI to Arduino Bridge

Control Arduino with your mind using Emotiv BCI headset.

## Files You Need

1. **`simple-emotiv.html`** - Web interface to test Emotiv connection
2. **`emotiv_arduino_bridge.py`** - Python script that connects Emotiv to Arduino
3. **`arduino_receiver.ino`** - Arduino code to receive commands
4. **`requirements.txt`** - Python dependencies

## How It Works

```
Emotiv Headset → Emotiv Cortex → Python Bridge → Arduino
```

The system reads any mental command (push) and only reads the stregth of the command and sends the strength to Arduino to control the fan.


## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt

```

### 2. Open Emotiv Launcher and Connect a headset
- Connect to a EMotiv insight or a simulated headset and leave that running.  

### 3. Upload Arduino Code
- Open `BCI_Fan_connected_to_Emotiv_1.ino` in Arduino IDE or Arduino Cloud editor
- Upload to your Arduino
- Note the COM port (e.g., COM3, COM4) but it should automatically detect
- After code is uploaded disconnect the connection cable and re connect it. (THis will free up the connection port so it can be used by the python script)


### 4. Run the Python file to take live data from EmotivBCI.
- Open the files in VS Code.
- In "emotiv_arduino_bridge.py", in lines 14 and 15 enter your Client ID and secret from your Cortex App
- Run "emotiv_arduino_bridge.py"


## Expected Behavior

- On initial run of the python file an approval message with the name of your cortex app (that you entered the client id and secret of) will appear. 
- Click "Approve".
- Now the python script should subscibe to recieve mental commands and their stengths from the headset.
- The stregths from the reading will be sent to the arduino and run through its "BCI_Fan_connected_to_Emotiv_1.ino" script. 
- Connecting the arduino to the fan as descibed before "See circuit diagram (not added yet)" will power the fan with the following conditions:
- The python script only sends signal greater than a strength od 0.3
- The fan scpeed is scaled as: Strength = 0.35 the fan stops
                               Strength > 0.35 to 1 the fan goes to max speed with the allowed voltage (unsure).

## Configuration

### Adjust Command Sensitivity
Edit `emotiv_arduino_bridge.py` line 44:
```python
strength > 0.3  # Only commands stronger than 0.3 are sent
```

### Adjust Send Frequency
Edit `emotiv_arduino_bridge.py` line 25:
```python
SEND_INTERVAL = 0.2  # Send to Arduino every 200ms (5 times per second)
```

## Troubleshooting

(For later)

## Files Overview

| File | Purpose |
|------|---------|
| `emotiv_arduino_bridge.py` | Main bridge script |
| `arduino_receiver.ino` | Arduino LED control code |
| `simple-emotiv.html` | Web test interface |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |