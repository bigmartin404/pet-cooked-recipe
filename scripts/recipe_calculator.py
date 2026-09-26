#!/usr/bin/env python3
"""
宠物熟自制配方计算器 v2.0
========================
用途：根据宠物档案和可用食材，精确计算营养需求，生成完整配方
输入：宠物档案JSON + 食材选择
输出：完整配方结果JSON（含营养分析、补充剂建议、喂养指南、六步执行记录）

依赖：
  - references/shared/common_ingredients_nutrients.json  (食材营养数据库)
  - references/shared/cooking_loss_factors.json           (烹饪损失因子)

使用方法：
  python recipe_calculator.py --profile <profile.json> [--ratio-template <route>] [--cooking-method boil] [--target-kcal 0]

路线：clinical / barf / pmr / forever_dog / modified_cooked

作者：pet-cooked-recipe SKILL v5.4
"""

import json
import os
import sys
import argparse
from pathlib import Path

# ============================================================
# 路径配置
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DB_PATH = SKILL_DIR / "references" / "shared" / "common_ingredients_nutrients.json"
COOKING_LOSS_PATH = SKILL_DIR / "references" / "shared" / "cooking_loss_factors.json"

# ============================================================
# 营养素ID映射 (FDC nutrient ID → 内部字段名)
# ============================================================
NUTRIENT_MAP = {
    # 宏量营养素
    "1003": "protein",       # 蛋白质
    "1004": "fat",           # 总脂肪
    "1005": "CHO",           # 碳水化合物
    "1008": "energyKCal",    # 能量(kcal)
    "1051": "water",         # 水分
    "1079": "dietaryFiber",  # 膳食纤维
    "1253": "cholesterol",   # 胆固醇
    # 矿物质
    "1087": "Ca",            # 钙
    "1089": "Fe",            # 铁
    "1090": "Mg",            # 镁
    "1091": "P",             # 磷
    "1092": "K",             # 钾
    "1093": "Na",            # 钠
    "1095": "Zn",            # 锌
    "1098": "Cu",            # 铜
    "1103": "Se",            # 硒
    "1101": "Mn",            # 锰
    # 维生素
    "1106": "vitaminA",      # 维生素A (RAE µg)
    "1114": "vitaminD",      # 维生素D (µg)
    "1109": "vitaminE",      # 维生素E (mg α-TE)
    "1185": "vitaminK",      # 维生素K
    "1165": "thiamin",       # 维生素B1
    "1166": "riboflavin",    # 维生素B2
    "1167": "niacin",        # 维生素B3
    "1175": "vitaminB6",     # 维生素B6
    "1177": "folate",        # 叶酸
    "1178": "vitaminB12",    # 维生素B12
    "1180": "choline",       # 胆碱
    "1168": "vitaminC",      # 维生素C
    # 脂肪酸
    "1258": "sat_fat",       # 饱和脂肪
    "1292": "mono_fat",      # 单不饱和脂肪
    "1293": "poly_fat",      # 多不饱和脂肪
    "1269": "linoleic_acid", # 亚油酸(ω6)
    "1270": "alpha_linolenic_acid",  # α-亚麻酸(ω3)
    "1278": "EPA",           # 二十碳五烯酸
    "1272": "DHA",           # 二十二碳六烯酸
    "1280": "arachidonic_acid",  # 花生四烯酸
}

# 反向映射
FIELD_TO_NUTRIENT_ID = {v: k for k, v in NUTRIENT_MAP.items()}

# ============================================================
# 中国食物成分表 v3 补充数据 (数据库中缺失的食材)
# ============================================================
V3_EXTRA_DATA = {
    "pork_leg_skin_on": {
        "zh_name": "猪肉(腿,带皮)", "category": "畜肉",
        "data_source": "中国食物成分表v3 (code 081111)",
        "protein": 17.9, "fat": 12.8, "CHO": 0.8, "energyKCal": 190,
        "Ca": 6, "P": 185, "Fe": 0.9, "Zn": 2.18, "Se": 13.40,
        "Cu": 0.14, "Mn": 0.04, "vitaminA": 3, "thiamin": 0.53,
        "riboflavin": 0.24, "niacin": 4.90, "vitaminE": 0.30,
        "K": 295, "Na": 63.0, "Mg": 25, "cholesterol": 79,
        "dietaryFiber": 0, "water": 67.6, "folate": 0,
        "vitaminB12": 0, "choline": 65, "vitaminD": 0.4,
        "vitaminC": 0, "vitaminB6": 0.35, "vitaminK": 0,
        "sat_fat": 4.5, "mono_fat": 5.8, "poly_fat": 1.8,
        "linoleic_acid": 1.4, "alpha_linolenic_acid": 0.12,
        "EPA": 0, "DHA": 0, "arachidonic_acid": 0.05,
    },
    "duck_breast_skinless": {
        "zh_name": "鸭胸脯肉(去皮)", "category": "禽肉",
        "data_source": "中国食物成分表v3 (code 092104)",
        "protein": 15.0, "fat": 1.5, "CHO": 4.0, "energyKCal": 90,
        "Ca": 6, "P": 86, "Fe": 4.1, "Zn": 1.17, "Se": 12.62,
        "Cu": 0.27, "Mn": 0.01, "vitaminA": 0, "thiamin": 0.01,
        "riboflavin": 0.07, "niacin": 4.20, "vitaminE": 1.98,
        "K": 126, "Na": 60.2, "Mg": 24, "cholesterol": 121,
        "dietaryFiber": 0, "water": 78.6, "folate": 0,
        "vitaminB12": 0.3, "choline": 20, "vitaminD": 0.1,
        "vitaminC": 0, "vitaminB6": 0.3, "vitaminK": 0,
        "sat_fat": 0.5, "mono_fat": 0.6, "poly_fat": 0.2,
        "linoleic_acid": 0.15, "alpha_linolenic_acid": 0.02,
        "EPA": 0, "DHA": 0, "arachidonic_acid": 0.02,
    },
    "wheat_berry": {
        "zh_name": "小麦仁(硬红小麦)", "category": "谷物",
        "data_source": "USDA SR Legacy 近似值",
        "protein": 16.4, "fat": 1.9, "CHO": 68.0, "energyKCal": 325,
        "Ca": 34, "P": 350, "Fe": 3.6, "Zn": 3.3, "Se": 70.7,
        "Cu": 0.5, "Mn": 3.6, "Mg": 125, "K": 340, "Na": 2,
        "dietaryFiber": 12.2, "water": 11.0, "niacin": 5.5,
        "thiamin": 0.45, "riboflavin": 0.16, "vitaminB6": 0.35,
        "folate": 38, "choline": 30, "vitaminE": 1.0,
        "vitaminK": 1.9, "vitaminA": 0, "vitaminD": 0,
        "vitaminB12": 0, "vitaminC": 0, "cholesterol": 0,
        "sat_fat": 0.3, "mono_fat": 0.2, "poly_fat": 0.9,
        "linoleic_acid": 0.7, "alpha_linolenic_acid": 0.05,
        "EPA": 0, "DHA": 0, "arachidonic_acid": 0,
    },
    "oyster_raw": {
        "zh_name": "生蚝(太平洋牡蛎)", "category": "贝类",
        "data_source": "USDA FoodData Central 近似值",
        "protein": 6.7, "fat": 1.4, "CHO": 3.0, "energyKCal": 56,
        "Ca": 7, "P": 86, "Fe": 3.8, "Zn": 39.3, "Se": 77.0,
        "Cu": 4.4, "Mn": 0.1, "Mg": 12, "K": 108, "Na": 120,
        "dietaryFiber": 0, "water": 84.8, "niacin": 1.4,
        "thiamin": 0.05, "riboflavin": 0.13, "vitaminB6": 0.08,
        "folate": 16, "choline": 45, "vitaminE": 0.3,
        "vitaminK": 0, "vitaminA": 0, "vitaminD": 0,
        "vitaminB12": 16.0, "vitaminC": 0, "cholesterol": 48,
        "sat_fat": 0.3, "mono_fat": 0.2, "poly_fat": 0.4,
        "linoleic_acid": 0.1, "alpha_linolenic_acid": 0.03,
        "EPA": 0.15, "DHA": 0.2, "arachidonic_acid": 0.02,
    },
}

