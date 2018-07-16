import json
import pytuya

d = pytuya.OutletDevice('<gwID>', '<IP>', '<productKey>')
data = d.status()

Debug = False
#Debug = True

if Debug:
    raw = json.dumps(data, indent=4)
    print(raw)

rt_state = data['dps']['1']

if rt_state:
    print('RecTec is on')
else:
    print('RecTec is off')

print('Target Temperature: %r' % data['dps']['102'])
print('Current Temperature: %r' % data['dps']['103'])
print('Probe A Temperature: %r' % data['dps']['105'])
print('Probe B Temperature: %r' % data['dps']['106'])

