from maya import cmds

from .._abstract import AbcAttr
from .._abstract import AbcPoint
from .._core import CNode
from .._attr import AAttr


class APoint(
        AbcAttr.AbcAttr,
        AbcPoint.AbcPoint
        ):
    '''
    this class is a representation of a Point Attribute
    '''

    ATTR_MATRIX = 'matrix'
    ATTR_DATA = 'data'

    @classmethod
    def generate(cls, node: CNode.CNode, **kwargs):
        '''
        this methode generate a point attribute on the given node
        :param node: CNode you want the attribute on
        :return: APoint
        '''
        dt = kwargs.pop('dataType', None)
        dt = kwargs.pop('dt', dt)

        at = kwargs.pop('attributeType', None)
        at = kwargs.pop('at', at)

        cmds.addAttr(node.node, at='compound', nc=2, **kwargs)

        ln = kwargs.pop('longName', None)
        ln = kwargs.pop('ln', ln)

        sn = kwargs.pop('shortName', None)
        sn = kwargs.pop('sn', sn)

        matrix_data = kwargs.copy()
        if ln:
            matrix_data['ln'] = f'{ln}_{cls.ATTR_MATRIX}'
        if sn:
            matrix_data['sn'] = f'{sn}_{cls.ATTR_MATRIX}'
        if dt:
            matrix_data['dt'] = dt
        if at:
            matrix_data['at'] = at

        matrix_data.pop('multi', None)
        matrix_data.pop('m', None)

        xform_data = kwargs.copy()
        if ln:
            xform_data['ln'] = f'{ln}_{cls.ATTR_DATA}'
        if sn:
            xform_data['sn'] = f'{sn}_{cls.ATTR_DATA}'
        if dt:
            xform_data['dt'] = dt
        if at:
            xform_data['at'] = at

        xform_data.pop('multi', None)
        xform_data.pop('m', None)

        cmds.addAttr(node.node, p=ln if ln else sn, **matrix_data)
        cmds.addAttr(node.node, p=ln if ln else sn, **xform_data)

        return cls(node.node, ln if ln else sn)

    @classmethod
    def check(cls, node: str, attr: str) -> bool:

        check_nbr_child = cmds.attributeQuery(attr, n=node, nc=True) or [0]
        check_nbr_child = check_nbr_child[0]
        check_nbr_child = check_nbr_child == 2

        children_attrs = cmds.attributeQuery(attr, n=node, lc=True) or []
        children_types = [cmds.attributeQuery(a, n=node, at=True) for a in children_attrs]
        check_children_types = len(list(set(children_types))) == 1

        if not check_nbr_child:

            return False

        if not check_children_types:

            return False

        data_attr = f'{attr}_{cls.ATTR_DATA}' in children_attrs
        matrix_attr = f'{attr}_{cls.ATTR_MATRIX}' in children_attrs

        return data_attr and matrix_attr

    @property
    def matrix(self):
        """The matrix property."""
        # return f'{self.item}.{self.attr}_{self.ATTR_MATRIX}'
        return AAttr.AAttr(
                self.node,
                f'{self.attr}.{self.name}_{self.ATTR_MATRIX}'
                )

    @property
    def data(self):
        """The data property."""
        return AAttr.AAttr(
                self.node,
                f'{self.attr}.{self.name}_{self.ATTR_DATA}'
                )
