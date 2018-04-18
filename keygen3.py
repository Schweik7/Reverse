#coding=utf8
from functools import reduce
import binascii
from z3 import *
'''
File: keygen3.py
Project: 1-python
File Created: Thursday, 12th April 2018 9:09:57 am
Author: Schweik7  weibidewo0@gmail.com
-----
Last Modified: Thursday, 12th April 2018 9:19:40 am
Modified By: Schweik7 
-----
Copyright 2018 - 2018 Schweik7, CSGXY
'''
#code 从4011e0开始;我们要从4011ec开始
code = """02 00 00 EB D5 8B 45 BC  C9 C2 10 00 55 8B EC 83
C4 FC 8B 45 0C 83 F8 10  75 0D 6A 00 E8 6B 02 00
00 33 C0 C9 C2 10 00 83  F8 0F 75 0E 8B 45 08 E8
18 01 00 00 33 C0 C9 C2  10 00 83 F8 01 75 06 33
C0 C9 C2 10 00 3D 11 01  00 00 0F 85 E7 00 00 00
8B 45 14 3B 05 60 31 40  00 75 1A 6A 00 68 96 30
40 00 68 A7 30 40 00 FF  75 08 E8 17 02 00 00 33
C0 C9 C2 10 00 3B 05 58  31 40 00 74 0C 3B 05 54
31 40 00 0F 85 AE 00 00  00 C7 05 D9 12 40 00 54 
45 58 00 6A 00 8D 45 FC  50 6A 64 FF 35 50 31 40
00 E8 BC 01 00 00 83 7D  FC 00 74 5F 50 6A 14 68
6C 31 40 00 FF 35 54 31  40 00 E8 AF 01 00 00 85
C0 74 48 A1 0B 30 40 00  BB 6C 31 40 00 03 03 43
81 FB 7C 31 40 00 75 F5  5B 03 C3 31 05 D9 12 40
00 C1 E8 10 66 29 05 D9  12 40 00 BE EC 11 40 00
B9 3E 00 00 00 33 DB EB  04 54 45 58 00 AD 33 D8
49 75 FA 81 FB FB CF FC  AF 74 EE 68 59 30 40 00
FF 35 5C 31 40 00 E8 7D  01 00 00 33 C0 C9 C2 10
00 68 73 30 40 00 FF 35  5C 31 40 00 E8 67 01 00
00 33 C0 C9 C2 10 00 FF  75 14 FF 75 10 FF 75 0C
FF 75 08 E8 08 01 00 00  C9 C2 10 00 55 8B EC 83
C4 AC 89 45 B0 8D 45 B8  50 FF 75 B0 E8 E3 00 00
00 89 45 FC 50 E8 4C 01  00 00 89 45 F8 B8 C9 00
00 00 25 FF FF 00 00 50  FF 35 64 31 40 00 E8 F1
00 00 00 89 45 AC 50 FF  75 F8 E8 3F 01 00 00 89
45 B4 68 20 00 CC 00 6A  00 6A 00 FF 75 F8 6A 51
68 C8 00 00 00 6A 0A 6A  32 FF 75 FC E8 FF 00 00
00 6A 01 FF 75 FC E8 19  01 00 00 68 FF FF 00 00
FF 75 FC E8 12 01 00 00  6A 1C 68 1C 30 40 00 6A
5F 6A 0A FF 75 FC E8 05  01 00 00 6A 17 68 39 30
40 00 68 87 00 00 00 6A  0A FF 75 FC E8 EF 00 00
00 6A 07 68 51 30 40 00  68 AF 00 00 00 6A 0A FF
75 FC E8 D9 00 00 00 8D  45 B8 50 FF 75 B0 E8 49
00 00 00 FF 75 B4 FF 75  F8 E8 B0 00 00 00 FF 75
F8 E8 9C 00 00 00 FF 75  FC E8 94 00 00 00 FF 75
AC E8 92 00 00 00 C9 C3  FF 25 28 20 40 00 FF 25
2C 20 40 00 FF 25 70 20  40 00 FF 25 6C 20 40 00
FF 25 68 20 40 00 FF 25  64 20 40 00 FF 25 60 20
40 00 FF 25 5C 20 40 00  FF 25 58 20 40 00 FF 25
54 20 40 00 FF 25 50 20  40 00 FF 25 3C 20 40 00
FF 25 38 20 40 00 FF 25  34 20 40 00 FF 25 74 20
40 00 FF 25 78 20 40 00  FF 25 44 20 40 00 FF 25
48 20 40 00 FF 25 4C 20  40 00 FF 25 40 20 40 00
FF 25 20 20 40 00 FF 25  1C 20 40 00 FF 25 18 20
40 00 FF 25 14 20 40 00  FF 25 10 20 40 00 FF 25
0C 20 40 00 FF 25 08 20  40 00 FF 25 04 20 40 00
FF 25 00 20 40 00 00 00  00 00 00 00 00 00 00 00"""
def word2num(word):  # 不管传入的是2个字节还是4个字节都不错;如果是空的就不行了
    if(len(word)!=0):
        return reduce(lambda x,y: 16*16*x+y,word)
    else:
        return 0
