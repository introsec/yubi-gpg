# Yubi-GPG

Restart the gpg-agent when the yubikey is inserted or removed to
update the keys available on the ssh-agent socket.

## Prerequisites

### libusb1

This uses the hotplug functionality introduced in libusb-1.0.16.

Any newer version should be ok. On the mac do:

    $ brew install libusb1

### python bindings to libusb1

I recommend using the system python version is installed in
*/usr/bin/python*. When using the homebrew version or a virtualenv
or anaconda version, adjust as necessary.

    $ sudo easy_install libusb1

and login to approve the installation.

The reason to use the system version is that the launcher will trigger
early in the login process when the PATH is not yet set.

## Install agent

Copy the following *plist* file to
*~/Library/LaunchAgents/com.snamellit.gpg_agent.plist*

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

    <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>Yubikey GPG Agent  Restart</string>
            <key>RunAtLoad</key>
            <false/>
            <key>KeepAlive</key>
            <dict>
                <key>SuccessfulExit</key>
                <false/>
            </dict>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python</string>
                <string>/Users/pti/playpen/python/yubi-gpg/yubi-gpg.py</string>
            </array>
        </dict>
    </plist>

Modify the path of the script to where the code was checked out.

Load it with

    $ /bin/launchctl load \
    "/Users/pti/Library/LaunchAgents/com.snamellit.yubi_gpg.plist"


## Test the agent

Now plug your key in and run

    $ ssh-add -l

and you should see your key id.

Now pull the key out and repeat. The key should be gone.

It takes about 2-3 seconds to update the status for ssh-agent.
