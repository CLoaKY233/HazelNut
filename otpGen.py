import random
import json
import os

def custom_hash_to_alphanumeric(hash_value):
    """
    Converts a numerical hash value to a 6-character alphanumeric string.
    """
    base_12_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    if hash_value == 0:
        return "0"

    while hash_value > 0:
        result = base_12_chars[hash_value % 12] + result
        hash_value //= 12

    # Truncate the hash to 6 characters if it exceeds that length
    result = result[:6]
    
    # Pad with leading zeros if the length is less than 6 characters
    result = result.rjust(6, '0')

    return result

def generate_unique_hash():
    """
    Generates a unique alphanumeric hash value and adds it to the JSON file.
    """
    # Check if the JSON file exists
    json_file = "hashed_values.json"
    if not os.path.exists(json_file):
        with open(json_file, "w") as file:
            json.dump({}, file,indent=2)

    while True:
        input_string = random.randint(500000, 1000000)  # Modify range as needed
        hashed_value = custom_hash_to_alphanumeric(input_string)

        with open(json_file, "r") as file:
            existing_hashes = json.load(file)

        if hashed_value not in existing_hashes.values():
            existing_hashes[input_string] = hashed_value
            with open(json_file, "w",) as file:
                json.dump(existing_hashes, file,indent=2)
            print(f"Input: {input_string}, Hash: {hashed_value}")
            break

# Generate a unique alphanumeric hash value and add it to the JSON file
generate_unique_hash()
