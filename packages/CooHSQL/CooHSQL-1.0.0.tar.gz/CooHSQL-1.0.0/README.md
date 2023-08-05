# CooHSQL
### 介绍：

***

##### 伪装 Slave 获取 MySQL binlog 从中解析到你想要的 SQL 语句，可以得到原始 SQL、回滚 SQL 语句。

### 用途：

***

* 数据库快速回滚(DML闪回) 
* 配合其它备份工具恢复数据
* 可以自己定制 binlog 衍生功能

### 环境：

***

##### MySQL 数据库中设置相关参数：

```shell
[mysqld]
server_id = 1
log_bin = /var/log/mysql/mysql-bin.log
max_binlog_size = 1G
binlog_format = row
binlog_row_image = full
```

##### CooHSQL 需要安装的依赖环境

```shell
python 3.6+
MySQL 5.7+
PyMySQL >= 0.7.11
wheel >= 0.29.0
mysql-replication >= 0.13
```

### 演示：

***

##### 测试一：测试环境数据库 School.Student 表设计如下：

```sql
desc Student;
```

| Field | Type          | Null | Key  | Default | Extra |
| :---- | :------------ | :--- | :--- | :------ | :---- |
| SId   | varchar\(10\) | YES  |      | NULL    |       |
| Sname | varchar\(10\) | YES  |      | NULL    |       |
| Sage  | datetime      | YES  |      | NULL    |       |
| Ssex  | varchar\(10\) | YES  |      | NULL    |       |

```sql
select * from Student;
```

| SId  | Sname | Sage                | Ssex |
| :--- | :---- | :------------------ | :--- |
| 01   | 赵雷  | 1990-01-01 00:00:00 | 男   |
| 02   | 钱电  | 1990-12-21 00:00:00 | 男   |
| 03   | 孙风  | 1990-12-20 00:00:00 | 男   |
| 04   | 李云  | 1990-12-06 00:00:00 | 男   |
| 05   | 周梅  | 1991-12-01 00:00:00 | 女   |
| 06   | 吴兰  | 1992-01-01 00:00:00 | 女   |

```sql
-- update 语句忘记写条件, 导致整张表被修改
update Student set Ssex = '女';

-- 查看表数据, Sexx 已经全被修改
select * from Student;
```

| SId  | Sname | Sage                | Ssex |
| :--- | :---- | :------------------ | :--- |
| 01   | 赵雷  | 1990-01-01 00:00:00 | 女   |
| 02   | 钱电  | 1990-12-21 00:00:00 | 女   |
| 03   | 孙风  | 1990-12-20 00:00:00 | 女   |
| 04   | 李云  | 1990-12-06 00:00:00 | 女   |
| 05   | 周梅  | 1991-12-01 00:00:00 | 女   |
| 06   | 吴兰  | 1992-01-01 00:00:00 | 女   |

```python
from CooHSQL.CooHSQL import CooHSQL

# mysql 连接参数
mysql_settings = {
    'host': '127.0.01',
    'port': 3306,
    'user': 'root',
    'password': 'coohsql'
}

CooHSQL = CooHSQL(mysql_settings, start_file='mysql-bin.000001', start_pos=143228)
CooHSQL.process_binlog()  # 加工 binlog 输出回滚语句
```

```sql
UPDATE `school`.`Student` SET `SId`=04,`Sname`='李云',`Sage`='1990-12-06 00:00:00',`Ssex`='男' WHERE `SId`=04 and `Sname`='李云' and `Sage`='1990-12-06 00:00:00' and `Ssex`='女';

UPDATE `school`.`Student` SET `SId`=03,`Sname`='孙风',`Sage`='1990-12-20 00:00:00',`Ssex`='男' WHERE `SId`=03 and `Sname`='孙风' and `Sage`='1990-12-20 00:00:00' and `Ssex`='女';

UPDATE `school`.`Student` SET `SId`=02,`Sname`='钱电',`Sage`='1990-12-21 00:00:00',`Ssex`='男' WHERE `SId`=02 and `Sname`='钱电' and `Sage`='1990-12-21 00:00:00' and `Ssex`='女';

UPDATE `school`.`Student` SET `SId`=01,`Sname`='赵雷',`Sage`='1990-01-01 00:00:00',`Ssex`='男' WHERE `SId`=01 and `Sname`='赵雷' and `Sage`='1990-01-01 00:00:00' and `Ssex`='女';
```

| SId  | Sname | Sage                | Ssex |
| :--- | :---- | :------------------ | :--- |
| 1    | 赵雷  | 1990-01-01 00:00:00 | 男   |
| 2    | 钱电  | 1990-12-21 00:00:00 | 男   |
| 3    | 孙风  | 1990-12-20 00:00:00 | 男   |
| 4    | 李云  | 1990-12-06 00:00:00 | 男   |
| 05   | 周梅  | 1991-12-01 00:00:00 | 女   |
| 06   | 吴兰  | 1992-01-01 00:00:00 | 女   |