# ============================================================
# 数据库数据修正 (已知错误)
# ============================================================
DB_CORRECTIONS = {
    "egg_whole_raw": {
        "Na": 142,  # 原数据3663mg错误, 正确值约142mg/100g
    },
    "pork_heart_raw": {
        "choline": 62,  # 原数据0, 修正为USDA值
    },
    "pork_liver_raw": {
        "choline": 290,  # 原数据0, 修正为USDA值
    },
    "chicken_heart_raw": {
        "choline": 60,  # 原数据0
    },
    "pork_kidney_raw": {
        "choline": 100,  # 原数据0
    },
    "beef_heart_raw": {
        "choline": 62,  # 原数据0
    },
}

# ============================================================
# NRC 营养需求标准 (每1000kcal, 成年维持)
# ============================================================
NRC_DOG_ADULT = {
    "protein": (25.0, "g", "RA"),
    "fat": (13.8, "g", "RA"),
    "Ca": (1000.0, "mg", "RA"),
    "P": (750.0, "mg", "RA"),
    "Mg": (150.0, "mg", "RA"),
    "K": (1000.0, "mg", "RA"),
    "Na": (200.0, "mg", "RA"),
    "Fe": (7.5, "mg", "RA"),
    "Cu": (1.5, "mg", "RA"),
    "Zn": (15.0, "mg", "RA"),
    "Mn": (1.2, "mg", "RA"),
    "Se": (87.5, "µg", "RA"),
    "vitaminA": (379.0, "µg", "RA"),
    "vitaminD": (3.4, "µg", "RA"),
    "vitaminE": (7.5, "mg", "RA"),  # 需加PUFA补偿
    "thiamin": (0.56, "mg", "RA"),
    "riboflavin": (1.3, "mg", "RA"),
    "niacin": (4.25, "mg", "RA"),
    "vitaminB6": (0.375, "mg", "RA"),
    "folate": (67.5, "µg", "RA"),
    "vitaminB12": (8.75, "µg", "RA"),
    "choline": (425.0, "mg", "RA"),
    "linoleic_acid": (2.8, "g", "RA"),
    "alpha_linolenic_acid": (0.11, "g", "RA"),
    "EPA": (0.055, "g", "RA"),
    "DHA": (0.055, "g", "RA"),
}

NRC_CAT_ADULT = {
    "protein": (40.0, "g", "RA"),
    "fat": (22.5, "g", "RA"),
    "Ca": (720.0, "mg", "RA"),
    "P": (600.0, "mg", "RA"),
    "Mg": (100.0, "mg", "RA"),
    "K": (1000.0, "mg", "RA"),
    "Na": (200.0, "mg", "RA"),
    "Fe": (10.0, "mg", "RA"),
    "Cu": (1.2, "mg", "RA"),
    "Zn": (18.5, "mg", "RA"),
    "Mn": (1.2, "mg", "RA"),
    "Se": (75.0, "µg", "RA"),
    "vitaminA": (200.0, "µg", "RA"),
    "vitaminD": (1.4, "µg", "RA"),
    "vitaminE": (10.0, "mg", "RA"),
    "thiamin": (0.65, "mg", "RA"),
    "riboflavin": (0.85, "mg", "RA"),
    "niacin": (4.0, "mg", "RA"),
    "vitaminB6": (0.4, "mg", "RA"),
    "folate": (67.5, "µg", "RA"),
    "vitaminB12": (7.5, "µg", "RA"),
    "choline": (425.0, "mg", "RA"),
    "taurine": (100.0, "mg", "RA"),
    "linoleic_acid": (3.0, "g", "RA"),
    "alpha_linolenic_acid": (0.1, "g", "RA"),
    "arachidonic_acid": (0.05, "g", "RA"),
    "EPA": (0.05, "g", "RA"),
    "DHA": (0.05, "g", "RA"),
}

# ============================================================
# 配方模板 (百分比组成)
# ============================================================
RATIO_TEMPLATES = {
    "dog": {
        # ===== 五条路线模板（依据 references/shared/multi_route_nutrition_kb.md）=====
        # 各类目取该路线 1000g 示例中"食物部分"归一化到 100%；补充体系由脚本单独核算
        "clinical": {
            "name": "临床营养学路线（犬）",
            "evidence": "A",
            "categories": {
                "muscle_meat": 53,
                "organs": 13,
                "vegetables": 16,
                "grains_carbs": 16,
                "oils_fats": 2,
            },
            "organ_split": {"liver": 0.46, "heart": 0.32, "other": 0.22},
            "description": "营养需要优先于固定比例，允许中等偏高熟碳水。源自教材成年犬低脂配方示例（鸡肉500/鸡肝60/鸡心胗70/蔬菜150/熟米150/油20）",
        },
        "barf": {
            "name": "BARF路线（犬·熟制转换）",
            "evidence": "C",
            "categories": {
                "muscle_meat": 53,
                "organs": 12,
                "fish": 6,
                "vegetables": 18,
                "grains_carbs": 11,
            },
            "organ_split": {"liver": 0.50, "heart": 0.30, "other": 0.20},
            "description": "原始为生食；熟制必须取消熟骨并重算钙/碘/牛磺酸/维E。源自示例（肉450/肝50/其他内脏50/鱼50/蔬菜150/熟燕麦米100）",
        },
        "pmr": {
            "name": "PMR猎物模型路线（犬·熟制转换）",
            "evidence": "C",
            "categories": {
                "muscle_meat": 68,
                "organs": 11,
                "fish": 5,
                "vegetables": 11,
                "grains_carbs": 5,
            },
            "organ_split": {"liver": 0.55, "heart": 0.27, "other": 0.18},
            "description": "复刻整只猎物，原版通常不加植物；此处保留少量蔬菜作纤维。源自示例（肉650/肝50/肾50/鱼50/南瓜100/熟米50）",
        },
        "forever_dog": {
            "name": "永远的爱犬路线（犬）",
            "evidence": "B",
            "categories": {
                "muscle_meat": 56,
                "organs": 14,
                "fish": 5,
                "vegetables": 20,
                "grains_carbs": 5,
            },
            "organ_split": {"liver": 0.57, "heart": 0.26, "other": 0.17},
            "description": "高动物原料＋植物多样性。官方鸡肉全阶段食谱：纯肉53.33%/肝7.68%/其他内脏5.33%/鱼5.33%/贝类4.80%/蔬菜21.66%，贝类已并入鱼类口径",
        },
        "modified_cooked": {
            "name": "生食改良熟制路线（犬）",
            "evidence": "C",
            "categories": {
                "muscle_meat": 56,
                "organs": 13,
                "fish": 5,
                "vegetables": 19,
                "grains_carbs": 5,
                "oils_fats": 2,
            },
            "organ_split": {"liver": 0.54, "heart": 0.28, "other": 0.18},
            "description": "保留高肉结构与轮换，全熟后重建补充体系。源自肉类版示例（肉550/肝70/心胗60/鱼50/菜180/熟燕麦米50/油20）",
        },
    },
    "cat": {
        # ===== 五条路线模板（猫）=====
        "clinical": {
            "name": "临床营养学路线（猫）",
            "evidence": "A",
            "categories": {
                "muscle_meat": 64,
                "organs": 17,
                "vegetables": 12,
                "grains_carbs": 6,
                "oils_fats": 1,
            },
            "organ_split": {"liver": 0.53, "heart": 0.28, "other": 0.19},
            "description": "高肉、熟碳水最小化，营养需要优先于固定比例。源自教材猫配方示例（鸡腿肉550/鸡肝80/鸡心70/西葫芦南瓜100/熟米50/鱼油10）",
        },
        "barf": {
            "name": "BARF路线（猫·熟制转换）",
            "evidence": "C",
            "categories": {
                "muscle_meat": 75,
                "organs": 10,
                "fish": 5,
                "vegetables": 5,
                "grains_carbs": 5,
            },
            "organ_split": {"liver": 0.50, "heart": 0.30, "other": 0.20},
            "description": "猫BARF更偏动物来源，植物0–5%。熟制须取消熟骨并重算钙/牛磺酸/维E/碘",
        },
        "pmr": {
            "name": "PMR猎物模型路线（猫·熟制转换）",
            "evidence": "C",
            "categories": {
                "muscle_meat": 75,
                "organs": 10,
                "fish": 5,
                "vegetables": 5,
                "grains_carbs": 5,
            },
            "organ_split": {"liver": 0.50, "heart": 0.30, "other": 0.20},
            "description": "猫PMR肌肉肉79–84%、生可食骨6%，此处按熟制转换（熟骨禁用）",
        },
        "forever_dog": {
            "name": "永远的爱犬路线（猫·改编）",
            "evidence": "B",
            "categories": {
                "muscle_meat": 66,
                "organs": 15,
                "fish": 5,
                "vegetables": 11,
                "grains_carbs": 3,
            },
            "organ_split": {"liver": 0.53, "heart": 0.28, "other": 0.19},
            "description": "借用永远的爱犬的多样性结构，但按猫的高肉需求上调肌肉肉、下调蔬菜",
        },
        "modified_cooked": {
            "name": "生食改良熟制路线（猫）",
            "evidence": "C",
            "categories": {
                "muscle_meat": 66,
                "organs": 15,
                "fish": 5,
                "vegetables": 8,
                "grains_carbs": 5,
                "oils_fats": 1,
            },
            "organ_split": {"liver": 0.53, "heart": 0.28, "other": 0.19},
            "description": "源自猫肉类版示例（肉650/肝80/心胗70/鱼50/菜80/淀粉40/油10）",
        },
    },
}

