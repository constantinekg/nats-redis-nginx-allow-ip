# nats-redis-nginx-allow-ip

Разрешить ip адрес пользователя в nginx после авторизации на форме через nats и обновления инфы в redis.

## Установка зависимостей

```bash
pip3 install nats-py redis
```

Далее перейти в /opt и слить туда все файлы:

```
cd /opt && git clone https://github.com/constantinekg/nats-redis-nginx-allow-ip
```

### Включение сервиса

```bash
nano /etc/systemd/system/loginbyip.service
```

Содержимое /etc/systemd/system/loginbyip.service :

```
[Unit]
Description = Allow user ip in nginx after user auth
After = network.target
 
[Service]
Type = simple
ExecStart = /opt/nats-redis-nginx-allow-ip/loginbyipdaemon.py
User = root
Group = root
Restart = on-failure
SyslogIdentifier = loginbyip
RestartSec = 5
TimeoutStartSec = infinity
 
[Install]
WantedBy = multi-user.target
```

После чего... 

```
systemctl daemon-reload
systemctl enable loginbyip.service
systemctl start loginbyip.service
```

### Добавление джоба в крон для перегенирации белого листа, исходя из истечения срока действия айпишников в редисе

В крон добавить:

```
# renew allow list for nginx
*/12 * * * * /opt/nats-redis-nginx-allow-ip/regenerateallowlist.py
```
