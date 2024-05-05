from app.utils import generate_random_alphanumeric


def test_generate_random_alphanumeric():
    # Test with default length
    result = generate_random_alphanumeric()
    assert isinstance(result, str)
    assert len(result) == 20

    # Test with custom length
    custom_length = 10
    result = generate_random_alphanumeric(custom_length)
    assert isinstance(result, str)
    assert len(result) == custom_length

    # Test with length 0
    zero_length = 0
    result = generate_random_alphanumeric(zero_length)
    assert isinstance(result, str)
    assert len(result) == zero_length

    # Test with negative length
    negative_length = -5
    result = generate_random_alphanumeric(negative_length)
    assert isinstance(result, str)
    assert len(result) == 0
