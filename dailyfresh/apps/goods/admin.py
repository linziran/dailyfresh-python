from django.contrib import admin
from goods.models import *


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name','detail')
    class Media:
        js = (
            '/static/js/kindeditor-4.1.6/kindeditor-min.js',
            '/static/js/kindeditor-4.1.6/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.6/config.js'
        )



admin.site.register(GoodsType)#'''商品类型模型类'''
admin.site.register(GoodsSKU)#'''商品SKU模型类'''
admin.site.register(Goods,GoodsAdmin)#'''商品SPU模型类'''
admin.site.register(GoodsImage) #'''商品图片模型类'''
admin.site.register(IndexGoodsBanner)#'''首页轮播商品展示模型类'''
admin.site.register(IndexTypeGoodsBanner)#'''首页分类商品展示模型类'''
admin.site.register(IndexPromotionBanner)#'''首页促销活动模型类'''


