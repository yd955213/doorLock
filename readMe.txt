1、使用前请输入命令安装依赖： pip install -r requirements.txt


# 备注小技巧：
# 使用 pipreqs ，github地址为： https://github.com/bndr/pipreqs

# 安装
pip install pipreqs
# 在当前目录生成 requirements.txt
pipreqs . --encoding=utf8 --force

# --encoding=utf8 为使用utf8编码
# --force 强制执行，当 生成目录下的requirements.txt存在时覆盖。