import nfc
import ndef
import time
import argparse
import sys


def wait_for_tag_removal(clf):
    print("Please remove the tag...")
    while True:
        tag_present = clf.sense(
            nfc.clf.RemoteTarget("106A"),  # Type A tag
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
                            tag_written = True
                            return True
                        except Exception as e:
                            print(f"Write failed: {e}. Try again.")
                            return False
                    else:
                        print("Tag is not NDEF formatted or not writable.")
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
