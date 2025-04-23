import nfc


def on_connect(tag):
    print("Tag UID:", tag.identifier.hex())
    return True


with nfc.ContactlessFrontend('tty:AMA0') as clf:
    clf.connect(rdwr={'on-connect': on_connect})
