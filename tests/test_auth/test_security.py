from app.auth.security import check_password, hash_password


def test_hash_password():
    # Test a simple password
    password = "password123"
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, bytes)

    # Test an empty password
    empty_password = ""
    hashed_empty_password = hash_password(empty_password)
    assert isinstance(hashed_empty_password, bytes)

    # Test a password with special characters
    special_chars_password = "!@#$%^&*"
    hashed_special_chars_password = hash_password(special_chars_password)
    assert isinstance(hashed_special_chars_password, bytes)

    # Test a long password
    long_password = "a" * 1000
    hashed_long_password = hash_password(long_password)
    assert isinstance(hashed_long_password, bytes)


def test_check_password():
    # Test a correct password
    password = "password123"
    hashed_password = hash_password(password)
    assert check_password(password, hashed_password) is True

    # Test an incorrect password
    incorrect_password = "wrongpassword"
    assert check_password(incorrect_password, hashed_password) is False

    # Test an empty password
    empty_password = ""
    hashed_empty_password = hash_password(empty_password)
    assert check_password(empty_password, hashed_empty_password) is True

    # Test a password with special characters
    special_chars_password = "!@#$%^&*"
    hashed_special_chars_password = hash_password(special_chars_password)
    assert check_password(special_chars_password, hashed_special_chars_password) is True

    # Test a long password
    long_password = "a" * 1000
    hashed_long_password = hash_password(long_password)
    assert check_password(long_password, hashed_long_password) is True
