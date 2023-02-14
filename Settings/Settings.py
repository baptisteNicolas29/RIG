import raisin._blackbox.BBlackbox as BBlackbox
import raisin._blackbox.BModule as BModule
import raisin._blackbox.BRig as BRig

import raisin._attr.AAttr as AAttr
import raisin._attr.APoint as APoint

import raisin._part.PPoint as PPoint


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
