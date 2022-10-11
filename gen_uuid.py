import uuid

print(str(uuid.uuid3(uuid.NAMESPACE_DNS, 'karakas.rustytub.com')).upper())