# ============================================================
# 各路线脂肪目标 (g/1000kcal) —— 六步法第2步的求解目标
# ============================================================
# 推导方式：把《猫狗熟自制多路线营养知识库》中每条路线的 1000g 示例，用本库食材折算，
# 得到"该路线自身结构所产生的脂肪/1000kcal"，作为该路线的脂肪目标。
# 交叉验证：永远的爱犬路线折算得 48.9，而知识库给出的官方 ME 数据为脂肪 48.21% ME = 53.6，
# 偏差约 9%（来自用本库鸡肉碎/三文鱼代替官方原料），说明折算方法可用。
# ⚠ 已知不一致（照实记录、不擅自修正）：知识库 §9.2 给出猫的脂肪设计区间 35%–50% ME
#   （= 38.9–55.6 g/1000kcal），但知识库自己的猫示例折算只有 33.6–40.2，低于其自述下限。
#   此处采用折算值，并在输出中提示该偏差。
ROUTE_FAT_TARGET = {
    "dog": {
        "clinical": 28.1,
        "barf": 29.8,
        "pmr": 30.9,
        "forever_dog": 48.9,
        "modified_cooked": 39.5,
    },
    "cat": {
        "clinical": 37.7,
        "barf": 33.6,
        "pmr": 33.6,
        "forever_dog": 36.1,
        "modified_cooked": 40.2,
    },
}

# ============================================================
# 烹饪损失因子 (煮-留汤)
# ============================================================
COOKING_LOSS_BOIL_RETAIN_BROTH = {
    "protein": 0.95, "fat": 0.95, "CHO": 0.95, "dietaryFiber": 0.95,
    "cholesterol": 0.95, "Ca": 0.95, "P": 0.95, "Fe": 0.90,
    "Zn": 0.90, "Cu": 0.90, "Mn": 0.90, "Se": 0.90, "Mg": 0.90,
    "K": 0.85, "Na": 0.95, "vitaminA": 0.85, "vitaminE": 0.85,
    "vitaminD": 0.90, "vitaminK": 0.90, "thiamin": 0.75,
    "riboflavin": 0.85, "niacin": 0.85, "vitaminB6": 0.75,
    "folate": 0.70, "vitaminB12": 0.80, "choline": 0.85,
    "vitaminC": 0.75, "sat_fat": 0.95, "mono_fat": 0.95,
    "poly_fat": 0.95, "linoleic_acid": 0.95,
    "alpha_linolenic_acid": 0.95, "EPA": 0.95, "DHA": 0.95,
    "arachidonic_acid": 0.95, "water": 0.90,
}

# ============================================================
# 食材分类 (用于配方模板自动分配)
# ============================================================
INGREDIENT_CATEGORIES = {
    "muscle_meat": [
        "pork_ground_raw", "pork_leg_skin_on", "pork_loin",
        "duck_breast_skinless", "duck_meat_raw",
        "chicken_breast_raw", "chicken_thigh_raw",
        "beef_ground_raw", "beef_chuck_raw",
        "turkey_breast_raw", "lamb_leg_raw",
        "salmon_atlantic_farmed_raw", "sardine_raw",
        "mussel_greenlip_raw", "oyster_raw",
    ],
    "organs": [
        "pork_heart_raw", "chicken_heart_raw", "beef_heart_raw",
        "pork_liver_raw", "chicken_liver_raw", "beef_liver_raw",
        "pork_kidney_raw", "beef_kidney_raw",
    ],
    "fish": [
        "salmon_atlantic_farmed_raw", "sardine_raw",
        "mackerel_raw", "herring_raw",
    ],
    "eggs": ["egg_whole_raw", "egg_yolk_raw"],
    "vegetables": [
        "broccoli_raw", "carrot_raw", "spinach_raw",
        "sweet_potato_raw", "pumpkin_raw", "green_beans_raw",
        "kale_raw", "zucchini_raw", "celery_raw",
    ],
    "grains_carbs": [
        "brown_rice_raw", "white_rice_raw", "wheat_berry",
        "oats_dry", "quinoa_raw", "sweet_potato_raw",
        "pumpkin_raw",
    ],
    "oils_fats": [
        "coconut_oil", "flaxseed_oil", "sunflower_oil",
        "olive_oil", "fish_oil", "mct_oil",
    ],
}


# ============================================================
# 核心类：营养数据库
# ============================================================
class NutrientDatabase:
    """统一食材营养数据库，支持FDC JSON + v3补充数据"""

    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        self.ingredients = {}
        self._load()

    def _load(self):
        """加载FDC JSON数据库"""
        if not self.db_path.exists():
            print(f"警告: 数据库文件不存在 {self.db_path}")
            return
        with open(self.db_path, encoding="utf-8") as f:
            raw = json.load(f)
        # 转换格式: {key: {field: value}}
        for key, info in raw.items():
            nut = info.get("nutrients_per_100g", {})
            entry = {
                "zh_name": info.get("zh_name", key),
                "category": info.get("category", ""),
                "description": info.get("description", ""),
                "data_source": info.get("data_source", ""),
                "fdc_id": info.get("fdc_id", ""),
            }
            for nid, field in NUTRIENT_MAP.items():
                if nid in nut:
                    v = nut[nid]
                    entry[field] = v.get("amount", 0) if isinstance(v, dict) else 0
            self.ingredients[key] = entry

        # 应用数据修正
        for key, corrections in DB_CORRECTIONS.items():
            if key in self.ingredients:
                self.ingredients[key].update(corrections)

        # 加载v3补充数据
        for key, data in V3_EXTRA_DATA.items():
            self.ingredients[key] = data

    def get(self, key):
        """获取食材营养数据（每100g生重）"""
        return self.ingredients.get(key, {})

    def search(self, keyword):
        """搜索食材"""
        results = []
        for key, info in self.ingredients.items():
            if keyword.lower() in key.lower() or keyword in info.get("zh_name", ""):
                results.append((key, info.get("zh_name", "")))
        return results

    def get_category(self, ingredient_key):
        """判断食材分类"""
        for cat, items in INGREDIENT_CATEGORIES.items():
            if ingredient_key in items:
                return cat
        # 模糊匹配
        info = self.get(ingredient_key)
        cat_name = info.get("category", "")
        if "肉" in cat_name or "meat" in cat_name.lower():
            return "muscle_meat"
        if "内脏" in cat_name or "organ" in cat_name.lower():
            return "organs"
        if "鱼" in cat_name or "fish" in cat_name.lower():
            return "fish"
        if "菜" in cat_name or "vegetable" in cat_name.lower():
            return "vegetables"
        if "油" in cat_name or "oil" in cat_name.lower():
            return "oils_fats"
        return "other"


