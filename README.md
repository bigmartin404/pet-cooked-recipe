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

## 文件结构

```
pet-cooked-recipe/
├── SKILL.md                              # 主技能文件（含完整工作流指令）
├── README.md                             # 本文件
├── references/                           # 参考资料库
│   ├── nrc_nutrient_requirements.md      # NRC 营养需求标准
│   ├── aafco_fediaf_nutrient_profiles.md # AAFCO + FEDIAF 营养标准
│   ├── cooking_loss_factors.json         # USDA 烹饪保留因子
│   ├── ancestral_diet_recipe_guide.md    # 祖先饮食六步配方法 + 食谱模板
│   ├── homemade_recipe_templates.md      # 在线自制食谱模板库
│   ├── dog_longevity_food_guide.md       # 犬类长寿饮食研究（871KB）
│   ├── ancestral_diet_comparison_guide.md # 祖先饮食对比研究
│   ├── clinical_nutrition_guide.md       # 临床兽医营养学指南
│   ├── common_ingredients_nutrients.json  # 预建食材营养数据库(32种)
│   ├── fooddata_central_nutrient_db.md   # USDA FoodData Central 速查
│   ├── chinese_food_composition.md        # 中国食物成分表
│   ├── cfct_pet_food_tables.md            # 中国食材宠物营养对比表
│   ├── supplement_dosage_reference.md    # 补充剂剂量参考
│   ├── aspca_toxic_foods.md              # ASPCA 有毒食物清单
│   ├── pet_food_database_reference.md     # 宠物食品数据库参考
│   └── clinical_ch*.txt                  # 临床营养学扩展原始数据
```

## 营养标准来源

| 标准     | 说明                                             |
| ------ | ---------------------------------------------- |
| NRC    | National Research Council 营养需求       |
| AAFCO  | Association of American Feed Control Officials |
| FEDIAF | European Pet Food Industry Federation          |

## 配方方法论

- 祖先饮食六步配方法（选肉→平衡脂肪→钙磷→蔬菜矿物质→复查脂肪→复查维D/E）
- 模拟祖先饮食：蛋白质49%、脂肪44%、碳水6%（按热量）
- 三种食材比例方案：祖先饮食型 / 长寿均衡型 / 传统临床型

## 安装方法


## 🤖 AI 一键安装

**直接复制以下指令发送给你的 AI（Claude Code / Cursor / Windsurf 等）：**

> **安装指令：**
> ```
> 请帮我安装这个 GitHub 上的 AI Skill：
> https://github.com/bigmartin404/pet-cooked-recipe
> 
> 要求：
> 1. 识别我当前使用的 IDE 或 AI 环境（Claude Code / Cursor 等）。
> 2. 自动将 Skill 克隆到对应的技能目录（全局或项目级）。
> 3. 确保 references 文件夹和 SKILL.md 结构完整，能被正确加载。
> 4. 安装完成后告诉我如何使用该 Skill。

### 🚀 或者，直接运行这条命令（AI 会自动接管）：
git clone https://github.com/bigmartin404/pet-cooked-recipe.git /tmp/pet-cooked-recipe && code /tmp/pet-cooked-recipe

## 使用方法
1. 自动匹配调用 当你的对话内容匹配到技能描述中的关键词时，AI 会自动加载该技能。触发关键词包括：

宠物自制食物 / 自制狗粮 / 熟自制
生成宠物食谱 / 狗狗食谱
计算营养配比 / 宠物营养
NRC / AAFCO / FEDIAF 标准
例如直接说："帮我为25斤的成犬生成一周的蒸煮食谱" 即可触发。

2. 斜杠命令显式调用 在对话中输入 /pet-cooked-recipe 直接调用技能。

## 版本

- v3.0: 全面重构交互流程，新增品种/疾病/过敏/中兽医方案，采用六步配方法
- v1.0: 犬版初始版本
- v1.1 (计划): 添加猫版支持

## License

MIT
