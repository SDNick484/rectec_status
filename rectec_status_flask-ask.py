# Currently depedent on Flask-Ask and python-tuya
# Tested on Gentoo Linux, ebuilds for above packages available at
# https://github.com/SDNick484/rectec_status/
#
# This script requires the following variables which can be found 
# with the device discover script on above GitHub site:
# GW_ID = gwID (also known as devID)
# LOCAL_IP = IP address of smoker
# LOCAL_KEY = productKey, does not need to be real value
#

import logging
import os
import pytuya
import time

import rt_function as rt

from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
#logging.getLogger('flask_ask').setLevel(logging.DEBUG)

# I originally was only polling data at start-up, need to eventually move it to a function
#def getRecTecInfo():
#    d = pytuya.OutletDevice('GW_ID', 'LOCAL_IP', 'LOCAL_KEY')
#    data = d.status()


# Launch the skill, response when you say "Open rectec stats"
@ask.launch
def launch():
    speech_text = 'Welcome to Rectec Status!'
    return question(speech_text).reprompt(speech_text).simple_card('Welcome', speech_text)

# Power intent to check if RecTec is powered on
@ask.intent('powerIntent')
def powerIntent():
    rt_state = rt.get_status()
    if rt_state['dps']['1']:
        speech_text = 'Your RecTec is powered on.'
        return statement(speech_text).simple_card('Power', speech_text)
    else:
        speech_text = 'Your RecTec is powered off.'
        return statement(speech_text).simple_card('Power', speech_text)

@ask.intent('turnOnIntent')
def turnOnIntent():
    rt.turn_on()
    time.sleep(1)
    rt_state = rt.get_status()
    if rt_state['dps']['1']:
        speech_text = 'Your RecTec is now powered on.'
        return statement(speech_text).simple_card('Power', speech_text)
    else:
        speech_text = 'Unable to turn your RecTec on.'
        return statement(speech_text).simple_card('Power', speech_text)

@ask.intent('turnOffIntent')
def turnOffIntent():
    rt.turn_off()
    time.sleep(1)
    rt_state = rt.get_status()
    if not rt_state['dps']['1']:
        speech_text = 'Your RecTec is now powered off.'
        return statement(speech_text).simple_card('Power', speech_text)
    else:
        speech_text = 'Unable to turn your RecTec off.'
        return statement(speech_text).simple_card('Power', speech_text)

# Intent to check current temperature
# Value is "0" if RecTec is not on
@ask.intent('currentTemperatureIntent')
def currentTemperatureIntent():
    rt_state = rt.get_status()
    speech_text = 'Current temperature is %r' % rt_state['dps']['103']
    return statement(speech_text).simple_card('Current Temp', speech_text)

# Intent to check target temperature
@ask.intent('targetTemperatureIntent')
def targetTemperatureIntentResponse():
    rt_state = rt.get_status()
    speech_text = 'Target temperature is %r' % rt_state['dps']['102']
    return statement(speech_text).simple_card('Target Temp', speech_text)

# Intent to check Probe A temperature
# I believe it returns the value from when it was last "on"
@ask.intent('probeATemperatureIntent')
def probeATemperatureIntentResponse():
    rt_state = rt.get_status()
    speech_text = 'Probe A temperature is %r' % rt_state['dps']['105']
    return statement(speech_text).simple_card('Probe A Temp', speech_text)

# Intent to check Probe B temperature
# I believe it returns the value from when it was last "on"
@ask.intent('probeBTemperatureIntent')
def probeBTemperatureIntentResponse():
    rt_state = rt.get_status()
    speech_text = 'Probe B temperature is %r' % rt_state['dps']['106']
    return statement(speech_text).simple_card('Probe B Temp', speech_text)

# Intent that pulls everything mentioned above
@ask.intent('everythingIntent')
def everythingIntentResponse():
    rt_state = rt.get_status()
    if rt_state['dps']['1']:
        everything_text = 'Your RecTec is powered on'
    else:
        everything_text = 'Your RecTec is powered off'
    target = ', Target temperature is %r' % rt_state['dps']['102']
    everything_text += target
    current = ', Current temperature is %r' % rt_state['dps']['103']
    everything_text += current
    probea = ', Probe A temperature is %r' % rt_state['dps']['105']
    everything_text += probea
    probeb = ', Probe B temperature is %r' % rt_state['dps']['106']
    everything_text += probeb
    return statement(everything_text).simple_card('Everything', everything_text)

# To do - write built-in intents
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can ask me the power status, target or current temperature, or the temperature of probe A or B, or ask me to tell you everything'
    return question(speech_text).reprompt(speech_text).simple_card('Help', speech_text)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    speech_text = "Sorry, I didn't get that."
    question_text = "You can ask me the power status, target or current temperature, or the temperature of probe A or B, or ask me to tell you everything"
    return question(speech_text).reprompt(question_text).simple_card('Help', question_text)

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
