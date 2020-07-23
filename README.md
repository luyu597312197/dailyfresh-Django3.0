# dailyfresh
配置环境和项目思路请查看：https://www.cnblogs.com/xiaodaima/p/11245292.html  
需求分析  
1.1  用户模块  
1） 注册页  
	注册时校验用户名是否已被注册。  
	完成用户信息的注册  
	给用户的注册邮箱发送邮件，用户点击邮件中的激活链接完成用户账户的激活。  
2）登陆页  
	实现用户的登录功能  
3）用户中心  
	用户中心信息页，显示登录用户的信息，包括用户名、电话和地址，同时页面下方显示出用户最近浏览的商品信息。  
	用户中心地址页：显示登陆用户的默认收件地址，页面下方的表单可以新增用户的收货地址。  
	用户中心订单页：显示登录用户的订单信息。  
4）其他  
	如果用户已经登陆，页面顶部显示用户的订单信息。  
1.2  商品模块  
1）首页  
	动态指定首页轮播商品信息。  
	动态指定首页活动信息。  
	动态获取商品的种类信息并显示。  
	动态指定首页显示的每个种类的商品（包括图片商品的文字商品）。  
	点击某一个商品时跳转到商品的详情页面。  
2）商品详情页  
	显示出某个商品的详细信息。  
	页面下方显示出该商品的两个新品信息。  
3）商品列表页  
	显示出某一个种类的商品的列表数据，分页显示并支持按照默认、价格和人气进行排序。  
	页面下方显示出该商品的两个新品信息。  
4）其他  
	通过搜索框搜索商品信息。  
1.3  购物车模块  
	列表页和详情页将商品添加到购物车。  
	用户登录后，首页，详情页，列表页显示用户购物车中的商品数目。  
	购物车页面：对用户购物车中的商品操作。如选择某件商品，增加或减少购物车中的商品数目。  
1.4  订单相关  
	提交订单页面：显示用户准备购买的商品信息。  
	点击提交订单完成订单的创建。  
	用户中心订单页显示用户的订单信息。  
	点击支付完成订单的支付。  
	点击评价完成订单的评价。  
  
2 开发环境和工具  
python>3.6  
Django >3.0   
pychram  
redis  
mysql 5.7  
celery  
fastDFS  
nginx  
Django-haystack  
whoosh  
jieba  
alipay  
requests  
  
配置环境和思路请查看：https://www.cnblogs.com/xiaodaima/p/11245292.html  
