#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2018  Seeed Technology Co.,Ltd.
#
'''
This is the grove.gpio.GPIO implemented by lgpio.
'''
import lgpio

class GPIO:
    OUT = 1
    IN = 0

    def __init__(self, pin, direction=None):
        self.pin = pin
        self.chip = lgpio.gpiochip_open(4)  # Raspberry Pi 5 uses gpiochip4
        if direction is not None:
            self.dir(direction)
        self._event_handle = None

    def dir(self, direction):
        lgpio.gpio_claim_output(self.chip, self.pin) if direction == self.OUT else lgpio.gpio_claim_input(self.chip, self.pin)

    def write(self, output):
        lgpio.gpio_write(self.chip, self.pin, output)

    def read(self):
        return lgpio.gpio_read(self.chip, self.pin)

    def _on_event(self, chip, event, timestamp):
        value = self.read()
        if self._event_handle:
            self._event_handle(self.pin, value)

    @property
    def on_event(self):
        return self._event_handle

    @on_event.setter
    def on_event(self, handle):
        if not callable(handle):
            return

        if self._event_handle is None:
            lgpio.gpio_claim_alert(self.chip, self.pin, lgpio.BOTH_EDGES)
            lgpio.gpio_register_callback(self.chip, self.pin, self._on_event)

        self._event_handle = handle

    def close(self):
        lgpio.gpiochip_close(self.chip)