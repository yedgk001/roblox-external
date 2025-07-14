import ctypes
import struct

PROCESS_ALL_ACCESS = 0x1F0FFF


def open_process(pid):
    return ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)


def read_bytes(handle, addr, size):
    buf = ctypes.create_string_buffer(size)
    ctypes.windll.kernel32.ReadProcessMemory(handle, ctypes.c_void_p(addr), buf, size, None)
    return buf.raw


def read_generic(handle, addr, fmt):
    size = struct.calcsize(fmt)
    data = read_bytes(handle, addr, size)
    return struct.unpack(fmt, data)[0]


def write_generic(handle, addr, fmt, value):
    data = struct.pack(fmt, value)
    written = ctypes.c_size_t()
    ctypes.windll.kernel32.WriteProcessMemory(handle, ctypes.c_void_p(addr), data, len(data), ctypes.byref(written))
    return written.value == len(data)
