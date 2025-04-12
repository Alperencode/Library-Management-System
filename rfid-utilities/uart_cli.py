import argparse
import nfc
import ndef
import sys
import time
from gpiozero import Buzzer
from gpiozero import LED

buzzer = Buzzer(18)
led = LED(23)


def buzz(duration=0.1):
    buzzer.on()
    led.on()
    time.sleep(duration)
    buzzer.off()
    led.off()


def read_tag():
    def on_connect(tag):
        if tag.ndef and tag.ndef.length > 0:
            records = list(tag.ndef.records)
            for record in records:
                if isinstance(record, ndef.TextRecord):
                    print(record.text)
                    buzz()
                else:
                    print("Unsupported record type.")
        else:
            print("No NDEF data found or tag not writable.")
        return True

    with nfc.ContactlessFrontend('tty:AMA0') as clf:
        clf.connect(rdwr={'on-connect': on_connect})


def write_tag(text):
    message = [ndef.TextRecord(text)]

    def on_connect(tag):
        if tag.ndef:
            tag.ndef.records = message
            print("Write successful.")
            buzz()
        else:
            print("Tag is not NDEF-formatted or not writable.")
        return True

    with nfc.ContactlessFrontend('tty:AMA0') as clf:
        clf.connect(rdwr={'on-connect': on_connect})


def main():
    parser = argparse.ArgumentParser(description="RFID Read/Write Tool using PN532")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("read", help="Read plain text from RFID tag")

    write_parser = subparsers.add_parser("write", help="Write plain text to RFID tag")
    write_parser.add_argument("text", type=str, help="Text to write")

    args = parser.parse_args()

    if args.command == "read":
        read_tag()
    elif args.command == "write":
        write_tag(args.text)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
