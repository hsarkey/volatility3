import argparse
import os
from typing import Tuple, Dict
from urllib import request

from volatility.framework import contexts, interfaces
from volatility.framework.layers import physical, msf


class PdbReader:
    """Class to read Microsoft PDB files"""

    sub_resolvers = {""}

    def __init__(self, context: interfaces.context.ContextInterface, location: str):
        self._layer_name, self._context = self.load_pdb_layer(context, location)
        self.types = []

    @property
    def context(self):
        return self._context

    @property
    def pdb_layer_name(self):
        return self._layer_name

    @classmethod
    def load_pdb_layer(cls, context: interfaces.context.ContextInterface,
                       location: str) -> Tuple[str, interfaces.context.ContextInterface]:
        """Loads a PDB file into a layer within the context and returns the name of the new layer

           Note: the context may be changed by this method
        """
        physical_layer_name = context.layers.free_layer_name("FileLayer")
        physical_config_path = interfaces.configuration.path_join("pdbreader", physical_layer_name)

        # Create the file layer
        # This must be specific to get us started, setup the config and run
        new_context = context.clone()
        new_context.config[interfaces.configuration.path_join(physical_config_path, "location")] = location

        physical_layer = physical.FileLayer(new_context, physical_config_path, physical_layer_name)
        new_context.add_layer(physical_layer)

        # Add on the MSF format layer
        msf_layer_name = context.layers.free_layer_name("MSFLayer")
        msf_config_path = interfaces.configuration.path_join("pdbreader", msf_layer_name)
        new_context.config[interfaces.configuration.path_join(msf_config_path, "base_layer")] = physical_layer_name
        msf_layer = msf.PdbMSF(new_context, msf_config_path, msf_layer_name)
        new_context.add_layer(msf_layer)

        msf_layer.read_streams()

        return msf_layer_name, new_context

    def read_tpi_stream(self):
        tpi_layer = self._context.layers.get(self._layer_name + "_stream2", None)
        if not tpi_layer:
            raise ValueError("No TPI stream available")
        module = self._context.module(module_name = tpi_layer.pdb_symbol_table, layer_name = tpi_layer.name, offset = 0)
        header = module.object(type_name = "TPI_HEADER", offset = 0)

        # Check the header
        if not (56 <= header.header_size < 1024):
            raise ValueError("TPI Stream Header size outside normal bounds")
        if header.index_min < 4096:
            raise ValueError("Minimum TPI index is 4096, found: {}".format(header.index_min))
        if header.index_max < header.index_min:
            raise ValueError("Maximum TPI index is smaller than minimum TPI index, found: {} < {} ".format(
                header.index_max, header.index_min))

        self.types = []

        offset = header.header_size
        # Ensure we use the same type everywhere
        length_type = "unsigned short"
        length_len = module.get_type(length_type).size
        type_index = 1
        while tpi_layer.maximum_address - offset > 0:
            length = module.object(type_name = length_type, offset = offset)
            if not isinstance(length, int):
                raise ValueError("Non-integer length provided")
            offset += length_len
            output, consumed = self.consume_type(module, offset, length)
            self.types.append(output)
            offset += length
            type_index += 1
            # Since types can only refer to earlier types, assigning the name at this point is fine

        if tpi_layer.maximum_address - offset != 0:
            raise ValueError("Type values did not fill the TPI stream correctly")

        return header

    def consume_type(self, module: interfaces.context.ModuleInterface, offset: int, length: int,
                     no_output = False) -> Tuple[Dict[str, Dict], int]:
        """Returns the dictionary for the type, and the number of bytes consumed"""
        result = {}
        leaf_type = self.context.object(
            module.get_enumeration("LEAF_TYPE"), layer_name = module._layer_name, offset = offset)
        consumed = leaf_type.vol.base_type.size
        offset += consumed

        if leaf_type in [
                leaf_type.LF_CLASS, leaf_type.LF_CLASS_ST, leaf_type.LF_STRUCTURE, leaf_type.LF_STRUCTURE_ST,
                leaf_type.LF_INTERFACE
        ]:
            structure = module.object(type_name = "LF_STRUCTURE", offset = offset)
            name = self.parse_string(leaf_type, structure.name, size = length - structure.vol.size - consumed)
            consumed = length
            result[name] = structure
        elif leaf_type in [leaf_type.LF_MEMBER, leaf_type.LF_MEMBER_ST]:
            member = module.object(type_name = "LF_MEMBER", offset = offset)
            name = self.parse_string(leaf_type, member.name, size = length - member.vol.size - consumed)
            result[name] = member
            print(name)
            consumed += member.vol.size + len(name) + 1
        elif leaf_type in [leaf_type.LF_MODIFIER, leaf_type.LF_POINTER, leaf_type.LF_PROCEDURE]:
            # TODO: Subresolve sub-types
            obj = module.object(type_name = leaf_type.lookup(), offset = offset)
            consumed = length
        elif leaf_type in [leaf_type.LF_FIELDLIST]:
            sub_length = length - consumed
            sub_offset = offset
            fields = []
            while length > consumed:
                subfield, sub_consumed = self.consume_type(module, sub_offset, sub_length, True)
                sub_consumed += self.consume_padding(module.layer_name, sub_offset + sub_consumed)
                sub_length -= sub_consumed
                sub_offset += sub_consumed
                consumed += sub_consumed
                fields.append(subfield)
            result = fields
        elif leaf_type in [leaf_type.LF_BITFIELD]:
            consumed = length
        elif leaf_type in [leaf_type.LF_ARRAY, leaf_type.LF_ARRAY_ST, leaf_type.LF_STRIDED_ARRAY]:
            consumed = length
        elif leaf_type in [leaf_type.LF_ARGLIST, leaf_type.LF_ENUMERATE, leaf_type.LF_ENUM, leaf_type.LF_UNION]:
            consumed = length
        else:
            raise ValueError("Unhandled leaf_type: {}".format(leaf_type))

        if not no_output:
            print(leaf_type.lookup())
        return result, consumed

    def consume_padding(self, layer_name: str, offset: int) -> int:
        """Returns the amount of padding used between fields"""
        val = self.context.layers[layer_name].read(offset, 1)
        if not (int(val[0]) & 0xf0):
            return 0
        return (int(val[0]) & 0x0f)

    def parse_string(self,
                     leaf_type: interfaces.objects.ObjectInterface,
                     structure: interfaces.objects.ObjectInterface,
                     size = 0) -> str:
        """Consumes either a c-string or a pascal string depending on the leaf_type"""
        if leaf_type > leaf_type.LF_ST_MAX:
            name = structure.cast("string", max_length = size, encoding = "latin-1")
        else:
            name = structure.cast("pascal_string")
            name = name.string.cast("string", max_length = name.length, encoding = "latin-1")
        return name


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help = "Provide the name of a pdb file to read", required = True)
    args = parser.parse_args()

    ctx = contexts.Context()
    if not os.path.exists(args.filename):
        parser.error("File {} does not exists".format(args.filename))
    location = "file:" + request.pathname2url(args.filename)

    reader = PdbReader(ctx, location)

    ### TESTING
    # x = ctx.object('pdb1!BIG_MSF_HDR', reader.pdb_layer_name, 0)
    header = reader.read_tpi_stream()

    import pdb

    pdb.set_trace()
    print(reader.types)