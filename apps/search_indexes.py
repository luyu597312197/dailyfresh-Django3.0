# 定义索引类

from .models import GoodsSKU
from haystack import indexes


class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段 use_template根据表中的哪些字段建立索引文件的说明放在一个文件中
    text = indexes.CharField(document=True, use_template=True)  # 有且只能有一个document=True
    # 对标题，简介，内容进行搜索
    # gtitle = indexes.CharField(model_attr='gtitle')
    # gjianjie = indexes.CharField(model_attr='gjianjie')
    # gcontent = indexes.CharField(model_attr='gcontent')

    def get_model(self):
        # 返回你的模型
        return GoodsSKU

    # 建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

