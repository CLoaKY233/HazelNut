import os
import shelve
import tempfile

TEMP_FOLDER = 'temp'

def write(name, otp):
    # Ensure the temporary directory exists
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    # Create or open the shelve file in the temporary directory
    with shelve.open(os.path.join(TEMP_FOLDER, 'data')) as db:
        db[name] = otp

def show(name):
    # Open the shelve file
    with shelve.open(os.path.join(TEMP_FOLDER, 'data')) as db:
        if name in db:
            otp = db[name]  # Retrieve the OTP
            del db[name]     # Delete the entry
            return otp
    return None


