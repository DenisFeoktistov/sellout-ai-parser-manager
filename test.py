import asyncio
import json
import re

from Processing.process_spu import process_spu
from main import get_spu_id

# skus = [
#     "32CP77931",                # cap
#     "HG6678",                   # adidas fur coat
#     "H069426CCCI",              # hermes bag
#     "NF0A4UDK-JK3",             # tnf hoodie
#     "CT5053-001",               # travis low
#     "35T9GTVT0B-200",           # mk bag
#     "NJ1DN60B",                 # tnf jacket
#     "CN5640-010",               # off-white hoodie
#     "CZ3986-001",               # Fragment x Clot
#     "H147992FO4",               # hermes chain
#     "35S1GM9T0L-001",           # Michael cors bag
#     "H064544CM2M-H073967CAAA",  # Hermes belt
#     "OMRB012E196470026000",     # Ow belt
#     "OMKN003R20E480016200",     # Ow bag
#     "ML2002RA",                 # Nb sneakers
#     "M1906RQ",                  # Nb sneakers
#     "M9043",                    # Lv belt
#     "M6334E",                   # Lv bracelet
#     "M41177",                   # Lv bag
#     "31TSN2131-50W",            # Mlb t
#     "AR5005-101",               # Nike t
#     "NT3916N-NG",               # Tnf t
#     "NT3850N-OW",               # Tnf t
#     "T425-AS"                   # Champion t
#     "OMBB009F161920891001"      # ow hoodie
# ]


with open('test_data.txt', 'r') as file:
    text = file.read()

# Define the regular expression pattern to match URLs
pattern = r'https?://\S+'

# Find all URLs in the text using the regular expression pattern
links = re.findall(pattern, text)


async def main():
    for i, link in enumerate(links[-1:]):
        # print(i)
        #
        # spu_id = get_spu_id(link)

        # spu_id = 2490245
        # spu_id = 1050494
        # spu_id = 3331198
        # spu_id = 11843281
        # spu_id = 1619798
        # spu_id = 2301110
        # spu_id = 7714807
        # spu_id = 11843281
        spu_id = 1372720  # Goyard bag

        result = await process_spu(spu_id)

        # name = result["brands"][0] + " " + result["model"] + " " + result["colorway"]
        # name = name.replace("/", "")
        #
        # with open(f"results/{i} {name}.json", "w", encoding="utf-8") as output:
        #     output.write(json.dumps(result, indent=4, ensure_ascii=False))


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
