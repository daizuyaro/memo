import asyncio
from bleak import BleakClient
from pytlv.TLV import *

address = "F0:47:7C:D2:32:51" # identify Node
UUID = "a02b947e-df97-4516-996a-1882521e0ead"
# distance: 3f0afd88-7770-46b0-b5e7-9fc099598964

async def run(address, loop):
    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))
        y = await client.read_gatt_char(UUID)
        print(y)
        print(y[0])

        tlv = TLV(["dwm_pos_t pos;"])
        y = await client.read_gatt_char(tlv)
        print(y)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))
