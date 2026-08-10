# pet-cooked-recipe
一个帮助宠物主人创建犬猫熟自制食谱的skill
# Pet Cooked Recipe Formulator | 宠物熟自制配方生成器

为犬类生成符合 NRC / AAFCO / FEDIAF 标准的熟自制食谱。

## 功能

- 基于狗的体重、年龄、活动量、品种生成定制化食谱
- 支持三种配方模式：系统自动生成 / 自选食材 / 预算生成
- 支持蒸、煮、低温慢煮三种烹饪方式
- 营养分析对照 NRC / AAFCO / FEDIAF 三大标准
- 基于 USDA 烹饪保留因子精确计算营养损失
- 补充剂双方案（补充剂 + 天然食物替代）
- 每日喂食量指南
- 食材替换建议
- 安全检查（ASPCA 有毒食物清单）
- 中兽医药食同源方案（含风险提示）

## 营养标准来源

| 标准  | 说明  |
| --- | --- |
| NRC | National Research Council 营养需求 |
| AAFCO | Association of American Feed Control Officials |
| FEDIAF | European Pet Food Industry Federation |

## 配方方法论

- 祖先饮食六步配方法（选肉→平衡脂肪→钙磷→蔬菜矿物质→复查脂肪→复查维D/E）
- 模拟祖先饮食：蛋白质49%、脂肪44%、碳水6%（按热量）
- 三种食材比例方案：祖先饮食型 / 长寿均衡型 / 传统临床型

## 使用方法

方法1.
一键安装，把下面的命令复制给你的Ai
请帮我安装以下技能，git clone https://github.com/bigmartin404/pet-cooked-recipe.git ~/.claude/skills/pet-cooked-recipe

方法2
将整个 `pet-cooked-recipe/` 目录放置在 ai 工具 的 `/skills/` 目录下即可自动加载。

## 调用方式：
1. 自动匹配调用 当你的对话内容匹配到技能描述中的关键词时，AI 会自动加载该技能。
2. 触发关键词包括：
宠物自制食物 / 自制狗粮 / 熟自制
生成宠物食谱 / 狗狗食谱
计算营养配比 / 宠物营养
NRC / AAFCO / FEDIAF 标准
例如直接说："帮我为25斤的成犬生成一周的蒸煮食谱" 即可触发。

2. 斜杠命令显式调用 在对话中输入 /pet-cooked-recipe 直接调用技能。

## 版本
- v2.1 (计划): 添加猫版支持
- v2.0: 全面重构交互流程，新增品种/疾病/过敏/中兽医方案，采用六步配方法
- v1.0: 犬版初始版本

## License

MIT
