#!/usr/bin/env python3
import json
data = json.load(open(r'C:\Users\lucci\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a771d667024180e389cecd4\.trae\skills\pet-cooked-recipe\references\common_ingredients_nutrients.json', 'r', encoding='utf-8'))

for key in ['beef_ground_90lean_raw', 'beef_liver_raw', 'chicken_breast_skinless_raw', 'salmon_atlantic_wild_raw', 'egg_whole_raw', 'spinach_raw']:
    item = data[key]
    n = item['nutrients_per_100g']
    print(f"\n{item['zh_name']} ({item['fdc_id']}): {item['nutrient_count']} nutrients")
    for nid in ['1003','1004','1008','1087','1091','1095','1103','1165','1178']:
        if nid in n:
            v = n[nid]
            print(f"  {v['name']}: {v['amount']} {v['unit']}")
        else:
            print(f"  [missing nid={nid}]")
