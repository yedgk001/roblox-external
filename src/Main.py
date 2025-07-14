import ctypes

import psutil

from Memory import open_process
from Offset import Offset
from RobloxService import read, write, find_child_by_name


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
    if not pid: return None

    handle = open_process(pid)
    base = get_module_base(pid)

    dm_fake = read(handle, base + Offset.FakeDataModelPointer, "<Q")
    dm = read(handle, dm_fake + Offset.FakeDataModelToDataModel, "<Q")
    players = find_child_by_name(handle, dm, "Players")
    local = read(handle, players + Offset.LocalPlayer, "<Q")
    char = read(handle, local + Offset.ModelInstance, "<Q")
    humanoid = find_child_by_name(handle, char, "Humanoid")

    write(handle, humanoid + Offset.WalkSpeed, "<f", 150.0)
    write(handle, humanoid + Offset.WalkSpeedCheck, "<f", 150.0)
    return None


if __name__ == "__main__":
    main()
