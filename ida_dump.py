import idaapi
data = idaapi.dbg_read_memory(start_address, data_length)
fp = open('path/to/dump', 'wb')
fp.write(data)
fp.close()

s = '全选复制完整的 Input Data 过来'
print(bytes.fromhex(s[2:]).decode('utf-8'))
