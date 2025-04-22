import nfc


def on_connect(tag):
    print("Tag UID:", tag.identifier.hex())
    print("Tag Type:", tag.type)
    if tag.ndef:
        if tag.ndef.length > 0:
            print("NDEF Records:")
            for record in tag.ndef.records:
                print(f" - TNF: {record.type}, Payload: {record}")
        else:
            print("No NDEF records found.")
    else:
        print("Tag is not NDEF formatted or not writable.")
    return True


with nfc.ContactlessFrontend('tty:AMA0') as clf:
    clf.connect(rdwr={'on-connect': on_connect})
