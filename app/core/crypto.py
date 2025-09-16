""" Util for cryptography """
import base64
import hashlib
from typing import Optional

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from app import settings

class TextInfo:
    """
        Object of text information
    """
    def __init__(self, plain_text:str, encrypted_text:str, hashed_text:str):
        self.plain_text=plain_text
        self.encrypted_text=encrypted_text
        self.hashed_text=hashed_text


class TextCrypto:
    """
        Class to encrypt and decrypt text
    """
    def __init__(self, plain_text: Optional[str]=None, encrypted_text:Optional[str]=None):
        """
            constructor gets the args and set the text or encrypted text
            args:
                plain_text[str] -> Plain text to hash or encrypted
                encrypted_text[str] -> Encrypted text
        """
        self.__plain_text: str = plain_text or ""
        self.__encrypted_text: str = encrypted_text or ""

    def get_text_info(self) -> TextInfo:
        """
            Return a text object with plain text and data crypto values
            return:
                object with plain_text, encrypted_text, hashed_text
        """
        self.__encrypted_text = self.encrypt_text()
        hashed_text = self.hash_text()

        return TextInfo(
            plain_text=self.__plain_text,
            encrypted_text=self.__encrypted_text,
            hashed_text=hashed_text
        )

    def set_text(self, plain_text:str):
        """
            set text to hash or encrypt
            args:
                plain_text: str -> text to hash
        """
        self.__plain_text = plain_text

    def set_encrypted_text(self, encrypted_text:str):
        """
            set encrypted text to decrypt
            args:
                encrypted_text: str -> encrypted text to decrypt
        """

    def hash_text(self) -> str:
        """
            Hash text from plain text to sha256
            args:
                plain text: str -> text to hash
            return:
                str of the hex of the sha256 hash
        """
        sha256 = hashlib.sha256()
        binary_text = self.__plain_text.encode("UTF-8")
        sha256.update(binary_text)
        return sha256.hexdigest()

    def compare_hash(self, hashed_text: str) -> bool:
        """
            Compare plain text with sha256 hash
            args:
                plain text: str -> text to compare
                hash: str -> a sha25 hash to compare
            return:
                Boolean result if are the same hashes or not
        """
        new_hashed_text = self.hash_text()
        return hashed_text == new_hashed_text

    def encrypt_text(self) -> str:
        """
            Encrypt text to AES
            args:
                plain text: str -> text to encrypt
            return:
                str of the base64 of the AES encryption
        """
        aes_context = AES.new(settings.AES_KEY, AES.MODE_CBC, settings.AES_IV)
        padded_text = pad(self.__plain_text.encode(), AES.block_size)
        encrypted_bytes = aes_context.encrypt(padded_text)
        return base64.b64encode(settings.AES_IV + encrypted_bytes).decode()

    def decrypt_text(self) -> str:
        """
            Decrypt AES to plain text
            args:
                encrypted_text: str -> encrypted base64 text to decrypt
            return:
                str of the plain text of the base64 text decryption
        """
        encrypted_data = base64.b64decode(self.__encrypted_text)
        iv = encrypted_data[:16]
        encrypted_bytes = encrypted_data[16:]
        cipher = AES.new(settings.AES_KEY, AES.MODE_CBC, iv)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        self.__plain_text = decrypted_bytes.decode()
        return self.__plain_text


def compare_hash(data, hashed_data) -> bool:
    """
    Compares a plain-text value with a hashed value to check for a match.

    Args:
        data (str): The plain-text input to be hashed and compared.
        hashed_data (str): The existing hashed value to compare against.

    Returns:
        bool: True if the hashed version of `data` matches `hashed_data`, False otherwise.
    """
    crypt_data = TextCrypto(plain_text=data)
    return crypt_data.hash_text() == hashed_data
