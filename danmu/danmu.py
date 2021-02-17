import asyncio
import websockets
import ssl
import pathlib
import re
import time
import unicodedata

from goto import with_goto

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("certification.pem")
ssl_context.load_verify_locations(localhost_pem)


def decode(data : bytes) -> map :
    s_data = str(data)[2:]
    result = {}
    key = ''
    seg1 = ''
    seg2 = ''
    i = 0
    while i < len(s_data) - 1:
        c_curr = s_data[i]
        c_post = s_data[i + 1]
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
    if result["type"] == "chatmsg":
        result["txt"] = result["txt"].encode("ascii").decode("unicode-escape").encode('latin-1').decode("utf-8")
        result["nn"] = result["nn"].encode("ascii").decode("unicode-escape").encode('latin-1').decode("utf-8")
    return result


def encode(data : map) -> bytes :
    result = ''
    for key in data.keys():
        i = 0
        while i < len(key):
            if key[i] is '@':
                result += '@A'
            elif key[i] is '/':
                result += '@S'
            else:
                result += key[i]
            i += 1
        result += '@='
        i = 0
        while i < len(data[key]):
            if data[key][i] is '@':
                result += '@A'
            elif data[key][i] is '/':
                result += '@S'
            else:
                result += data[key][i]
            i += 1
        result += '/'
    return bytes(result, encoding="utf-8")

'''
@with_goto
async def douyu1():
    uri = 'wss://wsproxy.douyu.com:6673/'
    loginreq = 'b6010000b6010000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d39333933362f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f70617373776f7264403d2f6c746b6964403d35383635333432392f62697a403d312f73746b403d653963313833383130383934646563342f6465766964403d63373363663237316231623636363137363861383131333730303032313630312f6374403d302f7074403d322f637672403d302f747672403d372f617064403d2f7274403d313631333534353734342f766b403d61363864653765313730396434383038373733393339663164666534303832622f766572403d32303139303631302f61766572403d3231383130313930312f646d6274403d6368726f6d652f646d6276403d39302f6572403d312f00'
    keepalive = '3b0000003b000000b102000074797065403d6b6565706c6976652f766277403d302f63646e403d2f7469636b403d313631333534353734352f6b64403d2f00'

    loginreq = bytes.fromhex(loginreq)
    # ssr = bytes.fromhex(ssr)
    keepalive = bytes.fromhex(keepalive)

    label .flag
    async with websockets.connect(
        uri, ssl=ssl_context, close_timeout=1, ping_interval=1, ping_timeout=1, max_size=None, max_queue=None
    ) as websocket:
        try:
            await websocket.send(loginreq)
            while True:
                await asyncio.sleep(0.1)
                header = keepalive[:13]
                body = decode(keepalive[12:-1])
                body["tick"] = str(int(time.time_ns() / 1000000000))
                # msg = bytes(header, encode(body), b'00')
                msg = header + encode(body) + b'f00'
                await websocket.send(msg)
                recv = await websocket.recv()
        except websockets.ConnectionClosedError as cce:
            goto .flag
'''

async def douyu2():
    uri = "wss://danmuproxy.douyu.com:8505/"

    '''
    6400651
    '''
    loginreq = 'fb000000fb000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d363430303635312f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    joingroup = '2d0000002d000000b102000074797065403d6a6f696e67726f75702f726964403d363430303635312f676964403d312f00'
    mrkl = '1400000014000000b102000074797065403d6d726b6c2f00'

    '''
    66666
    '''
    loginreq = 'f9000000f9000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d36363636362f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    joingroup = '2b0000002b000000b102000074797065403d6a6f696e67726f75702f726964403d36363636362f676964403d312f00'

    '''
    22222
    '''
    loginreq = 'fa000000fa000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d3239303933352f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    joingroup = '2c0000002c000000b102000074797065403d6a6f696e67726f75702f726964403d3239303933352f676964403d312f00'

    '''
    99999
    '''
    loginreq = 'f9000000f9000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d39393939392f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
    joingroup = '2b0000002b000000b102000074797065403d6a6f696e67726f75702f726964403d39393939392f676964403d312f00'

    loginreq = bytes.fromhex(loginreq)
    joingroup = bytes.fromhex(joingroup)
    mrkl = bytes.fromhex(mrkl)

    i = 0
    while i >= 0:
        while 'websocket' not in locals().keys() or websocket.open is not True : 
            websocket = await websockets.connect(
                uri, ssl=ssl_context, close_timeout=1, max_size=None, max_queue=None
            )
            await websocket.send(loginreq)
            await websocket.send(joingroup)
            await websocket.send(mrkl)
        try:
            if i % 10 == 0:
                await websocket.send(mrkl)
            recv = await websocket.recv()
            recv = decode(recv[12:-1])
        except websockets.ConnectionClosedError as cce:
            print("cce")
        if "type" in recv and str(recv["type"]) == "chatmsg":
            print(recv["nn"] + " : " + recv["txt"])
        i += 1

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

# asyncio.get_event_loop().run_until_complete(bilibili())


async def main():
    # task1 = asyncio.create_task(douyu1())
    task2 = asyncio.create_task(douyu2())
    # await task1
    await task2

asyncio.run(main())
