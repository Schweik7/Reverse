def dword2num(word):  # 不管传入的是2个字节还是4个字节都不错;如果是空的就不行了
    if(len(word)!=0):
        return reduce(lambda x,y: 16*16*x+y,word)
    else:
        return 0
def num2dword(num):
    word=[0,0,0,0]
    for i in range(4):
        word[3-i]=num&0xff
        num>>=8
    return word
def sighed2unsighed_word(ax):
    if ax & 0x8000:
        return (ax - 1) ^ 0xffff
    return ax
def sighed2unsighed_dword(eax):
    if eax & 0x8000:
        return (eax - 1) ^ 0xffff
    return eax
import base64
table = 'VWpJNGQxcEZjSFpSYlRSNlZqSkplRnBSUFQwPQ=='.encode('ascii')
name=input('name:').encode('ascii')
for i in range(3):
    name=base64.encodebytes(name)[:-1]
for i in range(len(table)):
    table=base64.decodebytes(table)
print(table)
# print(name)
# enc=base64.encodestring(base64.enc)
