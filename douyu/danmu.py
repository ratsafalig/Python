import asyncio
import websockets
import ssl
import pathlib
import re
import time
from goto import with_goto

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("shark2.douyucdn.cn.pem")
ssl_context.load_verify_locations(localhost_pem)


def decode(data : bytes) -> map :
    data = str(data)[2:]
    result = {}
    key = ''
    seg1 = ''
    seg2 = ''
    i = 0
    while i < len(data) - 1:
        c_curr = data[i]
        c_post = data[i + 1]
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

@with_goto
async def hello():
    i = 0
    uri = "wss://danmuproxy.douyu.com:8505/"

    cce_cnt = 0
    txt_cnt = 0

    label .flag
    async with websockets.connect(
        uri, ssl=ssl_context, close_timeout=5, ping_interval=5, ping_timeout=5, max_size=None, max_queue=None
    ) as websocket:
        loginreq = 'f8000000f8000000b102000074797065403d6c6f67696e7265712f726f6f6d6964403d393939392f64666c403d736e4041413d31303640415373734041413d314053736e4041413d31303740415373734041413d314053736e4041413d31303840415373734041413d314053736e4041413d31303540415373734041413d314053736e4041413d31313040415373734041413d314053736e4041413d756e646566696e656440415373734041413d312f757365726e616d65403d6175746f5f455a4253344f5559436d2f756964403d313437373435372f766572403d32303139303631302f61766572403d3231383130313930312f6374403d302f00'
        joingroup = '2a0000002a000000b102000074797065403d6a6f696e67726f75702f726964403d393939392f676964403d312f00'
        mrkl = '1400000014000000b102000074797065403d6d726b6c2f00'

        loginreq = bytes.fromhex(loginreq)
        joingroup = bytes.fromhex(joingroup)
        mrkl = bytes.fromhex(mrkl)

        print(decode(loginreq))
        print(decode(joingroup))
        print(decode(mrkl))

        try:
            await websocket.send(loginreq)
            await websocket.send(joingroup)
            await websocket.send(mrkl)
            while True:
                time.sleep(1)
                recv = await websocket.recv()
                recv = recv[12:-1]
                print("")
                print(" ----- " + str(i) + " ----- ")
                recv = decode(recv)
                print(recv)
                print(" ----- " + str(i) + " ----- ")
                print("")

                if "txt" in recv:
                    print("")
                    print(" ----- " + str(txt_cnt) + " ----- ")
                    print(str(bytes(recv["txt"], encoding="utf-8"), encoding="utf-8"))
                    print(" ----- " + str(txt_cnt) +" ----- ") 
                    print("")
                    txt_cnt += 1

                i += 1
        except websockets.ConnectionClosedError as cce:
            print("")
            print(" ----- " + str(cce_cnt) + " ----- ")
            print(cce)
            print(" ----- " + str(cce_cnt) + " ----- ")
            print("")
            cce_cnt += 1
            goto .flag

asyncio.get_event_loop().run_until_complete(hello())


