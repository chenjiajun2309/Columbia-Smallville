import os, json, copy

# === 绝对路径：你的 Columbia 资源根目录（与截图一致）===
COLUMBIA_ROOT = "/Users/chenjiajun/Downloads/GenerativeAgentsCN-main/generative_agents/frontend/static/assets/Columbia"
AGENTS_DIR = os.path.join(COLUMBIA_ROOT, "agents")

# === 资源包名（决定 agent.json 里 portrait/texture 的相对 URL 前缀）===
ASSETS_PACK = "Columbia"  # 即 assets/Columbia/...

# === 合并 roster 的输出路径（可选）===
ROSTER_OUT = "/Users/chenjiajun/Downloads/GenerativeAgentsCN-main/generative_agents/data/rosters/roster.columbia.en.json"

# === 通用的校园空间树（各角色共享，可按需删减/扩展）===
CAMPUS_TREE = {
    "Low Library": {
        "Office": ["desk", "meeting table", "bookshelf"],
        "Lobby": ["info desk", "map"]
    },
    "Butler Library": {
        "Reading Room": ["tables", "stacks", "circulation desk"],
        "Reference Desk": ["counter", "computer"]
    },
    "Mudd Hall": {
        "CS Lab": ["workstations", "whiteboard", "servers"],
        "Office": ["desk", "bookshelf"]
    },
    "Schermerhorn Hall": {
        "GIS Lab": ["workstations", "maps"],
        "Classroom": ["podium", "seats"]
    },
    "Math Building": {
        "Classroom 3": ["blackboard", "desks"]
    },
    "Humanities Hall": {
        "Seminar Room": ["circle chairs", "projector"]
    },
    "Lerner Hall": {
        "Student Center": ["lobby", "auditorium"]
    },
    "Residence Halls": {
        "Dorm A": ["rooms", "common area"],
        "Dorm B": ["rooms", "laundry"]
    },
    "Cafeteria": {
        "Kitchen": ["stoves", "prep tables"],
        "Serving Line": ["counter", "trays"]
    },
    "Security Office": {
        "Briefing Room": ["desk", "radio", "logbook"],
        "Locker Room": ["uniform rack", "storage"]
    },
    "Facilities": {
        "Workshop": ["tools", "storage"]
    },
    "Journalism School": {
        "Newsroom": ["desks", "studio"]
    },
    "Campus Plaza": {
        "Plaza": ["benches", "fountain"]
    }
}

# === 12 位 Columbia 角色元信息（坐标为占位；地图完成后再按 Tiled 实际网格调整）===
AGENTS = [
    {
        "name": "Evelyn Park",
        "age": 52,
        "innate": "decisive, diplomatic, visionary",
        "learned": "university governance, fundraising, ethical leadership",
        "lifestyle": "early meetings; midday campus walks; late policy reviews",
        "currently": "Evelyn is preparing a campus-wide address on research ethics and student well-being.",
        "coord": [50, 40],
        "living_area": ["Columbia Campus", "Low Library", "Office"]
    },
    {
        "name": "Marta Lopez",
        "age": 44,
        "innate": "patient, meticulous, helpful",
        "learned": "information retrieval, academic archiving, data literacy",
        "lifestyle": "opens Butler in the morning; community events in the evening",
        "currently": "Marta is organizing a data literacy workshop at Butler Library.",
        "coord": [45, 58],
        "living_area": ["Columbia Campus", "Butler Library", "Reference Desk"]
    },
    {
        "name": "Daniel Kim",
        "age": 41,
        "innate": "curious, analytical, calm",
        "learned": "urban geography, GIS methods, field design",
        "lifestyle": "morning lectures; afternoon labs; evening walks",
        "currently": "Daniel is preparing a field-mapping exercise on urban heat islands.",
        "coord": [63, 52],
        "living_area": ["Columbia Campus", "Schermerhorn Hall", "GIS Lab"]
    },
    {
        "name": "Priya Nair",
        "age": 38,
        "innate": "inventive, disciplined, warm",
        "learned": "human-centered AI, scalable systems",
        "lifestyle": "code review after lunch; office hours at 4 PM",
        "currently": "Priya is advising a student team on their AI capstone project.",
        "coord": [70, 38],
        "living_area": ["Columbia Campus", "Mudd Hall", "CS Lab"]
    },
    {
        "name": "Liam OConnor",
        "age": 45,
        "innate": "logical, precise, slightly eccentric",
        "learned": "graph theory, combinatorics",
        "lifestyle": "coffee, chalk, and long blackboard sessions",
        "currently": "Liam is drafting examples for a proof techniques lecture.",
        "coord": [58, 44],
        "living_area": ["Columbia Campus", "Math Building", "Classroom 3"]
    },
    {
        "name": "Grace Chen",
        "age": 47,
        "innate": "empathetic, reflective, articulate",
        "learned": "comparative literature, narrative theory",
        "lifestyle": "seminars in late morning; readings at the plaza",
        "currently": "Grace is curating a reading list on modern poetry and identity.",
        "coord": [54, 48],
        "living_area": ["Columbia Campus", "Humanities Hall", "Seminar Room"]
    },
    {
        "name": "Noah Patel",
        "age": 36,
        "innate": "diligent, observant, kind",
        "learned": "efficient scheduling, safety procedures",
        "lifestyle": "early rounds across classrooms and corridors",
        "currently": "Noah is checking maintenance requests and cleaning common areas.",
        "coord": [54, 60],
        "living_area": ["Columbia Campus", "Facilities", "Workshop"]
    },
    {
        "name": "Jason Wright",
        "age": 35,
        "innate": "alert, fair, composed",
        "learned": "patrol routines, emergency response, first aid",
        "lifestyle": "rotating shifts; peak patrol in evenings",
        "currently": "Jason is patrolling the campus plaza and assisting lost visitors.",
        "coord": [50, 56],
        "living_area": ["Columbia Campus", "Security Office", "Briefing Room"]
    },
    {
        "name": "Rosa Martinez",
        "age": 41,
        "innate": "energetic, organized, friendly",
        "learned": "inventory and crowd flow optimization",
        "lifestyle": "early prep; busy noon service",
        "currently": "Rosa is planning a healthy menu and managing the lunch rush.",
        "coord": [46, 62],
        "living_area": ["Columbia Campus", "Cafeteria", "Kitchen"]
    },
    {
        "name": "Ava Lee",
        "age": 20,
        "innate": "curious, collaborative, proactive",
        "learned": "web frameworks and teamwork",
        "lifestyle": "morning classes; afternoon group study",
        "currently": "Ava is debugging a web app for her group project.",
        "coord": [63, 66],
        "living_area": ["Columbia Campus", "Residence Halls", "Dorm A"]
    },
    {
        "name": "Benjamin Carter",
        "age": 24,
        "innate": "methodical, curious, helpful",
        "learned": "statistical modeling, experiment tracking",
        "lifestyle": "late-night coding; afternoon seminars",
        "currently": "Benjamin is running experiments for a diffusion model report.",
        "coord": [64, 67],
        "living_area": ["Columbia Campus", "Mudd Hall", "CS Lab"]
    },
    {
        "name": "Sophia Rossi",
        "age": 21,
        "innate": "outgoing, observant, ethical",
        "learned": "interview techniques and fact checking",
        "lifestyle": "reporting in afternoons; editing in evenings",
        "currently": "Sophia is interviewing students about study habits at the plaza.",
        "coord": [56, 66],
        "living_area": ["Columbia Campus", "Journalism School", "Newsroom"]
    }
]

