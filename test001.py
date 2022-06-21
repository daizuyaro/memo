import asyncio
from bleak import BleakClient
from pytlv.TLV import *

address = "D0:9D:BF:57:EF:1F" # identify Node
UUID = "f0f26c9b-2c8c-49ac-ab60-fe03def1b40c"

#MAC Address
# Tag: F0:47:7C:D2:32:51
# Initiator pc: FF:03:E8:15:5D:23

#UUID
# Distance: 3f0afd88-7770-46b0-b5e7-9fc099598964
# Acnhor position: f0f26c9b-2c8c-49ac-ab60-fe03def1b40c
# Acnhor list: 5b10c428-af2f-486f-aee1-9dbd79b6bccb

# bytearray1 = bytearray(b"xxxx") #ByteArray作成
#a = 1234
#a.to_bytes(2, 'big')  # 2バイトでビッグエンディアン
#a.to_bytes(4, 'little') # 4バイトでリトルエンディアン



b = 227, 129, 130
print(bytearray(b))
# bytearray(b'\xe3\x81\x82')

ba = bytearray(b)
ba[1] = 127
print(ba)
# bytearray(b'\xe3\x7f\x82')

x = b'\xe3\x81\x82'
y = bytes(0x79)
z = bytes(0x79)
q = bytes(0x64)










async def run(address, loop):
    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))
        #y = await client.read_gatt_char(UUID) # read from Nord

        b = 227, 129, 130
        print(bytearray(b))
        # bytearray(b'\xe3\x81\x82')

        ba = bytearray(b)
        ba[1] = 127
        print(ba)
        # bytearray(b'\xe3\x7f\x82')

        x = b'\xe3\x81\x82'
        y = bytes(0x79)
        z = bytes(0x79)
        q = bytes(0x64)

        #x1 = (x1).to_bytes(4, byteorder="big")
        #y1 = (y1).to_bytes(4, byteorder="big")
        #z1 = (z1).to_bytes(4, byteorder="big")
        #quality_factor = (q1).to_bytes(4, byteorder="big")

        print(x)
        a = await client.write_gatt_char(UUID, x) # write to Nord
        print(a)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))