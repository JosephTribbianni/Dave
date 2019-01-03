#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : Su18
# @Copyright : <phoebebuffayfan9527@gmail.com>
# @For U : Like knows like.

import struct
import time
from . import win32, process

asm_code = bytes()


def _asm_init():
    global asm_code
    asm_code = bytes()


def asm_add_byte(value):
    global asm_code
    asm_code += struct.pack("<1B", value)


def asm_add_word(value):
    global asm_code
    asm_code += struct.pack("<1H", value)


def asm_add_dword(value):
    global asm_code
    asm_code += struct.pack("<1I", value)


def asm_add_bytes(values):
    for code in values:
        asm_add_byte(code)


def asm_push(value):
    asm_add_byte(0x68)
    asm_add_dword(value)


asm_mov_exx_code = {
    "eax": [0xB8],
    "ebx": [0xBB],
    "ecx": [0xB9],
    "edx": [0xBA],
    "esi": [0xBE],
    "edi": [0xBF],
    "ebp": [0xBD],
    "esp": [0xBC],
}


def asm_mov_exx(register, value):
    asm_add_bytes(asm_mov_exx_code[register])
    asm_add_dword(value)


asm_add_exx_code = {
    "eax": [0x05],
    "ebx": [0x81, 0xC3],
    "ecx": [0x81, 0xC1],
    "edx": [0x81, 0xC2],
    "esi": [0x81, 0xC6],
    "edi": [0x81, 0xC7],
    "ebp": [0x81, 0xC5],
    "esp": [0x81, 0xC4],
}


def asm_add_exx(register, value):
    asm_add_bytes(asm_add_exx_code[register])
    asm_add_dword(value)


asm_mov_exx_dword_ptr_code = {
    "eax": [0x3E, 0xA1],
    "ebx": [0x3E, 0x8B, 0x1D],
    "ecx": [0x3E, 0x8B, 0x0D],
    "edx": [0x3E, 0x8B, 0x15],
    "esi": [0x3E, 0x8B, 0x35],
    "edi": [0x3E, 0x8B, 0x3D],
    "ebp": [0x3E, 0x8B, 0x2D],
    "esp": [0x3E, 0x8B, 0x25],
}


def asm_mov_exx_dword_ptr(register, value):
    asm_add_bytes(asm_mov_exx_dword_ptr_code[register])
    asm_add_dword(value)


asm_mov_exx_dword_ptr_exx_add_code = {
    "eax": [0x8B, 0x80],
    "ebx": [0x8B, 0x9B],
    "ecx": [0x8B, 0x89],
    "edx": [0x8B, 0x92],
    "esi": [0x8B, 0xB6],
    "edi": [0x8B, 0xBF],
    "ebp": [0x8B, 0xAD],
    "esp": [0x8B, 0xA4, 0x24],
}


def asm_mov_exx_dword_ptr_exx_add(register, value):
    asm_add_bytes(asm_mov_exx_dword_ptr_exx_add_code[register])
    asm_add_dword(value)


asm_push_exx_code = {
    "eax": [0x50],
    "ebx": [0x53],
    "ecx": [0x51],
    "edx": [0x52],
    "esi": [0x56],
    "edi": [0x57],
    "ebp": [0x55],
    "esp": [0x54],
}


def asm_push_exx(register):
    asm_add_bytes(asm_push_exx_code[register])


asm_pop_exx_code = {
    "eax": [0x58],
    "ebx": [0x5B],
    "ecx": [0x59],
    "edx": [0x5A],
    "esi": [0x5E],
    "edi": [0x5F],
    "ebp": [0x5D],
    "esp": [0x5C],
}


def asm_pop_exx(register):
    asm_add_bytes(asm_pop_exx_code[register])


def asm_ret():
    asm_add_byte(0xC3)


def asm_call(address):
    asm_add_bytes([0xE8, 0x02, 0x00, 0x00, 0x00])
    asm_add_bytes([0xEB, 0x06])
    asm_push(address)
    asm_ret()


def asm_code_inject():
    length = len(asm_code)
    thread_addr = win32.VirtualAllocEx(process.pvz_handle, None, length, win32.MEM_COMMIT, win32.PAGE_EXECUTE_READWRITE)

    if thread_addr is not None:
        win32.WriteProcessMemory(process.pvz_handle, thread_addr, asm_code, length, None)
        start = win32.LPTHREAD_START_ROUTINE(thread_addr)
        thread_handle = win32.CreateRemoteThread(process.pvz_handle, None, 0, start, None, 0, None)
        if thread_handle is not None:
            win32.WaitForSingleObject(thread_handle, win32.INFINITE)
            win32.CloseHandle(thread_handle)
        win32.VirtualFreeEx(process.pvz_handle, thread_addr, 0, win32.MEM_RELEASE)


def asm_code_inject_safely():
    process.write_memory("unsigned char", 0xFE, 0x00552014)
    time.sleep(0.01)
    if process.is_valid():
        asm_code_inject()
    process.write_memory("unsigned char", 0xDB, 0x00552014)
