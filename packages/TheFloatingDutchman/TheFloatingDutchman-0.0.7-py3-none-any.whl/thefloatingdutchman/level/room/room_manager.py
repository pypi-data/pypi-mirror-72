from typing import List

import networkx as nx
from pygame import Surface

from thefloatingdutchman.manager import Manager
from thefloatingdutchman.level.room.room import Room
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite


class RoomManager(Manager):
    def __init__(self):
        super().__init__()
        self._number_of_rooms = 0
        self._rooms = []
        self._rooms_per_row = []
        self._room_graph = nx.DiGraph()
        self._current_room_id = 0

    def _generate_room_graph(self):
        self._number_of_rooms = 11

        for i in range(0, self._number_of_rooms):
            self._rooms.append(Room())

        # room_rows = 5 == len(self.rooms_per_row)
        # first and last row should always have 1
        self.rooms_per_row.append(1)  # 0
        self.rooms_per_row.append(2)  # 1, 2
        self.rooms_per_row.append(4)  # 3, 4, 5, 6
        self.rooms_per_row.append(3)  # 7, 8, 9
        self.rooms_per_row.append(1)  # 10

        self._room_graph.add_edges_from(
            [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 5),
             (2, 6), (3, 7), (4, 7), (5, 8), (6, 9),
             (7, 10), (8, 10), (9, 10)
             ])

    def spawn(self, level: int):
        self._rooms = []
        self._rooms_per_row = []
        self._current_room_id = 0

        self._room_graph.clear()
        self._generate_room_graph()

        for i, room in enumerate(self._rooms):
            room.spawn(level, i)

    def get_available_rooms(self) -> List[int]:

        # room must be cleared to move on
        if not self._rooms[self._current_room_id].cleared():
            return []

        # gets pairs of edges from current room to next available rooms
        edges = self._room_graph.edges(self._current_room_id)

        # gets list of rooms player can move to next
        return [v2 for v1, v2 in edges]

    def is_level_cleared(self) -> bool:

        return self._rooms[self.current_room_id].cleared() and not self.get_available_rooms()

    def set_current_room(self, _id: int):
        # TODO(kayton): Add checks to ensure id is valid
        self._current_room_id = _id

    def update(self, player: PlayerSprite, screen: Surface):
        self._rooms[self._current_room_id].update(player, screen)

    def draw(self, screen):
        self._rooms[self._current_room_id].draw(screen)

    def get_current_enemies(self) -> List[EnemySprite]:
        return self.rooms[self.current_room_id].get_enemies()

    @property
    def current_room_id(self):
        return self._current_room_id

    @property
    def rooms(self) -> List[Room]:
        return self._rooms

    @property
    def rooms_per_row(self) -> List[int]:
        return self._rooms_per_row
