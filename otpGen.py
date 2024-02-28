import hashlib

# Generate a random hexadecimal key (32 characters)
hex_key = hashlib.sha256(b"LAY_KI_BHUTIYA").hexdigest()

# Function to hash a number based on the key
def hash_number(number):
    key_bytes = bytes.fromhex(hex_key)
    number_bytes = bytes(str(number), 'utf-8')
    hashed = hashlib.sha256(key_bytes + number_bytes).hexdigest()
    return hashed[6:16]  # Take only the first 8 characters of the hash

# Example: Hashing numbers from 0 to 9
for i in range(100):
    hashed_number = hash_number(i)
    print(f"Number: {i}, Hash: {hashed_number}")
