# notification_service
docker run --env-file /path/to/configs/notify_service_env.list -d --restart=always --name notify -p 5005:80 arty234e/notify

## Telegram notification:
##### URL:
```
my.domain/api/v1/telegram
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
