from twilio.rest import Client

account_sid = "AC6fd8fb0b2ed2660e2ccc6d27b8b3afdf"
auth_token = "ec092433772d10b7fd3248f0043f600c"

client = Client(account_sid, auth_token)
message = client.messages.create(
    body="Testing Sms Code",
    from_='+17174834697',
    to='+918738801988'
)

print(message.sid)
print(message.status)