#!/usr/bin/env python3
"""
诊断脚本：检查哪些 FDC ID 在 food.csv 中存在，但在 food_nutrient.csv 中缺失。
"""
import csv
from pathlib import Path

DATA_DIR = Path(r"E:\1-Projects\FEED\fooddata_temp\_full_extract")
FOOD_CSV = DATA_DIR / "food.csv"
FOOD_NUTRIENT_CSV = DATA_DIR / "food_nutrient.csv"

# v2 脚本中的所有 FDC ID
INGREDIENTS = {
    174030: "牛肉末(90%瘦)",
    169451: "牛肝",
    168625: "牛心",
    169449: "牛肾",
    169454: "牛脾",
    171077: "鸡胸肉(去皮去骨)",
    172385: "鸡腿肉",
    171060: "鸡肝",
    171458: "鸡心",
    167810: "猪瘦肉",
    167862: "猪肝",
    168267: "猪心",
    168270: "猪肾",
    172479: "羊肉(瘦)",
    172531: "羊肝",
    172410: "鸭肉(纯肉)",
    173686: "三文鱼(大西洋野生)",
    173706: "金枪鱼(蓝鳍生)",
    171287: "全蛋(生鲜)",
    172184: "蛋黄(生)",
    170379: "西兰花(生)",
    168462: "菠菜(生)",
    170393: "胡萝卜(生)",
    168482: "红薯(生)",
    168448: "南瓜(生)",
    168469: "西葫芦(生)",
    171661: "燕麦(干)",
    169703: "糙米(生)",
    168874: "藜麦(生)",
    172343: "三文鱼油",
    171017: "葵花籽油",
    171412: "椰子油",
}

# 已有数据的 FDC ID
FOUND_IDS = {168448, 167810, 170379, 168462, 174030, 171412, 172343, 172479}

print("=" * 70)
print("Step 1: Checking food.csv for all FDC IDs")
print("=" * 70)

found_in_food = {}
not_in_food = []

with open(FOOD_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            fdc_id = int(row["fdc_id"])
        except (ValueError, KeyError):
            continue
        if fdc_id in INGREDIENTS:
            found_in_food[fdc_id] = row.get("description", "")
            found_in_food[fdc_id] += f" | data_type={row.get('data_type', '')}"

for fdc_id, name in sorted(INGREDIENTS.items()):
    if fdc_id in found_in_food:
        status = "OK" if fdc_id in FOUND_IDS else "IN FOOD BUT NO NUTRIENTS"
        print(f"  {name}: FDC={fdc_id} -> {status}")
        if fdc_id not in FOUND_IDS:
            print(f"    desc: {found_in_food[fdc_id]}")
    else:
        not_in_food.append(fdc_id)
        print(f"  {name}: FDC={fdc_id} -> NOT IN food.csv!")

print(f"\n  Found in food.csv: {len(found_in_food)}/{len(INGREDIENTS)}")
print(f"  Not in food.csv: {len(not_in_food)}")

if not_in_food:
    print("\n" + "=" * 70)
    print("Step 2: Searching food.csv for alternative descriptions")
    print("=" * 70)
    # Search for similar descriptions
    search_terms = {}
    for fdc_id in not_in_food:
        name = INGREDIENTS[fdc_id]
        # Extract key search term from Chinese name
        if "牛" in name:
            search_terms[fdc_id] = ["Beef"]
        elif "鸡" in name:
            search_terms[fdc_id] = ["Chicken"]
        elif "猪" in name:
            search_terms[fdc_id] = ["Pork"]
        elif "羊" in name:
            search_terms[fdc_id] = ["Lamb"]
        elif "鸭" in name:
            search_terms[fdc_id] = ["Duck"]
        elif "三文鱼" in name:
            search_terms[fdc_id] = ["Salmon"]
        elif "金枪鱼" in name:
            search_terms[fdc_id] = ["Tuna"]
        elif "蛋" in name:
            search_terms[fdc_id] = ["Egg"]
        elif "胡萝卜" in name:
            search_terms[fdc_id] = ["Carrot"]
        elif "红薯" in name:
            search_terms[fdc_id] = ["Sweet potato"]
        elif "西葫芦" in name:
            search_terms[fdc_id] = ["Squash, summer, zucchini"]
        elif "燕麦" in name:
            search_terms[fdc_id] = ["Oats"]
        elif "糙米" in name:
            search_terms[fdc_id] = ["Rice, brown"]
        elif "藜麦" in name:
            search_terms[fdc_id] = ["Quinoa"]
        elif "葵花" in name:
            search_terms[fdc_id] = ["Oil, sunflower"]

    # Collect all candidates
    candidates = {fdc_id: [] for fdc_id in not_in_food}
    with open(FOOD_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "")
            fdc_id_str = row.get("fdc_id", "")
            try:
                fdc_id = int(fdc_id_str)
            except ValueError:
                continue
            for missing_id, terms in search_terms.items():
                if missing_id in found_in_food:
                    continue
                for term in terms:
                    if term.lower() in desc.lower() and "raw" in desc.lower():
                        candidates[missing_id].append((fdc_id, desc, row.get("data_type", "")))

    # Print top candidates
    for fdc_id in not_in_food:
        name = INGREDIENTS[fdc_id]
        cands = candidates[fdc_id]
        print(f"\n  {name} (FDC={fdc_id}): {len(cands)} raw candidates found")
        for cid, cdesc, dtype in cands[:5]:
            print(f"    -> FDC={cid} | {cdesc} | {dtype}")

# Now check food_nutrient.csv for missing IDs that ARE in food.csv
missing_but_in_food = [fid for fid in INGREDIENTS if fid in found_in_food and fid not in FOUND_IDS]
if missing_but_in_food:
    print("\n" + "=" * 70)
    print(f"Step 3: Checking food_nutrient.csv for {len(missing_but_in_food)} IDs that exist in food.csv")
    print("=" * 70)

    target_strings = {f',"{fid}",' for fid in missing_but_in_food}
    found_in_nutrient = set()

    line_count = 0
    with open(FOOD_NUTRIENT_CSV, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            if line_count % 5000000 == 0:
                print(f"  Scanned {line_count/1e6:.0f}M lines...")
            for ts in target_strings:
                if ts in line:
                    fields = next(csv.reader([line]))
                    if len(fields) >= 4:
                        try:
                            fdc = int(fields[1])
                            if fdc in missing_but_in_food:
                                found_in_nutrient.add(fdc)
                        except (ValueError, IndexError):
                            pass
                    break

    print(f"\n  Found in food_nutrient.csv: {len(found_in_nutrient)}/{len(missing_but_in_food)}")
    for fid in missing_but_in_food:
        name = INGREDIENTS[fid]
        status = "FOUND" if fid in found_in_nutrient else "NOT FOUND"
        print(f"    {name} (FDC={fid}): {status}")

print("\nDone!")
