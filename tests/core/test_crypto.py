import base64
import hashlib
import pytest
from Crypto.Cipher import AES
from app.core import config
from app.core.crypto import TextCrypto, TextInfo, compare_hash

@pytest.fixture
def mock_aes_config(mocker):
    """Mock AES configuration with fixed key and IV for deterministic encryption."""
    mocker.patch.object(config, "AES_KEY", b"0123456789abcdef")
    mocker.patch.object(config, "AES_IV", b"abcdef9876543210")
    return config


def test_hash_text(mock_aes_config):
    text = "hello"
    crypto = TextCrypto(plain_text=text)
    hashed = crypto.hash_text()
    expected_hash = hashlib.sha256(text.encode()).hexdigest()
    assert hashed == expected_hash
    assert len(hashed) == 64

def test_compare_hash_true_false(mock_aes_config):
    text = "password"
    crypto = TextCrypto(plain_text=text)
    hash_val = crypto.hash_text()

    assert crypto.compare_hash(hash_val) is True
    assert crypto.compare_hash("invalid_hash") is False

def test_encrypt_and_decrypt_text(mock_aes_config):
    plain_text = "encryption test"
    crypto = TextCrypto(plain_text=plain_text)
    encrypted = crypto.encrypt_text()

    # It should be base64
    decoded = base64.b64decode(encrypted)
    assert len(decoded) > 16  # IV + ciphertext
    assert isinstance(encrypted, str)

    # Decrypt and check it matches original
    decryptor = TextCrypto(encrypted_text=encrypted)
    decrypted = decryptor.decrypt_text()
    assert decrypted == plain_text

def test_get_text_info(mock_aes_config):
    text = "sensitive"
    crypto = TextCrypto(plain_text=text)
    info = crypto.get_text_info()

    assert isinstance(info, TextInfo)
    assert info.plain_text == text
    assert isinstance(info.encrypted_text, str)
    assert len(info.hashed_text) == 64


def test_global_compare_hash(mock_aes_config):
    text = "checkme"
    hash_val = hashlib.sha256(text.encode()).hexdigest()
    assert compare_hash(text, hash_val) is True
    assert compare_hash(text, "invalid") is False


def test_encrypt_text_consistent_with_same_key(mock_aes_config):
    text = "repeatable"
    crypto1 = TextCrypto(plain_text=text)
    crypto2 = TextCrypto(plain_text=text)

    enc1 = crypto1.encrypt_text()
    enc2 = crypto2.encrypt_text()

    # Should produce same result due to fixed IV and key
    assert enc1 == enc2


def test_decrypt_with_invalid_base64(mock_aes_config):
    crypto = TextCrypto(encrypted_text="not_base64")
    with pytest.raises(Exception):
        crypto.decrypt_text()
