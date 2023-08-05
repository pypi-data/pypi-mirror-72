# HoldingProfit_test_PU
## unit_info
+ discription = 计算品种持仓盈亏
+ lang = python
> 语言包括：python C++ 
+ type = pu
## upper_unit
+ tick_data_PU
+ sina_data_PU
## data_base
> 生成所有表的获取接口，生成时需要连接数据库，读表结构
> 只生成读的函数，参数为： 表明、字段名列表 、where条件
> Oracle需要字段：+ dbtype、hosts 、port 、 pd、 dbname（service name或者SID） 、 user
> Mysql需要字段： dbtype、hosts 、port 、 pd、 dbname（service name或者SID） 、 user
> sqlserver需要字段： dbtype、hosts 、port 、 pd、 dbname（service name或者SID） 、 user
+ dbtype = Oracle
+ hosts = localhost
+ port = 1521
+ pd = Passw0rd
+ dbname = ZHANG.ZKTEST
+ user = system
### SQL
+ sqlname1 = select * from STUDENT where XH = 2
+ sqlname2 = select * from STUDENT where rownum < 10
## Interface
### calSymbolProfit()
#### input
+ accountid = 42313454332
+ sttime = 20200401
+ symbol = cu2010
#### output
> 注意，md语法每行最后双空格再换行才是换行,转pdf时注意

{
    "trade_dic" :
    {
        "tradeId" : "str", # 交易代码
        "tradeTime" : "datetime", # 交易时间
        "buyPrice" : "st", # 买入价
        "symbolinfo" :  # 标的信息
        {
            "symbol":"str", # 标的名
            "exchange":"str", # 交易所
            "priceInfo": # 价格信息
            {
                "pricetick":"float", # 最小变动价格
                "margin":"float"
            }
        }
    }
}

#### meta_data
+ ownerID = 500
+ ownerGroupID = 200
+ acCode = 777
+ did = 9527
+ zipDataSize = 692k
+ rawDataSize = 1428k
+ md5 = lkjliudfadf12jolx
+ dataTime = 20200109
+ version = 1.0
+ description = 这里写了一堆的数据描述

# Holding_PU
## unit_info
+ discription = 计算品种持仓盈亏
+ lang = cpp
> 语言包括：python C++ 
+ type = pu
## upper_unit
+ HoldingProfit_test_PU
## data_base
> 生成所有表的获取接口，生成时需要连接数据库，读表结构
> 只生成读的函数，参数为： 表明、字段名列表 、where条件
> Oracle需要字段：+ dbtype、hosts 、port 、 pd、 dbname（service name或者SID） 、 user
> Mysql需要字段： dbtype、hosts 、port 、 pd、 dbname（service name或者SID） 、 user
> sqlserver需要字段： dbtype、hosts 、port 、 pd、 dbname（service name或者SID） 、 user
+ dbtype = Oracle
+ hosts = localhost
+ port = 1521
+ pd = Passw0rd
+ dbname = ZHANG.ZKTEST
+ user = system
### SQL
+ sqlname1 = select * from STUDENT where XH = 2
+ sqlname2 = select * from STUDENT where rownum < 10
## Interface
### calSymbolProfit()
#### input
+ accountid = 42313454332
+ sttime = 20200401
+ symbol = cu2010
#### output
> 注意，md语法每行最后双空格再换行才是换行,转pdf时注意

{
    "trade_dic" :
    {
        "tradeId" : "str", # 交易代码
        "tradeTime" : "datetime", # 交易时间
        "buyPrice" : "st", # 买入价
        "symbolinfo" :  # 标的信息
        {
            "symbol":"str", # 标的名
            "exchange":"str", # 交易所
            "priceInfo": # 价格信息
            {
                "pricetick":"float", # 最小变动价格
                "margin":"float"
            }
        }
    }
}

#### meta_data
+ ownerID = 500
+ ownerGroupID = 200
+ acCode = 777
+ did = 9527
+ zipDataSize = 692k
+ rawDataSize = 1428k
+ md5 = lkjliudfadf12jolx
+ dataTime = 20200109
+ version = 1.0
+ description = 这里写了一堆的数据描述

