# uTools-CPP-DOC

 - 英文: https://en.cppreference.com/w/Cppreference:Archives
 - 中文: https://zh.cppreference.com/w/Cppreference:Archives
 
## 说明
1. 下载HTML文档
2. 从英文版文档中提取`cppreference-doxygen-local.tag.xml`文件，放于项目录下。
3. 合并两文档的reference, 放于`pubcic`目录下。
4. 执行`python data2json.py`,将在`public`目录下生成索引文件。
5. 打包使用。


第4步执行后，文件目录应为:
```
.
├── README.md
├── cppreference-doxygen-local.tag.xml
├── data2json.py
├── prase.py
└── public
    ├── README.md
    ├── favicon.png
    ├── indexes-cn.json
    ├── indexes-en.json
    ├── plugin.json
    ├── preload.js
    └── reference
        ├── common
        ├── en
        └── zh
```
