# 宠物档案系统

每只宠物一个 JSON 档案，持久化存储，避免每次重复询问。

## 文件命名规范

```
<名字>_<物种>.json
```

示例：
- `旺财_dog.json`
- `咪咪_cat.json`

## 档案结构

### 犬 (dog_template.json)

```json
{
  "schema_version": "1.0",
  "profile_type": "dog",
  "basic_info": {
    "name": "",
    "breed": "",
    "age_years": 0,
    "age_months": 0,
    "sex": "",
    "neutered": false,
    "body_weight_kg": 0,
    "ideal_weight_kg": 0,
    "body_condition_score": 0,
    "activity_level": "moderate",
    "activity_hours_per_day": 0,
    "activity_description": ""
  },
  "feeding_goal": {
    "goal": "maintain",
    "weight_change_rate_kg_per_week": 0,
    "target_calorie_factor": 1.0
  },
  "lifestage": "adult",
  "medical_history": {
    "chronic_conditions": [],
    "allergies": [],
    "food_intolerances": [],
    "medications": [],
    "special_dietary_needs": ""
  },
  "available_ingredients": {
    "primary_proteins": [],
    "secondary_proteins": [],
    "organ_meats": [],
    "fish": [],
    "eggs": [],
    "vegetables": [],
    "grains_carbs": [],
    "oils_fats": [],
    "bones": []
  },
  "current_supplements": {
    "calcium_source": "",
    "iodine_source": "",
    "vitamin_e": "",
    "vitamin_d": "",
    "zinc": "",
    "copper": "",
    "selenium": "",
    "other": []
  },
  "feeding_preferences": {
    "cooking_method": "boil",
    "meals_per_day": 2,
    "include_bones": false,
    "include_fiber": true,
    "ratio_template": "modified_cooked"
  },
  "calculation_history": []
}
```

### 猫 (cat_template.json)

结构类似，额外增加牛磺酸、花生四烯酸、预成型VA等猫特有字段。

## 活动量等级

### 犬

| 等级 | key | 描述 | MER系数 |
|------|-----|------|---------|
| 久坐 | sedentary | <30min/天 | 1.2 |
| 轻度 | low | 30-60min/天 | 1.4 |
| 适度 | moderate | 1-1.5h/天，散步为主 | 1.6 |
| 中高 | moderate_high | 1.5-2h/天，含跑跳 | 1.8 |
| 高 | high | 2-3h/天，大量运动 | 2.0 |
| 极高 | very_high | 3h+/天 | 2.5 |

### 猫

| 等级 | key | 描述 | MER系数 |
|------|-----|------|---------|
| 室内/绝育 | indoor_neutered | 大部分室内 | 1.3 |
| 一般 | moderate | 室内外活动 | 1.5 |
| 活跃/未绝育 | active_intact | 户外活动量大 | 1.7 |

## 喂养目标

| 目标 | key | 热量调整 |
|------|-----|---------|
| 维持 | maintain | × 1.0 |
| 适度增重 | gain | × 1.15 |
| 快速增重 | gain_fast | × 1.25 |
| 健康减重 | lose | × 0.8 |
| 快速减重 | lose_fast | × 0.7 |

## 食材键名速查

数据库中常用食材的键名（用于 `available_ingredients` 字段）：

### 肉类
- `pork_ground_raw` — 猪肉末
- `pork_leg_skin_on` — 猪肉(腿,带皮) v3
- `duck_breast_skinless` — 鸭胸脯肉(去皮) v3
- `chicken_breast_raw` — 鸡胸肉
- `chicken_thigh_raw` — 鸡腿肉
- `beef_ground_raw` — 牛肉末
- `salmon_atlantic_farmed_raw` — 三文鱼(大西洋养殖)
- `mussel_greenlip_raw` — 青口贝(绿唇贻贝)

### 内脏
- `pork_heart_raw` — 猪心
- `chicken_heart_raw` — 鸡心
- `beef_heart_raw` — 牛心
- `pork_liver_raw` — 猪肝
- `chicken_liver_raw` — 鸡肝
- `pork_kidney_raw` — 猪肾
- `beef_kidney_raw` — 牛肾

### 蔬菜
- `broccoli_raw` — 西兰花
- `carrot_raw` — 胡萝卜
- `spinach_raw` — 菠菜
- `sweet_potato_raw` — 红薯
- `pumpkin_raw` — 南瓜

### 谷物/碳水
- `brown_rice_raw` — 糙米
- `wheat_berry` — 小麦仁
- `oats_dry` — 燕麦(干)
- `quinoa_raw` — 藜麦(生)

### 油脂
- `coconut_oil` — 椰子油
- `flaxseed_oil` — 亚麻籽油
- `sunflower_oil` — 葵花籽油
- `olive_oil` — 橄榄油

### 蛋类
- `egg_whole_raw` — 全蛋(生)

## 配方路线（`feeding_preferences.ratio_template`）

五条路线犬猫通用；比例随路线不同，**不可跨路线混用**。详见 `references/shared/multi_route_nutrition_kb.md` 与 SKILL.md Step 3。

| 路线 key | 证据等级 | 一句话 |
|---------|---------|--------|
| `clinical` | A | 营养需要优先于固定比例，允许高熟碳水 |
| `barf` | C | 生物适宜，原始为生食；熟制须转换 |
| `pmr` | C | 复刻整只猎物，原版通常不用植物 |
| `forever_dog` | B | 高动物原料＋植物多样性 |
| `modified_cooked` | C/B | 保留高肉结构，全熟后重建补充体系 |

> 旧模板 `longevity_balanced` / `longevity_carb` / `ancestral_carnivore` / `low_fat` / `ancestral_omnivore` / `balanced` 已移除。档案里若仍写着旧值，脚本会自动回退到该物种的第一条路线，并应在下次对话中请用户重新选择。
