# FoodData Central 营养数据库参考

> 来源：USDA FoodData Central (2025-12-18 版)
> 完整数据库：`E:\1-Projects\FEED\FoodData_Central_csv_2025-12-18.zip`
> 本地CSV子集：项目 `fooddata_temp/` 目录
> 用途：为 SKILL 提供食材营养素精确查询

---

## 一、数据库概述

FoodData Central 是 USDA 维护的美国权威食物成分数据库，包含：

| 表名 | 记录数 | 内容 |
|------|--------|------|
| `food.csv` | 2,021,090 | 所有食物条目 |
| `food_nutrient.csv` | 26,235,946 | 食物-营养素对应值 |
| `branded_food.csv` | 1,947,155 | 品牌食品数据 |
| `foundation_food.csv` | 265 | 基础食物（最权威） |
| `sr_legacy_food.csv` | 7,793 | USDA SR 遗留数据 |
| `survey_fndds_food.csv` | 5,624 | 膳食调查用食物 |
| `nutrient.csv` | 477 | 营养素定义表 |
| `food_category.csv` | 28 | 食物分类码 |
| `retention_factor.csv` | 270 | 烹饪保留因子（USDA Release 6） |
| `food_portion.csv` | 47,837 | 食物份量转换 |

**数据优先级**：Foundation Food > SR Legacy > Survey FNDDS > Branded Food

---

## 二、宠物配方关键营养素 ID 速查

### 2.1 宏量营养素

| 营养素 ID | 名称 | 单位 | 营养素编号 |
|-----------|------|------|-----------|
| 1003 | Protein (蛋白质) | G | 203 |
| 1004 | Total lipid (fat) (总脂肪) | G | 204 |
| 1005 | Carbohydrate, by difference (碳水化合物) | G | 205 |
| 1008 | Energy (能量) | KCAL | 208 |
| 1079 | Fiber, total dietary (总膳食纤维) | G | 291 |
| 1051 | Water (水分) | G | 255 |
| 1007 | Ash (灰分) | G | 207 |

### 2.2 矿物质

| 营养素 ID | 名称 | 单位 | 营养素编号 |
|-----------|------|------|-----------|
| 1087 | Calcium, Ca (钙) | MG | 301 |
| 1091 | Phosphorus, P (磷) | MG | 305 |
| 1092 | Potassium, K (钾) | MG | 306 |
| 1093 | Sodium, Na (钠) | MG | 307 |
| 1090 | Magnesium, Mg (镁) | MG | 304 |
| 1089 | Iron, Fe (铁) | MG | 303 |
| 1095 | Zinc, Zn (锌) | MG | 309 |
| 1098 | Copper, Cu (铜) | MG | 312 |
| 1101 | Manganese, Mn (锰) | MG | 315 |
| 1100 | Iodine, I (碘) | UG | 314 |
| 1103 | Selenium, Se (硒) | UG | 317 |

### 2.3 维生素

| 营养素 ID | 名称 | 单位 | 营养素编号 |
|-----------|------|------|-----------|
| 1104 | Vitamin A, IU | IU | 318 |
| 1109 | Vitamin E (alpha-tocopherol) | MG | 323 |
| 1110 | Vitamin D (D2 + D3), IU | IU | 324 |
| 1185 | Vitamin K (phylloquinone) | UG | 430 |
| 1162 | Vitamin C, total ascorbic acid | MG | 401 |
| 1165 | Thiamin (B1) | MG | 404 |
| 1166 | Riboflavin (B2) | MG | 405 |
| 1167 | Niacin (B3) | MG | 406 |
| 1170 | Pantothenic acid (B5) | MG | 410 |
| 1175 | Vitamin B-6 | MG | 415 |
| 1177 | Folate, total (B9) | UG | 417 |
| 1178 | Vitamin B-12 | UG | 418 |
| 1180 | Choline, total (胆碱) | MG | 421 |

### 2.4 必需氨基酸（均以 G 为单位）

| 营养素 ID | 名称 | 营养素编号 |
|-----------|------|-----------|
| 1210 | Tryptophan (色氨酸) | 501 |
| 1211 | Threonine (苏氨酸) | 502 |
| 1212 | Isoleucine (异亮氨酸) | 503 |
| 1213 | Leucine (亮氨酸) | 504 |
| 1214 | Lysine (赖氨酸) | 505 |
| 1215 | Methionine (蛋氨酸) | 506 |
| 1216 | Cystine (胱氨酸) | 507 |
| 1217 | Phenylalanine (苯丙氨酸) | 508 |
| 1218 | Tyrosine (酪氨酸) | 509 |
| 1219 | Valine (缬氨酸) | 510 |
| 1220 | Arginine (精氨酸) | 511 |
| 1221 | Histidine (组氨酸) | 512 |
| 1234 | Taurine (牛磺酸) | 529 |

