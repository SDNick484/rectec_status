# rectec_status
Scripts to talk to [RecTec pellet smokers](http://www.rectecgrills.com/) with WiFi controllers 

The WiFi controllers on RecTec smokers leverage the [Tuya Smart IoT platform](https://en.tuya.com/) which can be reached over TCP or MQTT.  The scripts currently leverage [python-tuya](https://github.com/clach04/python-tuya) and communicate via TCP on port 6668 over the LAN.  Through additional exploration and collaboration, I'd like to expand the scripts to support remote access via MQTT.

### Device Information
Details of what's possible with the RecTec are still being discovered.  The device returns JSON output such as:
```
{
    "devId": "##################", \\ 20 character device ID, not clear if its unique or same for all RecTecs
    "dps": {
        "1": false,   \\ bool, True if on, False if off
        "102": 275,   \\ number, "Target" temperature
        "103": 0,     \\ number, "Current" temperature
        "104": 60,    \\ number, minimum feed rate, 60 = 6.0%
        "105": 112,   \\ number, "Probe A" temperature
        "106": 107,   \\ number, "Probe B" temperature
        "107": 0,     \\ number, unknown
        "109": false, \\ bool, unknown
        "110": false, \\ bool, unknown
        "111": false  \\ bool, unknown
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