***

##### 测试二：mode 参数两种用法

```sql
select * from Student;
```

| SId  | Sname | Sage                | Ssex |
| :--- | :---- | :------------------ | :--- |
| 1    | 赵雷  | 1990-01-01 00:00:00 | 男   |
| 2    | 钱电  | 1990-12-21 00:00:00 | 男   |
| 3    | 孙风  | 1990-12-20 00:00:00 | 男   |
| 4    | 李云  | 1990-12-06 00:00:00 | 男   |
| 05   | 周梅  | 1991-12-01 00:00:00 | 女   |
| 06   | 吴兰  | 1992-01-01 00:00:00 | 女   |

```sql
-- 插入 李华 信息
insert into Student value (07, '李华', '1992-01-01', '男');
```

mode = "flashback" 时生成的回滚语句，可以将李华的信息删除。

```sql
DELETE FROM `school`.`Student` WHERE `SId`=7 and `Sname`='李华' and `Sage`='1992-01-01 00:00:00' and `Ssex`='男';
```

mode = "dump" 时是直接从 binlog 中翻译出原 SQL 语句。

```sql
INSERT INTO `school`.`Student`(SId,Sname,Sage,Ssex) VALUE (07,'李华','1992-01-01 00:00:00','男');
```

### 参数：

***

* **mysql_settings**：mysql 的连接信息 ip 地址、用户名、密码、端口格式如下：

  ```python
  mysql_settings = {
      'host': '127.0.01',
      'port': 3306,
      'user': 'root',
      'password': 'coohsql'
  }
  ```

  ```sql
  -- 建议授权
  GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 
  ```
  
* **max_filtration**：语句中的 where 条件最长字符数量，这个比较难理解，先看一条 update 语句：

  ```sql
  UPDATE `school`.`SC` SET `SId`=10,`CId`=4,`score`=100.0 WHERE `SId`=10 and `CId`=4 and `score`=99.0;
  ```

  可以看到有 **where** 等式条件，如果这个等式特别大比如：**digest=“此处省去1000字”**  这样的等式无意义，虽然优化器也绝对不会使用，但是导出过程比较占用空间，所以在组成 **where** **条件等式**时，会进行筛选，默认少于 20 字符，可以组成 where **条件等式**。**max_filtration** 就是来避免使用大字段组成 **where 条件等式** 如果有特殊情况可以自行调整它。

* **start_file**：与 **start_pos** 参数配合使用，需要解析的 binlog 日志文件，如果不指定会读取全部 binlog 如果数据量比较大，建议先确定一个范围，目前版本不支持多文件读取，未来 1.5 版本会添加多文件读取，敬请期待！

  ```sql
  -- 查看正在使用的 binlog 文件和 log_pos
  show master logs;
  ```

  | Log\_name        | File\_size |
  | :--------------- | :--------- |
  | mysql-bin.000001 | 1461120    |
  | mysql-bin.000002 | 132332     |

  如果 show master logs 可以查看当前使用的 binlog 文件，可以看到 mysql-bin.000001 已经弃用，如果解析的数据量比较小，那么直接指定 start_file 为 mysql-bin.000002 避免加载多余的数据。

* **start_pos**：与 **start_file** 参数配合使用，binlog 日志中的 log_pos 起点，可以更加准确的定位到需要解析或者回滚到数据。默认不指定，建议先使用 **show binlog events** 确定大概范围，可以提升解析速度。

* **event_schemas**：需要解析或者回滚的数据库，默认为 None 则解析全部数据库，如果指定数据库，则只加载相关的数据库。

* **event_tables**：需要解析或回滚的数据表，配合 **event_schemas** 一起使用，可以定位到数据表。

* **mode**：属于 **process_binlog** 中的参数，有两种 binlog 的解析方式 flashback 和 dump 

  * flashback：生成回滚 SQL 语句，默认。
  * dump：翻译 binlog 生成 SQL 语句。

* **server_id**：CooHSQL 伪装为 slave 所以需要 **server_id** 默认为 8023 如果重复请自行修改此参数。

* **start_time**：开始时间，通过时间来过滤 binlog 日志生成某个时间段你需要的 SQL 格式为 1990-01-01 00:00:00。

* **stop_time**：结束时间，通过时间来过滤 binlog 日志生成某个时间段你需要的 SQL 格式为 1990-01-01 00:00:00。

### 后记：

目前只能应用于 DML 语句回滚，不支持 DDL 语句。目前项目处于维护测试阶段，将不断完善，敬请期待！

### 已经 BUG

在空值和时间字典组成的 where 条件中可能会出现异常。将来未来 1.5 版本中修复。

### 联系：

如有任何问题，发送到我的邮箱：huabing8023@126.com