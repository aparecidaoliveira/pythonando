from datetime import datetime
from pathlib import Path

class BaseModel:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'

    # devolve o nome da classe qiue efetuou a chamada
    def save(self):
        table_path = Path(self.DB_DIR / f'{self.__class__.__name__}.txt')  
        if not table_path.exists():
            table_path.touch()   #cria o arquivo quando o mesmo não exista
        with open(table_path, 'a') as arq:
            # map(str) => transforma em string
            # list => transforma em uma lista 
            arq.write("|".join(list(map(str, self.__dict__.values()))))  #grava a nova senha com os atributos separados por "|" 
            arq.write('\n')


    @classmethod
    def get(cls):
        table_path = Path(cls.DB_DIR / f'{cls.__name__}.txt')
        if not table_path.exists():
            table_path.touch()
        with open(table_path, 'r') as arq:
            x = arq.readlines()
    
        results = []
        atributos = vars(cls()).keys()
        for i in x:
            split_v = i.split('|')
            tmp_dict = dict(zip(atributos, split_v))  #cria um dicionário unificado/zipado com os atributos e valores
            results.append(tmp_dict)
        return results 
         
class Password(BaseModel):
    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()
        self.expire = 1 if expire else 0

p1 = Password(domain='youtube.com.br', password='2345')
#p1.save()
Password.get()