import re, sys, json
from typing import Union
from pymem.process import module_from_name
from tool.netvar.recv_classes import ClientClass
 
 
__all__ = ['NetvarsManager']
 
 
class NetvarsManager:
    def __init__(self, csgo_handle):
        client_handle = module_from_name(csgo_handle.process_handle, 'client.dll')
        client_bytes = csgo_handle.read_bytes(client_handle.lpBaseOfDll, client_handle.SizeOfImage)

        world_decal = re.search(rb'DT_TEWorldDecal', client_bytes).start()
        world_decal += client_handle.lpBaseOfDll

        all_classes = csgo_handle.read_int(client_bytes.find(world_decal.to_bytes(4, 'little')) + 0x2B + client_handle.lpBaseOfDll)

        self._client_classes = all_classes
        self._handle = csgo_handle
        self._netvars_dict = dict()

        self._dump_netvars_internal()
 
    def get_netvar(self, table_name: str, prop_name: str) -> Union[int, None]:
        return self._netvars_dict.get(table_name, dict()).get(prop_name)
 
    def dump_netvars(self, out_file = sys.stdout, json_format=False) -> None:
        if json_format:
            out_file.write(json.dumps(self._netvars_dict, indent=4))
            return

        for table in self._netvars_dict.keys():
            out_file.write(table + '\n')
            max_name_len = len(sorted(self._netvars_dict[table].keys(), reverse=True, key=lambda x: len(x))[0])

            for prop_name, prop_offset in self._netvars_dict[table].items():
                out_file.write('\t{0:<{1}} 0x{2:08x}\n'.format(prop_name, max_name_len, prop_offset))
 
    def _dump_table(self, table) -> None:
        table_name = table.get_table_name()

        for i in range(table.get_max_props()):
            prop = table.get_prop(i)
            prop_name = prop.get_name()

            if prop_name.isnumeric(): continue

            prop_offest = prop.get_offset()
            table_existed_data = self._netvars_dict.get(table_name, dict())

            table_existed_data.update({prop_name: prop_offest})
            self._netvars_dict.update({table_name: table_existed_data})

            try:
                data_table = prop.get_data_table()
                if not data_table: continue

            except Exception: continue

            else:
                try:
                    self._dump_table(data_table)

                except Exception: continue
 
    def _dump_netvars_internal(self) -> None:
        client_class = ClientClass(self._handle.read_int(self._client_classes + 0x10), self._handle)

        while client_class is not None:
            try:
                table = client_class.get_table()
                table_name = table.get_table_name()

                if not table_name: break

            except Exception: break
            
            self._dump_table(table)
            client_class = client_class.get_next_class()