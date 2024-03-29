# 1. 拉代码到 /var/www/belife
# 2. 执行 bash deploy.sh

# -e 脚本中的命令一旦运行失败就终止脚本的执行
# -x 用于显示出命令与其执行结果（默认shell脚本中只显示执行结果）
set -ex

# 系统设置
apt-get update
apt-get install -y zsh curl ufw
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 465
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
apt-get install -y git supervisor nginx python3-pip mysql-server redis-server
pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy flask_mail redis celery marrow.mailer

# 删除测试用户和测试数据库
# 删除测试用户和测试数据库并限制关闭公网访问
mysql -u root -pWeb*2019 -e "DELETE FROM mysql.user WHERE User='';"
mysql -u root -pWeb*2019 -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -u root -pWeb*2019 -e "DROP DATABASE IF EXISTS test;"
mysql -u root -pWeb*2019 -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
# 设置密码并切换成密码验证
mysql -u root -pWeb*2019 -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Web*2019';"

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

cp /var/www/belife/belife.conf /etc/supervisor/conf.d/belife.conf
# 不要再 sites-available 里面放任何东西
cp /var/www/belife/belife.nginx /etc/nginx/sites-enabled/belife
chmod -R o+rwx /var/www/belife

# 初始化
cd /var/www/belife
python3 reset.py

# 重启服务器
service supervisor restart
service nginx restart

echo 'succsss'
echo 'ip'
hostname -I
