from Memory import read, read_string_safe
from Offset import Offset


def get_children(handle, addr):
    arr = read(handle, addr + Offset.Children, "<Q")
    end = read(handle, arr + Offset.ChildrenEnd, "<Q")
    current = read(handle, arr, "<Q")
    return [read(handle, current + i * 0x10, "<Q") for i in range((end - current) // 0x10)]


def find_child_by_name(handle, addr, name):
    return next((c for c in get_children(handle, addr) if read_string_safe(handle, c) == name), "null")
