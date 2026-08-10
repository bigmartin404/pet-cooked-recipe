#!/usr/bin/env python3
"""
预建宠物配方常用食材营养数据库（单次扫描优化版）。
一次扫描 food.csv 收集所有 FDC ID，一次扫描 food_nutrient.csv 收集所有营养数据。

用法: python build_ingredient_db.py
输出: references/common_ingredients_nutrients.json
"""
import csv
import json
import os
import sys
import re
from pathlib import Path

DATA_DIR = Path(r"E:\1-Projects\FEED\fooddata_temp\_full_extract")
FOOD_CSV = DATA_DIR / "food.csv"
FOOD_NUTRIENT_CSV = DATA_DIR / "food_nutrient.csv"
OUTPUT_FILE = Path(__file__).parent.parent / "references" / "common_ingredients_nutrients.json"

COMMON_INGREDIENTS = {
    "beef_ground_90lean_raw": {"search": "Beef, ground, 90* lean*10* fat, raw", "type": "sr_legacy_food", "zh": "牛肉末(90%瘦)"},
    "beef_brisket_lean_raw": {"search": "Beef, brisket, whole, separable lean only, raw", "type": "sr_legacy_food", "zh": "牛腩(瘦肉)"},
    "beef_liver_raw": {"search": "Beef, liver, raw", "type": "sr_legacy_food", "zh": "牛肝"},
    "beef_heart_raw": {"search": "Beef, heart, raw", "type": "sr_legacy_food", "zh": "牛心"},
    "beef_kidney_raw": {"search": "Beef, kidney, raw", "type": "sr_legacy_food", "zh": "牛肾"},
    "beef_spleen_raw": {"search": "Beef, spleen, raw", "type": "sr_legacy_food", "zh": "牛脾"},
    "chicken_breast_skinless_raw": {"search": "Chicken, breast, skinless, boneless, raw", "type": "sr_legacy_food", "zh": "鸡胸肉(去皮去骨)"},
    "chicken_thigh_raw": {"search": "Chicken, thigh, raw", "type": "sr_legacy_food", "zh": "鸡腿肉"},
    "chicken_liver_raw": {"search": "Chicken, liver, raw", "type": "sr_legacy_food", "zh": "鸡肝"},
    "chicken_heart_raw": {"search": "Chicken, heart, raw", "type": "sr_legacy_food", "zh": "鸡心"},
    "pork_lean_raw": {"search": "Pork, fresh, *lean*, raw", "type": "sr_legacy_food", "zh": "猪瘦肉"},
    "pork_liver_raw": {"search": "Pork, liver, raw", "type": "sr_legacy_food", "zh": "猪肝"},
    "pork_heart_raw": {"search": "Pork, heart, raw", "type": "sr_legacy_food", "zh": "猪心"},
    "pork_kidney_raw": {"search": "Pork, kidney, raw", "type": "sr_legacy_food", "zh": "猪肾"},
    "lamb_lean_raw": {"search": "Lamb, *lean*, raw", "type": "sr_legacy_food", "zh": "羊肉(瘦)"},
    "lamb_liver_raw": {"search": "Lamb, liver, raw", "type": "sr_legacy_food", "zh": "羊肝"},
    "duck_raw": {"search": "Duck, raw", "type": "sr_legacy_food", "zh": "鸭肉"},
    "salmon_raw": {"search": "Salmon, *raw", "type": "sr_legacy_food", "zh": "三文鱼(生)"},
    "sardine_raw": {"search": "Sardine, raw", "type": "sr_legacy_food", "zh": "沙丁鱼(生)"},
    "tuna_raw": {"search": "Tuna, fresh, *raw", "type": "sr_legacy_food", "zh": "金枪鱼(生)"},
    "egg_whole_raw": {"search": "Egg, whole, raw", "type": "sr_legacy_food", "zh": "全蛋(生)"},
    "egg_yolk_raw": {"search": "Egg, yolk, raw", "type": "sr_legacy_food", "zh": "蛋黄(生)"},
    "broccoli_raw": {"search": "Broccoli, raw", "type": "sr_legacy_food", "zh": "西兰花(生)"},
    "spinach_raw": {"search": "Spinach, raw", "type": "sr_legacy_food", "zh": "菠菜(生)"},
    "carrot_raw": {"search": "Carrot, raw", "type": "sr_legacy_food", "zh": "胡萝卜(生)"},
    "sweet_potato_raw": {"search": "Sweet potato, raw", "type": "sr_legacy_food", "zh": "红薯(生)"},
    "pumpkin_raw": {"search": "Pumpkin, raw", "type": "sr_legacy_food", "zh": "南瓜(生)"},
    "zucchini_raw": {"search": "Squash, summer, zucchini, raw", "type": "sr_legacy_food", "zh": "西葫芦(生)"},
    "oats_raw": {"search": "Oats, raw", "type": "sr_legacy_food", "zh": "燕麦(生)"},
    "brown_rice_raw": {"search": "Rice, brown, raw", "type": "sr_legacy_food", "zh": "糙米(生)"},
    "quinoa_raw": {"search": "Quinoa, raw", "type": "sr_legacy_food", "zh": "藜麦(生)"},
    "fish_oil_salmon": {"search": "Fish oil, salmon", "type": "sr_legacy_food", "zh": "三文鱼油"},
    "sunflower_oil": {"search": "Oil, sunflower", "type": "sr_legacy_food", "zh": "葵花籽油"},
    "coconut_oil": {"search": "Oil, coconut", "type": "sr_legacy_food", "zh": "椰子油"},
    "oysters_raw": {"search": "Oyster, *raw", "type": "sr_legacy_food", "zh": "生蚝(生)"},
}

