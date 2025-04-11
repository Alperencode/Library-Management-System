from pynfc import Nfc

nfc = Nfc("pn532_i2c:/dev/i2c-1")

print("Waiting for a tag...")
for tag in nfc.poll():
    print("Tag detected")
    print("UID:", tag.uid.hex())
    break
