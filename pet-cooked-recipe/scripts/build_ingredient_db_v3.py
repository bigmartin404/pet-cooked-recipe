#!/usr/bin/env python3
"""
预建宠物配方常用食材营养数据库（高效版v3）。
使用手动查找的 FDC ID 列表，单次扫描 food_nutrient.csv 提取所有营养数据。
优化：使用集合查找 + 快速前缀过滤，避免逐行多次字符串搜索。
"""
import csv
import json
import os
from pathlib import Path

DATA_DIR = Path(r"E:\1-Projects\FEED\fooddata_temp\_full_extract")
FOOD_NUTRIENT_CSV = DATA_DIR / "food_nutrient.csv"
OUTPUT_FILE = Path(__file__).parent.parent / "references" / "common_ingredients_nutrients.json"

# 手动查找到的 FDC ID 列表（32种食材）
INGREDIENTS = {
    "beef_ground_90lean_raw": {"fdc_id": 174030, "zh": "牛肉末(90%瘦)", "desc": "Beef, ground, 90% lean meat / 10% fat, raw"},
    "beef_liver_raw": {"fdc_id": 169451, "zh": "牛肝", "desc": "Beef, variety meats and by-products, liver, raw"},
    "beef_heart_raw": {"fdc_id": 168625, "zh": "牛心", "desc": "Beef, variety meats and by-products, heart, raw"},
    "beef_kidney_raw": {"fdc_id": 169449, "zh": "牛肾", "desc": "Beef, variety meats and by-products, kidneys, raw"},
    "beef_spleen_raw": {"fdc_id": 169454, "zh": "牛脾", "desc": "Beef, variety meats and by-products, spleen, raw"},
    "chicken_breast_skinless_raw": {"fdc_id": 171077, "zh": "鸡胸肉(去皮去骨)", "desc": "Chicken, breast, skinless, boneless, meat only, raw"},
    "chicken_thigh_raw": {"fdc_id": 172385, "zh": "鸡腿肉", "desc": "Chicken, thigh, meat and skin, raw"},
    "chicken_liver_raw": {"fdc_id": 171060, "zh": "鸡肝", "desc": "Chicken, liver, all classes, raw"},
    "chicken_heart_raw": {"fdc_id": 171458, "zh": "鸡心", "desc": "Chicken, heart, all classes, raw"},
    "pork_lean_raw": {"fdc_id": 167810, "zh": "猪瘦肉", "desc": "Pork, fresh, composite of trimmed leg, loin, shoulder, separable lean and fat, raw"},
    "pork_liver_raw": {"fdc_id": 167862, "zh": "猪肝", "desc": "Pork, fresh, variety meats and by-products, liver, raw"},
    "pork_heart_raw": {"fdc_id": 168267, "zh": "猪心", "desc": "Pork, fresh, variety meats and by-products, heart, raw"},
    "pork_kidney_raw": {"fdc_id": 168270, "zh": "猪肾", "desc": "Pork, fresh, variety meats and by-products, kidneys, raw"},
    "lamb_lean_raw": {"fdc_id": 172479, "zh": "羊肉(瘦)", "desc": "Lamb, composite of trimmed retail cuts, separable lean and fat, raw"},
    "lamb_liver_raw": {"fdc_id": 172531, "zh": "羊肝", "desc": "Lamb, variety meats and by-products, liver, raw"},
    "duck_meat_raw": {"fdc_id": 172410, "zh": "鸭肉(纯肉)", "desc": "Duck, domesticated, meat only, raw"},
    "salmon_atlantic_wild_raw": {"fdc_id": 173686, "zh": "三文鱼(大西洋野生)", "desc": "Fish, salmon, Atlantic, wild, raw"},
    "tuna_bluefin_raw": {"fdc_id": 173706, "zh": "金枪鱼(蓝鳍生)", "desc": "Fish, tuna, fresh, bluefin, raw"},
    "egg_whole_raw": {"fdc_id": 171287, "zh": "全蛋(生鲜)", "desc": "Egg, whole, raw, fresh"},
    "egg_yolk_raw": {"fdc_id": 172184, "zh": "蛋黄(生)", "desc": "Egg, yolk, raw, fresh"},
    "broccoli_raw": {"fdc_id": 170379, "zh": "西兰花(生)", "desc": "Broccoli, raw"},
    "spinach_raw": {"fdc_id": 168462, "zh": "菠菜(生)", "desc": "Spinach, raw"},
    "carrot_raw": {"fdc_id": 170393, "zh": "胡萝卜(生)", "desc": "Carrots, raw"},
    "sweet_potato_raw": {"fdc_id": 168482, "zh": "红薯(生)", "desc": "Sweet potato, raw, unprepared"},
    "pumpkin_raw": {"fdc_id": 168448, "zh": "南瓜(生)", "desc": "Pumpkin, raw"},
    "zucchini_raw": {"fdc_id": 168469, "zh": "西葫芦(生)", "desc": "Squash, summer, zucchini, includes skin, raw"},
    "oats_dry": {"fdc_id": 171661, "zh": "燕麦(干)", "desc": "Cereals, oats, instant, fortified, plain, dry"},
    "brown_rice_raw": {"fdc_id": 169703, "zh": "糙米(生)", "desc": "Rice, brown, long-grain, raw"},
    "quinoa_raw": {"fdc_id": 168874, "zh": "藜麦(生)", "desc": "Quinoa, uncooked"},
    "fish_oil_salmon": {"fdc_id": 172343, "zh": "三文鱼油", "desc": "Fish oil, salmon"},
    "sunflower_oil": {"fdc_id": 171017, "zh": "葵花籽油", "desc": "Oil, sunflower, linoleic (less than 60%)"},
    "coconut_oil": {"fdc_id": 171412, "zh": "椰子油", "desc": "Oil, coconut"},
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
    1222: ("亮氨酸", "g"),
}

