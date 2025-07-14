from Memory import read_bytes, read_generic, write_generic
from Offset import Offset


def read(handle, addr, fmt): return read_generic(handle, addr, fmt)


def write(handle, addr, fmt, value): return write_generic(handle, addr, fmt, value)


def read_string(handle, addr):
    name_ptr = read(handle, addr + Offset.Name, "<Q")
    length = read(handle, name_ptr + 0x10, "<I")
    if length >= 16:
        ptr = read(handle, name_ptr, "<Q")
        return read_bytes(handle, ptr, length).decode('utf-8', errors='ignore')
    return read_bytes(handle, name_ptr, 16).split(b'\x00')[0].decode('utf-8', errors='ignore')


def get_children(handle, addr):
    arr = read(handle, addr + Offset.Children, "<Q")
    end = read(handle, arr + Offset.ChildrenEnd, "<Q")
    current = read(handle, arr, "<Q")
    return [read(handle, current + i * 0x10, "<Q") for i in range((end - current) // 0x10)]


def find_child_by_name(handle, addr, name):
    return next((c for c in get_children(handle, addr) if read_string(handle, c) == name), 0)
