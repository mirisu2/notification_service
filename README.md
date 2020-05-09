# notification_service
Notification service

## Telegram notification:
### URL:
```
my.domain/api/v1/telegram
```
### Method: 
```
GET
```
### Header:
```
{
  'Content-Type: application/json',
  'X-NOTIFY-API-Key: 9dc82trbbca'
}
```
### Data:
```
{
  'id': '45948587',
  'text': 'My message'
}
```  
## E-mail notification:
### URL:
```
my.domain/api/v1/email
```
### Method: 
```
GET
```
### Header:
```
{
  'Content-Type: application/json',
  'X-NOTIFY-API-Key: 9dc82trbbca'
}
```
### Data:
```
{
  'email': 'komy@to.tam',
  'subject': 'my subject',
  'body": 'my message'
}
```
