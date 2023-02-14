from maya import cmds

from . import BBlackbox
from .._core import CNode
from .._attr import AAttr


class BModule(BBlackbox.BBlackbox):

    DAG_PUBLIC = 'public'
    DAG_PRIVATE = 'private'

    ATTR_TYPE = 'type'
    ATTR_PUBLIC = 'public'
    ATTR_PRIVATE = 'private'

    @classmethod
    def generate(cls, name: str = None, manager: CNode.CNode = None):

        bb = super().generate(name, manager)

        public_name = '_'.join([name, cls.DAG_PUBLIC]) if name else cls.DAG_PUBLIC
        private_name = '_'.join([name, cls.DAG_PRIVATE]) if name else cls.DAG_PRIVATE

        public_node = CNode.CNode.generate(
                'transform', n=public_name, p=bb.node
                )

        private_node = CNode.CNode.generate(
                'transform', n=private_name, p=bb.node
                )

        public_attr = AAttr.AAttr.generate(
                bb, ln=cls.ATTR_PUBLIC,
                at='message')

        private_attr = AAttr.AAttr.generate(
                bb, ln=cls.ATTR_PRIVATE,
                at='message')

        cmds.connectAttr(
                f'{public_node.node}.msg',
                public_attr.item)

        cmds.connectAttr(
                f'{private_node.node}.msg',
                private_attr.item)

        return cls(bb.node)

    @classmethod
    def check(cls): pass

    @property
    def public(self) -> CNode.CNode:

        conn = cmds.listConnections(
                f'{self.node}.{self.ATTR_PUBLIC}',
                s=True, d=False
                ) or []

        if conn:
            return CNode.CNode(conn[0])

        else:
            raise NameError('{self.node}: fail to found public node')

    @property
    def private(self) -> CNode.CNode:

        conn = cmds.listConnections(
                f'{self.node}.{self.ATTR_PRIVATE}',
                s=True, d=False
                ) or []

        if conn:
            # return Bb.BlackboxManager.BlackboxManager(conn[0])
            return CNode.CNode(conn[0])

        else:
            raise NameError('{self.node}: fail to found output node')
