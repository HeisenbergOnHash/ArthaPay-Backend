# Fetch Admin Username Based on Phone Number
fetch_admin_query = """
    SELECT admin_username 
    FROM master 
    WHERE admin_phone_number = %s
"""

# Fetch User Username Based on Phone Number
fetch_user_query = """
    SELECT username 
    FROM user_demographics 
    WHERE phone_number = %s
"""

# Query to authenticate an admin by retrieving their hashed password
authenticate_admin_query = """
    SELECT admin_password AS password 
    FROM master 
    WHERE admin_username = %s
"""

# Query to authenticate a user by retrieving their hashed password
authenticate_user_query = """
    SELECT hashed_password AS password 
    FROM user_demographics 
    WHERE username = %s
"""

# Query to get the user payout wallet balance by their username
fetch_user_balance = """
    SELECT wallet.imps_balance
    FROM wallet
    JOIN user_demographics ON wallet.user_id = user_demographics.user_id
    WHERE user_demographics.username = %s;
"""

# transaction_authorizer Query 
transaction_authorizer_query ="""
    SELECT kyc_status, t_pin
    FROM user_demographics
    WHERE username = %s;
"""

# Query to insert a new transaction request into the transactions table
insert_transaction_request_query= """
    INSERT INTO transactions (
        username, beneficiary_name, bank_account, 
        ifsc, amount, transfer_id, status) 
    VALUES (%s, %s, %s, %s, %s, %s, %s);
"""