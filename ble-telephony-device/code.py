"""
!!!
This usage is likely not supported by the host OS.
!!!
"""
import time
import struct

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
# from adafruit_hid.keyboard import Keyboard
# from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
# from adafruit_hid.keycode import Keycode
# from adafruit_hid.mouse import Mouse
# from adafruit_hid.consumer_control import ConsumerControl
# from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid import find_device

# Vendor-Defined Report (Report ID 5/6, USAGE 0xFFFE) was attached
hid_descriptor = (
    b"\x05\x0B"  # USAGE_PAGE (Telephony Devices)
    b"\x09\x05"  # USAGE (Headset)
    b"\xA1\x01"  # COLLECTION (Application)
    b"\x85\x01"  # REPORT_ID (1)
    b"\x15\x00"  # LOGICAL_MINIMUM (0)
    b"\x25\x01"  # LOGICAL_MAXIMUM (1)
    b"\x75\x01"  # REPORT_SIZE (1)
    b"\x95\x02"  # REPORT_COUNT (2)
    b"\x09\x20"  # USAGE (Hook Switch)
    b"\x09\x2F"  # USAGE (Phone Mute)
    b"\x81\x02"  # INPUT (Data, Variable, Absolute)
    b"\x95\x06"  # REPORT_COUNT (6)
    b"\x81\x03"  # INPUT (Constant, Variable, Absolute)

    b"\x85\x02"  # REPORT_ID (2)
    b"\x15\x00"  # LOGICAL_MINIMUM (0)
    b"\x25\x01"  # LOGICAL_MAXIMUM (1)
    b"\x75\x01"  # REPORT_SIZE (1)
    b"\x95\x03"  # REPORT_COUNT (3)
    b"\x05\x08"  # USAGE_PAGE (LED)  <-- ここを追加
    b"\x09\x47"  # USAGE (Mute LED)
    b"\x09\x48"  # USAGE (Off-Hook LED)
    b"\x09\x4B"  # USAGE (Ring LED)
    b"\x91\x02"  # OUTPUT (Data, Variable, Absolute)
    b"\x95\x05"  # REPORT_COUNT (5)
    b"\x91\x03"  # OUTPUT (Constant, Variable, Absolute)
    b"\xC0"      # END COLLECTION
)

try:
    hid = HIDService(hid_descriptor=hid_descriptor)
except Exception as e:
    import sys
    print("HIDService init failed:", e)
    print("hid_descriptor type:", type(hid_descriptor), "len:", len(
        hid_descriptor) if hid_descriptor is not None else None)
    print("hid_descriptor repr:", repr(hid_descriptor)[:200])
    raise

device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
# Advertise as Generic Wearable Audio Device
# https://www.bluetooth.com/specifications/assigned-numbers/
advertisement.appearance = 0x0940
scan_response = Advertisement()
scan_response.complete_name = "CP_Telephony"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected")
    print(ble.connections)

# k = Keyboard(hid.devices)
# kl = KeyboardLayoutUS(k)
# cc = ConsumerControl(hid.devices)
# m = Mouse(hid.devices)
vd = find_device(hid.devices, usage_page=0x0b, usage=0x05)

while True:
    ite = 0
    while not ble.connected:
        pass
    print("Start typing:")

    while ble.connected:
        while (ite < 100):
            print("ite:", ite)
            # k.send(Keycode.SHIFT, Keycode.L)  # add shift modifier
            # cc.press(ConsumerControlCode.VOLUME_DECREMENT)
            # cc.release()
            # m.move(x=4, y=2)
            time.sleep(1)
            to_send_1b = bytearray(1)
            # send hook command
            if ite % 10 == 9:
                struct.pack_into("<B", to_send_1b, 0, 1)
                vd.send_report(to_send_1b)
            print(f"write(id1): {to_send_1b}")
            print(f"read(id2): {vd.get_last_received_report(2)}")
            ite += 1

    ble.start_advertising(advertisement)
