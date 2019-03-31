import RPi.GPIO as GPIO
import time
import os
try:
    import paramiko
except:
    try:
        import paramiko
    except:
        print("There was an error with the paramiko module")


PIN=18

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

l_password = "maker"
l_host = "192.168.105.46"
l_user = "robot"
cmd = "sudo reboot"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

while True:
    input_state = GPIO.input(PIN)
    if input_state == False:
        print(":)")
        try:
            ssh.connect(l_host,username=l_user,password=l_password)
            print("succesfully conected")
        except:
            print("There was an Error conecting")
        stdin, stdout, stderr = ssh.exec_command(cmd,get_pty = True)
        stdin.write('maker\n')
        stdin.flush()
        print(stderr.readlines())
        print(stdout.readlines())

        time.sleep(1)






