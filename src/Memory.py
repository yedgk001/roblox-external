import ctypes, struct

PROCESS_ALL_ACCESS = 0x1F0FFF

def open_process(pid: int):
    return ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

def read_bytes(handle, addr: int, size: int) -> bytes:
    buf = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t()
    ctypes.windll.kernel32.ReadProcessMemory(handle, ctypes.c_void_p(addr), buf, size, ctypes.byref(bytes_read))
    return buf.raw

def read(handle, addr: int, fmt: str):
    data = read_bytes(handle, addr, struct.calcsize(fmt))
    return struct.unpack(fmt, data)[0]

def write(handle, addr: int, fmt: str, value):
    data = struct.pack(fmt, value)
    written = ctypes.c_size_t()
    ctypes.windll.kernel32.WriteProcessMemory(handle, ctypes.c_void_p(addr), data, len(data), ctypes.byref(written))
    return written.value == len(data)
