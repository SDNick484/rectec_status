"""
Simple platform to control **SOME** Tuya switch devices.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.tuya/
"""

import logging
import asyncio

from homeassistant.components.climate.const import (
    STATE_HEAT, STATE_COOL, STATE_ECO, STATE_FAN_ONLY, STATE_IDLE, STATE_MANUAL, STATE_AUTO,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_OPERATION_MODE, SUPPORT_FAN_MODE, 
    SUPPORT_ON_OFF, SUPPORT_AWAY_MODE)


from homeassistant.components.climate import (PLATFORM_SCHEMA,  ENTITY_ID_FORMAT, ClimateDevice)

from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_ID, PRECISION_WHOLE, TEMP_CELSIUS, TEMP_FAHRENHEIT , ATTR_TEMPERATURE)

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from time import time
from time import sleep
from threading import Lock

REQUIREMENTS = ['pytuya==7.0.2']

_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_ID = 'device_id'
CONF_LOCAL_KEY = 'local_key'
CONF_MIN_TEMP = 'min_temp'
CONF_MAX_TEMP = 'max_temp'

DEVICE_TYPE = 'climate'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_DEVICE_ID): cv.string,
    vol.Required(CONF_LOCAL_KEY): cv.string,
    vol.Optional(CONF_MIN_TEMP): vol.Coerce(float),
    vol.Optional(CONF_MAX_TEMP): vol.Coerce(float)
})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up of the Tuya switch."""
    import pytuya
    
    
    name = config.get(CONF_NAME)
    dev_id = config.get(CONF_DEVICE_ID)
    host = config.get(CONF_HOST)
    local_key = config.get(CONF_LOCAL_KEY)
    min_temp = config.get(CONF_MIN_TEMP)
    max_temp = config.get(CONF_MAX_TEMP)
    
    climate = []
    
    climate_device = TuyaCache(
        pytuya.OutletDevice(
            config.get(CONF_DEVICE_ID),
            config.get(CONF_HOST),
            config.get(CONF_LOCAL_KEY) 
        )
    )
    
   
    climate.append(
        TuyaClimate(
            climate_device,
            config.get(CONF_NAME),
            None, 
            None, 
            None, 
            None, 
            TEMP_CELSIUS, 
            min_temp, 
            max_temp
        )
    )


    async_add_entities(climate)

class TuyaCache:
    
    def __init__(self, device):
        """Initialize the cache."""
        self._cached_status = ''
        self._cached_status_time = 0
        self._device = device
        self._lock = Lock()

    def __get_status(self):
        for i in range(5):
            try:
                status = self._device.status()
                _LOGGER.debug("Debug LocalTuya: " + str(status))
                return status
            except ConnectionError:
                if i+1 == 5:
                    _LOGGER.warning("Failed to update status")
                    raise ConnectionError("Failed to update status.")

    def set_status(self, state, switchid):
        self._cached_status = ''
        self._cached_status_time = 0
        return self._device.set_status(state, switchid)

    def status(self):
        """Get state of Tuya switch and cache the results."""
        self._lock.acquire()
        try:
           now = time()
           _LOGGER.debug("UPDATING status")
           self._cached_status = self.__get_status()
           self._cached_status_time = time()
           return self._cached_status
        finally:
            self._lock.release()



class TuyaClimate(ClimateDevice):
    """Representation of a Tuya switch."""

    def __init__(self, device, name, target_temperature,current_temperature, current_operation, is_on, unit_of_measurement, min_temp, max_temp):
        """Initialize the Tuya switch."""
        self._away = None
        self._device = device
        self._name = name
        self._lock = Lock()
        self._target_temperature = target_temperature
        self._current_temperature = current_temperature
        self._current_operation = current_operation
        self._unit_of_measurement = unit_of_measurement
        self._state = is_on
        self._min_temp = min_temp
        self._max_temp = max_temp
        self._support_flags = SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE | SUPPORT_ON_OFF | SUPPORT_AWAY_MODE
        self._temp_precision = 0.5
        self._operation_list = [STATE_IDLE, STATE_MANUAL, STATE_HEAT, STATE_AUTO, STATE_ECO]
        status = self._device.status()

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        if self._min_temp:
            return self._min_temp

        # get default temp from super class
        return super().min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        if self._max_temp:
            return self._max_temp

        # Get default temp from super class
        return super().max_temp

    
    @property
    def is_away_mode_on(self):
        """Return if away mode is on."""
        
        return self._away
    
    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return [STATE_HEAT, STATE_AUTO, STATE_ECO]
        
    @property
    def name(self):
        """Get name of Tuya switch."""
        return self._name

    @property
    def is_on(self):
        """Check if Tuya switch is on."""
        return self._state
        
    @property
    def current_temperature(self):
        """Return the sensor temperature."""
        return self._current_temperature

    @property
    def current_operation(self):
        """Return current operation."""
        return self._current_operation

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature
        
    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement
        
    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._support_flags

    async def async_turn_on(self, **kwargs):
        """Turn Tuya switch on."""
        self._lock.acquire()
        self._device.set_status(True, '1')
        self._lock.release()

    async def async_turn_off(self, **kwargs):
        """Turn Tuya switch off."""
        self._lock.acquire()
        self._device.set_status(False, '1')
        self._lock.release()
    
    async def async_set_temperature(self, **kwargs):
        while True:
           try:
               self._lock.acquire()
               temperature = int(float(kwargs[ATTR_TEMPERATURE])*2)
               _LOGGER.debug("Set Temperature: " + str(temperature))
               if ATTR_TEMPERATURE in kwargs:
                   self._device.set_status(temperature, '2')
                   sleep(1)
               self._lock.release()
           except:
               _LOGGER.warning("Set Temperature Retry")
               continue
           break
            
            
    def turn_away_mode_on(self):
        """Turn away on."""
        self._lock.acquire()
        self._device.set_status( True , '5')
        self._lock.release()

    def turn_away_mode_off(self):
        """Turn away off."""
        self._lock.acquire()
        self._device.set_status( False , '5')
        self._lock.release()
        
    async def async_set_operation_mode(self, operation_mode):
        """Set operation mode."""
        self._lock.acquire()
        if operation_mode == STATE_HEAT:
            self._device.set_status( '1' , '4')
        elif operation_mode == STATE_AUTO:
            self._device.set_status( '0' , '4')
        elif operation_mode == STATE_ECO:
            self._device.set_status( True , '5')
        else:
            _LOGGER.error("Unrecognized operation mode: %s", operation_mode)
            return
        sleep(1)
        self.schedule_update_ha_state()
        self._lock.release()
    
    async def async_update(self):
        """Get state of Tuya switch."""
        _LOGGER.debug("UPDATING")
        try:
           status = self._device.status()
           self._target_temperature = float(status['dps']['2']) /2
           self._current_temperature = float(status['dps']['3']) /2
           self._state = status['dps']['1']
           
           auto_manual = status['dps']['4']
           eco_mode = status['dps']['5']
           if eco_mode == True:
               self._away = True
           else:
               self._away = False
           on_off = status['dps']['1']
           _LOGGER.debug("Device: " + str(status['devId']))
           
           if str(auto_manual) == '0':
              mode = 'Auto'
           else:
              mode = 'Manual'
           
           if on_off == False:
              self._current_operation = STATE_IDLE
           if auto_manual == '0':
              self._current_operation = STATE_AUTO
           else:
              self._current_operation = STATE_HEAT
           if eco_mode == True:
              self._current_operation = STATE_ECO
        except:
            _LOGGER.debug("Update Fail, maybe device busy")
        
