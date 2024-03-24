import random
import json
import os
import hashlib  # Importing hashlib for a more secure hashing algorithm

def generate_unique_hash():
  """
  Generates a unique alphanumeric hash value for a given string and adds it to the JSON file.
  """
  # Check if the JSON file exists
  json_file = "hashed_values.json"
  if not os.path.exists(json_file):
    with open(json_file, "w") as file:
      json.dump({}, file, indent=2)

  while True:
    input_string = input("Enter a string: ")  # User input for string

    hashed_value = hashlib.sha256(input_string.encode()).hexdigest()[:10]  # Generate 10-character hash

    with open(json_file, "r") as file:
      existing_hashes = json.load(file)

    if hashed_value not in existing_hashes.values():
      existing_hashes[input_string] = hashed_value
      with open(json_file, "w") as file:
        json.dump(existing_hashes, file, indent=2)
      print(f"Input: {input_string}, Hash: {hashed_value.upper()}")
      break

# Generate a unique alphanumeric hash value and add it to the JSON file
generate_unique_hash()