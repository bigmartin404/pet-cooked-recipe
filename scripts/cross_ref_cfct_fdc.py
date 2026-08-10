#!/usr/bin/env python3
"""
交叉验证：将中国食物成分表数据与 FoodData Central 预建数据库对比，
输出补全后的对比表格数据。
"""
import json

# 加载预建数据库
with open(r'C:\Users\lucci\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a771d667024180e389cecd4\.trae\skills\pet-cooked-recipe\references\common_ingredients_nutrients.json', 'r', encoding='utf-8') as f:
    fdc_db = json.load(f)

# CFCT食材 -> 预建数据库key 的映射
CFCT_TO_FDC = {
    "菠菜": "spinach_raw",
    "西兰花": "broccoli_raw",
    "红薯": "sweet_potato_raw",
    "南瓜": "pumpkin_raw",
    "胡萝卜": "carrot_raw",
    "芹菜": None,  # 不在预建库中
    "燕麦": "oats_dry",
    "糙米": "brown_rice_raw",
    "藜麦": "quinoa_raw",
    "牛肉(瘦)": "beef_ground_90lean_raw",  # 近似
    "猪肉(瘦)": "pork_lean_raw",
    "鸡胸肉": "chicken_breast_skinless_raw",
    "羊肉(瘦)": "lamb_lean_raw",
    "鸭肉": "duck_meat_raw",
    "牛肝": "beef_liver_raw",
    "鸡肝": "chicken_liver_raw",
    "猪心": "pork_heart_raw",
    "猪肾": "pork_kidney_raw",
    "三文鱼": "salmon_atlantic_wild_raw",
    "沙丁鱼": None,  # 不在预建库中
    "鸡蛋": "egg_whole_raw",
    "蛋黄": "egg_yolk_raw",
    "牛心": "beef_heart_raw",
    "牛肾": "beef_kidney_raw",
    "牛脾": "beef_spleen_raw",
    "鸡腿肉": "chicken_thigh_raw",
    "鸡心": "chicken_heart_raw",
    "羊肝": "lamb_liver_raw",
    "金枪鱼": "tuna_bluefin_raw",
}

# 营养素ID -> 中文名
NID_MAP = {
    "1003": "蛋白质", "1004": "脂肪", "1005": "碳水化合物", "1008": "能量",
    "1079": "膳食纤维", "1051": "水分", "1007": "灰分",
    "1087": "钙", "1091": "磷", "1092": "钾", "1093": "钠", "1090": "镁",
    "1089": "铁", "1095": "锌", "1098": "铜", "1101": "锰", "1103": "硒",
    "1104": "维生素A", "1110": "维生素D", "1109": "维生素E",
    "1185": "维生素K", "1162": "维生素C",
    "1165": "维生素B1", "1166": "维生素B2", "1167": "维生素B3",
    "1170": "维生素B5", "1175": "维生素B6", "1178": "维生素B12",
    "1177": "叶酸", "1180": "胆碱",
    "1253": "胆固醇", "1234": "牛磺酸",
    "1214": "赖氨酸", "1210": "蛋氨酸", "1212": "半胱氨酸",
    "1219": "精氨酸", "1220": "组氨酸", "1221": "异亮氨酸",
    "1222": "亮氨酸", "1216": "苏氨酸", "1217": "色氨酸", "1218": "缬氨酸",
    "1269": "亚油酸LA", "1270": "亚麻酸ALA",
    "1278": "EPA", "1272": "DHA", "1271": "花生四烯酸AA",
    "1257": "总饱和脂肪酸", "1258": "总单不饱和脂肪酸", "1292": "总多不饱和脂肪酸",
}

# 关键营养素列表（按宠物配方重要性排序）
KEY_NUTRIENTS_BASIC = ["1008", "1003", "1004", "1005", "1079", "1051", "1007"]
KEY_NUTRIENTS_MINERAL = ["1087", "1091", "1092", "1093", "1090", "1089", "1095", "1098", "1101", "1103"]
KEY_NUTRIENTS_VITAMIN = ["1104", "1165", "1166", "1167", "1162", "1109", "1178", "1177"]
KEY_NUTRIENTS_FAT = ["1257", "1258", "1292", "1269", "1270", "1278", "1272"]
KEY_NUTRIENTS_AMINO = ["1214", "1219", "1220", "1222", "1210", "1234"]
KEY_NUTRIENTS_OTHER = ["1253"]

def get_fdc_value(fdc_key, nid_str):
    """从预建数据库获取值"""
    if fdc_key and fdc_key in fdc_db:
        nutrients = fdc_db[fdc_key].get("nutrients_per_100g", {})
        if nid_str in nutrients:
            return nutrients[nid_str]["amount"], nutrients[nid_str]["unit"]
    return None, None

# 输出每个CFCT食材的FDC交叉验证数据
print("=" * 80)
print("CFCT 与 FoodData Central 交叉验证数据")
print("=" * 80)

for cfct_name, fdc_key in sorted(CFCT_TO_FDC.items(), key=lambda x: x[1] or ""):
    if fdc_key is None:
        print(f"\n{cfct_name}: 不在预建库中")
        continue

    if fdc_key not in fdc_db:
        print(f"\n{cfct_name} ({fdc_key}): 预建库中无数据")
        continue

    item = fdc_db[fdc_key]
    n = item["nutrients_per_100g"]
    print(f"\n{cfct_name} -> {fdc_key} ({item['zh_name']}) FDC={item['fdc_id']} [{item['nutrient_count']} nutrients]")

    # 输出所有营养素
    for nid_str in sorted(NID_MAP.keys(), key=lambda x: int(x)):
        if nid_str in n:
            v = n[nid_str]
            print(f"  {NID_MAP[nid_str]}({nid_str}): {v['amount']} {v['unit']}")

# 输出预建库中有但CFCT中没有的食材
print("\n" + "=" * 80)
print("预建库中有但CFCT中没有的食材:")
print("=" * 80)
cfct_keys = set(CFCT_TO_FDC.values())
for key, item in fdc_db.items():
    if key not in cfct_keys:
        print(f"  {key}: {item['zh_name']} ({item['nutrient_count']} nutrients)")
