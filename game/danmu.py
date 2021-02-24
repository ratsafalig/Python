import asyncio
import websockets
import ssl
import pathlib
import re
import time
import unicodedata
import zlib

from goto import with_goto


@with_goto
async def bilibili():
    i = 0
    uri = "wss://tx-gz-live-comet-11.chat.bilibili.com/sub"

    label .flag

    async with websockets.connect(
        uri, ssl=ssl_context, close_timeout=1, ping_interval=5, ping_timeout=5, max_size=None, max_queue=None
    ) as websocket:
        msg1 = '000001120010000100000007000000017b22756964223a34393835343231372c22726f6f6d6964223a383137383439302c2270726f746f766572223a322c22706c6174666f726d223a22776562222c22636c69656e74766572223a22322e362e3235222c2274797065223a322c226b6579223a22505a7a4b4d35756e5f4c7339334a786f72587461674e494e44735a463977477234316b6659484b7a7267514364796331795f74686d4e5a634a59753747516a4e45614763704c6e64525670714e546651486f483139364c755263687531524e59476a4672674f534d5252426c5235304745446633356665465637665653533543383837724d57455f63724a4c4169436263774b336455343332773d3d227d'
        msg2 = '0000001f0010000100000002000000015b6f626a656374204f626a6563745d'

        msg1 = bytes.fromhex(msg1)
        msg2 = bytes.fromhex(msg2)

        try:
            await websocket.send(msg1)
            await websocket.send(msg2)
            while True:
                if i % 100 is 0:
                    pass
                    # await websocket.send(msg2)
                recv = await websocket.recv()
                i += 1
        except websockets.ConnectionClosedError as cce:
            goto .flag

class Douyu():

    ssl_context = ''
    uri = ''
    loginreq = ''
    joingroup = ''
    mrkl = ''
    listRecv = list()

    def __init__(self, loginreq, joingroup):
        self.uri = "wss://danmuproxy.douyu.com:8505/"
        self.loginreq = loginreq
        self.joingroup = joingroup
        self.mrkl = '1400000014000000b102000074797065403d6d726b6c2f00'
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.load_verify_locations(pathlib.Path(__file__).with_name("certification.pem"))
    '''
    '''
    def __bytes2dict(self, data):
        listBinaryMessage = list()
        i = 0
        length = 0
        while i < len(data):
            header = data[i : i + 12]
            length = int.from_bytes(header[ : 4], byteorder="little")
            listBinaryMessage.append(data[i + 12 : i + 12 + length - 8 - 1])
            i = (i + 12 + length - 8)
        for BinaryMessage in listBinaryMessage:
            BinaryMessage = str(BinaryMessage)[2:]
            result = {}
            key = ''
            seg1 = ''
            seg2 = ''
            i = 0
            while i < len(BinaryMessage) - 1:
                c_curr = BinaryMessage[i]
                c_post = BinaryMessage[i + 1]
                if c_curr is '@' and c_post is 'A':
                    seg1 += '@'
                    i += 1
                elif c_curr is '@' and c_post is 'S':
                    seg1 += '/'
                    i += 1
                elif c_curr is '@' and c_post is '=':
                    key = seg1
                    result[key] = ''
                    seg1 = ''
                    seg2 = ''
                    i += 1
                elif c_curr is '/':
                    seg2 += seg1
                    result[key] = seg1
                    seg1 += '/'
                    seg1 = ''
                else:
                    seg1 += c_curr
                i += 1
            result[key] = seg2
            try:
                if "txt" in result.keys():
                    result["txt"] = result["txt"].encode("ascii").decode("unicode-escape").encode('latin-1').decode("utf-8")
                if "nn" in result.keys():
                    result["nn"] = result["nn"].encode("ascii").decode("unicode-escape").encode('latin-1').decode("utf-8")
                if "bnn" in result.keys():
                    result["bnn"] = result["bnn"].encode("ascii").decode("unicode-escape").encode('latin-1').decode("utf-8")
                if "nickname" in result.keys():
                    result["nickname"] = result["nickname"].encode("ascii").decode("unicode-escape").encode('latin-1').decode("utf-8")
            except Exception:
                pass
            yield result

    async def __call__(self):

        uri = self.uri
        loginreq = bytes.fromhex(self.loginreq)
        joingroup = bytes.fromhex(self.joingroup)
        mrkl = bytes.fromhex(self.mrkl)

        i = 0
        while i >= 0:
            while 'websocket' not in locals().keys() or websocket.open is not True : 
                websocket = await websockets.connect(
                    uri, ssl=self.ssl_context, close_timeout=1, max_size=None, max_queue=None
                )
                await websocket.send(loginreq)
                await websocket.send(joingroup)
                await websocket.send(mrkl)
            try:
                if i % 3 == 0:
                    await websocket.send(mrkl)
                recv = await websocket.recv()
                # convert from bytes to map
                recv = self.__bytes2dict(recv)
                for rec in recv:
                    self.listRecv.append(rec)
                    print(rec)
            except websockets.ConnectionClosedError as cce:
                print(cce)
            i += 1

douyu = None

def main(loginreq=None, joingroup=None):
    '''
    6400651
    '''
    loginreq = 'fb000000fb000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d363430303635312f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    joingroup = '2d0000002d000000b102000074797065403d6a6f696e67726f75702f726964403d363430303635312f676964403d312f00'
    '''
    66666
    '''
    # loginreq = 'f9000000f9000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d36363636362f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    # joingroup = '2b0000002b000000b102000074797065403d6a6f696e67726f75702f726964403d36363636362f676964403d312f00'
    '''
    22222
    '''
    # loginreq = 'fa000000fa000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d3239303933352f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    # joingroup = '2c0000002c000000b102000074797065403d6a6f696e67726f75702f726964403d3239303933352f676964403d312f00'
    '''
    99999
    '''
    # loginreq = 'f9000000f9000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d39393939392f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    # joingroup = '2b0000002b000000b102000074797065403d6a6f696e67726f75702f726964403d39393939392f676964403d312f00'
    '''
    9999
    '''
    # loginreq = 'f8000000f8000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d393939392f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    # joingroup = '2a0000002a000000b102000074797065403d6a6f696e67726f75702f726964403d393939392f676964403d312f00'
    global douyu
    douyu = Douyu(loginreq=loginreq, joingroup=joingroup)
    asyncio.run(douyu())
