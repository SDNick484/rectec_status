import pytuya
import json
import time

GW_ID = 'AAAAAAAAAAAAAAAAAAAA'
LOCAL_IP = 'BBB.BBB.BBB.BBB'
LOCAL_KEY = 'CCCCCCCCCCCCCCCC'

# Specify the smoker 
d = pytuya.OutletDevice(GW_ID, LOCAL_IP, LOCAL_KEY)

def get_status():
    for i in range(3):
        try:
            data = d.status()
            return(data)
        except ConnectionError:
            if i+1 == 3:
                raise ConnectionError("Failed to update status.")

def print_status():
    rt_state = get_status()
    if rt_state['dps']['1']:
        print('RecTec is on')
    else:
        print('RecTec is off')
    print('Target Temperature: %r' % rt_state['dps']['102'])
    print('Current Temperature: %r' % rt_state['dps']['103'])
    print('Probe A Temperature: %r' % rt_state['dps']['105'])
    print('Probe B Temperature: %r' % rt_state['dps']['106'])

def power_state():
    rt_state = get_status()
    if rt_state['dps']['1']:
        print('RecTec is on.')
    else:
        print('RecTec is off.')


def turn_on(**kwargs):
    """Turn the smoker on."""
    for i in range(3):
        try:
            d.set_status(True, 1)
            time.sleep(1)
            power_state()
            return()
        except ConnectionError:
            if i+1 == 3:
                raise ConnectionError("Failed to turn on the smoker.")

def turn_off(**kwargs):
    """Turn the smoker off."""
    for i in range(3):
        try:
            d.set_status(False, 1)
            time.sleep(1)
            power_state()
            return()
        except ConnectionError:
            if i+1 == 3:
                raise ConnectionError("Failed to turn off the smoker.")

def main():
    done = False
    while not done:
        print("A. Turn on the smoker.")
        print("B. Turn off the smoker.")
        print("C. Check if the smoker is on.")
        print("D. Check the current temperatures.")
        print("Q. Quit")
        print("\n")
        user_choice = input("How would you like to proceed? ")

        if user_choice.upper() == "Q": # Quit
            print("\n")
            done = True
        elif user_choice.upper() == "D": # Status
            print("\n")
            print_status()
            print("\n")
        elif user_choice.upper() == "C": # Power State
            print("\n")
            power_state()
            print("\n")
        elif user_choice.upper() == "B": # Smoker off
            print("\n")
            turn_off()
            print("\n")
        elif user_choice.upper() == "A": # Smoker on
            print("\n")
            turn_on()
            print("\n")

if __name__ == "__main__":
    main()

