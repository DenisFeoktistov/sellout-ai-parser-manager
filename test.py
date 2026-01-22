import asyncio
from Processing.process_spu import process_spu


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

spus = [1]


async def main():
    for spu in spus:
        await process_spu(spu)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
