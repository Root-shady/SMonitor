# SMonitor
Django App for server monitor.

## 安装运行

1. 建议使用Python Virtualenv进行环境隔离(推荐virtualenvwrapper)

2. 在创建虚拟环境后，将相关的项目运行参数写入 `virtualenv/bin/postactivate` 文件里面
根据相关项目生成，和本地数据库设置进行配置修改，关于数据库初始化可见 `/Utils/initial.sql`
```
export USER='smonitor'
export NAME='smonitor'
export PASSWORD='password'
export HOSt='localhost'
export PORT='3306'
export SECRET\_KEY='1o#j7*ev=&!jmev+flyr(v$n$-_i3e403m@-)hse-33489=44909dh49'
```

3. 安装相关的依赖
pip3 install -r requirement.txt

4. 确认项目成功安装
```
python3 manage.py check
```

## 相关APP
1. account: 用户账户管理                功能：登录验证，相关的账户管理
2. rolepermission: 用户权限管理(RBC)    功能： 用户权限控制
3. projectlog: 系统日志模块             功能：相关的登录日志、操作日志
4. system: 用户系统模块                 功能：相关的运行参数、菜单配置
2. server: 服务器管理模块               功能： 服务器实例管理
