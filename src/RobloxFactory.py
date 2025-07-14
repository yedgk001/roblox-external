from Memory import read_bytes, read, write
from Offset import Offsets

def read_uint64(handle, addr): return read(handle, addr, "<Q")
def read_uint32(handle, addr): return read(handle, addr, "<I")
def write_float(handle, addr, value): return write(handle, addr, "<f", value)

def read_string(handle, addr):
    namePtr = read_uint64(handle, addr + Offsets.Name)
    length = read_uint32(handle, namePtr + 0x10)
    if length >= 16:
        ptr = read_uint64(handle, namePtr)
        return read_bytes(handle, ptr, length).decode('utf-8', errors='ignore')
    else:
        return read_bytes(handle, namePtr, 16).split(b'\x00')[0].decode('utf-8', errors='ignore')

def get_children(handle, addr):
    arr = read_uint64(handle, addr + Offsets.Children)
    end = read_uint64(handle, arr + Offsets.ChildrenEnd)
    current = read_uint64(handle, arr)
    result = []
    while current < end:
        result.append(read_uint64(handle, current))
        current += 0x10
    return result

def find_child_by_class(handle, addr, class_name):
    for c in get_children(handle, addr):
        if None: pass
    return 0
def find_child_by_name(handle, addr, name):
    for c in get_children(handle, addr):
        if read_string(handle, c) == name:
            return c
    return 0
