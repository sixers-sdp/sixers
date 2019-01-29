import time
import json, socket
from enum import Enum
import ev3dev.ev3 as ev3

## helper functions ##

def _send(socket,data):
    try:
        serialized = json.dumps(data)
    except (TypeError, ValueError):
        raise Exception('You can only send JSON-serializable data')
    # send the length of the serialized data first
    socket.send(bytes('%d\n' % len(serialized),'utf8'))
    # send the serialized data
    socket.sendall(bytes(serialized,'utf8'))

def _recv(socket):
    # read the length of the data, letter by letter until we reach EOL
    length_str = ''
    char = socket.recv(1).decode("ascii")
    while char != '}':
        length_str += char
        char = socket.recv(1).decode("ascii")
    string = length_str.split("\n")[1]+"}"
    return json.loads(string)

class Client(object):
    """
    """
    socket = None

    def __del__(self):
        self.close()

    def connect(self, host, port):
        self.socket = socket.socket()
        self.socket.connect((host,port))
        return self

    def send(self, data):
        if not self.socket:
            raise Exception('You have to connect first before sending data')
        _send(self.socket, data)
        return self

    def recv(self):
        if not self.socket:
            raise Exception('You have to connect first before receiving data')
        return _recv(self.socket)

    def recv_and_close(self):
        data = self.recv()
        self.close()
        return data

    def close(self):
        if self.socket:
            self.socket.close()
            self.client = None

def turn(m1,m2,m3,m4,value,time):
    m1.run_timed(speed_sp=value,time_sp=time)
    m2.run_timed(speed_sp=value,time_sp=time)
    m3.run_timed(speed_sp=-value,time_sp=time)
    m4.run_timed(speed_sp=-value,time_sp=time)

def go_forward(m1,m2,m3,m4,value=700):
    m1.run_timed(speed_sp=value,time_sp=400)
    m2.run_timed(speed_sp=value,time_sp=400)
    m3.run_timed(speed_sp=value,time_sp=400)
    m4.run_timed(speed_sp=value,time_sp=400)

class Type(Enum):
    FORWARD = "forward"
    STOP = "stop"
    TURN = "turn"

if __name__ == "__main__":
    #host = 'LOCALHOST'
    host = '192.168.105.135'
    port = 5005

    m1=ev3.LargeMotor('outA')
    m2=ev3.LargeMotor('outB')
    m3=ev3.LargeMotor('outC')
    m4=ev3.LargeMotor('outD')

    if not (m1.connected):
        print("Plug a motor into port A")
    elif not (m2.connected):
        print("Plug a motor into port B")
    elif not (m3.connected):
        print("Plug a motor into port C")
    elif not (m4.connected):
        print("Plug a motor into port D")
    else:
        while True:
            client = Client()
            client.connect(host,port)
            response = client.recv()
            if (response['type']==Type.FORWARD.value):
                #go forward
                go_forward(m1,m2,m3,m4)
                t=0.4
                print(response,"FORWARD")
            elif (response['type']==Type.STOP.value):
                print(response,"STOP")
                t=0.4
            elif (response['type']==Type.TURN.value):
                t = int(response['time'])
                if (response['direction']=='right'):
                    v=700
                else:
                    v=-700
                turn(m1,m2,m3,m4,v,t)
                t=t/1000
                #print(response,"TURN")
                #turn
            time.sleep(t)
            client.close()
