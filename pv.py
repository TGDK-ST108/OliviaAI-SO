from twilio.rest import Client

def validate_phone_number(phone):
    client = Client(account_sid, auth_token)
    try:
        phone_info = client.lookups.phone_numbers(phone).fetch()
        if phone_info.country_code in ['US', 'GB', 'JP', 'DE']:
            return True
        return False
    except Exception as e:
        return False