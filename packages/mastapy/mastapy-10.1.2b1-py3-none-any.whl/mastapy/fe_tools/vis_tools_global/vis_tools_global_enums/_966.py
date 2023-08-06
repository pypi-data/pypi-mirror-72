'''_966.py

ContactPairReferenceSurfaceType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONTACT_PAIR_REFERENCE_SURFACE_TYPE = python_net_import('SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums', 'ContactPairReferenceSurfaceType')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactPairReferenceSurfaceType',)


class ContactPairReferenceSurfaceType(Enum):
    '''ContactPairReferenceSurfaceType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CONTACT_PAIR_REFERENCE_SURFACE_TYPE

    __hash__ = None

    ELEMENT_EDGE = 2
    ELEMENT_FACE = 3
    ANALYTIC_SURFACE = 2660