### 2.5 脂肪酸（均以 G 为单位，胆固醇除外）

| 营养素 ID | 名称 | 营养素编号 |
|-----------|------|-----------|
| 1253 | Cholesterol (胆固醇) | MG, 601 |
| 1258 | Fatty acids, total saturated (总饱和) | 606 |
| 1292 | Fatty acids, total monounsaturated (总单不饱和) | 645 |
| 1293 | Fatty acids, total polyunsaturated (总多不饱和) | 646 |
| 1269 | PUFA 18:2 (亚油酸, LA, omega-6) | 618 |
| 1270 | PUFA 18:3 (亚麻酸, ALA, omega-3) | 619 |
| 1271 | PUFA 20:4 (花生四烯酸, AA) | 620 |
| 1278 | PUFA 20:5 n-3 (EPA) | 629 |
| 1272 | PUFA 22:6 n-3 (DHA) | 621 |
| 1280 | PUFA 22:5 n-3 (DPA) | 631 |
| 1268 | MUFA 18:1 (油酸) | 617 |
| 1316 | PUFA 18:2 n-6 c,c (LA, 特定异构体) | 675 |
| 1404 | PUFA 18:3 n-3 c,c,c (ALA, 特定异构体) | 851 |

---

## 三、食物分类码

| 分类码 | 分类名称 | 宠物配方相关性 |
|--------|----------|---------------|
| 0100 | Dairy and Egg Products | 鸡蛋、酸奶 |
| 0200 | Spices and Herbs | 草本调料 |
| 0400 | Fats and Oils | 鱼油、亚麻籽油 |
| 0500 | Poultry Products | 鸡肉、火鸡、鸭肉 |
| 0700 | Sausages and Luncheon Meats | 不建议使用 |
| 0900 | Fruits and Fruit Juices | 南瓜、蓝莓、苹果 |
| 1000 | Pork Products | 猪肉 |
| 1100 | Vegetables and Vegetable Products | 蔬菜类 |
| 1200 | Nut and Seed Products | 亚麻籽、葵花籽 |
| 1300 | Beef Products | 牛肉 |
| 1500 | Finfish and Shellfish Products | 沙丁鱼、三文鱼、牡蛎 |
| 1600 | Legumes and Legume Products | 豆类 |
| 1700 | Lamb, Veal, and Game Products | 羊肉、鹿肉 |
| 2000 | Cereal Grains and Pasta | 燕麦、糙米 |

---

## 四、如何使用 FoodData Central 查询食材营养

### 4.1 在线 API 查询

```
# 按名称搜索食材
https://api.nal.usda.gov/fdc/v1/foods/search?api_key=YOUR_KEY&query=beef+liver&dataType=Foundation

# 按 FDC ID 查询具体食物
https://api.nal.usda.gov/fdc/v1/food/FDC_ID?api_key=YOUR_KEY
```

**免 API Key 方式**：直接访问 https://fooddata.central.usda.gov/ 搜索

### 4.2 本地 CSV 查询

使用已下载的 CSV 文件查询：

1. 在 `food.csv` 中按名称搜索食物，获取 FDC ID
2. 在 `food_nutrient.csv` 中按 FDC ID 查询所有营养素值
3. 在 `nutrient.csv` 中对照营养素名称和单位

### 4.3 常用食材 FDC ID 参考

> 以下为 Foundation Food 类型的常用食材 ID（最权威数据源）

| 食材 | 英文名 | FDC ID | 备注 |
|------|--------|--------|------|
| 牛肉（瘦，90%瘦肉） | Beef, ground, 90% lean | 748967 | 祖先饮食配方标准用肉 |
| 牛肝 | Beef, liver | 748947 | 维生素A丰富 |
| 牛心 | Beef, heart | 748944 | 牛磺酸来源 |
| 牛肾 | Beef, kidney | 748945 | |
| 牛脾 | Beef, spleen | 748960 | 铁丰富 |
| 鸡肉（带皮） | Chicken, whole with skin | 748967 | |
| 鸡肝 | Chicken, liver | 748946 | 铜较低 |
| 鸡心 | Chicken, heart | 748943 | 牛磺酸来源 |
| 猪肉（瘦） | Pork, fresh, lean | 748967 | |
| 羊肉 | Lamb, fresh | 748967 | |
| 鸡蛋 | Egg, whole, raw | 748967 | |
| 沙丁鱼 | Sardines, canned | 748967 | omega-3 + 维D |
| 三文鱼 | Salmon, raw | 748967 | omega-3 |
| 牡蛎 | Oysters, raw | 748967 | 锌 + 铜 |
| 菠菜 | Spinach, raw | 748967 | 锰 + 铁 |
| 西兰花 | Broccoli, raw | 748967 | |
| 红薯 | Sweet potato, raw | 748967 | |
| 南瓜 | Pumpkin, raw | 748967 | |
| 燕麦 | Oats | 748967 | 锰来源 |

