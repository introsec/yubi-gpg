#!/usr/bin/env python
import usb1
import os

YUBIKEY_VENDOR_ID=int('1050',16)
YUBIKEY_PRODUCT_ID=int('0116',16)

def is_yubikey(device):
    print(device.getVendorID(), device.getProductID())
    print(YUBIKEY_VENDOR_ID, YUBIKEY_PRODUCT_ID)
    return device.getVendorID() == YUBIKEY_VENDOR_ID \
        and device.getProductID() == YUBIKEY_PRODUCT_ID

def restart_gpg_agent():
    print("restarting gpg-agent")
    os.spawnlp(os.P_WAIT, '/usr/local/bin/gpgconf', 'gpgconf', '--kill', 'gpg-agent')
    os.spawnlp(os.P_WAIT, '/usr/local/bin/gpgconf', 'gpgconf', '--launch', 'gpg-agent')
    print('restarted gpg-agent')

def hotplug_callback(context, device, event):
    print ("Device %s: %s" % (
        {
            usb1.HOTPLUG_EVENT_DEVICE_ARRIVED: 'arrived',
            usb1.HOTPLUG_EVENT_DEVICE_LEFT: 'left',
        }[event],
        device))

    if is_yubikey(device):
        restart_gpg_agent()



def main():
    with usb1.USBContext() as context:
        if not context.hasCapability(usb1.CAP_HAS_HOTPLUG):
            print('Hotplug support is missing. Please update your libusb version.')
            return
        print('Registering hotplug callback...')
        opaque = context.hotplugRegisterCallback(hotplug_callback)
        print('Callback registered. Monitoring events, ^C to exit')
        try:
            while True:
                context.handleEvents()
        except (KeyboardInterrupt, SystemExit):
            print('Exiting')

if __name__ == '__main__':
    main()
