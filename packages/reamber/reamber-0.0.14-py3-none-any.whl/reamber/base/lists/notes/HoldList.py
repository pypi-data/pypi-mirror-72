from __future__ import annotations
from typing import List, Tuple
from reamber.base.HoldObj import HoldObj
from abc import ABC, abstractmethod


class HoldList(ABC):
    @abstractmethod
    def data(self) -> List[HoldObj]: ...

    def lastOffset(self) -> float:
        """ Get Last Note Offset """
        return sorted(self.data(), key=lambda x: x.offset)[-1].tailOffset()

    def firstLastOffset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset
        This is slightly faster than separately calling the singular functions since it sorts once only
        """
        hos = sorted(self.data())
        return hos[0].offset, hos[-1].tailOffset()

    def offsets(self, flatten=True):
        """ Grabs all offsets and tail offsets of objects

        :param flatten: Whether to flatten it to a 1D list
        :return: A 1D List if flatten else 2D
        """
        if flatten: return [i for j in [(obj.offset, obj.tailOffset()) for obj in self.data()] for i in j]
        return [(obj.offset, obj.tailOffset()) for obj in self.data()]

    def tailOffsets(self) -> List[float]:
        return [obj.tailOffset() for obj in self.data()]

    def lengths(self) -> List[float]:
        """ Grabs all object lengths as a list """
        return [obj.length for obj in self.data()]
