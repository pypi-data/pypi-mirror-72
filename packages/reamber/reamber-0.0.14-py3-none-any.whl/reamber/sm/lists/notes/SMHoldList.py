from __future__ import annotations
from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMHoldObj import SMHoldObj
from reamber.base.lists.notes.HoldList import HoldList
from typing import List


class SMHoldList(List[SMHoldObj], HoldList, SMNoteList):

    def _upcast(self, objList: List = None) -> SMHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: SMHoldList
        """
        return SMHoldList(objList)

    def data(self) -> List[SMHoldObj]:
        return self
