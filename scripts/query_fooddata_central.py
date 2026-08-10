#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\food#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc_id": row["fdc_id"],
                    "description": row["description"],
                    "data_type": dtype,
                    "priority": priority,
                })

    results.sort(key=lambda x: (x["priority"],#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc_id": row["fdc_id"],
                    "description": row["description"],
                    "data_type": dtype,
                    "priority": priority,
                })

    results.sort(key=lambda x: (x["priority"], x["description"]))
    return results[:limit]

def get_nutrients_for_food(fdc_id):
    path = os.path.join(DATA_DIR, "food_nutrient.csv")
    nutrients#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc_id": row["fdc_id"],
                    "description": row["description"],
                    "data_type": dtype,
                    "priority": priority,
                })

    results.sort(key=lambda x: (x["priority"], x["description"]))
    return results[:limit]

def get_nutrients_for_food(fdc_id):
    path = os.path.join(DATA_DIR, "food_nutrient.csv")
    nutrients = {}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["fdc_id"] == fdc_id:#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc_id": row["fdc_id"],
                    "description": row["description"],
                    "data_type": dtype,
                    "priority": priority,
                })

    results.sort(key=lambda x: (x["priority"], x["description"]))
    return results[:limit]

def get_nutrients_for_food(fdc_id):
    path = os.path.join(DATA_DIR, "food_nutrient.csv")
    nutrients = {}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["fdc_id"] == fdc_id:
                nid = int(row["nutrient_id"])
                if nid in NUTRIENT_IDS:
                    amount = float(row["amount"]) if row["amount"] else 0
                    unit = row.get("unit_name",#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc_id": row["fdc_id"],
                    "description": row["description"],
                    "data_type": dtype,
                    "priority": priority,
                })

    results.sort(key=lambda x: (x["priority"], x["description"]))
    return results[:limit]

def get_nutrients_for_food(fdc_id):
    path = os.path.join(DATA_DIR, "food_nutrient.csv")
    nutrients = {}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["fdc_id"] == fdc_id:
                nid = int(row["nutrient_id"])
                if nid in NUTRIENT_IDS:
                    amount = float(row["amount"]) if row["amount"] else 0
                    unit = row.get("unit_name", "")
                    nutrients[nid] = {
                        "name": NUTRIENT_IDS[nid],
                        "amount": amount,
                        "unit": unit,
                    }

    return nutrients

def format_output(food#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc_id": row["fdc_id"],
                    "description": row["description"],
                    "data_type": dtype,
                    "priority": priority,
                })

    results.sort(key=lambda x: (x["priority"], x["description"]))
    return results[:limit]

def get_nutrients_for_food(fdc_id):
    path = os.path.join(DATA_DIR, "food_nutrient.csv")
    nutrients = {}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["fdc_id"] == fdc_id:
                nid = int(row["nutrient_id"])
                if nid in NUTRIENT_IDS:
                    amount = float(row["amount"]) if row["amount"] else 0
                    unit = row.get("unit_name", "")
                    nutrients[nid] = {
                        "name": NUTRIENT_IDS[nid],
                        "amount": amount,
                        "unit": unit,
                    }

    return nutrients

def format_output(food, nutrients):
    lines = []
    lines.append(f"FDC ID: {food['fdc_id']}")
    lines.append(f"Description: {food['description']}")
    lines.append(f"Data Type#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc_id": row["fdc_id"],
                    "description": row["description"],
                    "data_type": dtype,
                    "priority": priority,
                })

    results.sort(key=lambda x: (x["priority"], x["description"]))
    return results[:limit]

def get_nutrients_for_food(fdc_id):
    path = os.path.join(DATA_DIR, "food_nutrient.csv")
    nutrients = {}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["fdc_id"] == fdc_id:
                nid = int(row["nutrient_id"])
                if nid in NUTRIENT_IDS:
                    amount = float(row["amount"]) if row["amount"] else 0
                    unit = row.get("unit_name", "")
                    nutrients[nid] = {
                        "name": NUTRIENT_IDS[nid],
                        "amount": amount,
                        "unit": unit,
                    }

    return nutrients

def format_output(food, nutrients):
    lines = []
    lines.append(f"FDC ID: {food['fdc_id']}")
    lines.append(f"Description: {food['description']}")
    lines.append(f"Data Type: {food['data_type']}")
    lines.append(f"{'Nutrient':<35} {'Amount':<12} {'Unit'}")
    lines.append("-" * 60)

    for nid in sorted#!/usr/bin/env python3
