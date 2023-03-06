from .._manager import AttrManager, BlackboxManager, PartManager
from .._part import PPoint
from .._attr import AAttr, APoint
from .._blackbox import BRig, BBlackbox, BModule


BlackboxManager.BlackboxManager.append_managed(BBlackbox.BBlackbox)
BlackboxManager.BlackboxManager.append_managed(BModule.BModule)
BlackboxManager.BlackboxManager.append_managed(BRig.BRig)

PartManager.PartManager.append_managed(PPoint.PPoint)

AttrManager.AttrManager.append_managed(AAttr.AAttr)
AttrManager.AttrManager.append_managed(APoint.APoint)
