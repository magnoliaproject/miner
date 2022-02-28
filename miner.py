# -*- coding: utf-8 -*-
import hashlib
import OpenSSL
import multiprocessing
from multiprocessing import Process, Manager
import time
import os
import requests
import json
import sys
import warnings
import random, string
from colored import fg, bg, attr
from math import ceil, floor

warnings.filterwarnings("ignore", category=FutureWarning)

hash_functions = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512
}

HASH_TYPE = 'sha256'
sys.tracebacklimit = 0
node = "magnolia.eslime.net"

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def exit():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def hash_func(*args) -> bytes:
    t = b''.join(str(arg).encode('utf-8') for arg in args)
    return hash_functions[HASH_TYPE](t).digest()


def expand(buf, cnt, space_cost) -> int:
    for s in range(1, space_cost):
        buf.append(hash_func(cnt, buf[s - 1]))
        cnt += 1
    return cnt


def mix(buf, cnt, delta, salt, space_cost, time_cost):
    for t in range(time_cost):
        for s in range(space_cost):
            buf[s] = hash_func(cnt, buf[s - 1], buf[s])
            cnt += 1
            for i in range(delta):
                other = int(hash_func(cnt, salt, t, s, i).hex(), 16) % space_cost
                cnt += 1
                buf[s] = hash_func(cnt, buf[s], buf[other])
                cnt += 1

def extract(buf) -> bytes:
    return buf[-1]


def balloon(password, salt, space_cost, time_cost, delta=3) -> bytes:
    buf = [hash_func(0, password, salt)]
    cnt = 1
    cnt = expand(buf, cnt, space_cost)
    mix(buf, cnt, delta, salt, space_cost, time_cost)
    return extract(buf)


def balloon_hash(password, salt):
    delta = 6
    time_cost = 12
    space_cost = 24
    return balloon(password, salt, space_cost, time_cost, delta=delta).hex()

def get_result(hash, diff):
    positions = [1, 2, 3, 5, 7, 11, 13, 17]
    val = 0;
    n=1;
    max = 0;
    for pos in positions:
        val = val + (int(hash[pos], 16)*(16**n))
        n = n + 1
        max = max + (15*(16**n))

    maxaccepted = round(max/int(diff*16), 0)
    if val <= maxaccepted:
        return 1
    else:
        return 0

def worker(num, address, node, dictmgr, diff, miningid, s, nolia):
    dictmgr[1] = 0
    response = ""
    run = 1
    errors = 0
    print('%s%s%sNET WORKER || Starting networker thread' % (fg(92), bg(0), attr(1)))
    while(run):
        try:
            nresponse = s.get('https://' + str(node) + '/server.php?q=getvalidatingtemplate&amount=' + str(nolia))
            data = nresponse.json()
            dictmgr[1] = data
            if response != dictmgr[1]:
                response = dictmgr[1]
                if num == 0:
                    print('%s%s%sNET WORKER ||' % (fg(207), bg(0), attr(1)) + ' New block to mine!! Height: ' + str(dictmgr[1]['result']['height']) + ", Diff: " + str(dictmgr[1]['result']['difficulty']) + ", Reward: " + str(dictmgr[1]['result']['amount']) + " NOLIA")
            time.sleep(3)
            errors = 0

        except Exception as e:
            errors = errors + 1
            if errors % 8 == 0:
                print("%s%s%sConnection error. Retrying..." % (fg(1), bg(0), attr(1)))
        except KeyboardInterrupt:
            run = 0
            print('$s%s%sInterrupted' % (fg(1), bg(0), attr(1)))


