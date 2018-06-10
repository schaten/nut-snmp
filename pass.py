#!/usr/bin/python3
import sys
import subprocess
import syslog as log

class Subtree:
    def __init__(self, top, data):
        self.data = data
        self.top = top
        self.arr = []
        for (i,key) in enumerate(self.data):
            self.data[key]['index'] = i
            self.arr.append((key, self.data[key]))

    def get(self, oid):
        if self.top not in oid:
            return False
        else:
            if oid in self.data:
                return self._getdata(oid)
            else:
                return False
    def getnext(self, oid):
        if oid in self.data:
            a = self.data[oid]['index']
            a+=1
        else:
            if self.top in oid or oid in self.top:
                a = 0
            else:
                return False
        if a < len(self.arr):
            oid = self.arr[a][0]
            return self._getdata(oid)
        return False
    def _getdata(self, oid):
        if self.data[oid]['source'] == 'const':
            res = self.data[oid]['value']
        elif self.data[oid]['source'] == 'extern':
            res = self._exec(  self.data[oid]['cmd'] )
        if 'transform' in self.data[oid]:
            res = self.data[oid]['transform'](res)
        return [oid, self.data[oid]['type'], res]

    def _exec(self, cmd):
        try:
            tmp = subprocess.run(cmd, stdout=subprocess.PIPE)
            return tmp.stdout
        except:
            return False

def mv2v(x):
    return int(1000*float(x[:-1].decode("UTF-8")))

upsoid = '.1.3.6.1.4.1.2021.13.16.4'
prog = 'upsc'
myups = 'ups-fs4@localhost'
mib = {
        '.1.3.6.1.4.1.2021.13.16.4.1.1.1': { 'type': 'INTEGER', 'source': 'const', 'value': '1'},
        '.1.3.6.1.4.1.2021.13.16.4.1.2.1': { 'type': 'STRING', 'source': 'const', 'value': 'UPS Input Voltage'},
        '.1.3.6.1.4.1.2021.13.16.4.1.3.1': { 'type': 'Gauge32', 'source': 'extern', 'cmd': [prog, myups, 'input.voltage'], 'transform': mv2v}
      }

tree = Subtree(upsoid, mib)
cont = True
while cont:
    tmp = input()

    if tmp!='PING':
        exit()
    print("PONG")

    command = input()
    oid = input()

    if command == 'set':
        input();
        print("not-writable")

    elif command == 'get':
        tmp = tree.get(oid)
        if tmp:
            print(tmp[0])
            print(tmp[1])
            print(tmp[2], flush=True)
        else:
            log.syslog('get failed')
            print("NONE", flush=True)

    elif command == 'getnext':
        tmp = tree.getnext(oid)
        if tmp:
            print(tmp[0])
            print(tmp[1])
            print(tmp[2], flush=True)
        else:
            log.syslog('getnext failed')
            print("NONE", flush=True) 
