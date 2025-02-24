# XHS

## 前言

> 这是一个基于[PyQt-Fluent-Widgets](https://github.com/DY13208/xhs/tree/master/PyQt-Fluent-Widgets)和xhs实现UI的小红书自动登录，以及文章发布的一个可视化项目，后续会更新成通过ai自动发帖运营回复评论

## 目前完成模块

- [x] 登录UI,发布文章UI,获取用户信息及API操作UI
- [x] 登录功能，Cookie自动登录
- [x] 文章发布功能
- [x] API操作
- [x] 自动填充文章功能
- [ ] AI自动填充文章
- [ ] AI自动发帖
- [ ] AI自动回复
- [ ] 账号运营维护

## 模块说明

> xhs
> ├── .idea （idea配置不必理会）
> ├── PyQt-Fluent-Widgets（PyQt-Fluent-Widgets 的UI原始文件，可以参考来写）
> ├── app（主要页面UI代码 [xhsCore](app\view\xhsCore) 的目录下是主要xhs核心控制页面代码）
> ├── config（配置文件）
> ├── core（都是一些暂未整理的模块不用理会）
> ├── data（都是一些暂未整理的模块不用理会）
> ├── database（都是一些暂未整理的模块不用理会）
> ├── js（JS脚本）
> ├── logs（都是一些暂未整理的模块不用理会）
> ├── models（都是一些暂未整理的模块不用理会）
> ├── qfluentwidgets（UI库的SDK）
> ├── resource（UI图片资源）
> ├── tasks（都是一些暂未整理的模块不用理会）
> ├── README.md（说明文档）
> ├── UI_demo.py（都是一些暂未整理的模块不用理会）
> ├── __init__.py
> ├── cookies.json（登录后保存的cookies文件）
> ├── demo.py（主程序代码）
> ├── error_post_article.png
> ├── error_select_country.png
> ├── error_send_code.png
> ├── gallery.pro
> ├── geckodriver.exe
> ├── main.py（都是一些暂未整理的模块不用理会）
> ├── requirements.txt（需要安装的版本库）
> ├── stealth.min.js（JS脚本UI库的）
> └── test.py