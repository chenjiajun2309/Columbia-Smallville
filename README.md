# Columbia Smallville
> LLM‑driven multi‑agent campus simulator for memory, planning, action, and interaction — with optional RL policy heads and discriminator rewards.

![python](https://img.shields.io/badge/Python-3.10+-blue)
![fastapi](https://img.shields.io/badge/FastAPI-API-green)
![react](https://img.shields.io/badge/React-Frontend-informational)
![pgvector](https://img.shields.io/badge/pgvector-embeddings-critical)
![license](https://img.shields.io/badge/License-MIT-black)

**Columbia Smallville（哥大校园小镇）**是一个以大学校园为背景的多智能体模拟平台。每个智能体由大语言模型（如 GPT‑4/兼容 API）驱动，具备**记忆、反思、规划、行动与社交交互**能力；可选地挂载**小模型策略头**（LoRA/BC/Offline RL/Online RL）来学习特定行为模式，并提供 **GAIL/DRAIL 风格的判别器奖励**接口。

本项目面向三类目标：
1) 研究：涌现式校园社会、信息扩散、规范遵循；  
2) 强化学习：从大模型“高层心智”切到“低层可训策略”；  
3) 应用：可复用的多智能体环境（PettingZoo/Gymnasium 适配）。

---

## ✨ 主要特性

- **Campus World**：2D 校园地图（教学楼/图书馆/食堂/宿舍/广场等），离散事件调度，地点容量与排队机制。
- **LLM Agent Stack**：三层记忆（短期/情节/社交）+ 反思合成；ReAct 决策循环；可检索 Top‑k 记忆（相关性/重要性/时近性）。
- **Tool 调用**：`move / talk / attend / buy / study / post / schedule / search` 等动作，带执行器校验与失败反馈。
- **数据与可视化**：PostgreSQL + pgvector 存储记忆与轨迹；事件流、社交图、地点热力、日记与每日总结面板。
- **可训练模块（可选）**：
  - **行为克隆/LoRA**：用小模型学“准点、排队、礼貌、自习”等微行为；
  - **Offline RL**（IQL/CQL 等）与 **Online RL**（PPO/SAC 等）；
  - **判别器奖励**：GAIL 标准 `log(D) - log(1-D)`；可切换 **DRAIL 扩散判别器**以获得更平滑的奖励面。
- **标准化接口**：PettingZoo/Gymnasium 适配，方便与现成 RL 库对接。

---

## 🧭 架构一览

