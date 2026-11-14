# 技术审阅指引

## 先看什么

1. `skills/producer-class-skill/SKILL.md`：触发、输入/缺口、按阶段路由、交付与返修；不依赖整段课堂笔记才能工作。
2. `references/cinematography-language.md`、`asset-prompts.md`：摄影判断与固定资产基底已经成为直接执行规则，具体示例另按需读。
3. `references/prompt-delivery.md`与`assets/`：最终格式与可复制例子；`scripts/assemble_video_prompt.py`只做可选单镜字段装配。
4. 从总控的「故事已有，准备分镜」一行打开[短剧分镜](skills/short-drama-storyboard/SKILL.md)，再打开其[镜头方法参考](skills/short-drama-storyboard/references/shot-craft.md)。这条路径可直接从解压目录读取。

## 建议关注的行为

| 试用输入 | 应观察到的结果 |
| --- | --- |
| “已有故事，先拆完整分镜” | 先交可通读的分镜草案，关键镜头带方案；不先批量生资产 |
| “画面要像从街对面窥视” | 转成距离/视野、焦点/遮挡与稳定性选择，保住具体信息；不只贴风格名 |
| “做写实人物资产，已有身份图” | 真实绑定、固定身份/可变造型、材质/视图/光色及完整固定基底；无视频时长/音效 |
| “这镜有点不对劲” | 用实际输出与上下镜定位首要缺口，修受影响部分；缺媒体时只给初判与最小资料缺口 |
| “给我可直接用的视频词” | 挂图顺序在外，九标签完整；风格每镜完整，动作末段含落幅，摄影/声音相容 |

这些是审阅用情境，不是已经用独立代理/真实模型评测通过的结论。

## 可运行与能力边界

`python3 tools/check_bundle.py`检查清单哈希、缺件/多件与符号链接，不执行Skill中的工具。可选单镜装配示例：

```sh
python3 skills/producer-class-skill/scripts/assemble_video_prompt.py --input skills/producer-class-skill/assets/video-prompt-example.json --output /tmp/film-shot-review.md --report /tmp/film-shot-review.json
```

输出文件需要尚不存在；命令只装配文本，媒体效果仍需人工/实际模型验证。schema 5仅接受project文本，主结构与原有效project输入保持，撤销旧的命名预设入口。日常用户不需要填JSON。

14个专业模块保留原来源字节和许可；其中模型资料标注的旧版本不保证当前入口规格。媒体生成/云服务需实际工具与授权，后期渲染依赖ffmpeg/ffprobe及特定模板的运行环境。本包没有替接收端安装它们或接入账户。若模块不可用，说明可完成部分，不伪称调用成功。

`VALIDATION.json`说明本轮真实检查；文件/语法/文本走查不等于安装发现、接口、生成、混制、口型或成片效果验收。方法来源与课堂案例见[课程证据](skills/producer-class-skill/references/course-evidence.md)。