> 注意：FDC ID 需要通过 API 或 CSV 确认，上表仅为参考方向。实际使用时应通过 `food.csv` 查询精确 FDC ID。

---

## 五、USDA 烹饪保留因子（Retention Factors）

`retention_factor.csv` 包含 270 条记录，来自 USDA Table of Nutrient Retention Factors Release 6 (2007)。

### 5.1 保留因子编码

食物按以下编码分类：
- 1: CHEESE (奶酪)
- 5: EGGS (鸡蛋)
- 8: OATMEAL/CEREAL (燕麦/谷物)
- 9: FRUITS (水果)
- 16: LEGUMES (豆类)
- 20: FLOUR/MEAL/RICE/PASTA (面粉/米饭/通心粉)

烹饪方式编码示例：
- BAKED (烘烤)
- BROILED (炙烤)
- COOKED W/LIQUID (带液体煮)
- STEAMED (蒸)
- BOILED, DRAINED (煮后沥干)
- BOILED, WATER USED (煮后留汤)
- REHEATED (复热)

### 5.2 与 cooking_loss_factors.json 的关系

`cooking_loss_factors.json` 模块已将 USDA Release 6 的保留因子转化为蒸/煮/低温慢煮三档系数，并添加了：
- loss_factor（= 1/retention_factor，配料需乘的补偿倍率）
- 留汤/倒汤区分（煮档）
- 食材特定覆盖（鱼禽牛磺酸、肝脏VA、鸡蛋biotin）
- 自动告警规则

**SKILL 使用时**：优先调用 `cooking_loss_factors.json`，该模块已整合 USDA 保留因子数据。

---

## 六、营养素来源分类

| 来源码 | 说明 | 可信度 |
|--------|------|--------|
| 1 | Analytical or derived from analytical (分析数据) | 最高 |
| 4 | Calculated or imputed (计算或估算) | 中 |
| 5 | Manufacturer label claim (厂家标签) | 中 |
| 6 | Aggregated data (汇总数据) | 中 |
| 7 | Assumed zero (假定为零) | 低 |
| 9 | Calculated by manufacturer (厂家计算) | 中 |
| 12 | Manufacturer's analytical, partial (厂家分析，部分文档) | 中 |
| 13 | Analytical from literature, partial (文献分析，部分文档) | 中 |

---

## 七、SKILL 集成指南

### 查询单个食材营养步骤

1. **确定食材**：用户指定或 AI 选择的食材（如"牛肉 90%瘦肉"）
2. **查询 FDC ID**：在 `food.csv` 中搜索 `description` 字段，筛选 `data_type = 'foundation_food'` 或 `'sr_legacy_food'`
3. **获取营养值**：在 `food_nutrient.csv` 中按 FDC ID 查询，对照 `nutrient.csv` 获取营养素名称和单位
4. **应用烹饪因子**：根据用户选择的烹饪方式，从 `cooking_loss_factors.json` 获取 retention_factor
5. **计算最终值**：`实际营养值 = 原始营养值 × retention_factor`

### 批量查询脚本示例（PowerShell）

```powershell
# 查询牛肉（90%瘦肉）的所有营养素
$fdcId = 748967  # 需要先确认实际 FDC ID
# 如果有完整数据库 CSV：
# Import-Csv food_nutrient.csv | Where-Object { $_.fdc_id -eq $fdcId }
```

---

## 八、与中国食物成分表对照

当食材为中国本地采购时，优先使用《中国食物成分表》第6版数据：
- 第一册（2018）：谷物、蔬菜、水果
- 第二册（2019）：肉类、蛋类、乳类、鱼类

中美数据库差异：
- 中国食物成分表使用每100g可食部
- FoodData Central 同时提供 per 100g 和 per serving
- 部分中国特有食材（如猪脾、鸭肉）在中国食物成分表中更完整
- FoodData Central 的脂肪酸分析更详细（区分 omega-3/6 各链长）

**推荐策略**：以 FoodData Central 为基础（数据量大、脂肪酸详细），中国特有食材补充中国食物成分表数据。
