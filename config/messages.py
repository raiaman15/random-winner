"""
The file contains the messages sent in response to any query.
"""

response_messages = {}
response_messages['profile_sms_verification_already_verified'] = 'You have already verified your contact number'
response_messages['profile_sms_verification_attempt_exceeded'] = 'You have attempted more than 3 times in last 5 minutes. Please try again later!'
response_messages['profile_sms_verification_successful'] = 'You have successfully verified your contact number'
response_messages['profile_sms_verification_incorrect_otp'] = 'You have provided an incorrect OTP. Please try again with the new OTP!'
response_messages['profile_identity_proof_upload_successful'] = 'You have successfully uploaded your Identity Proof. Out team will verify it shortly.'
response_messages['profile_identity_proof_under_review'] = 'Your ID Proof document is still under review. Our team will verify it shortly.'
response_messages['profile_detail_update_successful'] = 'You have successfully updated your profile details'
response_messages['profile_apply_poolmaster_successful'] = 'You have successfully applied for PoolMaster. Our team will reach out to you shortly.'
response_messages['profile_contact_number_unverified'] = 'You have not verified your contact number yet. Please verify before you apply for PoolMaster.'
response_messages['profile_details_incomplete'] = 'You have not provided the necessary details yet. Please update before you apply for PoolMaster.'
response_messages['profile_identity_proof_unverified'] = 'Your ID Proof document is not verified yet. Our team will approve/reject shortly. In case of rejection, please go through the reason and retry.'
response_messages['profile_password_reset_attempt_exceeded'] = 'You have attempted more than 3 times in last 5 minutes. Please try again later!'
response_messages['profile_password_reset_incorrect_otp'] = 'You have provided an incorrect OTP. Please try again with the new OTP!'
response_messages['pool_creation_limit_exceeded'] = 'You have exceeded the limit of pool creation. You can create only 1 pool per day!'
response_messages['profile_billing_address_incomplete'] = 'You have not provided your billing address. Kindly provide your valid billing address to proceed further.'
response_messages['profile_bank_account_detail_incomplete'] = 'You have not provided your bank account details. Kindly provide your valid bank account details to proceed further.'