# ============================================================
# 核心类：配方计算器
# ============================================================
class RecipeCalculator:
    """熟自制配方计算器"""

    def __init__(self, db: NutrientDatabase):
        self.db = db

    # ---------- 能量计算 ----------
    def calculate_rer(self, weight_kg):
        """计算静息能量需求 RER = 70 × (体重kg)^0.75"""
        return 70 * (weight_kg ** 0.75)

    def calculate_mer_factor(self, profile):
        """根据活动量和目标计算MER系数"""
        info = profile.get("basic_info", {})
        goal_info = profile.get("feeding_goal", {})
        goal = goal_info.get("goal", "maintain")
        activity = info.get("activity_level", "moderate")
        neutered = info.get("neutered", True)
        lifestage = profile.get("lifestage", "adult")

        # 自定义系数覆盖（用户指定时直接使用，不经过活动量/绝育/目标计算）
        custom_factor = goal_info.get("target_calorie_factor", 0)
        if custom_factor and custom_factor > 0:
            return custom_factor

        # 基础活动系数
        activity_factors = {
            "sedentary": 1.2,      # 久坐不动 (<30min/天)
            "low": 1.4,            # 轻度活动 (30-60min/天)
            "moderate": 1.6,       # 适度活动 (1-1.5h/天, 主要散步)
            "moderate_high": 1.8,  # 中高活动 (1.5-2h/天, 含跑跳)
            "high": 2.0,           # 高强度活动 (2-3h/天, 大量运动)
            "very_high": 2.5,      # 极高活动 (3h+/天, 工作犬/运动犬)
            "working": 3.0,        # 工作犬
        }
        factor = activity_factors.get(activity, 1.6)

        # 绝育调整（成犬与老年犬均适用）
        if neutered and lifestage in ("adult", "senior"):
            factor *= 0.9  # 绝育犬能量需求略低

        # 已知缺口：本函数未单独建模"年龄导致的代谢下降"。
        # 参考资料 pet_food_database_reference.md 给出 成犬(绝育)=1.6×RER、老年(绝育)=1.4×RER。
        # 此处仍按活动量表推算，对活动量偏高的老年犬会略高估；
        # 需精确控制时，请在档案中直接设定 feeding_goal.target_calorie_factor（会覆盖本函数）。

        # 生长/繁殖阶段
        if lifestage == "puppy":
            age_mo = info.get("age_months", 0) + info.get("age_years", 0) * 12
            if age_mo < 4:
                factor = 3.0
            elif age_mo < 8:
                factor = 2.5
            else:
                factor = 2.0
        elif lifestage == "pregnant":
            factor = 1.8
        elif lifestage == "lactating":
            factor = 3.0

        # 目标调整
        goal_factors = {
            "lose": 0.8,
            "maintain": 1.0,
            "gain": 1.15,
            "gain_fast": 1.25,
        }
        factor *= goal_factors.get(goal, 1.0)

        return factor

    def calculate_target_kcal(self, profile):
        """计算每日目标热量"""
        weight = profile.get("basic_info", {}).get("body_weight_kg", 0)
        rer = self.calculate_rer(weight)
        mer_factor = self.calculate_mer_factor(profile)
        return {
            "rer": round(rer, 1),
            "mer_factor": round(mer_factor, 2),
            "target_kcal": round(rer * mer_factor, 0),
        }

    # ---------- 营养需求 ----------
    def get_nrc_requirements(self, species, lifestage="adult"):
        """获取NRC营养需求标准 (每1000kcal)"""
        if species == "dog":
            return dict(NRC_DOG_ADULT)
        else:
            return dict(NRC_CAT_ADULT)

    # ---------- 配方构建 ----------
    def build_recipe(self, profile, target_kcal=None):
        """
        按祖先饮食六步配方法生成配方：
          1 选择瘦肉与内脏  2 平衡脂肪  3 确保钙磷
          4 添加蔬菜与矿物质  5 复查脂肪  6 复查维生素D和E
        脚本是这六步的计算引擎：选料与顺序由路线模板和档案决定，每一步的算术与核验由脚本完成。
        返回: 完整配方结果字典（含 six_step_log）
        """
        species = profile.get("profile_type", "dog")
        info = profile.get("basic_info", {})
        available = profile.get("available_ingredients", {})
        prefs = profile.get("feeding_preferences", {})
        log = []

        # 目标热量
        if target_kcal is None or target_kcal == 0:
            energy = self.calculate_target_kcal(profile)
            target_kcal = energy["target_kcal"]
        else:
            energy = {
                "rer": round(self.calculate_rer(info.get("body_weight_kg", 0)), 1),
                "mer_factor": 0,
                "target_kcal": target_kcal,
            }

        # 路线模板
        templates = RATIO_TEMPLATES.get(species, {})
        if not templates:
            raise ValueError("没有 %s 的路线模板" % species)
        template_name = prefs.get("ratio_template") or list(templates.keys())[0]
        if template_name not in templates:
            template_name = list(templates.keys())[0]
        template = templates[template_name]
        categories = dict(template.get("categories", {}))
        organ_split = template.get("organ_split")
        fat_target = ROUTE_FAT_TARGET.get(species, {}).get(template_name)
        cooking_method = prefs.get("cooking_method", "boil")

        # ---------- 第1步：选择瘦肉与内脏 ----------
        base_cats = {k: v for k, v in categories.items() if k != "oils_fats"}
        oil_pct0 = categories.get("oils_fats", 0)
        oil_keys = available.get("oils_fats", []) or []
        split_txt = ""
        if organ_split:
            split_txt = "（肝/心/其他 = %s/%s/%s）" % (
                organ_split.get("liver"), organ_split.get("heart"), organ_split.get("other"))
        log.append({
            "step": 1, "name": "选择瘦肉与内脏",
            "detail": "路线「%s」：瘦肉类目 %s%%、内脏 %s%%%s；肝脏按路线目标 5%%–10%% 核查" % (
                template.get("name", ""), base_cats.get("muscle_meat", 0),
                base_cats.get("organs", 0), split_txt),
        })

        def compose(oil_pct):
            """把 base_cats 与油脂占比归一到 100，并算出该组合下的成品指标"""
            cats = dict(base_cats)
            if oil_pct > 0:
                cats["oils_fats"] = oil_pct
            s = sum(cats.values()) or 1.0
            cats = {k: v * 100.0 / s for k, v in cats.items()}
            ing = self._select_ingredients(available, cats, species, organ_split)
            if not ing:
                return None
            ed = self._calc_energy_density(ing)
            if ed <= 0:
                return None
            tf = target_kcal / (ed / 100)
            amts = {k: tf * r / 100 for k, r in ing.items()}
            raw = self._calc_total_nutrients(amts)
            if cooking_method == "boil":
                ck = self._apply_cooking_loss(raw, COOKING_LOSS_BOIL_RETAIN_BROTH)
            else:
                ck = dict(raw)
            return {
                "oil_pct": oil_pct, "ingredients": ing, "amounts": amts,
                "raw": raw, "cooked": ck, "total_food": tf,
                "fat_per_1000": ck.get("fat", 0) * 1000 / target_kcal,
            }

        # ---------- 第2步：平衡脂肪（油脂作为控制量，解算到路线脂肪目标） ----------
        OIL_MAX = 20.0
        solved = None
        fat_note = ""
        if fat_target and oil_keys:
            e0 = compose(0.0)
            if e0 is not None and e0["fat_per_1000"] >= fat_target:
                solved = e0
                fat_note = ("基准食材本身已提供 %.1f g/1000kcal，达到或超过路线目标，故不再添加油脂；"
                            "若要下调脂肪需改选更瘦的肉或去掉皮脂" % e0["fat_per_1000"])
            else:
                emax = compose(OIL_MAX)
                if emax is not None and emax["fat_per_1000"] < fat_target:
                    solved = emax
                    fat_note = ("油脂已加到上限 %.0f%% 仍只有 %.1f g/1000kcal，低于目标 %.1f"
                                % (OIL_MAX, emax["fat_per_1000"], fat_target))
                else:
                    lo, hi = 0.0, OIL_MAX
                    for _ in range(40):
                        mid = (lo + hi) / 2.0
                        em = compose(mid)
                        if em is None:
                            break
                        if em["fat_per_1000"] < fat_target:
                            lo = mid
                        else:
                            hi = mid
                    solved = compose((lo + hi) / 2.0)
        if solved is None:
            solved = compose(oil_pct0)
        if solved is None:
            solved = compose(0.0)
        if solved is None:
            raise ValueError("无法构建配方：可用食材或食材库数据不足")

        recipe_ingredients = solved["ingredients"]
        amounts = solved["amounts"]
        raw_nutrients = solved["raw"]
        cooked_nutrients = solved["cooked"]
        total_food = solved["total_food"]

        if fat_target:
            delta = solved["fat_per_1000"] - fat_target
            tol = max(1.5, fat_target * 0.05)
            tag = "达标" if abs(delta) <= tol else ("偏低" if delta < 0 else "偏高")
            log.append({
                "step": 2, "name": "平衡脂肪",
                "detail": "油脂解算为 %.1f%%；实际脂肪 %.1f g/1000kcal，路线目标 %.1f（%s）%s" % (
                    solved["oil_pct"], solved["fat_per_1000"], fat_target, tag,
                    ("。" + fat_note) if fat_note else ""),
            })
        else:
            log.append({
                "step": 2, "name": "平衡脂肪",
                "detail": "该路线未设脂肪目标，按模板油脂比例 %.1f%%；实际脂肪 %.1f g/1000kcal" % (
                    solved["oil_pct"], solved["fat_per_1000"]),
            })

        # 每1000kcal营养素 + NRC对照
        nrc = self.get_nrc_requirements(species)
        per_1000 = {k: v * 1000 / target_kcal for k, v in cooked_nutrients.items() if v > 0}
        gaps = self._calculate_gaps(per_1000, nrc, cooked_nutrients, target_kcal)

        # ---------- 第3步：确保钙磷 ----------
        ca_p = self._adjust_calcium_phosphorus(raw_nutrients, gaps, nrc)
        raw_nutrients["Ca"] = ca_p["final_ca_mg"]
        cooked_nutrients["Ca"] = raw_nutrients["Ca"] * 0.95
        per_1000["Ca"] = cooked_nutrients["Ca"] * 1000 / target_kcal
        gaps = self._calculate_gaps(per_1000, nrc, cooked_nutrients, target_kcal)
        log.append({
            "step": 3, "name": "确保钙磷",
            "detail": "食材钙 %s mg / 磷 %s mg → 补蛋壳粉 %s g，最终 Ca:P = %s" % (
                ca_p["food_ca_mg"], ca_p["food_p_mg"], ca_p["eggshell_needed_g"], ca_p["final_ratio"]),
        })

        # ---------- 第4步：添加蔬菜与矿物质（核查） ----------
        watch = ["Mn", "Cu", "Zn", "Mg", "Fe", "Se"]
        short = []
        for n in watch:
            ra = nrc.get(n, (0,))[0]
            if ra and per_1000.get(n, 0) < ra:
                short.append("%s %.2f/%.2f" % (n, per_1000.get(n, 0), ra))
        liver_pct = 0.0
        for k, g in amounts.items():
            if "肝" in self.db.get(k).get("zh_name", ""):
                liver_pct += g / total_food * 100
        log.append({
            "step": 4, "name": "添加蔬菜与矿物质",
            "detail": "蔬菜与全谷物已计入；肝脏占整体 %.1f%%（路线要求 5%%–10%%）；微量元素：%s" % (
                liver_pct, ("缺 " + "、".join(short)) if short else "锰/铜/锌/镁/铁/硒均达标"),
        })

        # ---------- 第5步：复查脂肪（蔬菜加入后重算） ----------
        fa = self._calc_fatty_acid_profile(per_1000)
        log.append({
            "step": 5, "name": "复查脂肪",
            "detail": "总脂肪 %s g/1000kcal；PUFA %s（%s）；ω6/ω3 = %s:1；EPA+DHA %.3f g/1000kcal" % (
                fa["total_fat_g"], fa["polyunsaturated_g"],
                "安全" if fa["pufa_safe"] else "超上限", fa["omega6_omega3_ratio"],
                fa["omega3_epa_g"] + fa["omega3_dha_g"]),
        })

        # 补充剂建议（在第3、4步的缺口基础上给出）
        supplements = self._recommend_supplements(gaps, profile, per_1000, target_kcal)

        # ---------- 第6步：复查维生素D和E ----------
        pufa_g = fa["polyunsaturated_g"]
        ve_need = 7.5 + pufa_g * 5.0
        log.append({
            "step": 6, "name": "复查维生素D和E",
            "detail": "维D %s/%s µg per 1000kcal；维E需求 = 基础7.5 + PUFA %s × 5 = %.1f mg/1000kcal，配方实际 %s" % (
                round(per_1000.get("vitaminD", 0), 2), nrc.get("vitaminD", (0,))[0],
                pufa_g, ve_need, round(per_1000.get("vitaminE", 0), 2)),
        })

        # 构建输出
        result = {
            "version": "2.0",
            "generation_method": "六步配方法",
            "pet_info": {
                "name": info.get("name", ""),
                "species": species,
                "breed": info.get("breed", ""),
                "weight_kg": info.get("body_weight_kg", 0),
                "age_years": info.get("age_years", 0),
                "lifestage": profile.get("lifestage", "adult"),
                "activity_level": info.get("activity_level", ""),
                "goal": profile.get("feeding_goal", {}).get("goal", ""),
            },
            "energy": energy,
            "template_used": {
                "name": template.get("name", ""),
                "key": template_name,
                "description": template.get("description", ""),
                "evidence_grade": template.get("evidence", "-"),
                "fat_target_g_per_1000kcal": fat_target,
                "fat_achieved_g_per_1000kcal": round(solved["fat_per_1000"], 1),
                "oil_solved_percent": round(solved["oil_pct"], 2),
            },
            "six_step_log": log,
            "cooking_method": cooking_method,
            "ingredients": amounts,
            "ingredients_zh": {k: self.db.get(k).get("zh_name", k) for k in amounts},
            "nutrients_raw": raw_nutrients,
            "nutrients_cooked": cooked_nutrients,
            "nutrients_per_1000kcal": per_1000,
            "nrc_requirements": nrc,
            "nutrient_gaps": gaps,
            "supplements": supplements,
            "calcium_adjustment": ca_p,
            "fatty_acid_profile": fa,
            "feeding_guide": {
                "total_food_g": round(total_food, 1),
                "meals_per_day": prefs.get("meals_per_day", 2),
                "per_meal_g": round(total_food / prefs.get("meals_per_day", 2), 1),
            },
        }

        return result

    def _select_ingredients(self, available, categories, species, organ_split=None):
        """
        根据可用食材和配方模板分类，选择食材并分配比例
        organ_split: 内脏内部拆分 {liver/heart/other: 权重}；缺省 肝30/心50/其他20
        返回: {ingredient_key: percentage}
        """
        selected = {}

        for cat, cat_pct in categories.items():
            # 获取该分类下的可用食材
            cat_ingredients = available.get(cat, [])
            if not cat_ingredients:
                # 尝试从primary_proteins等字段找
                if cat == "muscle_meat":
                    cat_ingredients = available.get("primary_proteins", []) + available.get("secondary_proteins", [])
                elif cat == "organs":
                    cat_ingredients = available.get("organ_meats", [])
                elif cat == "fish":
                    cat_ingredients = available.get("fish", [])
                elif cat == "eggs":
                    cat_ingredients = available.get("eggs", [])
                elif cat == "vegetables":
                    cat_ingredients = available.get("vegetables", [])
                elif cat in ("grains_carbs", "bone", "seeds_nuts"):
                    cat_ingredients = available.get("grains_carbs", [])
                elif cat == "oils_fats":
                    cat_ingredients = available.get("oils_fats", [])

            if not cat_ingredients:
                continue

            # 平均分配（如果分类有2种以上食材）
            n = len(cat_ingredients)
            if n == 1:
                selected[cat_ingredients[0]] = cat_pct
            elif cat == "muscle_meat":
                # 两种主蛋白各一半
                half = cat_pct / 2
                for ing in cat_ingredients[:2]:
                    selected[ing] = half
            elif cat == "organs":
                # 心/肝/其他内脏按模板给定的 organ_split 拆分（缺省 肝30/心50/其他20）
                liver = [i for i in cat_ingredients if "liver" in i.lower() or "肝" in self.db.get(i).get("zh_name", "")]
                heart = [i for i in cat_ingredients if "heart" in i.lower() or "心" in self.db.get(i).get("zh_name", "")]
                other = [i for i in cat_ingredients if i not in liver and i not in heart]

                split = dict(organ_split) if organ_split else {"liver": 0.30, "heart": 0.50, "other": 0.20}
                share = {k: max(0.0, float(v)) for k, v in split.items()}
                buckets = {"liver": liver, "heart": heart, "other": other}
                present = [k for k in ("liver", "heart", "other") if buckets[k]]

                if present:
                    # 若某类内脏缺货，其份额按在场类别的权重比例转出去
                    present_share = sum(share.get(k, 0.0) for k in present) or 1.0
                    for k in present:
                        allot = cat_pct * share.get(k, 0.0) / present_share
                        for ing in buckets[k]:
                            selected[ing] = allot / len(buckets[k])
                else:
                    per = cat_pct / n
                    for ing in cat_ingredients:
                        selected[ing] = per
            else:
                per = cat_pct / n
                for ing in cat_ingredients:
                    selected[ing] = per

        return selected

    def _calc_energy_density(self, recipe_ingredients):
        """计算每100g混合食物的能量(kcal)"""
        total_energy = 0
        total_pct = 0
        for key, pct in recipe_ingredients.items():
            info = self.db.get(key)
            e = info.get("energyKCal", 0)
            total_energy += e * pct / 100
            total_pct += pct
        return total_energy / (total_pct / 100) if total_pct > 0 else 0

    def _calc_total_nutrients(self, amounts):
        """计算所有营养素总量（生重）"""
        totals = {}
        for key, grams in amounts.items():
            info = self.db.get(key)
            if not info:
                continue
            factor = grams / 100
            for field, val in info.items():
                if isinstance(val, (int, float)) and field not in ("fdc_id",):
                    if field not in ("zh_name", "category", "description", "data_source"):
                        totals[field] = totals.get(field, 0) + val * factor
        return totals

    def _apply_cooking_loss(self, raw_nutrients, loss_factors):
        """应用烹饪损失因子"""
        cooked = {}
        for field, val in raw_nutrients.items():
            factor = loss_factors.get(field, 0.95)
            cooked[field] = val * factor
        return cooked

    def _calculate_gaps(self, per_1000, nrc, cooked_total, target_kcal):
        """计算营养缺口"""
        gaps = {
            "deficient": {},    # 不足
            "sufficient": {},   # 充足
            "excess": {},       # 过量
        }
        for nutrient, (ra, unit, _level) in nrc.items():
            val = per_1000.get(nutrient, 0)
            daily_val = cooked_total.get(nutrient, 0)
            if val >= ra:
                gaps["sufficient"][nutrient] = {
                    "ra_1000kcal": ra,
                    "actual_1000kcal": round(val, 3),
                    "actual_daily": round(daily_val, 3),
                    "unit": unit,
                    "ratio": round(val / ra, 2) if ra > 0 else 999,
                }
            else:
                deficit = ra - val
                daily_deficit = deficit * target_kcal / 1000
                gaps["deficient"][nutrient] = {
                    "ra_1000kcal": ra,
                    "actual_1000kcal": round(val, 3),
                    "actual_daily": round(daily_val, 3),
                    "deficit_1000kcal": round(deficit, 3),
                    "deficit_daily": round(daily_deficit, 3),
                    "unit": unit,
                    "ratio": round(val / ra, 2) if ra > 0 else 0,
                }
        return gaps

    def _recommend_supplements(self, gaps, profile, per_1000, target_kcal):
        """
        推荐补充剂（尽量用天然食物，减少人工补剂）
        策略：
        1. 钙 → 蛋壳粉/骨粉 (计算精确量)
        2. 碘 → 碘化钾片/海藻粉 (精确剂量)
        3. 维E → 根据PUFA计算
        4. 其他矿物质 → 先看能否用天然食物替代，不行才推荐补剂
        """
        species = profile.get("profile_type", "dog")
        supplements = {
            "required": [],      # 必须补剂
            "optional": [],      # 可选补剂
            "natural_food_fixes": [],  # 天然食物调整建议
            "notes": [],
        }

        deficient = gaps.get("deficient", {})
        sufficient = gaps.get("sufficient", {})

        # ---- 维生素E: PUFA补偿计算 ----
        pufa = per_1000.get("poly_fat", 0)
        la = per_1000.get("linoleic_acid", 0)
        ala = per_1000.get("alpha_linolenic_acid", 0)
        epa = per_1000.get("EPA", 0)
        dha = per_1000.get("DHA", 0)
        if pufa == 0:
            pufa = la + ala + epa + dha

        ve_base = 7.5 if species == "dog" else 10
        ve_need_1000 = ve_base + pufa * 5  # 每g PUFA加5mg维E
        ve_have_1000 = per_1000.get("vitaminE", 0)
        ve_def_1000 = max(0, ve_need_1000 - ve_have_1000)
        ve_def_daily = ve_def_1000 * target_kcal / 1000

        if ve_def_daily > 5:
            # 检查用户已有维E
            user_ve = profile.get("current_supplements", {}).get("vitamin_e", "")
            supplements["required"].append({
                "nutrient": "vitaminE",
                "name": "维生素E (d-α-生育酚)",
                "daily_dosage": round(ve_def_daily, 1),
                "unit": "mg",
                "reason": f"PUFA({pufa:.1f}g/1000kcal)消耗维E，需PUFA补偿(pufa×5mg + 基础{ve_base}mg = {ve_need_1000:.0f}mg)",
                "food_amount": ve_have_1000,
                "user_supplement": user_ve,
            })
        elif ve_def_daily > 0:
            supplements["optional"].append({
                "nutrient": "vitaminE",
                "name": "维生素E",
                "daily_dosage": round(ve_def_daily, 1),
                "unit": "mg",
                "reason": "缺口小，可酌情补充",
            })

        # ---- 锌 ----
        if "Zn" in deficient:
            zn_def = deficient["Zn"]["deficit_daily"]
            # 判断能否用天然食物增加
            supplements["required"].append({
                "nutrient": "Zn",
                "name": "锌 (葡萄糖酸锌)",
                "daily_dosage": round(zn_def, 1),
                "unit": "mg元素锌",
                "equivalent": f"葡萄糖酸锌片(50mg, 含锌6.5mg): 每天{round(zn_def/6.5, 1)}片",
                "reason": "植物性锌吸收率低，肉类锌不足时需补充",
                "natural_alternative": "增加生蚝/牡蛎(约39mg Zn/100g)",
            })

        # ---- 铜 ----
        if "Cu" in deficient:
            cu_def = deficient["Cu"]["deficit_daily"]
            if cu_def < 0.5:
                supplements["natural_food_fixes"].append({
                    "nutrient": "Cu",
                    "fix": f"铜缺口较小({cu_def:.2f}mg/天)，可通过增加肝/肾类内脏补充",
                })
            else:
                supplements["optional"].append({
                    "nutrient": "Cu",
                    "name": "铜 (蛋氨酸铜)",
                    "daily_dosage": round(cu_def, 2),
                    "unit": "mg元素铜",
                    "reason": "铜缺口较大",
                })

        # ---- 硒 ----
        if "Se" in deficient:
            se_def = deficient["Se"]["deficit_daily"]
            supplements["natural_food_fixes"].append({
                "nutrient": "Se",
                "fix": f"硒缺口({se_def:.0f}µg/天)，增加三文鱼/沙丁鱼等海鱼或1颗巴西坚果(约70µg)",
            })

        # ---- 镁 ----
        if "Mg" in deficient:
            mg_def = deficient["Mg"]["deficit_daily"]
            if mg_def < 20:
                supplements["natural_food_fixes"].append({
                    "nutrient": "Mg",
                    "fix": f"镁缺口较小({mg_def:.0f}mg/天)，增加菠菜/南瓜籽/坚果",
                })
            else:
                supplements["optional"].append({
                    "nutrient": "Mg",
                    "name": "镁 (柠檬酸镁)",
                    "daily_dosage": round(mg_def, 0),
                    "unit": "mg",
                })

        # ---- 维生素D ----
        if "vitaminD" in deficient:
            vd_def = deficient["vitaminD"]["deficit_daily"]
            if vd_def < 1:
                supplements["natural_food_fixes"].append({
                    "nutrient": "vitaminD",
                    "fix": f"维D缺口较小({vd_def:.1f}µg/天)，增加三文鱼/多晒太阳",
                })
            else:
                supplements["optional"].append({
                    "nutrient": "vitaminD",
                    "name": "维生素D3",
                    "daily_dosage": round(vd_def, 1),
                    "unit": "µg",
                    "equivalent": f"约{round(vd_def*40)} IU",
                })

        # ---- B12 ----
        if "vitaminB12" in deficient:
            b12_def = deficient["vitaminB12"]["deficit_daily"]
            if b12_def < 2:
                supplements["natural_food_fixes"].append({
                    "nutrient": "vitaminB12",
                    "fix": f"B12缺口较小({b12_def:.1f}µg/天)，增加肝脏/肾脏即可",
                })
            else:
                supplements["optional"].append({
                    "nutrient": "vitaminB12",
                    "name": "维生素B12 (氰钴胺)",
                    "daily_dosage": round(b12_def, 1),
                    "unit": "µg",
                })

        # ---- 胆碱 ----
        if "choline" in deficient:
            chol_def = deficient["choline"]["deficit_daily"]
            if chol_def < 50:
                supplements["natural_food_fixes"].append({
                    "nutrient": "choline",
                    "fix": f"胆碱缺口较小({chol_def:.0f}mg/天)，增加蛋黄(1个蛋黄≈90mg胆碱)",
                })
            else:
                supplements["optional"].append({
                    "nutrient": "choline",
                    "name": "胆碱 (胆碱酒石酸氢盐)",
                    "daily_dosage": round(chol_def, 0),
                    "unit": "mg",
                    "equivalent": f"约{round(chol_def/200, 1)}片(500mg片含200mg胆碱)",
                })

        # ---- 猫特有: 牛磺酸 ----
        if species == "cat" and "taurine" in deficient:
            tau_def = deficient["taurine"]["deficit_daily"]
            supplements["required"].append({
                "nutrient": "taurine",
                "name": "牛磺酸",
                "daily_dosage": round(tau_def, 0),
                "unit": "mg",
                "reason": "猫为专性肉食动物，牛磺酸必需氨基酸",
            })

        # ---- 碘 (总是需要补剂，因为熟自制食材碘含量低且不稳定) ----
        iodine_source = profile.get("current_supplements", {}).get("iodine_source", "")
        iodine_need_1000 = 220 if species == "dog" else 350
        iodine_need_daily = iodine_need_1000 * target_kcal / 1000
        supplements["required"].insert(0, {
            "nutrient": "iodine",
            "name": "碘 (碘化钾片 或 海藻粉)",
            "daily_dosage": round(iodine_need_daily, 0),
            "unit": "µg",
            "recommendation": f"NOW Potassium + Iodine 1片/天 (225µg碘, 钠仅5mg) " if abs(iodine_need_daily - 225) < 50 else f"碘化钾滴剂，精确取{iodine_need_daily:.0f}µg",
            "user_supplement": iodine_source,
            "warning": "不推荐加碘盐（钠过高，碘含量不稳定）",
        })

        # 统计
        supplements["summary"] = {
            "total_required": len(supplements["required"]),
            "total_optional": len(supplements["optional"]),
            "natural_fixes_count": len(supplements["natural_food_fixes"]),
        }

        return supplements

    def _adjust_calcium_phosphorus(self, raw_nutrients, gaps, nrc):
        """调整钙磷比，计算蛋壳粉需要量"""
        ca = raw_nutrients.get("Ca", 0)
        p = raw_nutrients.get("P", 0)

        target_ratio = 1.3
        ca_needed = target_ratio * p
        ca_deficit = max(0, ca_needed - ca)
        eggshell_grams = ca_deficit / 380  # 蛋壳粉380mg Ca/g

        cooked_ca = ca + ca_deficit
        cooked_p = p
        ratio = cooked_ca / cooked_p if cooked_p > 0 else 0

        return {
            "food_ca_mg": round(ca, 1),
            "food_p_mg": round(p, 1),
            "target_ratio": target_ratio,
            "eggshell_needed_g": round(eggshell_grams, 2),
            "final_ca_mg": round(cooked_ca, 1),
            "final_p_mg": round(cooked_p, 1),
            "final_ratio": round(ratio, 2),
        }

    def _calc_fatty_acid_profile(self, per_1000):
        """计算脂肪酸概况"""
        la = per_1000.get("linoleic_acid", 0)
        ala = per_1000.get("alpha_linolenic_acid", 0)
        epa = per_1000.get("EPA", 0)
        dha = per_1000.get("DHA", 0)
        o3 = ala + epa + dha
        pufa = per_1000.get("poly_fat", la + o3)
        sat = per_1000.get("sat_fat", 0)
        mono = per_1000.get("mono_fat", 0)
        total_fat = per_1000.get("fat", sat + mono + pufa)

        return {
            "total_fat_g": round(total_fat, 2),
            "saturated_g": round(sat, 2),
            "monounsaturated_g": round(mono, 2),
            "polyunsaturated_g": round(pufa, 2),
            "omega6_linoleic_g": round(la, 2),
            "omega3_total_g": round(o3, 2),
            "omega3_ala_g": round(ala, 3),
            "omega3_epa_g": round(epa, 3),
            "omega3_dha_g": round(dha, 3),
            "omega6_omega3_ratio": round(la / o3, 1) if o3 > 0 else 999,
            "pufa_percent_of_fat": round(pufa / total_fat * 100, 1) if total_fat > 0 else 0,
            "pufa_safe": pufa <= 16.3,  # NRC安全上限
        }


