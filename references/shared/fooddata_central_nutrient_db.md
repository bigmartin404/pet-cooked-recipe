# 食材营养数据库参考

> 来源：
> 1. USDA FoodData Central 2025-12 CSV（foundation_food + sr_legacy_food，最完整）
> 2. 中国食物成分表第6版 v3 JSON (2026-08-25 版)
> 3. USDA FoodData Central Foundation Food JSON (2026-04-30 版)
> 预建数据库：`common_ingredients_nutrients.json`（42种常用食材，双源对照）
> 用途：为 SKILL 提供食材营养素精确查询

---

## 一、数据库概述

SKILL 使用三个权威数据源，预建为统一格式的 `common_ingredients_nutrients.json`：

| 优先级 | 数据源 | 数量 | 特点 | 适用场景 |
|--------|--------|------|------|---------|
| **1（最高）** | **USDA FoodData Central 2025 CSV** (foundation + sr_legacy) | 8,229 种食物 | 数据最完整，47-51种营养素/食材，含完整氨基酸/脂肪酸谱 | 西式食材、需要完整氨基酸/脂肪酸分析 |
| **2** | **中国食物成分表 v3** | 1,677 种食物 | 中国本地食材，覆盖全面 | 中式食材、中国特有食材、双源对照验证 |
| **3** | **USDA Foundation Food 2026 JSON** | 363 种食物 | USDA最新Foundation级数据 | 补充2025 CSV中缺失的食材 |

**数据优先级**：USDA FoodData Central 2025 CSV > 中国食物成分表 v3 > USDA Foundation Food 2026 JSON

**预建数据库**：`common_ingredients_nutrients.json` 已精选 42 种宠物熟自制最常用食材，其中 38 种带双源对照（可交叉验证数据准确性），每食材含 47-51 种营养素。

---

## 二、预建数据库格式

`common_ingredients_nutrients.json` 结构：

```json
{
  "食材key": {
    "zh_name": "中文名",
    "category": "分类（畜肉/禽肉/内脏/鱼类/蔬菜/...）",
    "fdc_id": 12345,              // FDC ID（仅FDC数据源有）
    "description": "英文描述",      // FDC数据源为英文名，v3数据源为中文名
    "data_source": "数据来源说明",
    "food_code": "12345",          // v3食物编码（仅v3数据源有）
    "nutrients_per_100g": {         // 主营养数据（每100g可食部）
      "营养素ID": {
        "name": "营养素中文名",
        "amount": 数值,
        "unit": "单位"
      }
    },
    "v3_nutrients_per_100g": {      // v3对照数据（双源食材才有）
      "v3_字段名": {
        "name": "营养素中文名",
        "amount": 数值,
        "unit": "单位"
      }
    }
  }
}
```

**营养素ID说明**：
- 数字ID（如 `"1003"`, `"1008"`）：FDC 营养素编号，对应 USDA FoodData Central 数据
- `v3_` 前缀（如 `"v3_protein"`, `"v3_Ca"`）：中国食物成分表 v3 字段，仅在 v3 对照数据中出现

---

## 三、预建食材清单（42种）

### 3.1 畜肉类（5种）

| Key | 中文名 | 数据源 | 营养素数 |
|-----|--------|--------|---------|
| beef_lean_raw | 牛肉(瘦) | FDC2025 + v3 | 51 |
| beef_ground_90lean_raw | 牛肉末(90%瘦) | FDC2025 + v3 | 51 |
| pork_loin_raw | 猪里脊 | FDC2025 + v3 | 51 |
| pork_ground_raw | 猪肉末 | FDC2025 + v3 | 51 |
| lamb_ground_raw | 羊肉末 | FDC2025 + v3 | 51 |

### 3.2 内脏类（10种）

| Key | 中文名 | 数据源 | 营养素数 |
|-----|--------|--------|---------|
| beef_liver_raw | 牛肝 | FDC2025 + v3 | 51 |
| beef_heart_raw | 牛心 | FDC2025 + v3 | 47 |
| beef_kidney_raw | 牛肾 | FDC2025 + v3 | 47 |
| beef_spleen_raw | 牛脾 | FDC2025 | 47 |
| pork_liver_raw | 猪肝 | FDC2025 + v3 | 47 |
| pork_heart_raw | 猪心 | FDC2025 + v3 | 48 |
| pork_kidney_raw | 猪肾 | FDC2025 + v3 | 47 |
| chicken_liver_raw | 鸡肝 | FDC2025 + v3 | 51 |
| chicken_heart_raw | 鸡心 | FDC2025 + v3 | 47 |
| lamb_liver_raw | 羊肝 | FDC2025 + v3 | 48 |

### 3.3 禽肉类（5种）

