import copy


import pydash as _
import re

from constants import TITLING, GENDERS, CATEGORY_NAMES, CATEGORY_FULL_PROCESS, TITLE_TRANSLATIONS, \
    SPU_CHANGE_LINES

titling_copy = copy.deepcopy(TITLING)
spu_change_lines_copy = copy.deepcopy(SPU_CHANGE_LINES)


# region Function remove_substring
def remove_substring(s, sub, replace=""):
    s_lower = s.lower()
    sub_lower = sub.lower()

    start = s_lower.find(sub_lower)

    if start != -1:
        end = start + len(sub)

        s = s[:start] + " ".join(map(str.capitalize, replace.split())) + s[end:]

    return s


# endregion


# region Function remove_chinese_symbols
def remove_chinese_symbols(text):
    chinese_pattern = "[\u4e00-\u9FFF|\u3400-\u4DBF|\U00020000-\U0002A6DF|\U0002A700-\U0002B73F|\U0002B740-\U0002B81F|\U0002B820-\U0002CEAF|\uF900-\uFAFF|\U0002F800-\U0002FA1F]"
    without_chinese = re.sub(chinese_pattern, '', text)
    without_chinese = ' '.join(without_chinese.split())
    return without_chinese


# endregion


def get_starting_categories(data):
    if str(data["categoryId"]) in CATEGORY_FULL_PROCESS:
        return copy.deepcopy(CATEGORY_FULL_PROCESS[str(data["categoryId"])]["categories_to_add_directly"])
    else:
        return ["Другие аксессуары"]


def translate_title(title):
    res = ""
    for subtitle in TITLE_TRANSLATIONS:
        if subtitle in title and TITLE_TRANSLATIONS[subtitle] not in title:
            res += TITLE_TRANSLATIONS[subtitle] + " "
    return res


