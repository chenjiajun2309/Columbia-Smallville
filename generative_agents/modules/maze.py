"""generative_agents.maze — Columbia Smallville compatible version"""

import random
from itertools import product

from modules import utils
from modules.memory.event import Event


class Tile:
    def __init__(self, coord, world, address_keys, address=None, collision=False):
        # world, sector, arena, game_object
        self.coord = coord
        self.address = [world]
        if address:
            self.address += address
        self.address_keys = address_keys
        self.address_map = dict(zip(address_keys[: len(self.address)], self.address))
        self.collision = collision
        self.event_cnt = 0
        self._events = {}
        if len(self.address) == 4:
            self.add_event(Event(self.address[-1], address=self.address))

    def abstract(self):
        address = ":".join(self.address)
        if self.collision:
            address += "(collision)"
        return {
            f"coord[{self.coord[0]},{self.coord[1]}]": address,
            "events": {k: str(v) for k, v in self.events.items()},
        }

    def __str__(self):
        return utils.dump_dict(self.abstract())

    def __eq__(self, other):
        if isinstance(other, Tile):
            return hash(self.coord) == hash(other.coord)
        return False

    @property
    def events(self):
        return self._events

    @property
    def is_empty(self):
        return len(self.address) == 1 and not self._events

    def get_events(self):
        return self.events.values()

    def add_event(self, event):
        if isinstance(event, (tuple, list)):
            event = Event.from_list(event)
        if all(e != event for e in self._events.values()):
            self._events["e_" + str(self.event_cnt)] = event
            self.event_cnt += 1
        return event

    def remove_events(self, subject=None, event=None):
        r_events = {}
        for tag, eve in self._events.items():
            if subject and eve.subject == subject:
                r_events[tag] = eve
            if event and eve == event:
                r_events[tag] = eve
        for r_eve in r_events:
            self._events.pop(r_eve)
        return r_events

    def update_events(self, event, match="subject"):
        u_events = {}
        for tag, eve in self._events.items():
            if match == "subject" and eve.subject == event.subject:
                self._events[tag] = event
                u_events[tag] = event
        return u_events

    def has_address(self, key):
        return key in self.address_map

    def get_address(self, level=None, as_list=True):
        level = level or self.address_keys[-1]
        assert level in self.address_keys, f"Can not find {level} from {self.address_keys}"
        pos = self.address_keys.index(level) + 1
        if as_list:
            return self.address[:pos]
        return ":".join(self.address[:pos])

    def get_addresses(self):
        if len(self.address) > 1:
            return [":".join(self.address[:i]) for i in range(2, len(self.address) + 1)]
        return []


class Maze:
    """兼容 Columbia 简化 maze.json 与原版 full schema"""

    def __init__(self, config, logger):
        self.logger = logger

        # ---- 1) tile 尺寸 ----
        self.tile_size = (
            config.get("tile_size")
            or config.get("tilewidth")
            or config.get("tileheight")
            or 32
        )

        # ---- 2) 尺寸 ----
        if "size" in config:
            self.maze_height, self.maze_width = config["size"]
        elif "maze" in config and config["maze"]:
            self.maze_height = len(config["maze"])
            self.maze_width = len(config["maze"][0])
        else:
            raise KeyError("maze size missing: provide 'size':[H,W] or a 'maze' grid")

        # ---- 3) address_keys / world 默认值 ----
        address_keys = config.get("tile_address_keys", ["world", "sector", "arena", "game_object"])
        world = config.get("world", "Columbia Campus")

        # ---- 4) 初始化 tile 网格 ----
        self.tiles = [
            [Tile((x, y), world, address_keys) for x in range(self.maze_width)]
            for y in range(self.maze_height)
        ]

        # ---- 5) 根据 maze 网格添加碰撞 ----
        if "maze" in config and config["maze"]:
            grid = config["maze"]
            for y in range(min(self.maze_height, len(grid))):
                for x in range(min(self.maze_width, len(grid[y]))):
                    if int(grid[y][x]) == 1:
                        self.tiles[y][x] = Tile((x, y), world, address_keys, collision=True)

        # ---- 6) 如果存在更详细的 tile 数据，进行覆盖 ----
        for t in config.get("tiles", []):
            t = dict(t)
            x, y = t.pop("coord")
            self.tiles[y][x] = Tile((x, y), world, address_keys, **t)

        # ---- 7) 地址索引 ----
        self.address_tiles = {}
        for i in range(self.maze_height):
            for j in range(self.maze_width):
                adds = self.tile_at([j, i]).get_addresses()
                for add in adds:
                    self.address_tiles.setdefault(add, set()).add((j, i))

    def tile_at(self, coord):
        return self.tiles[coord[1]][coord[0]]

    def update_obj(self, coord, obj_event):
        tile = self.tile_at(coord)
        if not tile.has_address("game_object"):
            return
        if obj_event.address != tile.get_address("game_object"):
            return
        addr = ":".join(obj_event.address)
        if addr not in self.address_tiles:
            return
        for c in self.address_tiles[addr]:
            self.tile_at(c).update_events(obj_event)

    def get_scope(self, coord, config):
        coords = []
        vision_r = config["vision_r"]
        if config["mode"] == "box":
            x_range = [max(coord[0] - vision_r, 0), min(coord[0] + vision_r + 1, self.maze_width)]
            y_range = [max(coord[1] - vision_r, 0), min(coord[1] + vision_r + 1, self.maze_height)]
            coords = list(product(list(range(*x_range)), list(range(*y_range))))
        return [self.tile_at(c) for c in coords]

    def get_around(self, coord, no_collision=True):
        coords = [
            (coord[0] - 1, coord[1]),
            (coord[0] + 1, coord[1]),
            (coord[0], coord[1] - 1),
            (coord[0], coord[1] + 1),
        ]
        if no_collision:
            coords = [c for c in coords if not self.tile_at(c).collision]
        return coords

    def get_address_tiles(self, address):
        addr = ":".join(address)
        if addr in self.address_tiles:
            return self.address_tiles[addr]
        # fallback：返回所有可走格子
        fallback = {
            (x, y)
            for y in range(self.maze_height)
            for x in range(self.maze_width)
            if not self.tile_at((x, y)).collision
        }
        if fallback:
            return fallback
        # 极端情况退回全图
        return {(x, y) for y in range(self.maze_height) for x in range(self.maze_width)}

    def find_path(self, src_coord, dst_coord):
        """简单 BFS 寻路"""
        map = [[0 for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        frontier, visited = [src_coord], set()
        map[src_coord[1]][src_coord[0]] = 1
        while map[dst_coord[1]][dst_coord[0]] == 0 and frontier:
            new_frontier = []
            for f in frontier:
                for c in self.get_around(f):
                    if (
                        0 <= c[0] < self.maze_width
                        and 0 <= c[1] < self.maze_height
                        and map[c[1]][c[0]] == 0
                        and c not in visited
                    ):
                        map[c[1]][c[0]] = map[f[1]][f[0]] + 1
                        new_frontier.append(c)
                        visited.add(c)
            frontier = new_frontier
        if map[dst_coord[1]][dst_coord[0]] == 0:
            return [src_coord, dst_coord]
        step = map[dst_coord[1]][dst_coord[0]]
        path = [dst_coord]
        while step > 1:
            for c in self.get_around(path[-1], no_collision=False):
                if map[c[1]][c[0]] == step - 1:
                    path.append(c)
                    break
            step -= 1
        return path[::-1]
