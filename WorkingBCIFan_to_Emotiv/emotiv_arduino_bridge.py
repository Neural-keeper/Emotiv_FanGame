import websocket
import json
import serial
import time
import threading

# Configuration
ARDUINO_PORT = 'COM3'  # Change to your Arduino port
BAUD_RATE = 9600
EMOTIV_URL = 'wss://localhost:6868'

# Emotiv credentials
USER = {
    'clientId': '2JT5PfdoaUL4Pfzc4CdX4JnAjFtgebCa5JJddkA2',
    'clientSecret': 'mNJM5L5a9iXyI1iO74xhVoXs1SqcCfHfmE8KL6HefgDERmT1MrmDHsq26DPAP6Tmh5WB37C6eE34KrQUs3Va9qP1fAMjCkhMwuUgVpkNNxw4VWVz7DAqadZ476nTvfMr',
    'license': '',
    'debit': 1
}

# Global variables
arduino = None
ws = None
auth_token = None
session_id = None
headset_id = None
last_arduino_send = 0
SEND_INTERVAL = 0.2  # Send to Arduino every 200ms (5 times per second)

def connect_arduino():
    global arduino
    try:
        arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to initialize
        print(f'Arduino connected on {ARDUINO_PORT}')
        return True
    except Exception as e:
        print(f'Arduino connection failed: {e}')
        return False

def send_to_arduino(command, strength):
    global last_arduino_send
    current_time = time.time()
    
    # Only send if enough time has passed AND strength is strong enough
    if (current_time - last_arduino_send >= SEND_INTERVAL and 
        strength > 0.3 and 
        arduino and arduino.is_open):
        
        message = f'{command},{strength:.2f}\n'
        arduino.write(message.encode())
        print(f'Arduino: {message.strip()}')
        last_arduino_send = current_time
    elif strength > 0.3:
        print(f'Throttled: {command} ({strength:.2f})')  # Show throttled commands

def send_message(ws, message):
    ws.send(json.dumps(message))
    print(f'Emotiv: {json.dumps(message)}')

def on_message(ws, message):
    global auth_token, session_id, headset_id
    
    data = json.loads(message)
    print(f'Emotiv: {json.dumps(data)}')
    
    if data.get('id') == 1:  # requestAccess response
        if data.get('result', {}).get('accessGranted'):
            print('Access granted')
            authorize(ws)
        else:
            print('Access denied')
    
    elif data.get('id') == 2:  # authorize response
        if data.get('result', {}).get('cortexToken'):
            auth_token = data['result']['cortexToken']
            print('Authorized')
            query_headsets(ws)
        else:
            print('Authorization failed')
    
    elif data.get('id') == 3:  # queryHeadsets response
        if data.get('result') and len(data['result']) > 0:
            headset_id = data['result'][0]['id']
            print(f'Headset found: {headset_id}')
            create_session(ws)
        else:
            print('No headset found')
    
    elif data.get('id') == 4:  # createSession response
        if data.get('result', {}).get('id'):
            session_id = data['result']['id']
            print('Session created')
            subscribe(ws)
        else:
            print('Session creation failed')
    
    elif data.get('id') == 5:  # subscribe response
        if data.get('result'):
            print('Subscribed to mental commands')
            print('Ready for mental commands!')
        else:
            print('Subscription failed')
    
    elif 'com' in data:  # Mental command data
        command = data['com'][0]
        strength = data['com'][1]
        print(f'COMMAND: {command} ({strength:.2f})')
        send_to_arduino(command, strength)

def on_error(ws, error):
    print(f'WebSocket error: {error}')

def on_close(ws, close_status_code, close_msg):
    print('WebSocket connection closed')

def on_open(ws):
    print('Connected to Emotiv Cortex')
    request_access(ws)

def request_access(ws):
    send_message(ws, {
        'jsonrpc': '2.0',
        'method': 'requestAccess',
        'params': {
            'clientId': USER['clientId'],
            'clientSecret': USER['clientSecret']
        },
        'id': 1
    })

def authorize(ws):
    send_message(ws, {
        'jsonrpc': '2.0',
        'method': 'authorize',
        'params': {
            'clientId': USER['clientId'],
            'clientSecret': USER['clientSecret'],
            'license': USER['license'],
            'debit': USER['debit']
        },
        'id': 2
    })

def query_headsets(ws):
    send_message(ws, {
        'jsonrpc': '2.0',
        'method': 'queryHeadsets',
        'params': {},
        'id': 3
    })

def create_session(ws):
    send_message(ws, {
        'jsonrpc': '2.0',
        'method': 'createSession',
        'params': {
            'cortexToken': auth_token,
            'headset': headset_id,
            'status': 'active'
        },
        'id': 4
    })

def subscribe(ws):
    send_message(ws, {
        'jsonrpc': '2.0',
        'method': 'subscribe',
        'params': {
            'cortexToken': auth_token,
            'session': session_id,
            'streams': ['com']
        },
        'id': 5
    })

def main():
    print('Starting Emotiv-Arduino Bridge...')
    
    # Connect to Arduino
    if not connect_arduino():
        print('Failed to connect to Arduino. Continuing without Arduino...')
    
    # Connect to Emotiv
    global ws
    ws = websocket.WebSocketApp(EMOTIV_URL,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.run_forever()

if __name__ == '__main__':
    main()