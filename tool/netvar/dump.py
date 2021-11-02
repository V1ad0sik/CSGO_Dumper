from tool.netvar.netvar_manager import NetvarsManager
from dumper import *
 
netvars_manager = NetvarsManager(pm)

with open(r"result/netvar.json", "w+") as fp:
	netvars_manager.dump_netvars(fp, json_format = "netvar.json".endswith('.json'))