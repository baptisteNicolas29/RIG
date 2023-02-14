from maya import cmds

from . import BBlackbox
from .._core import CNode
from .._attr import AAttr


class BRig(BBlackbox.BBlackbox):

    DAG_ROOT = 'rig'
    DAG_GEOMETRY = 'geo'
    DAG_PLACER = 'placer'
    DAG_CONTROL = 'control'
    DAG_RESUTL = 'result'

    ATTR_TYPE = 'type'
    ATTR_GEOMETRY = 'geo'
    ATTR_PLACER = 'placer'
    ATTR_CONTROL = 'ctrl'
    ATTR_RESUTL = 'result'

    @classmethod
    def generate(cls, name: str = None, manager: CNode.CNode = None):

        bb = super().generate(name, manager)

        names = [
                cls.DAG_GEOMETRY,
                cls.DAG_PLACER,
                cls.DAG_CONTROL,
                cls.DAG_RESUTL
                ]

        attrs = [
                cls.ATTR_GEOMETRY,
                cls.ATTR_PLACER,
                cls.ATTR_CONTROL,
                cls.ATTR_RESUTL
                ]
        for suffix, attr in zip(names, attrs):

            node_name = suffix

            if name:

                node_name = f'{name}_{suffix}'

            node = CNode.CNode.generate(
                    'transform', n=node_name,
                    p=bb.node, ss=True
                    )
            conn_attr = AAttr.AAttr.generate(bb, ln=attr, at='message')
            cmds.connectAttr(f'{node.node}.msg', conn_attr.item)

        return cls(bb.node)

    @classmethod
    def check(cls): pass

    @property
    def geometry(self) -> CNode.CNode:

        conn = cmds.listConnections(
                f'{self.node}.{self.ATTR_GEOMETRY}',
                s=True, d=False
                ) or []

        if conn:
            return CNode.CNode(conn[0])

        else:
            raise NameError('{self.node}: fail to found geometry node')

    @property
    def placer(self) -> CNode.CNode:

        conn = cmds.listConnections(
                f'{self.node}.{self.ATTR_PLACER}',
                s=True, d=False
                ) or []

        if conn:
            return CNode.CNode(conn[0])

        else:
            raise NameError('{self.node}: fail to found placer node')

    @property
    def control(self) -> CNode.CNode:

        conn = cmds.listConnections(
                f'{self.node}.{self.ATTR_CONTROL}',
                s=True, d=False
                ) or []

        if conn:
            return CNode.CNode(conn[0])
            # return BlackboxManager.BlackboxManager(conn[0])

        else:
            raise NameError('{self.node}: fail to found control node')

    @property
    def result(self) -> CNode.CNode:

        conn = cmds.listConnections(
                f'{self.node}.{self.ATTR_RESUTL}',
                s=True, d=False
                ) or []

        if conn:
            return CNode.CNode(conn[0])

        else:
            raise NameError('{self.node}: fail to found result node')
