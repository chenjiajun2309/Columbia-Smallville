import json, math, os

TILEMAP_JSON = "/Users/chenjiajun/Downloads/ColumbiaSmallville/generative_agents/frontend/static/assets/Columbia/tilemap/tilemap.json"
MAZE_OUT     = "/Users/chenjiajun/Downloads/ColumbiaSmallville/generative_agents/frontend/static/assets/Columbia/maze.json"

m = json.load(open(TILEMAP_JSON, "r", encoding="utf-8"))
tw, th = m["tilewidth"], m["tileheight"]
W, H = m["width"], m["height"]
grid = [[0 for _ in range(W)] for _ in range(H)]

for L in m["layers"]:
    if L["type"] == "objectgroup" and L["name"].lower() == "colliders":
        for obj in L.get("objects", []):
            x0 = int(obj["x"] // tw)
            y0 = int(obj["y"] // th)
            x1 = int(math.ceil((obj["x"] + obj.get("width", 0)) / tw))
            y1 = int(math.ceil((obj["y"] + obj.get("height", 0)) / th))
            for y in range(y0, y1):
                for x in range(x0, x1):
                    if 0 <= x < W and 0 <= y < H:
                        grid[y][x] = 1

maze = {"tilewidth": tw, "tileheight": th, "size": [H, W], "maze": grid}
json.dump(maze, open(MAZE_OUT, "w", encoding="utf-8"), indent=2)
print("✅ wrote", MAZE_OUT, f"({W}x{H}, tile {tw}x{th})")