#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python fooddata_query.py "牛肉" ["chicken" "beef liver" ...]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""
import csv
import sys
import os
import json
from pathlib import Path

DATA_DIR = Path(r"E:\1-Projects\FEED\fooddata_temp\_full_extract")
NUTRIENT_CSV = DATA_DIR / "nutrient.csv"
FOOD_CSV = DATA_DIR / "food.csv"
FOOD_NUTRIENT_CSV = DATA_DIR / "food_nutrient.csv"
FOUNDATION_CSV = DATA_DIR / "foundation_food.csv"
SR_LEGACY_CSV = DATA_DIR / "sr_legacy_food.csv"

# 宠物配方关键营养素 ID → 中文名映射
KEY_NUTRIENTS = {
    1003: ("蛋白质", "g"), 1004: ("脂肪", "g"), 1005: ("碳水化合物", "g"),
    1008: ("能量", "kcal"), 1079: ("膳食纤维", "g"), 1051: ("水分", "g"),
    1087: ("钙", "mg"), 1091: ("磷", "mg"), 1092: ("钾", "mg"),
    1093: ("钠", "mg"), 1090: ("镁", "mg"),
    1089: ("铁", "mg"), 1095: ("锌", "mg"), 1098: ("铜", "mg"),
    1101: ("锰", "mg"), 1100: ("碘", "µg"), 1103: ("硒", "µg"),
    1104: ("维生素A", "IU"), 1110: ("维生素D", "IU"), 1109: ("维生素E", "IU"),
    1185: ("维生素K", "µg"), 1162: ("维生素C", "mg"),
    1165: ("维生素B1", "mg"), 1166: ("维生素B2", "mg"), 1167: ("维生素B3", "mg"),
    1170: ("维生素B5", "mg"), 1175: ("维生素B6", "mg"), 1178: ("维生素B12", "µg"),
    1177: ("叶酸", "µg"), 1180: ("胆碱", "mg"),
    1234: ("牛磺酸", "mg"), 1214: ("赖氨酸", "g"),
    1269: ("亚油酸LA", "g"), 1270: ("亚麻酸ALA", "g"),
    1278: ("EPA", "g"), 1272: ("DHA", "g"), 1271: ("花生四烯酸AA", "g"),
}


def load_nutrient_names():
    names = {}
    with open(NUTRIENT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names


def search_foods(query, max_results=10):
    results = []
    query_lower = query.lower().strip()
    with open(FOOD_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                fdc_id = int(row["fdc_id"])
                data_type = row.get("data_type", "")
                results.append({
                    "fdc_id": fdc_id,
                    "description": row.get("description", ""),
                    "data_type": data_type,
                    "food_category_id": row.get("food_category_id", ""),
                })
                if len(results) >= max_results:
                    break
    # Sort by data type priority
    priority = {"foundation_food": 0, "sr_legacy_food": 1, "survey_fndds_food": 2, "branded_food": 3}
    results.sort(key=lambda x: priority.get(x["data_type"], 4))
    return results


def get_nutrients(fdc_id):
    nutrients = {}
    with open(FOOD_NUTRIENT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["fdc_id"]) == fdc_id:
                nid = int(row["nutrient_id"])
                if nid in KEY_NUTRIENTS:
                    name, unit = KEY_NUTRIENTS[nid]
                    val = float(row.get("amount", 0))
                    nutrients[nid] = {
                        "name": name,
                        "amount": val,
                        "unit": unit,
                    }
    return nutrients


def query_ingredient(query, max_results=5):
    print(f"\n{'='*60}")
    print(f"搜索: {query}")
    print(f"{'='*60}")
    foods = search_foods(query, max_results)
    if not foods:
        print("  未找到匹配食材")
        return None
    for i, food in enumerate(foods):
        print(f"\n[{i+1}] FDC ID: {food['fdc_id']}")
        print(f"    名称: {food['description']}")
        print(f"    类型: {food['data_type']}")
        nutrients = get_nutrients(food["fdc_id"])
        if nutrients:
            print(f"    营养成分 (每100g):")
            for nid in sorted(KEY_NUTRIENTS.keys()):
                if nid in nutrients:
                    n = nutrients[nid]
                    print(f"      {n['name']:12s}: {n['amount']:>10.2f} {n['unit']}")
        else:
            print(f"    (无营养数据)")
    return foods


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python fooddata_query.py <食材名称> [食材名称2 ...]")
        print("示例: python fooddata_query.py \"beef\" \"chicken liver\"")
        sys.exit(1)
    for query in sys.argv[1:]:
        query_ingredient(query)