"""
FoodData Central 食材营养查询脚本
用法: python query_fooddata_central.py "ground beef" [--limit 5] [--dtype foundation,sr_legacy]
数据源: E:\1-Projects\FEED\fooddata_temp\_full_extract\
"""

import csv
import sys
import os
import argparse
from collections import defaultdict

DATA_DIR = r"E:\1-Projects\FEED\fooddata_temp\_full_extract"
NUTRIENT_DIR = r"E:\1-Projects\FEED\fooddata_temp"

NUTRIENT_IDS = {
    1003: "Protein (g)",
    1004: "Total Fat (g)",
    1005: "Carbohydrate (g)",
    1008: "Energy (kcal)",
    1079: "Fiber (g)",
    1051: "Water (g)",
    1007: "Ash (g)",
    1087: "Calcium (mg)",
    1091: "Phosphorus (mg)",
    1092: "Potassium (mg)",
    1093: "Sodium (mg)",
    1090: "Magnesium (mg)",
    1089: "Iron (mg)",
    1095: "Zinc (mg)",
    1098: "Copper (mg)",
    1101: "Manganese (mg)",
    1100: "Iodine (µg)",
    1103: "Selenium (µg)",
    1104: "Vitamin A (µg RAE)",
    1109: "Vitamin E (mg)",
    1110: "Vitamin D (µg)",
    1185: "Vitamin K (µg)",
    1162: "Vitamin C (mg)",
    1165: "Thiamin B1 (mg)",
    1166: "Riboflavin B2 (mg)",
    1167: "Niacin B3 (mg)",
    1170: "Pantothenic acid B5 (mg)",
    1175: "Vitamin B6 (mg)",
    1177: "Folate (µg)",
    1178: "Vitamin B12 (µg)",
    1180: "Choline (mg)",
    1234: "Taurine (mg)",
    1214: "Lysine (g)",
    1269: "Linoleic acid LA (g)",
    1270: "Alpha-linolenic acid ALA (g)",
    1271: "Arachidonic acid AA (g)",
    1272: "DHA (g)",
    1278: "EPA (g)",
}

DATA_TYPE_PRIORITY = {
    "foundation_food": 1,
    "sr_legacy_food": 2,
    "survey_fndds_food": 3,
    "branded_food": 4,
}

def load_nutrient_names():
    path = os.path.join(NUTRIENT_DIR, "nutrient.csv")
    names = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = int(row["id"])
            names[nid] = row["name"]
    return names

def search_foods(query, limit=10, dtypes=None):
    path = os.path.join(DATA_DIR, "food.csv")
    results = []
    query_lower = query.lower()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "").lower()
            if query_lower in desc:
                dtype = row.get("data_type", "")
                if dtypes and dtype not in dtypes:
                    continue
                priority = DATA_TYPE_PRIORITY.get(dtype, 5)
                results.append({
                    "fdc_id": row["fdc_id"],
                    "description": row["description"],
                    "data_type": dtype,
                    "priority": priority,
                })

    results.sort(key=lambda x: (x["priority"], x["description"]))
    return results[:limit]

def get_nutrients_for_food(fdc_id):
    path = os.path.join(DATA_DIR, "food_nutrient.csv")
    nutrients = {}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["fdc_id"] == fdc_id:
                nid = int(row["nutrient_id"])
                if nid in NUTRIENT_IDS:
                    amount = float(row["amount"]) if row["amount"] else 0
                    unit = row.get("unit_name", "")
                    nutrients[nid] = {
                        "name": NUTRIENT_IDS[nid],
                        "amount": amount,
                        "unit": unit,
                    }

    return nutrients

def format_output(food, nutrients):
    lines = []
    lines.append(f"FDC ID: {food['fdc_id']}")
    lines.append(f"Description: {food['description']}")
    lines.append(f"Data Type: {food['data_type']}")
    lines.append(f"{'Nutrient':<35} {'Amount':<12} {'Unit'}")
    lines.append("-" * 60)

    for nid in sorted(NUTRIENT_IDS.keys()):
        if nid in nutrients:
            n = nutrients[nid]
            lines.append(f"{n['name']:<35} {n['amount']:<12.4f} {n['