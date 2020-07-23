from django.contrib import admin
from goods.models import *
from django.core.cache import cache
from celery_tasks.tasks import generate_static_index_html


# Register your models here.


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """新增或更新表中的数据时调用"""
        super().save_model(request, obj, form, change)
        # 发出任务，让celery tasks重新生成静态页面
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete("index_page_data")

    def delete_model(self, request, obj):
        """删除表中数据时调用"""
        super().delete_model(request, obj)
        # 发出任务，让celery tasks重新生成静态页面
        generate_static_index_html.delay()


class GoodTypeAdmin(BaseModelAdmin):
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass


admin.site.register(GoodsType, GoodTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(GoodsSPU)