NUTRIENT_NAMES = {
    1003: ("蛋白质", "g"), 1004: ("脂肪", "g"), 1005: ("碳水化合物", "g"),
    1008: ("能量", "kcal"), 1079: ("膳食纤维", "g"), 1051: ("水分", "g"), 1007: ("灰分", "g"),
    1087: ("钙", "mg"), 1091: ("磷", "mg"), 1092: ("钾", "mg"), 1093: ("钠", "mg"), 1090: ("镁", "mg"),
    1089: ("铁", "mg"), 1095: ("锌", "mg"), 1098: ("铜", "mg"), 1101: ("锰", "mg"), 1103: ("硒", "µg"),
    1104: ("维生素A", "IU"), 1110: ("维生素D", "IU"), 1109: ("维生素E", "mg"),
    1185: ("维生素K", "µg"), 1162: ("维生素C", "mg"),
    1165: ("维生素B1", "mg"), 1166: ("维生素B2", "mg"), 1167: ("维生素B3", "mg"),
    1170: ("维生素B5", "mg"), 1175: ("维生素B6", "mg"), 1178: ("维生素B12", "µg"),
    1177: ("叶酸", "µg"), 1180: ("胆碱", "mg"),
    1214: ("赖氨酸", "g"),
    1269: ("亚油酸LA", "g"), 1270: ("亚麻酸ALA", "g"),
    1278: ("EPA", "g"), 1272: ("DHA", "g"), 1271: ("花生四烯酸AA", "g"),
    1234: ("牛磺酸", "mg"),
    1253: ("胆固醇", "mg"), 1100: ("碘", "µg"),
    1257: ("总饱和脂肪酸", "g"), 1258: ("总单不饱和脂肪酸", "g"), 1292: ("总多不饱和脂肪酸", "g"),
    1210: ("蛋氨酸", "g"), 1212: ("半胱氨酸", "g"),
    1213: ("苯丙氨酸", "g"), 1215: ("酪氨酸", "g"),
    1216: ("苏氨酸", "g"), 1217: ("色氨酸", "g"),
    1218: ("缬氨酸", "g"), 1219: ("精氨酸", "g"),
    1220: ("组氨酸", "g"), 1221: ("异亮氨酸", "g"),
    1222: ("亮氨酸", "g"), 1223: ("丙氨酸", "g"),
    1224: ("天冬氨酸", "g"), 1225: ("谷氨酸", "g"),
    1226: ("甘氨酸", "g"), 1227: ("脯氨酸", "g"),
    1228: ("丝氨酸", "g"),
}


