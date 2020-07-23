from django.test import TestCase

# Create your tests here.


ORDER_STATUS = {
        '1': '待支付',
        '2': '待发货',
        '3': '待收货',
        '4': '待评价',
        '5': '已完成',
    }
a = "1"
print(ORDER_STATUS["1"])