| Key | 中文名 | 数据源 | 营养素数 |
|-----|--------|--------|---------|
| chicken_breast_skinless_raw | 鸡胸肉(去皮) | FDC2025 + v3 | 51 |
| chicken_thigh_skinless_raw | 鸡腿肉(去皮) | FDC2025 + v3 | 51 |
| chicken_thigh_withskin_raw | 鸡腿肉(带皮) | FDC2025 + v3 | 51 |
| chicken_ground_raw | 鸡肉末 | FDC2025 + v3 | 50 |
| duck_meat_raw | 鸭肉 | FDC2025 + v3 | 51 |

### 3.4 鱼类/贝类（5种）

| Key | 中文名 | 数据源 | 营养素数 |
|-----|--------|--------|---------|
| salmon_atlantic_farmed_raw | 三文鱼(大西洋养殖) | FDC2025 + v3 | 51 |
| salmon_sockeye_wild_raw | 三文鱼(红鲑野生) | FDC2025 + v3 | 51 |
| tuna_bluefin_raw | 金枪鱼(蓝鳍) | FDC2025 + v3 | 51 |
| sardine_raw | 沙丁鱼 | FDC2025 + v3 | 51 |
| mussel_greenlip_raw | 青口贝(绿唇贻贝) | FDC2025 + v3 | 51 |

### 3.5 蛋类（3种）

| Key | 中文名 | 数据源 | 营养素数 |
|-----|--------|--------|---------|
| egg_whole_raw | 全蛋(生) | FDC2025 + v3 | 51 |
| egg_yolk_raw | 蛋黄(生) | FDC2025 + v3 | 51 |
| egg_white_raw | 蛋清(生) | FDC2025 + v3 | 51 |

### 3.6 蔬菜/薯类（6种）

| Key | 中文名 | 数据源 | 营养素数 |
|-----|--------|--------|---------|
| broccoli_raw | 西兰花(生) | FDC2025 + v3 | 51 |
| spinach_raw | 菠菜(生) | FDC2025 + v3 | 51 |
| carrot_raw | 胡萝卜(生) | FDC2025 + v3 | 51 |
| pumpkin_raw | 南瓜(生) | FDC2025 + v3 | 51 |
| zucchini_raw | 西葫芦(生) | FDC2025 + v3 | 51 |
| sweet_potato_raw | 红薯(生) | FDC2025 + v3 | 51 |

### 3.7 谷物类（4种）

| Key | 中文名 | 数据源 | 营养素数 |
|-----|--------|--------|---------|
| oats_dry | 燕麦(干) | FDC2025 + v3 | 51 |
| brown_rice_raw | 糙米(生) | FDC2025 + v3 | 51 |
| quinoa_raw | 藜麦(生) | FDC2025 + v3 | 47 |
| white_rice_raw | 白米(生) | FDC2025 + v3 | 51 |

### 3.8 油脂类（4种）

| Key | 中文名 | 数据源 | 营养素数 |
|-----|--------|--------|---------|
| fish_oil_salmon | 三文鱼油 | FDC2025 | 34 |
| sunflower_oil | 葵花籽油 | FDC2025 | 50 |
| coconut_oil | 椰子油 | FDC2025 + v3 | 51 |
| flaxseed_oil | 亚麻籽油 | FDC2025 | 37 |

---

## 四、常用营养素FDC ID速查

### 4.1 基础营养

| ID | 名称 | 单位 |
|----|------|------|
| 1003 | 蛋白质 | g |
| 1004 | 脂肪 | g |
| 1005 | 碳水化合物 | g |
| 1008 | 能量 | kcal |
| 1051 | 水分 | g |
| 1079 | 膳食纤维 | g |
| 1253 | 胆固醇 | mg |

### 4.2 矿物质

| ID | 名称 | 单位 |
|----|------|------|
| 1087 | 钙 | mg |
| 1089 | 铁 | mg |
| 1090 | 镁 | mg |
| 1091 | 磷 | mg |
| 1092 | 钾 | mg |
| 1093 | 钠 | mg |
| 1095 | 锌 | mg |
| 1098 | 铜 | mg |
| 1100 | 碘 | µg |
| 1103 | 硒 | µg |
| 1101 | 锰 | mg |

### 4.3 维生素

| ID | 名称 | 单位 |
|----|------|------|
| 1106 | 维生素A(RAE) | µg |
| 1114 | 维生素D | µg |
| 1109 | 维生素E(a-生育酚) | mg |
| 1185 | 维生素K(叶绿醌) | µg |
| 1165 | 维生素B1(硫胺素) | mg |
| 1166 | 维生素B2(核黄素) | mg |
| 1167 | 烟酸(B3) | mg |
| 1175 | 维生素B6 | mg |
| 1177 | 叶酸(B9) | µg |
| 1178 | 维生素B12 | µg |
| 1180 | 胆碱 | mg |
| 1176 | 生物素(B7) | µg |
| 1170 | 泛酸(B5) | mg |

