# rectec_status
Scripts to talk to [Rec Tec Grills pellet smokers](http://www.rectecgrills.com/) with the Rec Tec Wi-Pellet WiFi controllers.  Supported models include the  RT-340, RT-590, & RT-700 which all include the WiFi controller by default, and the RT-300 & RT-680 that are upgradable to the WiFi controller.

The WiFi controllers on RecTec smokers leverage the [Tuya Smart IoT platform](https://en.tuya.com/) which can be reached over TCP or MQTT.  The scripts currently leverage [python-tuya](https://github.com/clach04/python-tuya) and communicate via TCP on port 6668 over the LAN.  Through additional exploration and collaboration, I'd like to expand the scripts to support remote access via MQTT.

### Device Information
JSON schema has been posted, a quick summary is below:
```
{
    "devId": "##################", \\ 20 character device ID, not clear if its unique or same for all RecTecs
    "dps": {
        "1": false,   \\ "Power", bool, rw, True if on, False if off
        "102": 275,   \\ "Set_temp", number, rw, Target ("Set Point") temperature
        "103": 0,     \\ "Actual_temp", number, ro, Current ("Actual") temperature
        "104": 60,    \\ "Min_Feedrate", number, rw, Minimum feeding amount, 60 = 6.0%
        "105": 112,   \\ "Food_temp1", number, ro, "Probe A" temperature
        "106": 107,   \\ "Food_temp2", number, ro, "Probe B" temperature
        "107": 0,     \\ "Temp_adjust", number, rw, "Temperature Calibration" 
        "108": false, \\ "Temp_unit", bool, ro, unavailable
        "109": false, \\ "ER1_alarm", bool, ro
        "110": false, \\ "ER2_alarm", bool, ro
        "111": false  \\ "ER3_alarm", bool, ro
    }
}
```
It also broadcasts over UDP port 6666 some potentially useful information in the format of:
```
{"ip":"xxx.xxx.xxx.xxx","gwId":"##################","active":2,"ability":0,"mode":0,"encrypt":true,"productKey":"yyyyyyyyyyyyyyyy","version":"3.1"}
```
where "ip" is the IP address of the controller, gwID is the devID in the JSON output above, and productKey is presumably some sort of key that will likely be required to set values.

### Dependencies
  * The Alexa skill requires [Flask-Ask](https://github.com/johnwheeler/flask-ask) & [python-tuya](https://github.com/clach04/python-tuya)
  * Additionally, to leverage the Alexa skill, you will need a web server or reverse proxy with a publicly signed certificate or a self-signed cert to forward the responses to Alexa.   

### Acknowledgements
  * Special thanks for all the hard work of [codetheweb](https://github.com/codetheweb/), [clach04](https://github.com/clach04), [blackrozes](https://github.com/blackrozes), [jepsonrob](https://github.com/jepsonrob), and all the other contributers on [tuyapi](https://github.com/codetheweb/tuyapi) and [python-tuya](https://github.com/clach04/python-tuya) who have made communicating to Tuya decices possible with open source code.
* Additional thanks to [John Wheeler](https://github.com/johnwheeler) of [Flask-Ask](https://github.com/johnwheeler/flask-ask) for greatly simplifying the process of building Alexa skills in Python.
