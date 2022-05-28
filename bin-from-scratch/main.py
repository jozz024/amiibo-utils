# making an amiibo bin from scratch
import random
import amiibo
import sys
import requests
import os

with open(os.path.join(os.getcwd(), "key_retail.bin"), "rb") as fp:
        keys = amiibo.AmiiboMasterKey.from_combined_bin(fp.read())

def get_mii():
    base_path = os.path.abspath(".")

    with open(os.path.join(base_path, "mii.bin"), "rb") as mii_file:
        return mii_file.read()

def generate_bin():
    # start off with a fully 0'd out 540 byte block
    bin = bytes.fromhex('00' * 540)
    # initialize the dump, and set is_locked to false so it doesn't verify anything yet
    dump = amiibo.AmiiboDump(keys, bin, False)
    # UID
    dump.uid_hex = generate_serial()
    # internal + static lock
    dump.data[0x09:0x0C] = bytes.fromhex('480FE0')
    # Capability Container
    dump.data[0x0C:0x10] = bytes.fromhex('F110FFEE')
    # 0xA5 lol
    dump.data[0x10] = 0xA5
    # write counter
    dump.data[0x11:13] = bytes.fromhex(gen_random_bytes(2))
    # settings
    dump.data[0x14:0x16] = bytes.fromhex('3000')
    # crc counter
    dump.data[0x16:0x18] = bytes.fromhex(gen_random_bytes(2))
    # last write date
    dump.data[0x1A:0x1C] = bytes.fromhex(gen_random_bytes(2))
    # owner mii
    dump.data[0xA0:0x100] = get_mii()
    # application titleid
    dump.data[0x100:0x108] = bytes.fromhex('01006A803016E000')
    # 2nd write counter
    dump.data[0x108:0x10A] = bytes.fromhex(gen_random_bytes(2))
    # dynamic lock + rfui
    dump.data[0x208:0x20C] = bytes.fromhex('01000FBD')
    # cfg0 + cfg1
    dump.data[0x20c:0x214] = bytes.fromhex('000000045F000000')
    # 2 extra bytes get added somewhere, i cant figure out where so i just remove them for now
    dump.data = dump.data[:-2]
    return dump

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
        if character == characters["character"]:
            return characters["head"] + characters["tail"]

def main(character_name, path):
    with open(os.path.join(os.getcwd(), "key_retail.bin"), "rb") as fp:
        keys = amiibo.AmiiboMasterKey.from_combined_bin(fp.read())

    raw_bin = generate_bin()

    # character
    raw_bin.data[0x54:0x5C] = bytes.fromhex(get_character_from_api(character_name))
    # nickname
    raw_bin.amiibo_nickname = 'AMIIBO'
    raw_bin.lock()
    raw_bin.unlock()
    raw_bin.lock()

    with open(path, 'wb') as bin_file:
        bin_file.write(raw_bin.data[0:540])

if __name__ == "__main__":
    try:
        main("Mario", "mario.bin")

    except IndexError:
        print("usage: gen.exe <character-name> <out-path>")






    # UID
    # raw_bin.uid_hex = generate_serial()
    # internal + static lock
    # raw_bin.data[0x09:0x0C] = bytes.fromhex('480FE0')
    # CC
    # raw_bin.data[0x0C:0x10] = bytes.fromhex('F110FFEE')
    # 0xA5 lol
    # raw_bin.data[0x10] = 0xA5
    # write counter
    # raw_bin.data[0x11:13] = bytes.fromhex(gen_random_bytes(2))
    # ??
    # raw_bin.data[0x13] = 0
    # settings
    # raw_bin.data[0x14:0x16] = bytes.fromhex('3000')
    # crc counter
    # raw_bin.data[0x16:0x18] = bytes.fromhex(gen_random_bytes(2))
    # init date
    # raw_bin.data[0x18:0x1A] = bytes.fromhex('0000')
    # last write date
    # raw_bin.data[0x1A:0x1C] = bytes.fromhex(gen_random_bytes(2))
    # crc
    # raw_bin.data[0x1C:0x20] = bytes.fromhex('00000000')
    # name
    # raw_bin.amiibo_nickname = 'AMIIBO'
    # locked hash
    # raw_bin.data[0x34:0x54] = bytes.fromhex('317DD4D5D547051DED744B90B7EE325083533AC73555CC5094025EF19EB53E47')
    # character id
    # raw_bin.data[0x54:0x5C] = bytes.fromhex(get_character_from_api(character_name))
    # ??
    # raw_bin.data[0x5C:0x60] = bytes.fromhex('0512A41A')
    # keygen salt + unfixed hash
    # raw_bin.data[0x60:0xA0] = bytes.fromhex('09 89 6D 03 38 C2 0B C9 AE 2A 22 D6 53 65 1D AE 17 18 AA 4C'.replace(' ', ''))
    # owner mii
    # base_path = os.path.abspath(".")

    # pathlist = os.listdir(os.path.join(base_path, "miis"))
    # mii = random.choice(pathlist)
    # with open(os.path.join(base_path, "miis", mii), "rb") as mii_file:
    #     raw_bin.data[0xA0:0x100] = mii_file.read()
    # game TID
    # raw_bin.data[0x100:0x108] = bytes.fromhex(gen_random_bytes(8))
    # write counter 2??
    # raw_bin.data[0x108:0x10A] = bytes.fromhex(gen_random_bytes(2))
    # amiibo appid
    # raw_bin.data[0x10A:0x10E] = bytes.fromhex(gen_random_bytes(4))
    # ??
    # raw_bin.data[0x10E:0x110] = bytes.fromhex(gen_random_bytes(2))
    # hash?
    # raw_bin.data[0x110:0x130] = bytes.fromhex('0001080813080800000000000000000000000000000000000000000074B9A14C')
    # application area
    # raw_bin.data[0x130:0x208] = bytes.fromhex(gen_random_bytes(216)
    # )
    # dynamic lock + rfui
    # raw_bin.data[0x208:0x20C] = bytes.fromhex('01000FBD')
    # cfg0 + cfg1
    # raw_bin.data[0x20c:0x214] = bytes.fromhex('000000045F000000')
    # pwd
    # raw_bin.data[0x214:0x218] = bytes.fromhex('D303325E')
    # pack + rfui2
    # raw_bin.data[0x218:0x21C] = bytes.fromhex('8080FFFF')