### 4.4 氨基酸

| ID | 名称 | 单位 |
|----|------|------|
| 1220 | 精氨酸 | g |
| 1214 | 赖氨酸 | g |
| 1215 | 蛋氨酸 | g |
| 1216 | 胱氨酸 | g |
| 1217 | 苯丙氨酸 | g |
| 1218 | 酪氨酸 | g |
| 1219 | 苏氨酸 | g |
| 1221 | 色氨酸 | g |
| 1222 | 缬氨酸 | g |
| 1212 | 亮氨酸 | g |
| 1213 | 异亮氨酸 | g |
| 1211 | 组氨酸 | g |
| 1226 | 牛磺酸 | mg |

### 4.5 脂肪酸

| ID | 名称 | 单位 |
|----|------|------|
| 1258 | 总饱和脂肪酸 | g |
| 1292 | 总单不饱和脂肪酸 | g |
| 1293 | 总多不饱和脂肪酸 | g |
| 1269 | 亚油酸(LA, n-6) | g |
| 1270 | a-亚麻酸(ALA, n-3) | g |
| 1278 | EPA (n-3) | g |
| 1272 | DHA (n-3) | g |
| 1280 | 花生四烯酸(AA, n-6) | g |

---

## 五、v3 中国食材字段对照

v3 数据字段（`v3_` 前缀）：

| 字段 | 中文名 | 单位 |
|------|--------|------|
| v3_protein | 蛋白质 | g |
| v3_fat | 脂肪 | g |
| v3_CHO | 碳水化合物 | g |
| v3_energyKCal | 能量 | kcal |
| v3_water | 水分 | g |
| v3_dietaryFiber | 膳食纤维 | g |
| v3_cholesterol | 胆固醇 | mg |
| v3_Ca | 钙 | mg |
| v3_Fe | 铁 | mg |
| v3_Mg | 镁 | mg |
| v3_P | 磷 | mg |
| v3_K | 钾 | mg |
| v3_Na | 钠 | mg |
| v3_Zn | 锌 | mg |
| v3_Cu | 铜 | mg |
| v3_Se | 硒 | µg |
| v3_Mn | 锰 | mg |
| v3_vitaminA | 维生素A | µg |
| v3_thiamin | 维生素B1 | mg |
| v3_riboflavin | 维生素B2 | mg |
| v3_niacin | 烟酸 | mg |
| v3_vitaminC | 维生素C | mg |
| v3_vitaminETotal | 维生素E(总) | mg |

---

## 六、食材营养查询方法

> **重要提示**：日常配方**优先使用预建数据库** `common_ingredients_nutrients.json`（已包含42种常用食材，47-51种营养素/食材）。仅当预建库中没有用户指定的特殊食材时，才参考本节方法手动查询原始数据。AI直接读取数据表进行计算，无需运行任何脚本。

### 查询步骤

1. **确定食材**：用户指定或 AI 选择的食材
2. **查预建库**：先在 `common_ingredients_nutrients.json` 中查找
3. **查 FoodData Central 2025 CSV**：预建库没有时，优先在 2025 CSV 的 foundation_food 和 sr_legacy_food 中搜索（数据最完整）
4. **查 v3 中国食材**：2025 CSV 没有的中国食材，在 v3 JSON 中搜索 `foodName` 字段
5. **查 Foundation Food 2026 JSON**：以上都没有时，作为补充来源
6. **应用烹饪因子**：根据烹饪方式，从 `cooking_loss_factors.json` 获取 retention_factor
7. **计算最终值**：`烹饪后值 = 原始值 × retention_factor`

---

## 七、三源数据对照

三个数据源差异：

| 对比项 | USDA FDC 2025 CSV | 中国食物成分表 v3 | USDA Foundation Food 2026 JSON |
|--------|-------------------|-------------------|-------------------------------|
| 食材数量 | 8,229 种 (foundation+sr_legacy) | 1,677 种 | 363 种 |
| 营养素/食材 | 47-51 种（精选后） | 24 种 | 18-24 种（Foundation新条目） |
| 氨基酸 | 完整（13+种） | 无单独氨基酸 | 部分有（新旧条目差异大） |
| 脂肪酸 | 完整（8+种分类） | 无单独脂肪酸 | 部分有 |
| 文件格式 | CSV（需解压480MB zip） | JSON（直接读取） | JSON（直接读取） |
| 优先级 | 最高 | 第二 | 第三 |

**推荐策略**：
- 西式/通用食材 → 优先用 2025 CSV（氨基酸/脂肪酸最完整）
- 中国特有食材 → 用 v3 数据（基础营养完整）
- 双源对照食材 → 两者对比验证，取 FDC 为主、v3 为辅
- 2026 Foundation Food JSON → 仅作为补充（新条目数据不如2025完整）
