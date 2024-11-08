import string, secrets, hashlib, base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from typing import Union

class FernetHasher:
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_lowercase
    BASE_DIR = Path(__file__).resolve().parent.parent  #fornece o caminho da raiz até o arquivo onde o processo está
    KEY_DIR = BASE_DIR / 'keys'   #pasta para armazenar os arquivos

    #Cria uma instãncia de Fernet para cada usuario/entidade diferente
    def __init__(self, key: Union[Path, str]):
        if not isinstance(key, bytes):
            key = key.encode()
        self.fernet = Fernet(key)

    @classmethod
    def _get_random_string(cls, lenght=25):   # gera string aleatória
        string = ''
        for i in range(lenght):
            string += secrets.choice(cls.RANDOM_STRING_CHARS)
        return string

    #Método para criar a hash da chave e converter para b64
    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_random_string()

        # encode a string transforma para byte
        # digest => tranforma para string de novo
        # base64 => forma padrão de comunicação entre sistemas binários
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)
        if archive:
            print(key)
            return key, cls.archive_key(key)
        return key, None

    #Método para salvar a chave
    @classmethod
    def archive_key(cls, key):
        file = 'key.key'
        while Path(cls.KEY_DIR / file).exists():
            file = f'key_{cls._get_random_string(5)}.key'
        
        with open(cls.KEY_DIR / file, 'wb') as arq:
            arq.write(key)
    
        return cls.KEY_DIR / file

    def encrypt(self, value):  #gera a senha criptografada
        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        return self.fernet.encrypt(value)

    def decrypt(self, value):   #descriptogra a senha
        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken as e:
            return 'Token inválido'

