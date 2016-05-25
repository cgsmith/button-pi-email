# Email on Button Push

Just a simple script that runs on a Raspberry Pi that allows an email to go out on a button push.

## Requirements

* python
* pip
* mandrill: `pip install mandrill`
* requests: `pip install requests`

These are the instructions to run the program continually on a Raspberry Pi.

1. Update `/etc/rc.local` to have `(sleep 30;python /button.py)&`

The python script will output it's status and button presses to the screen