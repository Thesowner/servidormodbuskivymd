from pymodbus.client import ModbusTcpClient


class ClienteModbus:
    def __init__(self, host, port, scan_time=1):
        self._tcp = ModbusTcpClient(host=host, port=port)
        self._tempo_varredura = scan_time

    def conectar(self):
        return self._tcp.connect()

    def desconectar(self):
        self._tcp.close()

    def get_scan_time(self):
        return self._tempo_varredura

    def set_scan_time(self, novo_tempo):
        self._tempo_varredura = float(novo_tempo)

    def ler_holding_register(self, endereco):
        resp = self._tcp.read_holding_registers(address=endereco, count=1, device_id=1)
        if resp and not resp.isError():
            return resp.registers[0]
        return None

    def escrever_holding_register(self, endereco, valor):
        resp = self._tcp.write_register(address=endereco, value=valor, device_id=1)
        if resp and not resp.isError():
            return True
        return False

    def ler_coil(self, endereco):
        r = self._tcp.read_coils(address=endereco, count=1, device_id=1)
        if r and not r.isError():
            return r.bits[0]
        return None

    def escrever_coil(self, endereco, valor):
        r = self._tcp.write_coil(address=endereco, value=bool(valor), device_id=1)
        if r and not r.isError():
            return True
        return False

    def ler_input_register(self, endereco):
        resp = self._tcp.read_input_registers(address=endereco, count=1, device_id=1)
        if resp and not resp.isError():
            return resp.registers[0]
        return None

    def ler_discrete_input(self, endereco):
        resp = self._tcp.read_discrete_inputs(address=endereco, count=1, device_id=1)
        if resp and not resp.isError():
            return resp.bits[0]
        return None

    def escrever_float(self, endereco, valor):
        regs = self._tcp.convert_to_registers(valor, self._tcp.DATATYPE.FLOAT32)
        r = self._tcp.write_registers(address=endereco, values=regs, device_id=1)
        if r and not r.isError():
            return True
        return False

    def ler_float(self, endereco):
        resp = self._tcp.read_holding_registers(address=endereco, count=2, device_id=1)
        if resp and not resp.isError():
            return self._tcp.convert_from_registers(resp.registers, self._tcp.DATATYPE.FLOAT32)
        return None

    def ler_bits_register(self, endereco):
        leitura = self.ler_holding_register(endereco)
        if leitura is None:
            return None
        bits = [(leitura >> i) & 1 for i in range(16)]
        return bits

    def escrever_bit_register(self, endereco, bit, estado):
        leitura = self.ler_holding_register(endereco)
        if leitura is None:
            return False
        if estado == 1:
            leitura = leitura | (1 << bit)
        else:
            leitura = leitura & ~(1 << bit)
        return self.escrever_holding_register(endereco, leitura)
