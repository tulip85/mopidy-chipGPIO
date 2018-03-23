from __future__ import unicode_literals
import logging
import traceback

from mopidy import core

import RPi.GPIO as GPIO
import time,os

import pykka




logger = logging.getLogger(__name__)


class chipGPIO(pykka.ThreadingActor, core.CoreListener):

    def eventDetected(self, channel):
        if channel == self.config['chipGPIO']['play_pin']:
            logger.info("pause")
            if self.core.playback.state.get() == "playing":
                self.core.playback.pause()
            elif self.core.playback.state.get() == "stopped":
                self.core.playback.play()
            else:
                self.core.playback.resume()
            
        if channel == self.config['chipGPIO']['previous_pin']:
            logger.info("previous")
            self.core.playback.previous()
            
        if channel == self.config['chipGPIO']['next_pin']:
            logger.info("next")
            self.core.playback.next()
            
        if channel == self.config['chipGPIO']['stop_pin']:
            logger.info("stop")
            self.core.playback.stop()

    def __init__(self, config, core):
        super(chipGPIO, self).__init__()
        self.menu = False
        self.core = core
        self.config = config
        GPIO.setmode(GPIO.BOARD)
        
        #register buttons
        if config['chipGPIO']['play_pin']:
            GPIO.setup(config['chipGPIO']['play_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(config['chipGPIO']['play_pin'], GPIO.RISING)
            GPIO.add_event_callback(config['chipGPIO']['play_pin'], self.eventDetected)
            
        if config['chipGPIO']['previous_pin']:
            GPIO.setup(config['chipGPIO']['previous_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(config['chipGPIO']['previous_pin'], GPIO.RISING)
            GPIO.add_event_callback(config['chipGPIO']['previous_pin'], self.eventDetected)
            
        if config['chipGPIO']['next_pin']:
            GPIO.setup(config['chipGPIO']['next_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(config['chipGPIO']['next_pin'], GPIO.RISING)
            GPIO.add_event_callback(config['chipGPIO']['next_pin'], self.eventDetected)
            
        if config['chipGPIO']['stop_pin']:
            GPIO.setup(config['chipGPIO']['stop_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(config['chipGPIO']['stop_pin'], GPIO.RISING)
            GPIO.add_event_callback(config['chipGPIO']['stop_pin'], self.eventDetected)
        
