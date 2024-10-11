import quicktoolbar
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pyperclip
password = input("输入密码").encode()
salt = input("输入盐密码").encode()
#region
# 密钥派生函数设置
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
# 根据密码生成密钥
key = base64.urlsafe_b64encode(kdf.derive(password))
# 使用密钥创建Fernet实例
cipher_suite = Fernet(key)
#endregion
def Encryption():
    clipboard = pyperclip.paste()
    if type(clipboard) is not str:
        return
    clipboard = clipboard.encode('utf-8')
    returnString = cipher_suite.encrypt(clipboard)
    returnString = base64.urlsafe_b64encode(returnString).decode('utf-8')
    pyperclip.copy(returnString)
    return 
    return returnString
quicktoolbar.createButton(
    name = "加密",
    command = Encryption,
    mode = quicktoolbar.Mode.Api,
    returnType=quicktoolbar.ReturnType.Auto,
)

def Decrypt():
    clipboard = pyperclip.paste()
    if type(clipboard) is not str:
        return
    recovered_encrypted_data = base64.urlsafe_b64decode(clipboard.encode('utf-8'))
    decrypted_data = cipher_suite.decrypt(recovered_encrypted_data).decode('utf-8')
    return decrypted_data
quicktoolbar.createButton(
    name = "解密",
    command = Decrypt,
    mode = quicktoolbar.Mode.Api,
    returnType=quicktoolbar.ReturnType.Auto,
)

quicktoolbar.run()