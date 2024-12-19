import simplepyble
print(f"Running on {simplepyble.get_operating_system()}")
adapters = simplepyble.Adapter.get_adapters()

if len(adapters) == 0:
    print("No adapters found")

for adapter in adapters:
    print(f"Adapter: {adapter.identifier()} [{adapter.address()}]")

if len(adapters) != 1:
    print("Please connect only one adapter")
    exit(1)

adapter = adapters[0]
adapter.set_callback_on_scan_start(lambda: print("Scan started."))
adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
def ble_log(peripheral):
    return print(f"Found {peripheral.address()} [{peripheral.identifier()}]")
adapter.set_callback_on_scan_found(ble_log)


def ble_scan(adapter, device_name, timeout=5000):
    device = None
    def on_receive(scan_entry):
        nonlocal device
        if scan_entry.identifier() == device_name and device == None:
            device = scan_entry
            print(f"Found {device.address()} [{device.identifier()}]")
    adapter.set_callback_on_scan_found(on_receive)
    adapter.scan_for(timeout)
    adapter.set_callback_on_scan_found(ble_log)

    return device