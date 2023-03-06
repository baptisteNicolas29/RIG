from .._blackbox import BBlackbox
from .._blackbox import BModule
from .._blackbox import BRig

from .._attr import AAttr
from .._attr import APoint

from .._part import PPoint


class Settings:

    __ATTR = [
            APoint.APoint,
            AAttr.AAttr
            ]

    __BLACKBOX = [
            BRig.BRig,
            BModule.BModule,
            BBlackbox.BBlackbox,
            ]

    __PART = [
            PPoint.PPoint
            ]
    __MODULE = []

    @classmethod
    def attr(cls):

        module_content_list = []
        for module in cls.__MODULE:
            module_content_list.extend(module.attr)

        final_module_content = []
        for mod in module_content_list:
            if mod not in final_module_content:
                final_module_content.append(mod)

        return [*final_module_content, *cls.__ATTR]

    @classmethod
    def blackbox(cls):
        print('Settings.blackbox -> start method')

        module_content_list = []
        for module in cls.__MODULE:
            module_content_list.extend(module.blackbox)

        final_module_content = []
        for mod in module_content_list:
            if mod not in final_module_content:
                final_module_content.append(mod)

        return [*final_module_content, *cls.__BLACKBOX]

    @classmethod
    def part(cls):

        module_content_list = []
        for module in cls.__MODULE:
            module_content_list.extend(module.part)

        final_module_content = []
        for mod in module_content_list:
            if mod not in final_module_content:
                final_module_content.append(mod)

        return [*final_module_content, *cls.__BLACKBOX]

    @classmethod
    def append_module(cls, module):

        cls.__MODULE.append(module)
