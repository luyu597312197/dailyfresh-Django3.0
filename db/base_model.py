from django.db import models


class BaseModel(models.Model):
    """模型抽象基类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="删除标记")

    class Meta:
        # 将abstract设置为True后，CommonInfo无法作为一个普通的Django模型，
        # 而是作为一个抽象基类存在，作用 是为其他的类提供一些公有的属性。利于公用信息的分解，避免重复编码。
        abstract = True





