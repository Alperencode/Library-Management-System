import nfc
import ndef


text = "Hello World"
ndef_message = [ndef.TextRecord(text)]


def on_connect(tag):
    if tag.ndef:
        print(f"Writing text: {text}")
        tag.ndef.records = ndef_message
        print("Write successful.")
    else:
        print("Tag is not NDEF-formatted or not writable.")
    return True


with nfc.ContactlessFrontend('tty:AMA0') as clf:
    clf.connect(rdwr={'on-connect': on_connect})
