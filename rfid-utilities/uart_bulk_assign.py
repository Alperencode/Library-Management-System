import nfc
import ndef
import time
import argparse
import sys
from gpiozero import Buzzer, LED
from threading import Thread

buzzer = Buzzer(18)

red_led = LED(22)
green_led = LED(27)
blue_led = LED(17)


def rgb_on(r=False, g=False, b=False):
    red_led.on() if r else red_led.off()
    green_led.on() if g else green_led.off()
    blue_led.on() if b else blue_led.off()


def buzz_and_blink(r=False, g=False, b=False, buzz_times=1, blink_times=1, duration=0.1):
    def _buzz():
        for _ in range(buzz_times):
            buzzer.on()
            time.sleep(duration)
            buzzer.off()
            time.sleep(duration)

    def _blink():
        for _ in range(blink_times):
            rgb_on(r, g, b)
            time.sleep(duration)
            rgb_on(False, False, False)
            time.sleep(duration)

    buzz_thread = Thread(target=_buzz)
    blink_thread = Thread(target=_blink)

    buzz_thread.start()
    blink_thread.start()

    buzz_thread.join()
    blink_thread.join()


def wait_for_tag_removal(clf):
    print("Please remove the tag...")
    while True:
        tag_present = clf.sense(
            nfc.clf.RemoteTarget("106A"),
            iterations=1,
            interval=0.2
        )
        if tag_present is None:
            print("Tag removed.")
            break
        time.sleep(0.5)


def assign_isbns(file_path):
    try:
        with open(file_path, 'r') as f:
            isbns = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading file: {e}")
        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        sys.exit(1)

    print(f"{len(isbns)} ISBNs loaded.")
    print("Hold a new RFID tag near the reader when prompted.")

    with nfc.ContactlessFrontend('tty:AMA0') as clf:
        for index, isbn in enumerate(isbns, start=1):
            print(f"\n[{index}/{len(isbns)}] Waiting to write ISBN: {isbn}")

            success = False
            while not success:
                tag_written = None

                def on_connect(tag):
                    nonlocal tag_written
                    if tag.ndef:
                        try:
                            tag.ndef.records = [ndef.TextRecord(isbn)]
                            print(f"ISBN '{isbn}' written successfully.")
                            buzz_and_blink(g=True)
                            tag_written = True
                            return True
                        except Exception as e:
                            print(f"Write failed: {e}. Try again.")
                            buzz_and_blink(r=True, buzz_times=2, blink_times=2)
                            return False
                    else:
                        print("Tag is not NDEF formatted or not writable.")
                        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
                        return False

                clf.connect(rdwr={'on-connect': on_connect})

                if tag_written:
                    wait_for_tag_removal(clf)
                    success = True
                else:
                    print("Retrying...")
                    time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(description="Assign ISBNs to RFID tags in bulk.")
    parser.add_argument("file", help="Path to text file containing ISBNs (one per line)")
    args = parser.parse_args()
    assign_isbns(args.file)


if __name__ == "__main__":
    main()
