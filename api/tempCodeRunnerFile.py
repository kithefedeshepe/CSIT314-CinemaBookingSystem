import base64
import uuid

# Base64-encoded binary value
base64_value = 'JmOISFo0Rb6qXKX/uLq/CQ=='

# Decode Base64 string
binary_value = base64.b64decode(base64_value)

# Interpret binary value as UUID
uuid_value = uuid.UUID(bytes=binary_value)

# Print UUID
print(uuid_value)