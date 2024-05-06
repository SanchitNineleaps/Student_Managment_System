def authenticate_user():
    """
    Function to authenticate user credentials.
    Returns True if authentication is successful, False otherwise.
    """
    # Ask the user to input their user_id and password
    user_id = input("Enter user ID: ")
    password = input("Enter password: ")

    # Perform authentication logic here
    # You can compare the entered user_id and password with stored credentials
    # For simplicity, let's assume a hardcoded user_id and password
    
    if user_id == "admin" and password == "password":
        return True
    else:
        return False