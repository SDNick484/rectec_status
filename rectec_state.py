import json
import pytuya

# Specify the smoker and get its status
d = pytuya.OutletDevice('<gwID>', '<IP>', '<productKey>')
data = d.status()

# Enable debug to see the raw JSON
Debug = False
#Debug = True
if Debug:
    raw = json.dumps(data, indent=4)
    print(raw)

# Simple if statement to check if the smoker is on
rt_state = data['dps']['1']

if rt_state:
    print('RecTec is on')
else:
    print('RecTec is off')

# The following values are based on observation
# dps = '102' & '103' might be swapped
print('Target Temperature: %r' % data['dps']['102'])
print('Current Temperature: %r' % data['dps']['103'])
# When smoker is off (data['dps']['1] = False)
# values of probes might be based on last "on"
print('Probe A Temperature: %r' % data['dps']['105'])
print('Probe B Temperature: %r' % data['dps']['106'])

