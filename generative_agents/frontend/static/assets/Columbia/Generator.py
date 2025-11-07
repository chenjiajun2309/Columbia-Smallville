from PIL import Image
import os

BASE_DIR = "/Users/chenjiajun/Downloads/GenerativeAgentsCN-main/generative_agents/frontend/static/assets/Columbia/agents"

def convert_texture_to_portrait(agent_dir):
    texture_path = os.path.join(agent_dir, "texture.png")
    portrait_path = os.path.join(agent_dir, "portrait.png")

    if not os.path.exists(texture_path):
        print(f"⚠️  Skipped (no texture): {agent_dir}")
        return

    sheet = Image.open(texture_path).convert("RGBA")
    frame_w = sheet.width // 13
    frame_h = sheet.height // 21

    col, row = 0, 2
    offset = frame_h * 0.11     # move down 10% of frame height

    x0 = col * frame_w
    y0 = row * frame_h / 3 + offset
    x1 = x0 + frame_w
    y1 = y0 + frame_h / 3 + offset
    frame = sheet.crop((x0, y0, x1, y1))

    upper_crop = frame.crop((0, 0, frame_w, int(frame_h * 0.8)))

    scale = 4
    portrait = upper_crop.resize(
        (frame_w * scale, int(frame_h * 0.8 * scale)),
        Image.Resampling.NEAREST
    )

    portrait.save(portrait_path)
    print(f"✅ Saved portrait for {os.path.basename(agent_dir)}")

for name in os.listdir(BASE_DIR):
    agent_path = os.path.join(BASE_DIR, name)
    if os.path.isdir(agent_path):
        convert_texture_to_portrait(agent_path)

print("🎉 All portraits generated successfully!")
