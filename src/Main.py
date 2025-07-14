import ctypes

import psutil


def get_pid(name="robloxplayerbeta.exe"):
    for p in psutil.process_iter(['name', 'pid']):
        if p.info['name'] and p.info['name'].lower() == name:
            return p.info['pid']
    return None


def get_module_base(pid):
    CreateSnap = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Module32First = ctypes.windll.kernel32.Module32First
    Module32Next = ctypes.windll.kernel32.Module32Next
    snapshot = CreateSnap(0x00000008, pid)
    if snapshot == -1: return None

    class ModuleEntry(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.c_ulong),
            ("th32ModuleID", ctypes.c_ulong),
            ("th32ProcessID", ctypes.c_ulong),
            ("GlblcntUsage", ctypes.c_ulong),
            ("ProccntUsage", ctypes.c_ulong),
            ("modBaseAddr", ctypes.c_void_p),
            ("modBaseSize", ctypes.c_ulong),
            ("hModule", ctypes.c_void_p),
            ("szModule", ctypes.c_char * 256),
            ("szExePath", ctypes.c_char * 260)
        ]

    me = ModuleEntry()
    me.dwSize = ctypes.sizeof(ModuleEntry)

    if not Module32First(snapshot, ctypes.byref(me)):
        ctypes.windll.kernel32.CloseHandle(snapshot)
        return None

    while True:
        if me.szModule.decode().lower() == "robloxplayerbeta.exe":
            ctypes.windll.kernel32.CloseHandle(snapshot)
            return me.modBaseAddr
        if not Module32Next(snapshot, ctypes.byref(me)): break

    ctypes.windll.kernel32.CloseHandle(snapshot)
    return None


def main():
    pid = get_pid()
    if not pid: return None
    return None


if __name__ == "__main__":
    main()
