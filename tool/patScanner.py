import sys, re
from dumper import *

def pattern_scanner(modname, pattern, extra = 0, offset = 0, relative = True):
	    module = pymem.process.module_from_name(pm.process_handle, modname)
	    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
	    match = re.search(pattern, bytes).start()

	    non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
	    yes_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll

	    return "0x{:X}".format(yes_relative) if relative else "0x{:X}".format(non_relative)


dwClientState = int(pattern_scanner('engine.dll', rb'\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0', 0, 1), 0)
dwClientState_ViewAngles = int(pattern_scanner('engine.dll', rb'\xF3\x0F\x11\x86....\xF3\x0F\x10\x44\x24.\xF3\x0F\x11\x86', 0, 4, 0), 0)
model_ambient_min = int(pattern_scanner('engine.dll', rb'\xF3\x0F\x10\x0D....\xF3\x0F\x11\x4C\x24.\x8B\x44\x24\x20\x35....\x89\x44\x24\x0C', 0, 4), 0)

dwEntityList = int(pattern_scanner('client.dll', rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', 0, 1), 0)
dwForceAttack = int(pattern_scanner('client.dll', rb'\x89\x0D....\x8B\x0D....\x8B\xF2\x8B\xC1\x83\xCE\x04', 0, 2), 0)
dwForceJump = int(pattern_scanner('client.dll', rb'\x89\x0D....\x8B\x0D....\x8B\xF2\x8B\xC1\x83\xCE\x04', 0, 2), 0)
dwGlowObjectManager = int(pattern_scanner('client.dll', rb'\xA1....\xA8\x01\x75\x4B', 4, 1), 0)
dwLocalPlayer = int(pattern_scanner('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3), 0)
dwMouseEnable = int(pattern_scanner('client.dll', rb'\xB9....\xFF\x50\x34\x85\xC0\x75\x10', 48, 1), 0)


file = open("result/offsets.txt", "w")
file.write(f"dwClientState = {dwClientState} \n")
file.write(f"dwClientState_ViewAngles = {dwClientState_ViewAngles} \n")
file.write(f"model_ambient_min = {model_ambient_min} \n")
file.write(f"dwEntityList = {dwEntityList} \n")
file.write(f"dwForceAttack = {dwForceAttack} \n")
file.write(f"dwForceJump = {dwForceJump} \n")
file.write(f"dwGlowObjectManager = {dwGlowObjectManager} \n")
file.write(f"dwLocalPlayer = {dwLocalPlayer} \n")
file.write(f"dwMouseEnable = {dwMouseEnable}")
file.close()