# ============================================================
# 输出格式化
# ============================================================
def format_result_markdown(result):
    """将计算结果格式化为Markdown报告"""
    pet = result["pet_info"]
    energy = result["energy"]
    sup = result["supplements"]
    ca_p = result["calcium_adjustment"]
    fa = result["fatty_acid_profile"]
    feed = result["feeding_guide"]
    nrc = result["nrc_requirements"]
    per_1000 = result["nutrients_per_1000kcal"]
    gaps = result["nutrient_gaps"]
    ingredients = result["ingredients"]
    zh = result["ingredients_zh"]
    template = result["template_used"]

    lines = []
    lines.append(f"# {pet.get('name', '宠物')} 熟自制配方报告")
    lines.append("")
    lines.append("## 基本信息")
    lines.append("")
    lines.append(f"- **物种**：{'犬' if pet['species']=='dog' else '猫'}")
    lines.append(f"- **品种**：{pet.get('breed', '未知')}")
    lines.append(f"- **体重**：{pet.get('weight_kg', 0)} kg")
    lines.append(f"- **年龄**：{pet.get('age_years', 0)}岁")
    lines.append(f"- **生命阶段**：{pet.get('lifestage', '成年')}")
    lines.append(f"- **活动量**：{pet.get('activity_level', '')}")
    goal_map = {"gain": "增重", "lose": "减重", "maintain": "维持", "gain_fast": "快速增重"}
    lines.append(f"- **目标**：{goal_map.get(pet.get('goal',''), pet.get('goal',''))}")
    lines.append(f"- **每日热量**：{energy['target_kcal']:.0f} kcal")
    lines.append(f"  - RER = {energy['rer']} kcal")
    lines.append(f"  - MER系数 = {energy['mer_factor']}")
    lines.append(f"- **烹饪方式**：{result['cooking_method']}（留汤）")
    lines.append(f"- **配方模板**：{template['name']}")
    lines.append(f"- **证据等级**：{template.get('evidence_grade', '-')}（A=营养需要/法规；B=完整数据库核算的公开配方；C=行业结构但生熟转换证据有限；D=网络经验）")
    lines.append(f"- **模板说明**：{template['description']}")
    lines.append("")

    lines.append("## 食材清单（每日量）")
    lines.append("")
    lines.append("| 食材 | 每日(g) | 占比 | 能量密度(kcal/100g) |")
    lines.append("|------|---------|------|-------------------|")

    total_pct = sum(ingredients.values())
    for key, grams in sorted(ingredients.items(), key=lambda x: -x[1]):
        info = result.get("_db", {}).get(key, {})
        pct = grams / feed["total_food_g"] * 100
        ed = info.get("energyKCal", 0)
        lines.append(f"| {zh.get(key, key)} | {grams:.1f} | {pct:.1f}% | {ed:.0f} |")

    lines.append("")
    lines.append(f"- **每日食物总量**：{feed['total_food_g']}g")
    lines.append(f"- **每日热量**：{energy['target_kcal']:.0f} kcal")
    lines.append(f"- **分{feed['meals_per_day']}餐**：每餐约{feed['per_meal_g']}g")
    lines.append("")

    # 钙调整
    lines.append("## 钙磷平衡")
    lines.append("")
    lines.append(f"| 项目 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 食材钙 | {ca_p['food_ca_mg']:.1f} mg |")
    lines.append(f"| 食材磷 | {ca_p['food_p_mg']:.1f} mg |")
    lines.append(f"| 目标Ca:P | {ca_p['target_ratio']}:1 |")
    lines.append(f"| **蛋壳粉补充** | **{ca_p['eggshell_needed_g']} g** |")
    lines.append(f"| 最终钙 | {ca_p['final_ca_mg']:.1f} mg |")
    lines.append(f"| 最终Ca:P | {ca_p['final_ratio']}:1 |")
    lines.append("")

    # 营养分析
    lines.append("## 营养分析（每1000kcal，烹饪后）")
    lines.append("")
    lines.append("| 营养素 | NRC标准 | 本配方 | 单位 | 状态 |")
    lines.append("|--------|---------|--------|------|------|")

    # 按重要性排序
    order = ["protein","fat","Ca","P","Mg","K","Na","Fe","Cu","Zn","Mn","Se",
             "vitaminA","vitaminD","vitaminE","thiamin","riboflavin","niacin",
             "vitaminB6","folate","vitaminB12","choline",
             "linoleic_acid","alpha_linolenic_acid","EPA","DHA"]

    for nutrient in order:
        if nutrient not in nrc:
            continue
        ra, unit, _ = nrc[nutrient]
        val = per_1000.get(nutrient, 0)
        status = "✓" if val >= ra else "✗"
        lines.append(f"| {nutrient} | {ra} | {val:.2f} | {unit} | {status} |")

    lines.append("")

    # 脂肪酸
    lines.append("## 脂肪酸分析")
    lines.append("")
    lines.append(f"| 指标 | 数值 | 参考 |")
    lines.append("|------|------|------|")
    lines.append(f"| 总脂肪 | {fa['total_fat_g']}g/1000kcal | NRC最低13.8g |")
    lines.append(f"| 饱和脂肪 | {fa['saturated_g']}g | — |")
    lines.append(f"| 单不饱和脂肪 | {fa['monounsaturated_g']}g | — |")
    lines.append(f"| 多不饱和脂肪 | {fa['polyunsaturated_g']}g | ≤16.3g(安全上限) |")
    lines.append(f"| ω6/ω3 比值 | {fa['omega6_omega3_ratio']}:1 | 2-6:1 |")
    lines.append(f"| ω6(亚油酸) | {fa['omega6_linoleic_g']}g | ≥2.8g |")
    lines.append(f"| ω3(ALA+EPA+DHA) | {fa['omega3_total_g']}g | ≥0.11g |")
    lines.append(f"| EPA | {fa['omega3_epa_g']}g | ≥0.055g |")
    lines.append(f"| DHA | {fa['omega3_dha_g']}g | ≥0.055g |")
    lines.append("")

    # 补充剂
    # 六步法执行记录
    step_log = result.get("six_step_log", [])
    if step_log:
        lines.append("## 六步法执行记录")
        lines.append("")
        for item in step_log:
            lines.append("- **第%s步 %s**：%s" % (item.get("step"), item.get("name"), item.get("detail")))
        lines.append("")

    lines.append("## 补充剂建议")
    lines.append("")

    if sup["required"]:
        lines.append("### 必需补充剂")
        lines.append("")
        for s in sup["required"]:
            lines.append(f"- **{s['name']}**：{s['daily_dosage']}{s.get('unit','')}/天")
            if "reason" in s:
                lines.append(f"  - 原因：{s['reason']}")
            if "equivalent" in s:
                lines.append(f"  - 等效：{s['equivalent']}")
            if "recommendation" in s:
                lines.append(f"  - 推荐：{s['recommendation']}")
            if s.get("warning"):
                lines.append(f"  - ⚠️ {s['warning']}")
            if s.get("user_supplement"):
                lines.append(f"  - 用户现有：{s['user_supplement']}")
        lines.append("")

    if sup.get("natural_food_fixes"):
        lines.append("### 天然食物调整建议")
        lines.append("")
        for fix in sup["natural_food_fixes"]:
            lines.append(f"- {fix.get('fix', '')}")
        lines.append("")

    if sup.get("optional"):
        lines.append("### 可选补充剂（差距较小）")
        lines.append("")
        for s in sup["optional"]:
            lines.append(f"- **{s['name']}**：{s['daily_dosage']}{s.get('unit','')}/天")
            if "reason" in s:
                lines.append(f"  - 原因：{s['reason']}")
        lines.append("")

    lines.append(f"**补充剂统计**：必需 {sup['summary']['total_required']} 种，可选 {sup['summary']['total_optional']} 种，天然食物调整 {sup['summary']['natural_fixes_count']} 项")
    lines.append("")

    # 喂养指南
    lines.append("## 喂养指南")
    lines.append("")
    lines.append(f"- 每日喂食总量：约{feed['total_food_g'] + ca_p['eggshell_needed_g']:.0f}g（含蛋壳粉）")
    lines.append(f"- 每日分{feed['meals_per_day']}餐，每餐约{(feed['total_food_g'] + ca_p['eggshell_needed_g']) / feed['meals_per_day']:.0f}g")
    lines.append(f"- 烹饪方式：{result['cooking_method']}，**必须留汤**（倒汤流失B1 50%、牛磺酸60-70%、磷35%）")
    lines.append("")

    lines.append("### 制作步骤")
    lines.append("")
    steps = [
        "谷物/豆类提前浸泡2-4小时，先煮至软烂",
        "肉类和内脏切块，冷水入锅，大火煮开撇去浮沫，转小火煮20-25分钟",
        "鱼类最后5分钟加入（避免过度烹饪损失omega-3）",
        "蔬菜单独焯水2-3分钟，切碎或打碎",
        "蛋类单独煮熟，切碎",
        "油脂拌入温热的食物中（不要高温加热）",
        "**肉汤保留**，拌入食物中增加适口性和营养保留",
        "蛋壳粉、碘片、维E、锌片等补充剂拌入温凉的食物中",
        f"混匀后分成{feed['meals_per_day']}份，早晚各喂1餐",
    ]
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    return "\n".join(lines)


