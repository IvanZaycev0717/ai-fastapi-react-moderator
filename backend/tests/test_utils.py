from services.utils import is_text_valid

def test_is_text_valid():
    text = '123'
    assert is_text_valid(text) is True