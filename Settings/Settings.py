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

        return [*module_content_list, *cls.__ATTR]

    @classmethod
    def blackbox(cls):
        print('Settings.blackbox -> start method')

        module_content_list = []
        for module in cls.__MODULE:
            module_content_list.extend(module.blackbox)

        return [*module_content_list, *cls.__BLACKBOX]

    @classmethod
    def part(cls):

        module_content_list = []
        for module in cls.__MODULE:
            module_content_list.extend(module.part)

        return [*module_content_list, *cls.__PART]

    @classmethod
    def append_module(cls, module):

        cls.__MODULE.append(module)