def build_agent_json(meta: dict) -> dict:
    """生成与项目兼容的 agent.json 结构（不额外加‘role’字段，避免破坏旧代码）"""
    name = meta["name"]
    portrait_rel = f"assets/{ASSETS_PACK}/agents/{name}/portrait.png"
    agent = {
        "name": name,
        "portrait": portrait_rel,
        "coord": meta["coord"],
        "currently": meta["currently"],
        "scratch": {
            "age": meta["age"],
            "innate": meta["innate"],
            "learned": meta["learned"],
            "lifestyle": meta["lifestyle"],
            "daily_plan": ""
        },
        "spatial": {
            "address": { "living_area": meta["living_area"] },
            "tree": { "Columbia Campus": copy.deepcopy(CAMPUS_TREE) }
        }
    }
    return agent

def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def write_json(path: str, obj) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def main():
    print("== Generating agent.json for 12 Columbia agents ==")
    ensure_dir(AGENTS_DIR)

    roster = []
    # 逐个写入 agent.json
    for meta in AGENTS:
        agent_folder = os.path.join(AGENTS_DIR, meta["name"])  # 保持带空格的目录名
        ensure_dir(agent_folder)

        agent_json = build_agent_json(meta)
        write_json(os.path.join(agent_folder, "agent.json"), agent_json)
        roster.append(agent_json)
        print(f"  ✅ {meta['name']}: agent.json written")

    # 生成 sprite.json（前端枚举每个角色的 texture）
    sprite_manifest = {
        "framesPerDir": 3,
        "dirs": ["down", "left", "right", "up"],
        "agents": [
            {
                "name": meta["name"],
                "texture": f"assets/{ASSETS_PACK}/agents/{meta['name']}/texture.png"
            }
            for meta in AGENTS
        ]
    }
    write_json(os.path.join(AGENTS_DIR, "sprite.json"), sprite_manifest)
    print("  🎨 sprite.json written")

    # （可选）写出合并 roster，方便后端一次性加载
    write_json(ROSTER_OUT, roster)
    print(f"  📦 roster written: {ROSTER_OUT}")

    print("\nAll done. Put/verify your portrait.png & texture.png under each folder, e.g.:")
    print("  /Users/chenjiajun/Downloads/GenerativeAgentsCN-main/generative_agents/frontend/static/assets/Columbia/agents/Ava Lee/portrait.png")
    print("  /Users/chenjiajun/Downloads/GenerativeAgentsCN-main/generative_agents/frontend/static/assets/Columbia/agents/Ava Lee/texture.png")

if __name__ == "__main__":
    main()
