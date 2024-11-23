from twilio.rest import Client

# Twilio credentials (replace these with your own)
account_sid = 'ACce1fe898731199051fc9ceb46dadcea0'
auth_token = '72804982b0a88b6a3053daf61e79d06b'

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Define caller and recipient phone numbers
from_phone = '+1 502 353 1291'  # Replace with your Twilio number
to_phone = '12345678'  # Replace with the recipient's number

# Make the call
call = client.calls.create(
    twiml='<Response><Say>Hello! This is a test call from your Python app.</Say></Response>',
    from_=from_phone,
    to=to_phone
)

print(f"Call initiated. Call SID: {call.sid}")
