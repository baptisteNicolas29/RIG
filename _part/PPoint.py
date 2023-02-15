import typing

from maya import cmds

from .._core import CNode
from .._attr import AAttr
from .._attr import APoint
from .._abstract import AbcPoint


class PPoint(CNode.CNode, AbcPoint.AbcPoint):

    ATTR_DATA = 'data'
    ATTR_POINT = 'point'
    ATTR_CHILDREN = 'children'

    @classmethod
    def generate(
            cls, node_type: str, data: AAttr.AAttr,
            point: typing.Optional[AbcPoint.AbcPoint] = None, **kwargs
            ):

        node = super().generate(node_type, **kwargs)
        node = cls.set(node.node, data, point=point)
        return node

    @classmethod
    def set(
            cls, node: str, data: AAttr.AAttr,
            point: typing.Optional[AbcPoint.AbcPoint] = None):

        # create attributes
        data_attr = AAttr.AAttr.generate(
                CNode.CNode(node), ln=cls.ATTR_DATA, at='message')

        point_attr = AAttr.AAttr.generate(
                CNode.CNode(node), ln=cls.ATTR_POINT, at='message')

        AAttr.AAttr.generate(
                CNode.CNode(node), ln=cls.ATTR_CHILDREN, at='message')

        # connecting attributes
        cmds.connectAttr(data.item, data_attr.item, f=True)

        if point is not None:
            cmds.connectAttr(point.item, point_attr.item)

        item = cls(node)
        item.__build()

        return item

    @property
    def item(self) -> str:

        return f'{self.node}.{self.ATTR_CHILDREN}'

    @property
    def parent(self):

        node = cmds.listConnections(
                AAttr.AAttr(self.node, self.ATTR_POINT).item,
                s=True, d=False, p=True
                ) or []

        if not node:
            return None

        elif node[0].endswith(f'.{self.ATTR_CHILDREN}'):
            return PPoint(node[0].split('.')[0])

        else:
            return APoint.APoint.from_string(node[0])

    @parent.setter
    def parent(self, parent) -> None:

        cmds.connectAttr(parent.item, f'{self.node}.{self.ATTR_POINT}', f=True)
        self.__build()

    @property
    def children(self):

        nodes = cmds.listConnections(
                AAttr.AAttr(self.node, self.ATTR_CHILDREN).item,
                s=False, d=True, p=True
                ) or []

        return_nodes = []

        for node in nodes:

            if node.endswith(f'.{self.ATTR_POINT}'):
                return_nodes.append(PPoint(node.split('.')[0]))

        return return_nodes

    @property
    def matrix(self) -> str:

        return AAttr.AAttr(self.node, 'wm')

    @property
    def data(self) -> AAttr.AAttr:

        node = cmds.listConnections(
                AAttr.AAttr(self.node, self.ATTR_DATA).item,
                s=True, d=False, p=True
                ) or []

        if not node:
            raise NameError('fail to found attr for data part')

        out = node[0]
        nod = out.split('.')[0]
        att = '.'.join(out.split('.')[1:])
        return AAttr.AAttr(nod, att)

    @data.setter
    def data(self, data) -> None:

        cmds.connectAttr(data.item, f'{self.node}.{self.ATTR_DATA}', f=True)
        self.__build()

        for child in self.children:
            child.parent = self

    def __build(self):

        opm_attr = None

        if isinstance(self.parent, APoint.APoint):
            mm = cmds.createNode('multMatrix', ss=True)
            im = cmds.createNode('inverseMatrix', ss=True)
            cmds.connectAttr(self.parent.data.item, f'{im}.imat')

            cmds.connectAttr(self.data.item, f'{mm}.i[0]', f=True)
            cmds.connectAttr(f'{im}.omat', f'{mm}.i[1]', f=True)
            cmds.connectAttr(self.parent.matrix.item, f'{mm}.i[2]', f=True)
            opm_attr = f'{mm}.o'

        elif isinstance(self.parent, PPoint):
            parent_node = (cmds.listRelatives(self.node, p=True) or [None])[0]

            mm = cmds.createNode('multMatrix', ss=True)
            im = cmds.createNode('inverseMatrix', ss=True)

            cmds.connectAttr(self.data.item, f'{mm}.i[0]', f=True)
            cmds.connectAttr(self.parent.data.item, f'{im}.imat', f=True)
            cmds.connectAttr(f'{im}.omat', f'{mm}.i[1]', f=True)

            if parent_node != self.parent.node:
                cmds.connectAttr(self.parent.matrix.item, f'{mm}.i[2]', f=True)
                opm_attr = f'{mm}.o'

            opm_attr = f'{mm}.o'

        else:
            opm_attr = self.data.item

        cmds.connectAttr(opm_attr, f'{self.node}.opm', f=True)
