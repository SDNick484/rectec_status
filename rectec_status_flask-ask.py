# Currently depedent on Flask-Ask and python-tuya
# Tested on Gentoo Linux, ebuilds for above packages available at
# https://github.com/SDNick484/rectec_status/
#
# This script requires the following variables which can be found 
# with the device discover script on above GitHub site:
# XXXXXXXXXXXXXXXXXXXX = gwID (also known as devID)
# YYY.YYY.YYY.YYY = IP address of smoker
# ZZZZZZZZZZZZZZZZ = productKey, does not need to be real value
#

import logging
import os

import pytuya

from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
#logging.getLogger('flask_ask').setLevel(logging.DEBUG)

# I originally was only polling data at start-up, need to eventually move it to a function
#def getRecTecInfo():
#    d = pytuya.OutletDevice('XXXXXXXXXXXXXXXXXXXX', 'YYY.YYY.YYY.YYY', 'ZZZZZZZZZZZZZZZZ')
#    data = d.status()


# Launch the skill, response when you say "Open rectec stats"
@ask.launch
def launch():
    speech_text = 'Welcome to Rectec Status!'
    return question(speech_text).reprompt(speech_text)

# Power intent to check if RecTec is powered on
@ask.intent('powerIntent')
def powerIntent():
    d = pytuya.OutletDevice('XXXXXXXXXXXXXXXXXXXX', 'YYY.YYY.YYY.YYY', 'ZZZZZZZZZZZZZZZZ')
    data = d.status()  
    rt_state = data['dps']['1']
    if rt_state:
        speech_text = 'Power is on'
        return statement(speech_text)
    else:
        speech_text = 'Power is off'
        return statement(speech_text)

# Intent to check current temperature
# Value is "0" if RecTec is not on
@ask.intent('currentTemperatureIntent')
def currentTemperatureIntent():
    d = pytuya.OutletDevice('XXXXXXXXXXXXXXXXXXXX', 'YYY.YYY.YYY.YYY', 'ZZZZZZZZZZZZZZZZ')
    data = d.status()  
    return statement('Current temperature is %r' % data['dps']['103'])

# Intent to check target temperature
@ask.intent('targetTemperatureIntent')
def targetTemperatureIntentResponse():
    d = pytuya.OutletDevice('XXXXXXXXXXXXXXXXXXXX', 'YYY.YYY.YYY.YYY', 'ZZZZZZZZZZZZZZZZ')
    data = d.status()  
    return statement('Target temperature is %r' % data['dps']['102'])

# Intent to check Probe A temperature
# I believe it returns the value from when it was last "on"
@ask.intent('probeATemperatureIntent')
def probeATemperatureIntentResponse():
    d = pytuya.OutletDevice('XXXXXXXXXXXXXXXXXXXX', 'YYY.YYY.YYY.YYY', 'ZZZZZZZZZZZZZZZZ')
    data = d.status()  
    return statement('Probe A temperature is %r' % data['dps']['106'])

# Intent to check Probe B temperature
# I believe it returns the value from when it was last "on"
@ask.intent('probeBTemperatureIntent')
def probeBTemperatureIntentResponse():
    d = pytuya.OutletDevice('XXXXXXXXXXXXXXXXXXXX', 'YYY.YYY.YYY.YYY', 'ZZZZZZZZZZZZZZZZ')
    data = d.status()  
    return statement('Probe B temperature is %r' % data['dps']['106'])

# Intent that pulls everything mentioned above
@ask.intent('everythingIntent')
def everythingIntentResponse():
    d = pytuya.OutletDevice('XXXXXXXXXXXXXXXXXXXX', 'YYY.YYY.YYY.YYY', 'ZZZZZZZZZZZZZZZZ')
    data = d.status()  
    rt_state = data['dps']['1']
    if rt_state:
        everything_text = 'Power is on'
    else:
        everything_text = 'Power is off'
    target = ', target temperature is %r' % data['dps']['102']
    everything_text += target
    current = ', current temperature is %r' % data['dps']['103']
    everything_text += current
    probea = ', probe A temperature is %r' % data['dps']['105']
    everything_text += probea
    probeb = ', probe B temperature is %r' % data['dps']['106']
    everything_text += probeb
    return statement(everything_text)

# To do - write built-in intents
#@ask.intent('AMAZON.HelpIntent')
#def help():
#    speech_text = 'You can say hello to me!'
#    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)
#    return question(speech_text).reprompt(speech_text)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    speech_text = "Sorry, I didn't get that."
    question_text = "You can ask me the power status, target or current temperature, or the temperature of probe a or b"
    return question(speech_text).reprompt(question_text)

# End session
@ask.session_ended
def session_ended():
    return "{}", 200

# Start the service
# It listens locally on port 5000 (i.e. http://127.0.0.1:5000)
# To work with Alexa, this should be fronted by a web server or reverse proxy
# Web server or proxy should have a valid certificate
# I currently use Apache 2.4 with mod_proxy
if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=False)
