# 供VeighNa社区版使用的Elitedb数据库接口
VeighNa Elite版提供的默认数据库相当惊艳，秒杀市面上的一众数据库，但是无法提供给VeighNa社区版使用。<br />
本模块用于供社区版调用Elitedb。<br />
尽管在速度方面无法匹敌原版，但还是可以比Sqlite快的5-6倍，比MongoDb快50%-80%。<br /><br />

使用方法：<br />
1.下载源码至：C:\veighna_studio\Lib\site-packages<br />
2.依赖库pyarrow安装：pip install pyarrow<br />
3.修改全局配置中database.name字段为elitedb<br />
4.数据管理请使用Elite原版<br /><br />
