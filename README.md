# Pet Cooked Recipe Formulator | 宠物熟自制配方生成器

为犬和猫生成符合 NRC / AAFCO / FEDIAF 标准的熟自制食谱。

## 功能

- 支持犬和猫双物种
- 基于体重、年龄、活动量、品种生成定制化食谱
- 支持三种配方模式：系统自动生成 / 自选食材 / 预算生成
- 支持蒸、煮、低温慢煮三种烹饪方式
- 营养分析对照 NRC / AAFCO / FEDIAF 三大标准
- 基于 USDA 烹饪保留因子精确计算营养损失
- 补充剂双方案（补充剂 + 天然食物替代）
- 每日喂食量指南
- 食材替换建议
- 安全检查（有毒食物清单）
- 中兽医药食同源方案（含风险提示）
- 品种特殊饮食需求（20+犬品种 + 15+猫品种）
- 疾病饮食调整（肾病、糖尿病、胰腺炎、心脏病、皮肤问题等）

## 文件结构

```
pet-cooked-recipe/
├── SKILL.md                          # 主技能文件（含完整工作流指令）
├── README.md                         # 本文件
├── scripts/                          # 计算脚本
│   └── recipe_calculator.py                 # 配方计算器（营养/烹饪损失/钙磷/补充剂）
├── profiles/                         # 宠物档案（每只宠物一个JSON，持久化）
│   ├── dog_template.json                    # 犬档案模板
│   ├── cat_template.json                    # 猫档案模板
│   └── sample_dog_8.9kg.json                # 示例档案
├── references/                       # 参考资料库
│   ├── shared/                       # 犬猫共用
│   │   ├── cooking_loss_factors.json        # USDA 烹饪保留因子
│   │   ├── multi_route_nutrition_kb.md       # 多路线营养知识库（五条路线+证据等级）
│   │   ├── common_ingredients_nutrients.json # 预建食材营养数据库(42种+V3扩展)
│   │   ├── fooddata_central_nutrient_db.md  # FoodData Central 速查
│   │   ├── chinese_food_composition.md       # 中国食物成分表
│   │   ├── cfct_pet_food_tables.md           # 中国食材对比表
│   │   ├── clinical_nutrition_guide.md       # 临床兽医营养学指南
│   │   ├── pet_food_database_reference.md    # 宠物食品数据库参考
│   │   ├── ancestral_diet_comparison_guide.md # 祖先饮食对比研究
│   │   └── clinical_ch*.txt                  # 临床营养学扩展原始数据
│   ├── dog/                          # 犬专用
│   │   ├── nrc_requirements.md              # NRC 犬营养需求标准
│   │   ├── aafco_fediaf_profiles.md         # AAFCO + FEDIAF 犬标准
│   │   ├── supplement_dosage.md             # 犬补充剂剂量参考
│   │   ├── toxic_foods.md                   # 犬有毒食物清单
│   │   ├── ancestral_diet_guide.md          # 祖先饮食六步配方法
│   │   ├── longevity_food_guide.md          # 犬类长寿饮食研究
│   │   ├── recipe_templates.md              # 犬食谱模板库
│   │   └── breed_specific_diets.md          # 犬品种特殊饮食
│   └── cat/                          # 猫专用
│       ├── nrc_requirements.md              # NRC 猫营养需求标准
│       ├── aafco_fediaf_profiles.md         # FEDIAF 猫标准 + AAFCO说明
│       ├── supplement_dosage.md             # 猫补充剂剂量参考
│       ├── toxic_foods.md                   # 猫有毒食物清单
│       └── breed_specific_diets.md          # 猫品种特殊饮食
```

## 营养标准来源

| 标准 | 说明 |
|------|------|
| NRC | National Research Council 营养需求（最严格，优先采用） |
| AAFCO | Association of American Feed Control Officials |
| FEDIAF | European Pet Food Industry Federation |

## 配方方法论

- **六步工作流**：确认物种 → 询问基本情况 → 询问喂养目标 → 选择配方路线 → 确认食材与补剂 → 按六步法生成配方
- **六步配方法**（生成配方的计算管线）：选瘦肉与内脏 → 平衡脂肪（油脂作为求解变量，二分法解算到路线脂肪目标）→ 确保钙磷 → 添加蔬菜与矿物质 → 复查脂肪 → 复查维生素D和E
- **五条可选路线**（比例随路线不同，不可混用）：

| 路线 | key | 证据等级 | 特点 |
|------|-----|---------|------|
| 临床营养学 | `clinical` | A | 营养需要优先于固定比例，碳水可到约50%湿重 |
| BARF | `barf` | C | 生物适宜，原始为生食；熟制须取消熟骨并重算 |
| PMR/猎物模型 | `pmr` | C | 复刻整只猎物，原版通常不用植物 |
| 永远的爱犬 | `forever_dog` | B | 高动物原料＋植物多样性 |
| 生食改良熟制 | `modified_cooked` | C(结构)/B(个体配方) | 保留高肉结构，全熟后重建补充体系 |

- 跨路线硬约束：肝脏 5%–10%、鱼单次 5%–10%、贝类 0%–5%、蛋 0%–10%、蔬菜犬 5%–20%/猫 0%–10%
- 猫特有营养素：牛磺酸、花生四烯酸、预成型维生素A、烟酸（必须独立核算，不能只靠"含肉"）

## 使用方法

将整个 `pet-cooked-recipe/` 目录放置在 skills 目录下即可自动加载。

调用方式：在对话中描述你的需求，如"帮我为5kg的成猫生成一周的蒸煮食谱"。

## 版本

- v5.4: 生成管线按六步法重构，脂肪目标按路线分设，清理6个旧模板，统一为五条路线体系
- v5.3: 接入多路线比例体系，新增多路线营养知识库，Step 3 重构为"选路线"，脚本新增10个路线模板+`organ_split`
- v5.2: 工作流最后一步改为"按六步配方法生成配方"，脚本定位为六步法的计算引擎
- v5.1: 修正长寿均衡型比例（依《永生狗》原始食谱逐项反推）
- v5.0: 新增计算脚本 `recipe_calculator.py` 与宠物档案系统 `profiles/`
- v4.2: 食材营养数据库升级——USDA Foundation Food 2026 + 中国食物成分表 v3 双源对照
- v4.1: 修复"计算脚本缺失"误报，JSON接口术语改为计算指南术语
- v4.0: 猫狗双版本，目录重构 shared/dog/cat，修复所有已知问题
- v3.0: 犬版全面重构
- v2.0: 整合全部资料，三标准对照
- v1.0: 犬版初始版本

## License

MIT
