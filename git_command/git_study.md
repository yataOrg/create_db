## git入门教程
https://www.liaoxuefeng.com/
### 方式一 clone
```
先在github平台上创建代码仓库 通过页面点击new
# git clone
git clone git@github:yataOrg/create_db.git
# 添加修改
git add .
# 提交本地修改
git commit -m "修改备注"
# 拉取远程仓库最新代码
git pull origin master
# 推送本地最新代码到远程仓库
git push origin master
```


### 方式二 本地和远程关联
```
现在本地创建一个目录并进入这个目录
git init

```