# Email on Button Push

Just a simple script that runs on a Raspberry Pi that allows an email to go out on a button push.

## Requirements

* Python 3
* pip
* [sparkpost](https://github.com/SparkPost/python-sparkpost): `pip install sparkpost`
* requests: `pip install requests` (should be installed with sparkpost)
* Raspberry Pi with IO Port 16 connected to a button

## Configuration

1. Setup a SparkPost account and create an API Key for the account.
1. Setup the environment variables below.
    1. Set them up under `/etc/environment` like below.
    1. All are required to run

```
SPARKPOST_API_KEY=longapikey
BTNPI_FROM_ADDRESS="email@example.com"
BTNPI_TO_ADDRESS="email@example.com"
BTNPI_TO_ANNOUNCE="email@example.com"
BTNPI_SUBJECT="Subject Line"
BTNPI_MESSAGE="Hello, the mailbox button was pressed."
```

* `SPARKPOST_API_KEY` environment variable for SparkPost to send messages
* `BTNPI_FROM_ADDRESS` address that the Pi sends out of
* `BTNPI_TO_ADDRESS` address that the Pi sends to when the button is pushed
* `BTNPI_TO_ANNOUNCE` when the Pi turns on it will email the External IP to this address
* `BTNPI_SUBJECT` subject line in the email
* `BTNPI_MESSAGE` message to send when the button is pressed

_Note_: All of these might be best in a JSON file - feel free to submit a PR :)

## Running the program on start

These are the instructions to run the program continually on a Raspberry Pi.

1. Update `/etc/rc.local` to have `(sleep 30;python /button.py)&`

The python script will output it's status and button presses to the screen