def num2word(num):
    word=[0,0,0,0]
    for i in range(4):
        word[3-i]=num&0xff
        num>>=8
    return word


def sighed2unsighed_word(ax):
    if ax & 0x8000:
        return (ax - 1) ^ 0xffff
    return ax
DEBUG=4
if DEBUG==4:
    name = raw_input('name:')
    name=list(map(ord,name))
    name+=[0 for i in range(20-len(name)+1)] # 为name补0
    serial=BitVec('serial',64)
    eax=0x58455443 #'CTEX'
    for i in range(0x10):
        eax += word2num(list(reversed(name[i:i + 4])))
        eax &= 0xffffffff
    print(hex(eax)) 
    eax+=serial
    eax&=0xffffffff
    mem=0x00584554
    mem^=eax
    mem_low = (mem & 0xffff) - (eax>>16)  # 低16位相减;注意这里可能是有符号数!
    mem=(mem&0xffff0000)+mem_low
    s=Solver()
    s.add(mem==0x585426eb)
    if s.check()==sat:
        print(s.model())
if DEBUG==5:
    name = '52pojie.cn'
    name = list(map(ord, name))
    name += [0 for i in range(20 - len(name) + 1)]  # 为name补0
    # serial = BitVec('serial', 64)
    serial=1454218211
    eax = 0x58455443  # 'CTEX'
    for i in range(0x10):
        eax += word2num(list(reversed(name[i:i + 4])))
        eax &= 0xffffffff
    eax += serial
    print(hex(eax))
    eax &= 0xffffffff
    # mem=[0x00,0x58,0x45,0x54]
    mem = 0x00584554
    mem ^= eax
    print(hex(mem))
    # eax = eax >> 16
    mem_low = (mem & 0xffff) - (eax >> 16)  # 低16位相减;注意这里可能是有符号数!
    print(hex(mem_low))
    mem = (mem & 0xffff0000) + mem_low
    print(hex(mem))
if DEBUG == 2:
    D9, DA, DB, DC = BitVecs('D9 DA DB DC', 8)
    con=BitVecVal(0xaffccffb,32)
    s = Solver()
    code = code.replace(' ', '').replace('\n', '')
    code = binascii.unhexlify(code)
    code = list(code[0xc:])
    code=list(map(ord,code))
    code[237:241] = [D9, DA, DB, DC]
    print(code[237:241])
    # ebx = BitVecVal(0,32)
    ebx=0
    ecx = 0x3e
    res=[0,0,0,0]
    for i in range(ecx):  # 四个字节的处理很那啥.我们一字节一字节的处理
        # l=list(reversed(code[(4 * i):(4 * i + 4)]))
        # eax = word2num(l)
        # print(hex(eax))
        # ebx = (ebx^eax)&0xffffffff
        res[0]^=code[4*i+3]
        res[1]^=code[4*i+2]
        res[2]^=code[4*i+1]
        res[3]^=code[4*i]
        if i>=59:
            print(i, "times:")
            print(res)
        # print(hex(ebx))
    # s.add(ebx==0xaffccffb)
    s.add(res[0]==0xaf)
    s.add(res[1]==0xfc)
    s.add(res[2]==0xcf)
    s.add(res[3]==0xfb)
    s.check()
    print(s.model())
if DEBUG==3:
    code = code.replace(' ', '').replace('\n', '')
    code = binascii.unhexlify(code)
    code = list(code[0xc:])
    code = list(map(ord, code))
    code[237:241] = [0xeb, 0x26, 0x54, 0x58]
    ebx = 0
    ecx = 0x3e
    for i in range(ecx):
        l=list(reversed(code[(4 * i):(4 * i + 4)]))
        eax = word2num(l)
        # print(hex(eax))
        ebx = (ebx^eax)&0xffffffff
        if i>=59:
            print(i, "times:")
            print(l)
            print(hex(eax))
            print(hex(ebx))
        # print(hex(ebx))
    if(ebx==0xaffccffb):
        print('success')