def process_preprocessed_api_data(preprocessed_data):
    # Вновь делаю копию, не знаю зачем, но где-то точно надо ее сделать.
    data = copy.deepcopy(preprocessed_data)

    # Этот словарь вернет данная ф-ция
    res = dict()

    res["is_collab"] = False
    res["collab_names"] = list()
    res["brands"] = list()
    res["model"] = remove_chinese_symbols(data["title"])
    res["lines"] = list()

    title = " " + data["title"].lower() + " "

    # region Find main brand
    brand_id = ""

    for brand_id1 in map(str, data["allBrands"]):
        if brand_id1 not in titling_copy:
            continue

        brand_id = brand_id1
        break
    # endregion

    # region Find lines
    lines = list()

    for line in _.get(titling_copy[brand_id], "lines", list()):
        for line_name in line["line_names"]:
            if line_name.lower() in title.lower() and none_in_string(title.lower(), _.get(line, "line_skip_names", [])):
                lines.append(line)
                break

        if len(lines) != 0 and not _.get(titling_copy[brand_id], "many_lines", False):
            break
    # endregion

    # region Find collabs
    collabs = list()

    for collab in _.get(titling_copy[brand_id], "collaborations", dict()):
        if len(collabs) != 0 and not _.get(titling_copy[brand_id], "many_collaborations", False):
            break

        collab_added = False

        for collab_name in _.get(titling_copy[brand_id]["collaborations"][collab], "collab_brand_names", list()):
            if collab_name.lower() in title.lower() and none_in_string(title.lower(), _.get(
                    titling_copy[brand_id]["collaborations"][collab],
                    "collab_skip_names", list())):
                collabs.append(collab)
                collab_added = True
                break

        if collab_added:
            continue

        for collab_brand_id in _.get(titling_copy[brand_id]["collaborations"][collab], "collab_brand_ids", list()):
            if collab_brand_id in map(str, data["allBrands"]):
                collabs.append(collab)
                collab_added = True
                break

        if collab_added:
            continue

        if data["manufacturer_sku"] in _.get(titling_copy[brand_id]["collaborations"][collab], "collab_skus", list()):
            collabs.append(collab)
            collab_added = True

        if collab_added:
            continue
    # endregion

    # region Изменяю дополнительно какие-то линейки
    for spu_change_line_copy in spu_change_lines_copy:
        if spu_change_line_copy == str(data["spuId"]):
            for collabs_to_remove in _.get(spu_change_lines_copy[spu_change_line_copy], "collabs_to_remove", []):
                collabs.remove(collabs_to_remove)
    # endregion

    # region Crop collabs, lines and brands
    for collab in collabs:
        for collab_name in sorted(_.get(titling_copy[brand_id]["collaborations"][collab], "collab_brand_names", list()),
                                  key=lambda s: -len(s)):
            if collab_name.lower() in res["model"].lower():
                for collab_name_no_crop in sorted(
                        _.get(titling_copy[brand_id]["collaborations"][collab], "collab_brand_names_no_crop", list()),
                        key=lambda s: -len(s)):
                    if collab_name_no_crop.lower() in collab_name.lower():
                        res["model"] = remove_substring(res["model"], collab_name, collab_name_no_crop)
                        break
                else:
                    res["model"] = remove_substring(res["model"], collab_name)
    for line in lines:
        for line_name in sorted(_.get(line, "line_names", list()), key=lambda s: -len(s)):
            if line_name.lower() in res["model"].lower():
                for line_name_no_crop in sorted(_.get(line, "line_name_no_crop", list()), key=lambda s: -len(s)):
                    if line_name_no_crop.lower() in line_name.lower():
                        res["model"] = remove_substring(res["model"], line_name, line_name_no_crop)
                        break
                else:
                    res["model"] = remove_substring(res["model"], line_name)

    for brand_name in sorted(titling_copy[brand_id]["brand_names"], key=lambda s: -len(s)):
        if brand_name.lower() in res["model"].lower():
            res["model"] = remove_substring(res["model"], brand_name)
            break

    # endregion

    # region Try to replace "Другие Jordan 1" to "High/Mid/Low"
    other_jordan_1_line = {
        "path": [
            "Jordan",
            "Air Jordan 1",
            "Другие Air Jordan 1"
        ],
        "line_names": [
            "Air Jordan 1 ",
            "Air Jordan retro 1 ",
            "jordan 1 ",
            "jordan retro 1 "
        ],
        "line_name_no_crop": [
            "retro"
        ]
    }
    air_jordan_1_high_line = {
        "path": [
            "Jordan",
            "Air Jordan 1",
            "Air Jordan 1 High"
        ],
        "line_names": [
            "Air Jordan 1 high",
            "Air Jordan high 1 ",
            "Air Jordan 1 retro high",
            "air jordan retro 1 high",
            "air jordan retro high 1 ",
            "jordan 1 high",
            "jordan high 1 ",
            "jordan retro 1 high",
            "jordan retro high 1 ",
            "jordan 1 retro high",
            "Air Jordan 1 hi "
        ],
        "line_name_no_crop": [
            "retro"
        ]
    }
    air_jordan_1_mid_line = {
        "path": [
            "Jordan",
            "Air Jordan 1",
            "Air Jordan 1 Mid"
        ],
        "line_names": [
            "Air Jordan 1 mid",
            "Air Jordan mid 1 ",
            "Air Jordan 1 retro mid",
            "air jordan retro 1 mid",
            "air jordan retro high 1 ",
            "jordan 1 mid",
            "jordan mid 1 ",
            "jordan retro 1 mid",
            "jordan retro high 1 ",
            "jordan 1 retro mid"
        ],
        "line_name_no_crop": [
            "retro"
        ]
    }
    air_jordan_1_low_line = {
        "path": [
            "Jordan",
            "Air Jordan 1",
            "Air Jordan 1 Low"
        ],
        "line_names": [
            "Air Jordan 1 low",
            "Air Jordan low 1 ",
            "Air Jordan 1 retro low",
            "air jordan retro 1 low",
            "air jordan retro high 1 ",
            "jordan 1 low",
            "jordan low 1 ",
            "jordan retro 1 low",
            "jordan retro high 1 ",
            "jordan 1 retro low"
        ],
        "line_name_no_crop": [
            "retro"
        ]
    }
    if other_jordan_1_line in lines:
        if "高帮" in title.lower():
            lines.remove(other_jordan_1_line)
            lines.append(air_jordan_1_high_line)
        elif "低帮" in title.lower():
            lines.remove(other_jordan_1_line)
            lines.append(air_jordan_1_low_line)
        elif "中帮" in title.lower():
            lines.remove(other_jordan_1_line)
            lines.append(air_jordan_1_mid_line)
    # endregion

    # region Try to replace "Другие Dunk" to "High/Mid/Low"
    other_dunk_line = {
        "path": [
            "Nike",
            "Nike Dunk",
            "Другие Nike Dunk"
        ],
        "line_names": [
            "dunk"
        ],
        "line_skip_names": []
    }
    dunk_high_line = {
        "path": [
            "Nike",
            "Nike Dunk",
            "Nike Dunk High"
        ],
        "line_names": [
            "dunk high",
            "high dunk",
            "dunk pro high",
            "high pro dunk",
            "dunk sb high",
            "high sb dunk",
            "dunk sb pro high",
            "dunk pro sb high",
            "high pro sb dunk",
            "high sb pro dunk"
        ],
        "line_skip_names": [],
        "line_name_no_crop": [
            "pro sb",
            "sb pro",
            "pro",
            "sb"
        ]
    }
    dunk_mid_line = {
        "path": [
            "Nike",
            "Nike Dunk",
            "Nike Dunk Mid"
        ],
        "line_names": [
            "dunk mid",
            "mid dunk",
            "dunk pro mid",
            "mid pro dunk",
            "dunk sb mid",
            "mid sb dunk",
            "dunk sb pro mid",
            "dunk pro sb mid",
            "mid pro sb dunk",
            "mid sb pro dunk"
        ],
        "line_skip_names": [],
        "line_name_no_crop": [
            "pro sb",
            "sb pro",
            "pro",
            "sb"
        ]
    }
    dunk_low_line = {
        "path": [
            "Nike",
            "Nike Dunk",
            "Nike Dunk Low"
        ],
        "line_names": [
            "dunk low",
            "low dunk",
            "dunk pro low",
            "low pro dunk",
            "dunk sb low",
            "low sb dunk",
            "dunk sb pro low",
            "dunk pro sb low",
            "low pro sb dunk",
            "low sb pro dunk"
        ],
        "line_skip_names": [],
        "line_name_no_crop": [
            "pro sb",
            "sb pro",
            "pro",
            "sb"
        ]
    }
    if other_dunk_line in lines:
        if "高帮" in title.lower():
            lines.remove(other_dunk_line)
            lines.append(dunk_high_line)
        elif "低帮" in title.lower():
            lines.remove(other_dunk_line)
            lines.append(dunk_low_line)
        elif "中帮" in title.lower():
            lines.remove(other_dunk_line)
            lines.append(dunk_mid_line)
    # endregion

    # region Try to replace "Другие Nike AF1" to "High/Mid/Low"
    other_force_line = {
        "path": [
            "Nike",
            "Nike Air Force 1",
            "Другие Nike Air Force 1"
        ],
        "line_names": [
            "air force 1",
            "af1"
        ],
        "line_skip_names": []
    }
    force_high_line = {
        "path": [
            "Nike",
            "Nike Air Force 1",
            "Nike Air Force 1 High"
        ],
        "line_names": [
            "air force 1 high",
            "af1 high"
        ],
        "line_skip_names": []
    }
    force_mid_line = {
        "path": [
            "Nike",
            "Nike Air Force 1",
            "Nike Air Force 1 Mid"
        ],
        "line_names": [
            "air force 1 mid",
            "af1 mid"
        ],
        "line_skip_names": []
    }
    force_low_line = {
        "path": [
            "Nike",
            "Nike Air Force 1",
            "Nike Air Force 1 Low"
        ],
        "line_names": [
            "air force 1 low",
            "af1 low"
        ],
        "line_skip_names": []
    }
    if other_force_line in lines:
        if "高帮" in title.lower():
            lines.remove(other_force_line)
            lines.append(force_high_line)
        elif "低帮" in title.lower():
            lines.remove(other_force_line)
            lines.append(force_low_line)
        elif "中帮" in title.lower():
            lines.remove(other_force_line)
            lines.append(force_mid_line)
    # endregion

    # region Изменяю дополнительно какие-то линейки
    for spu_change_line_copy in spu_change_lines_copy:
        if spu_change_line_copy == str(data["spuId"]):
            for line_to_remove in _.get(spu_change_lines_copy[spu_change_line_copy], "lines_to_remove", []):
                lines.remove(line_to_remove)
            for line_to_add in _.get(spu_change_lines_copy[spu_change_line_copy], "lines_to_add", []):
                lines.append(line_to_add)
    # endregion

    # region Add lines, brands, collabs to res
    for brand_ids in map(str, data["allBrands"]):
        if brand_ids in titling_copy:
            res["brands"].append(titling_copy[brand_ids]["brand_names"][0])

    for line in lines:
        res["lines"].append(line["path"])

    for collab in collabs:
        res["collab_names"].append(collab)

    if len(collabs) > 0 or len(data["allBrands"]) > 1 or " x " in title.lower():
        res["is_collab"] = True

    # endregion

    # region Process date

    res["date"] = ""
    res["approximate_date"] = ""

    if data['releaseDate'] == "":
        res["date"] = "12.02.2021"

    data['releaseDate'] = data['releaseDate'].replace("年", "")

    if len(data['releaseDate'].split(".")) == 3:
        res["date"] = remove_chinese_symbols(data['releaseDate'])
        res["approximate_date"] = remove_chinese_symbols(data['releaseDate'])

        if len(res["approximate_date"].split(".")[0]) == 4:
            res["approximate_date"] = ".".join(res["approximate_date"].split(".")[::-1])

    elif "春夏" in data['releaseDate']:
        res["date"] = data['releaseDate'].rstrip("春夏").rstrip(".") + ".05.04"
        res["approximate_date"] = "Весна/лето " + data['releaseDate'].rstrip("春夏")
    elif "秋冬" in data['releaseDate']:
        res["date"] = data['releaseDate'].rstrip("秋冬").rstrip(".") + ".10.16"
        res["approximate_date"] = "Осень/зима " + data['releaseDate'].rstrip("秋冬")
    elif "秋季" in data['releaseDate']:
        res["date"] = data['releaseDate'].rstrip("秋季").rstrip(".") + ".09.27"
        res["approximate_date"] = "Осень " + data['releaseDate'].rstrip("秋季")
    elif "冬季" in data['releaseDate']:
        res["date"] = data['releaseDate'].rstrip("冬季").rstrip(".") + ".01.01"
        res["approximate_date"] = "Зима " + data['releaseDate'].rstrip("冬季")
    elif "春季" in data['releaseDate']:
        res["date"] = data['releaseDate'].rstrip("春季").rstrip(".") + ".03.01"
        res["approximate_date"] = "Весна " + data['releaseDate'].rstrip("春季")
    elif "夏季" in data['releaseDate']:
        res["date"] = data['releaseDate'].rstrip("夏季").rstrip(".") + ".08.09"
        res["approximate_date"] = "Лето " + data['releaseDate'].rstrip("夏季")
    elif len(data['releaseDate'].split(".")) == 2:
        res["date"] = data['releaseDate'] + ".01"
        res["approximate_date"] = data['releaseDate']

        if len(res["approximate_date"].split(".")[0]) == 4:
            res["approximate_date"] = ".".join(res["approximate_date"].split(".")[::-1])

        year = res["approximate_date"].split(".")[-1]
        month = res["approximate_date"].split(".")[-2]

        month_list = ["", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
                      "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        res["approximate_date"] = month_list[int(month)] + " " + year

    if len(res["date"].split(".")[0]) == 4:
        res["date"] = ".".join(res["date"].split(".")[::-1])
    # endregion
    # region Crop model
    for collab_name in res["collab_names"]:
        for i in range(collab_name.count(" x ")):
            res["model"] = remove_substring(res["model"], " x ")

    res["model"] = res["model"].rstrip("#")
    res["model"] = res["model"].replace("】", " ").replace("【", " ")
    res["model"] = res["model"].strip("-")
    res["model"] = res["model"].strip("-")
    res["model"] = res["model"].strip("/")
    res["model"] = res["model"].strip("|")
    res["model"] = res["model"].strip("\\")
    res["model"] = res["model"].strip(".")
    res["model"] = res["model"].strip(",")
    res["model"] = " ".join(res["model"].split()).strip()

    if res["model"]:
        res["model"] = res["model"][0].capitalize() + res["model"][1:]

    # endregion

    # region Process custom

    res["custom"] = False
    if "定制" in title or "team" in data["manufacturer_sku"].lower():
        res["custom"] = True

    # endregion

    # region Process categories

    res["categories"] = get_starting_categories(data)

    # endregion

    # region Process gender and manufacturer SKU and likesCount

    res["gender"] = copy.copy(GENDERS[str(data["fitId"])])
    if res["gender"] == ["F"] and (brand_id == "13" or brand_id == "144") and "Обувь" in \
            CATEGORY_NAMES[res["categories"][0]]["path"]:
        res["gender"].append("M")

    if res["gender"] == ["M"] and (brand_id == "13" or brand_id == "144") and "Обувь" in \
            CATEGORY_NAMES[res["categories"][0]]["path"]:
        res["gender"].append("F")

    res["manufacturer_sku"] = remove_chinese_symbols(data["manufacturer_sku"]).strip("\\").strip("/").strip('-')
    res["formatted_manufacturer_sku"] = ''.join(
        ''.join(res["manufacturer_sku"].split()).split(
            '-')).lower()

    res["poizon_likes_count"] = data["likesCount"]

    # endregion

    # region add colorway

    if len(lines):
        res["colorway"] = res["model"]
        if "Другие" in lines[0]["path"][-1]:
            if lines[0]["path"][-1] == "Другие Air Jordan 1":
                res["model"] = "Air Jordan 1"
            elif lines[0]["path"][-1] == "Другие Yeezy":
                res["model"] = "Yeezy"
            else:
                res["model"] = ' '.join(lines[0]["path"][-1].split()[2:])
        elif brand_id == "13":
            if lines[0]["path"][-1].startswith("Air"):
                res["model"] = lines[0]["path"][-1]
            else:
                res["model"] = (lines[0]["path"][-1]).replace(res["brands"][0], "").strip()
        else:
            res["model"] = (lines[0]["path"][-1]).replace(res["brands"][0], "").strip()

    if not lines:
        res["colorway"] = res["model"]
        res["model"] = CATEGORY_NAMES[res["categories"][0]]["singular_russian_name"]

    res["colorway"] = capitalize_first_letter(res["colorway"])

    res["model"] = res["model"].replace("(", "")
    res["model"] = res["model"].replace(")", "")
    res["model"] = res["model"].replace("（", "")
    res["model"] = res["model"].replace("）", "")
    res["colorway"] = res["colorway"].replace("(", "")
    res["colorway"] = res["colorway"].replace(")", "")
    res["colorway"] = res["colorway"].replace("（", "")
    res["colorway"] = res["colorway"].replace("）", "")

    title_extra_translation = translate_title(data["title"].lower())

    res["colorway"] = (res["colorway"] + " " + title_extra_translation).strip()
    # endregion

    return res


# Делаем заглавной первую букву строки
def capitalize_first_letter(s):
    for i, char in enumerate(s):
        if char.isalpha():
            return s[:i] + char.upper() + s[i + 1:]
    return s


def none_in_string(input_string, string_list):
    for item in string_list:
        if item.lower() in input_string.lower():
            return False
    return True