def match_pattern(desc, pattern):
    """简单通配符匹配：* 匹配任意字符序列"""
    regex = "^" + re.escape(pattern).replace("\\*", ".*") + "$"
    return bool(re.match(regex, desc, re.IGNORECASE))


def main():
    print("=" * 60)
    print("Building common ingredients nutrient database")
    print(f"Food CSV: {FOOD_CSV} ({os.path.getsize(FOOD_CSV)/1e6:.0f} MB)")
    print(f"Nutrient CSV: {FOOD_NUTRIENT_CSV} ({os.path.getsize(FOOD_NUTRIENT_CSV)/1e9:.1f} GB)")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)

    # Step 1: Find FDC IDs for all common ingredients (single pass through food.csv)
    print("\n[1/2] Scanning food.csv for ingredient FDC IDs...")
    fdc_map = {}  # key -> (fdc_id, description)
    found_count = 0

    with open(FOOD_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "")
            dtype = row.get("data_type", "")
            for key, info in COMMON_INGREDIENTS.items():
                if key in fdc_map:
                    continue
                if dtype == info["type"] and match_pattern(desc, info["search"]):
                    fdc_map[key] = (int(row["fdc_id"]), desc)
                    found_count += 1
                    print(f"  ✓ {info['zh']}: FDC={row['fdc_id']} ({desc})")

    print(f"\n  Found {found_count}/{len(COMMON_INGREDIENTS)} ingredients")

    # Collect all FDC IDs to search for
    target_fdc_ids = {v[0] for v in fdc_map.values()}
    fdc_to_keys = {}
    for key, (fdc_id, desc) in fdc_map.items():
        fdc_to_keys.setdefault(fdc_id, []).append(key)

    # Step 2: Single pass through food_nutrient.csv (1.7GB) collecting all nutrients
    print(f"\n[2/2] Scanning food_nutrient.csv (1.7GB) for {len(target_fdc_ids)} FDC IDs...")
    all_nutrients = {fdc_id: {} for fdc_id in target_fdc_ids}
    line_count = 0
    found_nutrient_count = 0

    with open(FOOD_NUTRIENT_CSV, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            if line_count % 5000000 == 0:
                print(f"  Scanned {line_count/1e6:.0f}M lines, found {found_nutrient_count} nutrient records...")

            # Fast check: does this line contain any of our FDC IDs?
            matched = False
            for fdc_id in target_fdc_ids:
                if f',"{fdc_id}",' in line:
                    matched = True
                    break

            if matched:
                fields = next(csv.reader([line]))
                if len(fields) >= 4:
                    try:
                        fdc = int(fields[1])
                        nid = int(fields[2])
                        amount = float(fields[3]) if fields[3] else 0.0
                        if fdc in all_nutrients and nid in NUTRIENT_NAMES:
                            name, unit = NUTRIENT_NAMES[nid]
                            all_nutrients[fdc][str(nid)] = {
                                "name": name,
                                "amount": amount,
                                "unit": unit,
                            }
                            found_nutrient_count += 1
                    except (ValueError, IndexError):
                        pass

    print(f"  Scanned {line_count/1e6:.0f}M lines total, found {found_nutrient_count} nutrient records")

    # Build final database
    database = {}
    for key, (fdc_id, desc) in fdc_map.items():
        nutrients = all_nutrients.get(fdc_id, {})
        database[key] = {
            "fdc_id": fdc_id,
            "description": desc,
            "zh_name": COMMON_INGREDIENTS[key]["zh"],
            "nutrients_per_100g": nutrients,
            "nutrient_count": len(nutrients),
        }
        print(f"  {COMMON_INGREDIENTS[key]['zh']}: {len(nutrients)} nutrients")

    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

    total_nutrients = sum(v["nutrient_count"] for v in database.values())
    print(f"\n{'='*60}")
    print(f"Done! {len(database)} ingredients, {total_nutrients} total nutrient records")
    print(f"Output: {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
