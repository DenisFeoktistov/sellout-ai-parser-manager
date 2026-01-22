# DEWU_API_PARSER_URL = lambda spu_id: f"https://sellout.su/parser_dewu_api/process_spu_id?spu_id={spu_id}"
DEWU_API_PARSER_URL = lambda spu_id: f"http://localhost:5000/parser_dewu_api/process_spu_id?spu_id={spu_id}"

DEWU_API_GET_NEW_PRODUCTS = "https://sellout.su/parser_dewu_api/get_new_products_spus"

HK_API_PARSER_URL = lambda sku: f"https://sellout.su/parser_hk_api/process_sku?sku={sku}"
# HK_API_PARSER_URL = lambda sku: f"http://localhost:5000/parser_hk_api/process_sku?sku={sku}"

BACKEND_PRODUCT_BY_SPU_URL = lambda spu_id: f"https://sellout.su/api/v1/product/spu_id_info/{spu_id}"
BACKEND_GET_ALL_PRODUCTS = "https://sellout.su/api/v1/product/dewu_info_list"
BACKEND_UPDATE_URL = "https://sellout.su/api/v1/product/add_list_spu_id_products"
