# notification_service
```
docker build -t notify .
docker run --env-file configs/notify_service_env.list -d --restart=always --security-opt apparmor=docker-default \
--cpus=1 --memory=1g --oom-kill-disable --name notify -p 5005:80 notify
```
## Telegram notification:
##### URL:
```
my.domain/api/v2/telegram
```
##### Method: 
```
GET
```
##### Header:
```
{
  'Content-Type: application/json',
  'X-NOTIFY-API-Key: 9dc82trbbca'
}
```
##### Data:
```
{
  'id': '45948587',
  'text': 'My message'
}
```  
## E-mail notification:
##### URL:
```
my.domain/api/v1/email
```
##### Method: 
```
GET
```
##### Header:
```
{
  'Content-Type: application/json',
  'X-NOTIFY-API-Key: 9dc82trbbca'
}
```
##### Data:
```
{
  'email': 'komy@to.tam',
  'subject': 'my subject',
  'body": 'my message'
}
```
