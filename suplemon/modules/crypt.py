# -*- encoding: utf-8
import base64
import hashlib
import binascii
from Crypto import Random
from Crypto.Cipher import AES

from suplemon.suplemon_module import Module
from suplemon.prompt import PromptPassword


def password_to_key(password, salt):
    # scrypt deflaults
    cost = 16384
    block_size = 8
    parallelization = 1
    dk = hashlib.scrypt(
        bytes(password, "utf-8"),
        salt=bytes(salt, "utf-8"),
        n=cost,
        r=block_size,
        p=parallelization,
        dklen=16
    )
    return binascii.hexlify(dk)


def pad_data(s):
    return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)


def unpad_data(s):
    return s[:-ord(s[len(s)-1:])]


def encrypt(data, password, salt):
    if not password:
        raise ValueError("password must be a non empty string")
    key = password_to_key(password, salt)
    data = pad_data(data)

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encoded = base64.b64encode(iv + cipher.encrypt(data)).decode('utf-8')
    return encoded


def decrypt(data, password, salt):
    key = password_to_key(password, salt)
    data = base64.b64decode(data)

    iv = data[:AES.block_size]

    cipher = AES.new(key, AES.MODE_CBC, iv)  # never use ECB in strong systems obviously
    decoded = cipher.decrypt(data[AES.block_size:]).decode("utf-8")
    result = unpad_data(decoded)
    return result


class Crypt(Module):
    """
    Encrypt or decrypt the current buffer. Lets you provide a passphrase and optional salt for encryption.
    Uses AES for encryption and scrypt for key generation.
    """

    def init(self):
        self.methods = {
            "e": self.encrypt,
            "d": self.decrypt,
        }

        self.actions = {
            "e": "Encryption",
            "d": "Decryption",
        }

    def encrypt(self, editor, options):
        result = encrypt(editor.get_data(), options[0], options[1])
        editor.set_data(result)

    def decrypt(self, editor, options):
        result = decrypt(editor.get_data(), options[0], options[1])
        editor.set_data(result)

    def query_options(self):
        pwd = self.app.ui._query("Password:", initial="", cls=PromptPassword, inst=None)

        if not pwd:
            return False
        salt = self.app.ui.query("Password Salt (optional):")

        if not salt:
            salt = ""
        return (pwd, salt)

    def handler(self, prompt, event):
        if event.key_name.lower() in self.methods.keys():
            prompt.set_data(event.key_name.lower())
            prompt.on_ready()
        return True  # Disable normal key handling

    def run(self, app, editor, args):
        key = app.ui.query_filtered("Press E to encrypt or D to decrypt:", handler=self.handler)
        if not key:
            return
        method = self.methods[key]

        options = self.query_options()
        if not options:
            app.set_status("You must specify a password!")
            return

        # Run the encryption or decryption on the editor buffer
        try:
            method(editor, options)
        except:
            app.set_status(self.actions[key] + " failed.")


module = {
    "class": Crypt,
    "name": "crypt",
}
