# This file is Copyright 2019 Volatility Foundation and licensed under the Volatility Software License 1.0
# which is available at https://www.volatilityfoundation.org/license/vsl-v1.0
#

from typing import Any, List, Optional, Tuple, Union

from volatility3.cli.volshell import generic
from volatility3.framework import constants, interfaces
from volatility3.framework.configuration import requirements
from volatility3.plugins.windows import pslist


class Volshell(generic.Volshell):
    """Shell environment to directly interact with a windows memory image."""

    @classmethod
    def get_requirements(cls):
        return [
            requirements.ModuleRequirement(name="kernel", description="Windows kernel"),
            requirements.PluginRequirement(
                name="pslist", plugin=pslist.PsList, version=(2, 0, 0)
            ),
            requirements.IntRequirement(
                name="pid", description="Process ID", optional=True
            ),
        ]

    def change_process(self, pid=None):
        """Change the current process and layer, based on a process ID"""
        processes = self.list_processes()
        for process in processes:
            if process.UniqueProcessId == pid:
                process_layer = process.add_process_layer()
                self.change_layer(process_layer)
                return None
        print(f"No process with process ID {pid} found")

    def list_processes(self):
        """Returns a list of EPROCESS objects from the primary layer"""
        # We always use the main kernel memory and associated symbols
        return list(
            pslist.PsList.list_processes(
                self.context, self.current_layer, self.current_symbol_table
            )
        )

    def get_process(self, pid=None, v_offset=None, p_offset=None):
        """Returns the EPROCESS object that matches the pid. If v_offset/p_offset is provided, construct the EPROCESS object at the provided address. Only one parameter is allowed."""

        if sum(1 if x is not None else 0 for x in [pid, v_offset, p_offset]) != 1:
            print("Only one parameter is accepted")
            return None

        kernel_name = self.config["kernel"]
        kernel = self.context.modules[kernel_name]

        kernel_layer_name = kernel.layer_name

        kernel_layer = self.context.layers[kernel_layer_name]
        memory_layer_name = kernel_layer.dependencies[0]

        eprocess_symbol = kernel.symbol_table_name + constants.BANG + "_EPROCESS"

        if v_offset is not None:
            eproc = self.context.object(
                eprocess_symbol,
                layer_name=kernel_layer_name,
                offset=v_offset,
            )

            return eproc

        if p_offset is not None:
            eproc = self.context.object(
                eprocess_symbol,
                layer_name=memory_layer_name,
                offset=p_offset,
                native_layer_name=kernel_layer_name,
            )

            return eproc

        if pid is not None:
            processes = self.list_processes()
            for process in processes:
                if process.UniqueProcessId == pid:
                    return process
            print(f"No process with process ID {pid} found")
            return None

        return None

    def construct_locals(self) -> List[Tuple[List[str], Any]]:
        result = super().construct_locals()
        result += [
            (["cp", "change_process"], self.change_process),
            (["lp", "list_processes", "ps"], self.list_processes),
            (["gp", "get_process"], self.get_process),
            (["symbols"], self.context.symbol_space[self.current_symbol_table]),
        ]
        if self.config.get("pid", None) is not None:
            self.change_process(self.config["pid"])
        return result

    def display_type(
        self,
        object: Union[
            str, interfaces.objects.ObjectInterface, interfaces.objects.Template
        ],
        offset: Optional[int] = None,
    ):
        """Display Type describes the members of a particular object in alphabetical order"""
        if isinstance(object, str):
            if constants.BANG not in object:
                object = self.current_symbol_table + constants.BANG + object
        return super().display_type(object, offset)

    def display_symbols(self, symbol_table: Optional[str] = None):
        """Prints an alphabetical list of symbols for a symbol table"""
        if symbol_table is None:
            symbol_table = self.current_symbol_table
        return super().display_symbols(symbol_table)

    @property
    def current_layer(self):
        if self.__current_layer is None:
            self.__current_layer = self.kernel.layer_name
        return self.__current_layer