def mining(num, address, privkey, pubkey, miningid, cores, dictmgr, diff, s, nolia):
    printed = 0
    n = 0
    it = int(time.time())
    response = ""
    run = 1
    errors = 0
    node = "magnolia.eslime.net"
    a = 0
    print("%s%s%sMINING || Starting " % (fg(92), bg(0), attr(1)) + "thread " + str(num))
    while(run):
        try:
            if (int(time.time()) % 30 == num and int(time.time()) != printed):
                printed = int(time.time())
                print("%s%s%sMINING || " % (fg(6), bg(0), attr(1)) + "Thread " + str(num) + ": " + str(round(n/(int(time.time()+1)-it),2)) + " h/s")
                it = int(time.time())
                n = 0
            a = randomword(16)
            res = balloon_hash(address + "-" + str(dictmgr[1]['result']['height']) + "-" + str(dictmgr[1]['result']['difficulty']) + "-" + str(dictmgr[1]['result']['amount']) + "-" + str(dictmgr[1]['result']['prevhash']), a)
            if get_result(res, int(dictmgr[1]['result']['difficulty'])) == 1:
                print("%s%s%sMINING || Block found!! Submititting block..." % (fg(2), bg(0), attr(1)))
                nresponse = s.get('https://' + str(node) + '/server.php?q=eth_submitblock&address=' + str(address) + '&nonce=' + a + '&amount=' + str(nolia))
                data = nresponse.json()
                if data['result']['status'] == 'OK':
                    print("%s%s%sMINING || Block accepted!! Hash: " % (fg(2), bg(0), attr(1)) + data['result']['hash'] + ", Reward: " + str(int(data['result']['reward'])/1000000000000000000) + " NOLIA")
                else:
                    print("%s%s%sMINING || Block rejected!! " % (fg(1), bg(0), attr(1)))
            n = n+1
            errors = 0
        except Exception as e:
            print(str(e))
            errors = errors + 1
        except KeyboardInterrupt:
            run = 0
            print('Interrupted')

def testmining(num, address, dictmgr):
    if num == 0:
        dictmgr[0]=0;
    it = int(time.time())
    a = ''
    print("%s%s%sTESTING || Starting test " % (fg(82), bg(0), attr(1)) + "thread " + str(num+1))
    while int(time.time())-60 < it:
        try:
            a = randomword(16)
            res = balloon_hash(address + "-12345-6000-1-" + address, a)
            get_result(res, 6000)
            dictmgr[0] = dictmgr[0] + 1
            errors = 0
        except Exception as e:
            errors = errors + 1
        except KeyboardInterrupt:
            errors = errors + 1

def startmining(address, cores):
    ismining = 0
    miningid = randomword(12)
    s = requests.Session()
    cores = int(cores)
    manager = Manager() 
    dictmgr = manager.dict()
    threads = [None] * cores
    print("Address: " + address + ", Threads: " + str(cores - 1))
    print("%s%s%sTESTING || Starting testing for calibrate miner. It will take " % (fg(82), bg(0), attr(1)) + str(60+cores+5) + " seconds")
    for i in range(cores-1):
        params = [i, address, dictmgr]
        threads[i] = Process(target=testmining, args=(params))
        threads[i].start()
        time.sleep(1)
    it = int(time.time())
    while int(time.time())-60-cores-5 < it:
        if int(time.time()) % 10 == 0:
            print("%s%s%sTESTING || " % (fg(82), bg(0), attr(1)) + str(it+60+cores+5-int(time.time())) + " seconds remaining...")
            time.sleep(1)
        time.sleep(1)
    hr = floor(dictmgr[0]/60)
    print("%s%s%sTESTING || Test finished!! " % (fg(82), bg(0), attr(1)))
    print("%s%s%sTESTING || Your total hashrate: " % (fg(82), bg(0), attr(1)) + str(hr) + " h/s")
    nolia = ceil(hr / 100)
    if nolia < 10:
        nolia = 10
    print("%s%s%sTESTING || NOLIA mined per block: " % (fg(82), bg(0), attr(1)) + str(nolia) + " NOLIA")
    print("%s%s%sTESTING || Expected: 1 block every " % (fg(82), bg(0), attr(1)) + str(floor(nolia*60000/hr)) + " seconds")
    manager = Manager()
    dictmgr = manager.dict()
    threads = [None] * cores
    for i in range(cores):
        if i == 0:
            params = [i, address, node, dictmgr, 0, miningid, s, nolia]
            threads[i] = Process(target=worker, args=(params))
        else:
            params = [i, address, "", "", miningid, cores, dictmgr, 0, s, nolia]
            threads[i] = Process(target=mining, args=(params))
        threads[i].start()
        time.sleep(1)
    ismining = 1
    while(1):
        time.sleep(45)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    try:
        args = len(sys.argv)
        cores = sys.argv[args-1]
        startmining(sys.argv[args-2].lower(), int(cores)+1)
    except Exception as e:
        print(e)
        print("Interrupted")
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
