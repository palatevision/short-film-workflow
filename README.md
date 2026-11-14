# 制作人班skill 影视合集｜审阅版 V2

2026-11-14。包含制作人班总控 0.11.2 与 14 个专业影视模块，共 15 个 Skill。

## 解压后开始

1. 解压整个 ZIP，保留原目录结构。包内 `skills/` 下每个模块都有独立的 `SKILL.md` 和随附资源。
2. 将解压目录交给助手，并让它先读本页与[制作人班总控](skills/producer-class-skill/SKILL.md)。例如说「请读这个目录的 README 和制作人班总控，再按其中的分镜模块帮我拆分镜。」
3. 做分镜时打开[短剧分镜](skills/short-drama-storyboard/SKILL.md)。总控也可直接读到这个同层模块。若要长期安装到支持目录型 Skill 的工具，请按该工具的安装方式放入整份模块目录，包括 `references/` 等随附资源。

其他模块见下表，技术检查见[审阅指引](REVIEW_GUIDE.md)。

| Skill | 主要交付 |
| --- | --- |
| [producer-class-skill](skills/producer-class-skill/SKILL.md) | 当前阶段总控、摄影/声音、提示词与课程方法 |
| [short-film-development](skills/short-film-development/SKILL.md) | 短片点子、人物/冲突、简介和结构 |
| [screenplay-and-scene-writing](skills/screenplay-and-scene-writing/SKILL.md) | 场次、对白、动作和节奏 |
| [style-cinematography-director](skills/style-cinematography-director/SKILL.md) | 画风、摄影、灯光和调度 |
| [character-location-prop-bible](skills/character-location-prop-bible/SKILL.md) | 人物/场景/道具及连续性 |
| [prompt-iteration-and-diagnostics](skills/prompt-iteration-and-diagnostics/SKILL.md) | 失败诊断和有依据的迭代 |
| [model-adaptation](skills/model-adaptation/SKILL.md) | 面向具体模型的格式/控制适配 |
| [short-drama](skills/short-drama/SKILL.md) | 中文短剧跨阶段入口与现有项目管理 |
| [short-drama-write](skills/short-drama-write/SKILL.md) | 中文单集剧本写作/修订 |
| [short-drama-assets](skills/short-drama-assets/SKILL.md) | 人物/地点/道具和状态拆解 |
| [short-drama-image-prompts](skills/short-drama-image-prompts/SKILL.md) | 角色图/场景图/风格帧提示词 |
| [short-drama-storyboard](skills/short-drama-storyboard/SKILL.md) | 分镜职责、动作/视线/轴线及关键帧 |
| [short-drama-video-prompts](skills/short-drama-video-prompts/SKILL.md) | 镜头动作、表演/运镜与声音提示词 |
| [short-drama-review](skills/short-drama-review/SKILL.md) | 剧本、资产、分镜/提示词/媒体审查 |
| [short-drama-edit](skills/short-drama-edit/SKILL.md) | 素材取舍、剪辑、声音/字幕与交付 |

故事→完整分镜草案→逐镜讨论→按需资产/提示词→制作/样片→剪辑反馈；已有项目从当前阶段继续。合适专业模块可独立主导，不全量加载，也不并行维护竞争稿。风格、摄影、声音按需贯穿。

完整视频词按[统一规范](skills/producer-class-skill/references/prompt-delivery.md)：时长、画幅、风格、参考图绑定与初态、动作、景别、摄影参数、声音、必要约束。挂图/镜号/预计剪辑取用在外，最后动作包含落幅。图片资产按[固定生成规范](skills/producer-class-skill/references/asset-prompts.md)，不套视频时长/声音字段。

目录：`skills/`是完整Skill资源；`AGENTS.md`是本合集协作约定；`THIRD_PARTY_NOTICES.md`及每模块许可保留第三方来源；`VALIDATION.json`记录实际验证范围；`MANIFEST.json`是逐文件SHA-256清单。可运行`python3 tools/check_bundle.py`核对解压后完整性，脚本不联网、不生成媒体。

本包可在解压目录内读取全部模块。若需要生成、对口型、混音或渲染，使用接收方环境已配置的工具和账号。

第三方许可见[声明](THIRD_PARTY_NOTICES.md)。课程原件、个人工作区日志、手机配置/缓存和历史项目档案未放入审阅包；可执行方法与必要示例保留。
