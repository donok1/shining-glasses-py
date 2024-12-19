from constants import AES_KEY, AES_MODE, DEFAULT_ATTEMPTS
from ble import ble_scan
from Crypto.Cipher import AES

cipher = AES.new(AES_KEY, AES_MODE)

class BLENotifications:
    callbacks = {}
    def __init__(self, driver):
        self.driver = driver

    def _key_from_kwargs(self, **k):
        if not k or 'suid' not in k or 'write_characteristic' not in k:
            raise ValueError("suid and write_characteristic are required")
        return f"{k['suid']}-{k['write_characteristic']}"

    def add_callback(self, callback, **k):
        unique_key = self._key_from_kwargs(**k)
        if unique_key not in self.driver.callbacks:
            self.driver.callbacks[unique_key] = set()
        self.driver.callbacks[unique_key].add(callback)

    def remove_callback(self, callback, **k):
        unique_key = self._key_from_kwargs(**k)
        if unique_key in self.driver.callbacks:
            self.driver.callbacks[unique_key].remove(callback)

    def dispatch(self, payload, **k):
        unique_key = self._key_from_kwargs(**k)
        if unique_key in self.driver.callbacks:
            for cb in list(self.driver.callbacks[unique_key]):
                cb(payload)


class BLEDriver:
    device = None
    notifications = BLENotifications()
    cipher = None

    _connected = False
    _align_amount = None

    def __init__(self, adapter, encryption=(AES_KEY, AES_MODE), align_amount=16, device_name=None):
        self.adapter = adapter
        if encryption:
            self.cipher = AES.new(*encryption)
        self._align_amount = align_amount
        self.device_name = device_name

    def align(self, value):
        if not self._align_amount:
            return value
        return value.ljust(self._align_amount, b'\x00')

    def encrypt(self, value):
        if not self.cipher:
            return value
        return self.cipher.encrypt(self.align(value))

    def connect(self):
        if not self.device_name:
            print("Device name is required")
            return

        device = None
        for i in range(DEFAULT_ATTEMPTS):
            device = ble_scan(self.adapter, self.device_name)
            if device is not None:
                break
        if not device:
            print("Device not found")
            return

        device.connect()
        print(f"Connected to {device.identifier()} [{device.address()}]")

        self.device = device
        self._connected = True

    def disconnect(self):
        if not self._connected:
            print("Not connected to device")
            return
        self.device.disconnect()
        self._connected = False

    def write(self, **k):
        show_command = k.pop('show_command', False)
        suid, write_characteristic, value = k.get('suid'), k.get('write_characteristic'), k.get('value')
        if not self._connected:
            print("Not connected to device")
            return

        show_command and print(f"[Write] {value}")
        value = self.encrypt(value)
        self.device.write_command(suid, write_characteristic, value)

    def read(self, **k):
        show_command = k.pop('show_command', False)
        suid, read_characteristic, value = k.get('suid'), k.get('read_characteristic'), k.get('value')
        if not self._connected:
            print("Not connected to device")
            return

        show_command and print(f"[Read] {value}")
        value = self.encrypt(value)
        return self.device.read_request(suid, read_characteristic, value)

    def request(self, **k):
        show_command = k.pop('show_command', False)
        suid, write_characteristic, value = k.get('suid'), k.get('write_characteristic'), k.get('value')
        if not self._connected:
            print("Not connected to device")
            return

        show_command and print(f"[Request] {value}")
        value = self.encrypt(value)
        return self.device.write_request(suid, write_characteristic, value)

    def notify(self, **k):
        suid, write_characteristic = k.get('suid'), k.get('write_characteristic'), k.get('value')
        if not self._connected:
            print("Not connected to device")
            return

        unique_key = f"{suid}-{write_characteristic}"
        if unique_key not in self.notifications.callbacks:
            self.notifications.callbacks[unique_key] = set()

        def callback(payload):
            self.notifications.dispatch(payload, **k)

        return self.device.notify(suid, write_characteristic, callback)


class ShiningGlassesDriver(BLEDriver):
    def __init__(self, adapter):
        super().__init__(
            adapter,
            encryption=(AES_KEY, AES_MODE),
            align_amount=16,
            device_name="GLASSES-02FB6E"
        )