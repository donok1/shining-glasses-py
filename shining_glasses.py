from enum import Enum
from decorators import Service, WriteCharacteristic
from util import assert_type, assert_int_range, assert_equal
from dataclasses import dataclass
from typing import Optional, Tuple

class SGTextMode(Enum):
    TEXT_STATIC = 1
    TEXT_BLINK = 2
    TEXT_SCROLL_RTL = 3
    TEXT_SCROLL_LTR = 4

class SGBackgroundColorMode(Enum):
    STATIC = 1
    RAINBOW = 2
    GRADIENT = 3

    BG_X = 4
    BG_XMAS = 5
    BG_LOVE = 6
    BG_SCREAM = 7

@dataclass
class SGTextType:
    content: str
    mode: SGTextMode
    speed: Optional[int]
    background_mode: Optional[SGBackgroundColorMode]
    background: Optional[Tuple[int, int, int]]
    foreground: Optional[Tuple[int, int, int]]

class SGText:
    text = SGTextType(
        "Hello, World!",
        SGTextMode.TEXT_STATIC,
        1,
        (0, 0, 0),
        (255, 255, 255)
    )

    def __init__(self, shining_glasses, text=None):
        self.shining_glasses = shining_glasses
        if text:
            self.text = text

    def update(self):
        if self.text.background_mode:
            self.shining_glasses.set_text_color_mode(self.text.background_mode)
        if self.text.background:
            self.shining_glasses.set_text_background_color(self.text.background)
        if self.text.foreground:
            self.shining_glasses.set_text_foreground_color(self.text.foreground)
        if self.text.speed:
            self.shining_glasses.set_text_speed(self.text.speed)
        self.shining_glasses.set_mode(self.text.mode)
        self.shining_glasses.set_text(self.text.content)

    def __str__(self):
        return f"SGText({self.text})"

class ShiningGlasses():
    def __init__(self, driver):
        self.driver = driver

    def _assert_connected(self):
        if not self.driver.is_connected():
            raise Exception("Not connected to the device")

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def play(self, n_imgs = 1, img_idcs = [0], **k):
        self._assert_connected()
        assert_type(n_imgs, int)
        assert_type(img_idcs, list)
        assert_int_range(n_imgs, 1, 255)
        assert_int_range(len(img_idcs), 1, 255)
        assert_equal(len(img_idcs), n_imgs)

        command = b'\x06PLAY' + bytes([n_imgs]) + bytes(img_idcs)
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129601")
    def subscribe_to_notifications(self, **k):
        self._assert_connected()
        status = self.driver.notify(**k)
        print(f"Subscribed: {status}")
        return status

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129601")
    def check(self, **k):
        self._assert_connected()
        self.driver.request(value=b'\x06CHEC', **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def set_light(self, brightness=0, **k):
        self._assert_connected()
        assert_type(brightness, int)
        assert_int_range(brightness, 0, 100)

        command = b'\x06LIGHT' + bytes([brightness])
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def set_image(self, img_idx=0, **k):
        self._assert_connected()
        assert_type(img_idx, int)
        assert_int_range(img_idx, 0, 21)
        command = b'\x06IMAG' + bytes([img_idx])
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def set_animation(self, img_idx=0, **k):
        self._assert_connected()
        assert_type(img_idx, int)
        assert_int_range(img_idx, 0, 21)
        command = b'\x06ANIM' + bytes([img_idx])
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def request_upload(self, image_length, **k):
        self._assert_connected()
        assert_type(image_length, int)
        assert_int_range(image_length, 0, 65535)
        command = b'\x06DATS' + image_length.to_bytes(2, 'big')
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def set_mode(self, mode, **k):
        self._assert_connected()
        if isinstance(mode, ShiningGlasses.SGTextMode):
            mode = mode.value
        assert_type(mode, int)
        assert_int_range(mode, 0, 5)
        command = b'\x06MODE' + bytes([mode])
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def set_text_speed(self, speed, **k):
        self._assert_connected()
        assert_type(speed, int)
        assert_int_range(speed, 0, 255)
        command = b'\x06SPEED' + bytes([speed])
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def set_text_color_mode(self, mode, **k):
        self._assert_connected()
        if isinstance(mode, ShiningGlasses.SGBackgroundColorMode):
            mode = mode.value
        assert_type(mode, int)
        assert_int_range(mode, 0, 7)
        command = b'\x06M' + bytes([mode])
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def set_text_foreground_color(self, color, **k):
        self._assert_connected()
        assert_equal(len(color), 3)
        assert_type(color[0], int)
        command = b'\x06FC' + bytes([color[0], color[1], color[2]])
        return self.driver.write(value=command, **k)

    @Service("0000fff0-0000-1000-8000-00805f9b34fb")
    @WriteCharacteristic("d44bc439-abfd-45a2-b575-925416129600")
    def set_text_background_color(self, color, **k):
        self._assert_connected()
        assert_equal(len(color), 3)
        assert_type(color[0], int)
        command = b'\x06BG' + bytes([color[0], color[1], color[2]])
        return self.driver.write(value=command, **k)
