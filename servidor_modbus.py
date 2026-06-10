from pyModbusTCP.server import DataBank, ModbusServer
import random
from time import sleep
from time import perf_counter


class ServidorMODBUS():
    """
    Classe Servidor Modbus
    """
    
    def __init__(self, host_ip, port):
        """
        Construtor
        """
        self._db = DataBank()
        self._server = ModbusServer(host=host_ip,port=port,no_block=True,data_bank=self._db)
       
        
    def run(self):
        """
        Execução do servidor Modbus
        """
        try:
            self._server.start()
            print("Servidor MODBUS em execução")
            count = 0
            while True:
                if count == 0:
                    t_init = perf_counter()
                    count += 1
                sleep(1)
                t = perf_counter() - t_init
                print('Servidor rodando a {:.0f}s'.format(t))
        except Exception as e:
            print("Erro: ",e.args)
if __name__ == '__main__':
    s = ServidorMODBUS('localhost', 502)
    s.run()