# ============================================================
# 主函数
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="宠物熟自制配方计算器")
    parser.add_argument("--profile", "-p", required=True, help="宠物档案JSON文件路径")
    parser.add_argument("--ratio-template", "-t", default=None, help="配方模板名称")
    parser.add_argument("--cooking-method", "-c", default="boil", help="烹饪方式")
    parser.add_argument("--target-kcal", "-k", type=float, default=0, help="目标热量(0=自动计算)")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径")
    parser.add_argument("--format", "-f", default="json", choices=["json", "markdown"], help="输出格式")
    args = parser.parse_args()

    # 加载数据库
    db = NutrientDatabase()
    print(f"[INFO] 数据库加载完成: {len(db.ingredients)} 种食材", file=sys.stderr)

    # 加载档案
    profile_path = Path(args.profile)
    if not profile_path.exists():
        print(f"错误: 档案文件不存在 {profile_path}", file=sys.stderr)
        sys.exit(1)

    with open(profile_path, encoding="utf-8") as f:
        profile = json.load(f)

    print(f"[INFO] 档案加载: {profile.get('basic_info',{}).get('name','无名')} ({profile.get('profile_type','')})", file=sys.stderr)

    # 覆盖模板
    if args.ratio_template:
        profile.setdefault("feeding_preferences", {})["ratio_template"] = args.ratio_template

    # 覆盖烹饪方式
    if args.cooking_method:
        profile.setdefault("feeding_preferences", {})["cooking_method"] = args.cooking_method

    # 计算
    calc = RecipeCalculator(db)
    result = calc.build_recipe(profile, target_kcal=args.target_kcal)

    # 附加数据库引用(用于markdown输出)
    result["_db"] = {k: db.get(k) for k in result["ingredients"]}

    # 输出
    if args.format == "markdown":
        output = format_result_markdown(result)
    else:
        # 去掉内部字段
        result.pop("_db", None)
        output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[INFO] 结果已保存到 {out_path}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
