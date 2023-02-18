from maya import cmds

from .._core import CNode
from .. import _attr as attr_m


class BBlackbox(CNode.CNode):

    DAG_ROOT = 'bb'
    DAG_INPUT = 'input'
    DAG_OUTPUT = 'output'

    ATTR_TYPE = 'type'
    ATTR_INPUT = 'input'
    ATTR_OUTPUT = 'output'

    @classmethod
    def generate(cls, name: str = None, manager: CNode.CNode = None):

        root_name = '_'.join([name, cls.DAG_ROOT]) if name else cls.DAG_ROOT
        in_name = '_'.join([name, cls.DAG_INPUT]) if name else cls.DAG_INPUT
        out_name = '_'.join([name, cls.DAG_OUTPUT]) if name else cls.DAG_OUTPUT

        root_node = CNode.CNode.generate(
                'transform', n=root_name
                )

        input_node = CNode.CNode.generate(
                'transform', n=in_name, p=root_node.node
                )

        output_node = CNode.CNode.generate(
                'transform', n=out_name, p=root_node.node
                )

        in_attr = attr_m.AAttr.AAttr.generate(
                root_node, ln=cls.ATTR_INPUT,
                at='message')

        ou_attr = attr_m.AAttr.AAttr.generate(
                root_node, ln=cls.ATTR_OUTPUT,
                at='message')

        cmds.connectAttr(
                f'{input_node.node}.msg',
                in_attr.item)

        cmds.connectAttr(
                f'{output_node.node}.msg',
                ou_attr.item)

        if isinstance(manager, CNode.CNode):

            cmds.parent(root_node.node, manager.node)

        return cls(root_node.node)

    @classmethod
    def check(cls, node: str) -> bool:

        has_in = cmds.attributeQuery(cls.ATTR_INPUT, n=node, ex=True)
        has_ou = cmds.attributeQuery(cls.ATTR_OUTPUT, n=node, ex=True)
        return has_in and has_ou

    @property
    def name(self) -> str:

        if self.node.endswith(f'_{self.DAG_ROOT}'):

            return self.node.strip(f'_{self.DAG_ROOT}')

        else:
            return self.node

    @property
    def input(self) -> CNode.CNode:

        conn = cmds.listConnections(
                f'{self.node}.{self.ATTR_INPUT}',
                s=True, d=False
                ) or []

        if conn:
            return CNode.CNode(conn[0])

        else:
            raise NameError('{self.node}: fail to found input node')

    @property
    def output(self) -> CNode.CNode:

        conn = cmds.listConnections(
                f'{self.node}.{self.ATTR_OUTPUT}',
                s=True, d=False
                ) or []

        if conn:
            return CNode.CNode(conn[0])

        else:
            raise NameError('{self.node}: fail to found output node')
