import time
import os
import subprocess as s


def sound():
    os.system('spd-say "Really Great Job , Keep Going"')

def send_notification():
    s.call(['notify-send','\t\t\tAnother 10 minutes in Productivity','\t\t\t\t     Keep Hustling Champ'])
    

while True:
    
    send_notification()
    sound()
    time.sleep(10)
    
    