import os
import shelve
import tempfile

TEMP_FOLDER = 'temp'

def write(name, otp):
    # Ensure the temporary directory exists
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    # Create or open the shelve file in the temporary directory
    with shelve.open(os.path.join(TEMP_FOLDER, 'otpdata')) as db:
        db[name] = otp

def show(name):
    # Open the shelve file
    with shelve.open(os.path.join(TEMP_FOLDER, 'otpdata')) as db:
        if name in db:
            otp = db[name]  # Retrieve the OTP
            del db[name]     # Delete the entry
            return otp
    return None



def writeinvite(name, otp, inviter,channelid):
    # Ensure the temporary directory exists
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    # Create or open the shelve file in the temporary directory
    with shelve.open(os.path.join(TEMP_FOLDER, 'invitedata')) as db:
        db[name] = {'otp': otp, 'inviter': inviter,'channelid':channelid}
    

def verifyinvite(name):
 
    # Open the shelve file
    with shelve.open(os.path.join(TEMP_FOLDER, 'invitedata')) as db:
        if name in db:
            invite_data = db[name]
            otp = invite_data['otp']  # Retrieve the OTP
            inviter = invite_data['inviter']
            channelid=invite_data['channelid']
            # Retrieve the teamname
            
            return otp, inviter,channelid
    return None, None,None



def delete(name):
    with shelve.open(os.path.join(TEMP_FOLDER, 'invitedata')) as db:
                if name in db:
                    db[name]=None
                    del db[name]