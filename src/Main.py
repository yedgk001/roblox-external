import ctypes

import psutil

from Memory import open_process
from Offset import Offsets
from RobloxService import read_uint64, find_child_by_name, write_float


def get_pid(name="RobloxPlayerBeta.exe"):
    for p in psutil.process_iter(['name', 'pid']):
        if p.info['name'] and p.info['name'].lower() == name.lower():
            return p.info['pid']
    return None


def get_module_base(pid):
    CreateSnap = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Module32First = ctypes.windll.kernel32.Module32First
    Module32Next = ctypes.windll.kernel32.Module32Next

    snapshot = CreateSnap(0x00000008, pid)
    if snapshot == -1: return None

    class MODULEENTRY(ctypes.Structure):
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

    me = MODULEENTRY()
    me.dwSize = ctypes.sizeof(MODULEENTRY)

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
    if not pid:
        print("Roblox not found");
        return
    h = open_process(pid)
    base = get_module_base(pid)
    dm_fake = read_uint64(h, base + Offsets.FakeDataModelPointer)
    dm = read_uint64(h, dm_fake + Offsets.FakeDataModelToDataModel)
    players = find_child_by_name(h, dm, "Players")
    local = read_uint64(h, players + Offsets.LocalPlayer)
    char = read_uint64(h, local + Offsets.ModelInstance)
    humanoid = find_child_by_name(h, char, "Humanoid")

    write_float(h, humanoid + Offsets.WalkSpeed, 100.0)
    write_float(h, humanoid + Offsets.WalkSpeedCheck, 100.0)
    print("✅ WalkSpeed ustawiony na 100")


if __name__ == "__main__":
    main()
