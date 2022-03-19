# making an amiibo bin from scratch
import random
import amiibo
import sys
import requests

def generate_serial():
        serial_number = "04"
        while len(serial_number) < 20:
            temp_sn = hex(random.randint(0, 255))
            # removes 0x prefix
            temp_sn = temp_sn[2:]
            # creates leading zero
            if len(temp_sn) == 1:
                temp_sn = '0' + temp_sn
            serial_number += ' ' + temp_sn
        return serial_number

def gen_random_bytes(byte_amt: int):
    generated_bytes = ""
    while len(generated_bytes) < byte_amt * 2:
        temp_gen = hex(random.randint(0, 255))
        temp_gen = temp_gen[2:]
        if len(temp_gen) == 1:
                temp_gen = '0' + temp_gen
        generated_bytes += temp_gen
    return generated_bytes

def get_character_from_api(character):
    api = requests.get('https://amiiboapi.com/api/amiibo').json()["amiibo"]
    for characters in api:
        print(characters)
        print(characters["head"] + characters["tail"])
        if character == characters["character"]:
            return characters["head"] + characters["tail"]

def main(character_name, path):
    keys = amiibo.AmiiboMasterKey.from_combined_bin(keys)

    bin = bytes.fromhex('00' * 540)

    raw_bin = amiibo.AmiiboDump(keys, bin, False)

    #UID
    raw_bin.uid_hex = generate_serial()
    #internal + static lock
    raw_bin.data[0x09:0x0C] = bytes.fromhex('480FE0')
    #CC
    raw_bin.data[0x0C:0x10] = bytes.fromhex('F110FFEE')
    #0xA5 lol
    raw_bin.data[0x10] = 0xA5
    #write counter
    raw_bin.data[0x11:13] = bytes.fromhex(gen_random_bytes(2))
    # ??
    ##raw_bin.data[0x13] = 0
    # settings
    raw_bin.data[0x14:0x16] = bytes.fromhex('3000')
    # crc counter
    raw_bin.data[0x16:0x18] = bytes.fromhex(gen_random_bytes(2))
    # init date
    #raw_bin.data[0x18:0x1A] = bytes.fromhex('0000')
    # last write date
    raw_bin.data[0x1A:0x1C] = bytes.fromhex(gen_random_bytes(2))
    # crc
    #raw_bin.data[0x1C:0x20] = bytes.fromhex('00000000')
    #name
    raw_bin.amiibo_nickname = '䂲¡里薚꭬찮뻪뼏事'
    #locked hash
    #raw_bin.data[0x34:0x54] = bytes.fromhex('317DD4D5D547051DED744B90B7EE325083533AC73555CC5094025EF19EB53E47')
    #character id
    raw_bin.data[0x54:0x5C] = bytes.fromhex(get_character_from_api(character_name))
    # ??
    #raw_bin.data[0x5C:0x60] = bytes.fromhex('0512A41A')
    #keygen salt + unfixed hash
    #raw_bin.data[0x60:0xA0] = bytes.fromhex('09 89 6D 03 38 C2 0B C9 AE 2A 22 D6 53 65 1D AE 17 18 AA 4C'.replace(' ', ''))
    #owner mii
    raw_bin.data[0xA0:0x100] = bytes.fromhex(
        "23211005e86061afc89b36f1a85a18237fa78e17f40a2d70eb3bcd630f9025ea7e779665a692c43db293b854ad54cada2f9bed66455707fe8c2ea1f4b5c5d7d14665a0fd60a39177d39cc5b1f0f9930fda2d0090187f19cf60ef65cca49788fa"
    )
    #game TID
    raw_bin.data[0x100:0x108] = bytes.fromhex('9c6266db5a22b6c9')
    #write counter 2??
    raw_bin.data[0x108:0x10A] = bytes.fromhex(gen_random_bytes(2))
    #amiibo appid
    raw_bin.data[0x10A:0x10E] = bytes.fromhex('aa0896c2')
    #??
    #raw_bin.data[0x10E:0x110] = bytes.fromhex(gen_random_bytes(2))
    #hash?
    #raw_bin.data[0x110:0x130] = bytes.fromhex('0001080813080800000000000000000000000000000000000000000074B9A14C')
    #application area
    raw_bin.data[0x130:0x208] = bytes.fromhex(
        "63694febbb3087b2f92fd3ce743f38720e8c11dcc9cdd62fe8024d2c7becf1dd9424528071b95ba7e63ffa512df4b3508dc42f911bfc0b3ca9788fd4cd0d04a83e9e667f3f8b614c7f2c4cc1cca368d40b7fbbd986a5239537d145b5400c0ab07866f77f8b26f22d7369da51c574dd44ff0bb78896843af28d95656b99258e708f590dcf662840ee7bf6a7a8871e6903ca585df9bc61f0d2177a660e18a21047e798481320abb0614b87cffcb711fd2486654f20017a63865d79cdfa77ec28ed62fda1235ac479cf0e7940073c18c56eb04f9f1aa812250d"
    )
    #dynamic lock + rfui
    raw_bin.data[0x208:0x20C] = bytes.fromhex('01000FBD')
    #cfg0 + cfg1
    raw_bin.data[0x20c:0x214] = bytes.fromhex('000000045F000000')
    #pwd
    #raw_bin.data[0x214:0x218] = bytes.fromhex('D303325E')
    #pack + rfui2
    #raw_bin.data[0x218:0x21C] = bytes.fromhex('8080FFFF')

    raw_bin.lock()
    raw_bin.unlock()
    print(raw_bin.data[0:540].hex())
    raw_bin.lock()

    with open(path, 'wb') as bin_file:
        bin_file.write(raw_bin.data[0:540])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])