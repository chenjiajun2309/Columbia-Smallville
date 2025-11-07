import json, glob, random, os

# Maze 大小
MAX_X, MAX_Y = 39, 29

base = "generative_agents/frontend/static/assets/Columbia/agents"

for f in glob.glob(f"{base}/*/agent.json"):
    with open(f, "r", encoding="utf-8") as x:
        data = json.load(x)

    x, y = data["coord"]

    if x > MAX_X or y > MAX_Y:
        # 重新随机分配合法坐标
        new_x = random.randint(5, MAX_X - 5)
        new_y = random.randint(5, MAX_Y - 5)
        print(f"修复 {f}: 原坐标 ({x},{y}) -> 新坐标 ({new_x},{new_y})")
        data["coord"] = [new_x, new_y]

        with open(f, "w", encoding="utf-8") as w:
            json.dump(data, w, indent=2, ensure_ascii=False)
    else:
        print(f"✅ 合法: {f} ({x},{y})")

print("\n🎉 坐标修复完成！所有 Agent 坐标均在 [0–39, 0–29] 范围内。")
