#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

from typing import List


class State(object):
    def __init__(self, name, enabled, is_dif):
        self.name = name
        self._enabled = enabled
        self._is_dif = is_dif

    def is_enabled(self):
        return self._enabled

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False
        
    def is_dif(self):
        return self._is_dif


class Topology(object):
    """List of _enabled and disabled detectors. If the flag '_iterate_by_dif' is disabled (default) the iterator
       iterates through the subdetectors. If the flag is _enabled the iterator iterates throught each DIF of the
       subdetectors."""

    def __init__(self, iterate_by_dif=False):
        # type: (bool) -> None
        self._iterate_by_dif = iterate_by_dif
        if self._iterate_by_dif:
            self.wallmrd_north_top = State("WallMRD north top", True, True)
            self.wallmrd_north_bottom = State("WallMRD north bottom", True, True)
            self.wallmrd_south_top = State("WallMRD south top", True, True)
            self.wallmrd_south_bottom = State("WallMRD south bottom", True, True)
            self.wagasci_upstream_top = State("WAGASCI upstream top", True, True)
            self.wagasci_upstream_side = State("WAGASCI upstream side", True, True)
            self.wagasci_downstream_top = State("WAGASCI downstream top", True, True)
            self.wagasci_downstream_side = State("WAGASCI downstream side", True, True)
        else:
            self.wallmrd_north = State("WallMRD north", True, False)
            self.wallmrd_south = State("WallMRD south", True, False)
            self.wagasci_upstream = State("WAGASCI upstream", True, False)
            self.wagasci_downstream = State("WAGASCI downstream", True, False)

    @property
    def iterate_by_dif(self):
        return self._iterate_by_dif

    def import_topology(self, topology):
        # type: (Topology) -> None
        if self.iterate_by_dif and not topology.iterate_by_dif:
            if topology.wagasci_upstream.is_enabled():
                self.wagasci_upstream_top.enable()
                self.wagasci_upstream_side.enable()
            else:
                self.wagasci_upstream_top.disable()
                self.wagasci_upstream_side.disable()
            if topology.wagasci_downstream.is_enabled():
                self.wagasci_downstream_top.enable()
                self.wagasci_downstream_side.enable()
            else:
                self.wagasci_downstream_top.disable()
                self.wagasci_downstream_side.disable()
            if topology.wallmrd_north.is_enabled():
                self.wallmrd_north_top.enable()
                self.wallmrd_north_bottom.enable()
            else:
                self.wallmrd_north_top.disable()
                self.wallmrd_north_bottom.disable()
            if topology.wallmrd_south.is_enabled():
                self.wallmrd_south_top.enable()
                self.wallmrd_south_bottom.enable()
            else:
                self.wallmrd_south_top.disable()
                self.wallmrd_south_bottom.disable()
        elif not self.iterate_by_dif and topology.iterate_by_dif:
            if topology.wagasci_upstream_top.is_enabled() or topology.wagasci_upstream_side.is_enabled():
                self.wagasci_upstream.enable()
            else:
                self.wagasci_upstream.disable()
            if topology.wagasci_downstream_top.is_enabled() or topology.wagasci_downstream_side.is_enabled():
                self.wagasci_downstream.enable()
            else:
                self.wagasci_downstream.disable()
            if topology.wallmrd_north_top.is_enabled() or topology.wallmrd_north_bottom.is_enabled():
                self.wallmrd_north.enable()
            else:
                self.wallmrd_north.disable()
            if topology.wallmrd_south_top.is_enabled() or topology.wallmrd_south_bottom.is_enabled():
                self.wallmrd_south.enable()
            else:
                self.wallmrd_south.disable()
        else:
            for key, value in vars(self).items():
                setattr(self, key, getattr(topology, key))

    def are_all_enabled(self):
        # type: (...) -> bool
        for value in vars(self).values():
            if isinstance(value, State) and value.is_enabled() is False:
                return False
        return True

    def disable_all_but(self, one):
        # type: (str) -> None
        for d in vars(self).values():
            if isinstance(d, State):
                if d.name == one:
                    d.enable()
                else:
                    d.disable()

    def how_many_enabled(self):
        # type: (...) -> int
        return len(self.get_enabled())

    def disable_all(self):
        # type: (...) -> None
        for d in vars(self).values():
            if isinstance(d, State):
                d.disable()

    def get_all(self):
        # type: (...) -> List[State]
        if self._iterate_by_dif:
            return [value for value in vars(self).values() if isinstance(value, State) and value.is_dif() is True]
        else:
            return [value for value in vars(self).values() if isinstance(value, State) and value.is_dif() is False]

    def get_enabled(self):
        # type: (...) -> List[State]
        if self._iterate_by_dif:
            return [value for value in vars(self).values()
                    if isinstance(value, State) and value.is_dif() is True and value.is_enabled() is True]
        else:
            return [value for value in vars(self).values()
                    if isinstance(value, State) and value.is_dif() is False and value.is_enabled() is True]

    def get_disabled(self):
        # type: (...) -> List[State]
        if self._iterate_by_dif:
            return [value for value in vars(self).values()
                    if isinstance(value, State) and value.is_dif() is True and value.is_enabled() is False]
        else:
            return [value for value in vars(self).values()
                    if isinstance(value, State) and value.is_dif() is False and value.is_enabled() is False]

    def __iter__(self):
        # type: (...) -> TopologyIterator
        """ Returns the Iterator object """
        return TopologyIterator(self)


class TopologyIterator(object):
    def __init__(self, topology):
        # type: (Topology) -> None
        # Difs object reference
        self._topology = topology
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        # type: (...) -> State
        """ Returns the next value from difs object's lists """
        if self._topology.iterate_by_dif:
            if self._index == 0:
                result = self._topology.wallmrd_north_top
            elif self._index == 1:
                result = self._topology.wallmrd_north_bottom
            elif self._index == 2:
                result = self._topology.wallmrd_south_top
            elif self._index == 3:
                result = self._topology.wallmrd_south_bottom
            elif self._index == 4:
                result = self._topology.wagasci_upstream_top
            elif self._index == 5:
                result = self._topology.wagasci_upstream_side
            elif self._index == 6:
                result = self._topology.wagasci_downstream_top
            elif self._index == 7:
                result = self._topology.wagasci_downstream_side
            else:
                raise StopIteration
        else:
            if self._index == 0:
                result = self._topology.wallmrd_north
            elif self._index == 1:
                result = self._topology.wallmrd_south
            elif self._index == 2:
                result = self._topology.wagasci_upstream
            elif self._index == 3:
                result = self._topology.wagasci_downstream
            else:
                raise StopIteration
        self._index += 1
        return result