# 构建 FDC ID -> 食材key 的映射
FDC_TO_KEY = {info["fdc_id"]: key for key, info in INGREDIENTS.items()}

# 所有目标 FDC ID
TARGET_IDS = set(FDC_TO_KEY.keys())

# 将 FDC ID 转为字符串形式用于快速查找
# food_nutrient.csv 格式: id,fdc_id,nutrient_id,amount,...
# 所以每行第二个字段是 fdc_id
TARGET_ID_STRS = {str(fid): fid for fid in TARGET_IDS}


def main():
    print("=" * 60)
    print(f"Building nutrient database for {len(INGREDIENTS)} ingredients")
    print(f"Single pass through food_nutrient.csv (1.7GB)")
    print("=" * 60)

    all_nutrients = {fid: {} for fid in TARGET_IDS}
    line_count = 0
    found_count = 0
    found_ingredients = set()

    with open(FOOD_NUTRIENT_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        print(f"  Header: {header}")

        for fields in reader:
            line_count += 1
            if line_count % 2000000 == 0:
                print(f"  Scanned {line_count/1e6:.0f}M lines, found {found_count} records, {len(found_ingredients)}/{len(TARGET_IDS)} ingredients...")

            if len(fields) < 4:
                continue

            # fdc_id is in column 1 (0-indexed)
            fdc_str = fields[1]
            if fdc_str not in TARGET_ID_STRS:
                continue

            fdc_id = TARGET_ID_STRS[fdc_str]
            found_ingredients.add(fdc_id)

            try:
                nid = int(fields[2])
                amount_str = fields[3]
                amount = float(amount_str) if amount_str else 0.0
            except (ValueError, IndexError):
                continue

            if nid in NUTRIENT_NAMES:
                name, unit = NUTRIENT_NAMES[nid]
                all_nutrients[fdc_id][str(nid)] = {
                    "name": name,
                    "amount": amount,
                    "unit": unit,
                }
                found_count += 1

    print(f"\n  Scanned {line_count/1e6:.0f}M lines total")
    print(f"  Found {found_count} nutrient records for {len(found_ingredients)}/{len(TARGET_IDS)} ingredients")

    # Build final database
    database = {}
    for key, info in INGREDIENTS.items():
        fdc = info["fdc_id"]
        nutrients = all_nutrients.get(fdc, {})
        database[key] = {
            "fdc_id": fdc,
            "description": info["desc"],
            "zh_name": info["zh"],
            "nutrients_per_100g": nutrients,
            "nutrient_count": len(nutrients),
        }
        status = "OK" if nutrients else "EMPTY"
        print(f"  {info['zh']}: {len(nutrients)} nutrients [{status}]")

    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

    total_nutrients = sum(v["nutrient_count"] for v in database.values())
    empty = [k for k, v in database.items() if v["nutrient_count"] == 0]
    print(f"\n{'='*60}")
    print(f"Done! {len(database)} ingredients, {total_nutrients} total nutrient records")
    if empty:
        print(f"WARNING: {len(empty)} ingredients have no nutrient data: {empty}")
    print(f"Output: {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
