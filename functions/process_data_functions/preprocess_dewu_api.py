import copy

import pydash as _


def preprocess_dewu_api(unprocessed_data):
    d = dict()

    data = copy.deepcopy(unprocessed_data)

    images = _.get(data, 'data.image.spuImage.images', list())

    d["images"] = list()
    for image in images:
        if "desc" in image:
            del image["desc"]
        d["images"].append(image)

    d["poizonSpuGroupList"] = _.get(data, 'data.spuGroupList.list', list())

    for poizonSpuGroupListItem in d["poizonSpuGroupList"]:
        if "logoUrl" in poizonSpuGroupListItem:
            del poizonSpuGroupListItem["logoUrl"]
        if "goodsType" in poizonSpuGroupListItem:
            del poizonSpuGroupListItem["goodsType"]
        if "title" in poizonSpuGroupListItem:
            del poizonSpuGroupListItem["title"]
        if "spu3d360ShowType" in poizonSpuGroupListItem:
            del poizonSpuGroupListItem["spu3d360ShowType"]

    d["gif"] = _.get(data, "data.image.spuImage.threeDimension.gifUrl", "")
    #
    d["brandId"] = _.get(data, "data.detail.brandId", "")

    d["relatedBrands"] = _.get(data, "data.detail.relationBrandIds", list())
    d["allBrands"] = d["relatedBrands"]

    if d["brandId"]:
        d["allBrands"] = [d["brandId"]] + d["allBrands"]
    #
    d["title"] = _.get(data, "data.detail.title", "")
    d["subTitle"] = _.get(data, "data.detail.subTitle", "")
    d["description"] = _.get(data, "data.detail.desc", "")
    #
    d["categoryId"] = _.get(data, "data.detail.categoryId", "")
    d["categoryName"] = _.get(data, "data.detail.categoryName", "")
    #
    d["level1CategoryId"] = _.get(data, "data.detail.level1CategoryId", "")
    d["level2CategoryId"] = _.get(data, "data.detail.level2CategoryId", "")
    #
    d["manufacturer_sku"] = _.get(data, "data.detail.articleNumber", "")
    skus = [_.get(data, "data.detail.articleNumber", ""), _.get(data, "data.detail.otherNumbers", "")] + _.get(data,
                                                                                                               "data.detail.articleNumbers",
                                                                                                               list())
    d["manufacturer_skus"] = list(set(skus))
    d["spuId"] = _.get(data, "data.detail.spuId", "")
    #
    d["releaseDate"] = _.get(data, "data.detail.sellDate", "")
    #
    d["retailPrice"] = _.get(data, "data.detail.authPrice", "")
    #
    d["fitId"] = _.get(data, "data.detail.fitId", "")
    #
    d["goodsType"] = _.get(data, "data.detail.goodsType", "")
    #
    #
    #
    d["item"] = _.get(data, "data.item", dict())
    d["includeTax"] = _.get(data, "data.item.includeTax", False)
    d["taxInfo"] = _.get(data, "data.item.taxInfo", "")
    #
    d["maxPricePoizon"] = _.get(data, "data.item.maxPrice", "")
    d["minPricePoizon"] = _.get(data, "data.item.floorPrice", "")
    d["pricePoizon"] = _.get(data, "data.item.price", "")
    #
    d["parameters"] = _.get(data, "data.keyProperties", "")
    d["likesCount"] = _.get(data, "data.favoriteCount.count", "")
    #
    d["skus"] = _.get(data, "data.skus", list())

    return d
