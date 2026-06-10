import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from cliente_modbus import ClienteModbus

_cliente = ClienteModbus('localhost', 502)
_cliente.conectar()
_tipo = 'HR'


class MyWidget(BoxLayout):

    def selecionar_tipo(self, tipo):
        global _tipo
        _tipo = tipo

    def ler(self):
        end_txt = self.ids.txt_reg.text.strip()
        if not end_txt.isdigit():
            self.ids.lbl_valor.text = 'Endereco invalido'
            return

        end = int(end_txt)
        val = None

        if _tipo == 'HR':
            val = _cliente.ler_holding_register(end)
        elif _tipo == 'IR':
            val = _cliente.ler_input_register(end)
        elif _tipo == 'COIL':
            val = _cliente.ler_coil(end)
        elif _tipo == 'DI':
            val = _cliente.ler_discrete_input(end)
        elif _tipo == 'FLOAT':
            val = _cliente.ler_float(end)
        elif _tipo == 'MB':
            val = _cliente.ler_bits_register(end)

        self.ids.lbl_valor.text = str(val) if val is not None else 'Falha'

    def escrever(self):
        end_txt = self.ids.txt_reg.text.strip()
        val_txt = self.ids.txt_escrita.text.strip()

        if not end_txt.isdigit():
            self.ids.lbl_valor.text = 'Endereco invalido'
            return

        end = int(end_txt)
        ok = False

        try:
            if _tipo == 'HR':
                ok = _cliente.escrever_holding_register(end, int(val_txt))
            elif _tipo == 'COIL':
                ok = _cliente.escrever_coil(end, int(val_txt))
            elif _tipo == 'FLOAT':
                ok = _cliente.escrever_float(end, float(val_txt))
            elif _tipo == 'MB':
                b, e = val_txt.split(',')
                ok = _cliente.escrever_bit_register(end, int(b), int(e))
            else:
                self.ids.lbl_valor.text = _tipo + ' somente leitura'
                return
        except Exception as ex:
            self.ids.lbl_valor.text = 'Erro: ' + str(ex)
            return

        self.ids.lbl_valor.text = 'OK' if ok else 'Falha'


class ModbusApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    Config.set('graphics', 'resizable', True)
    ModbusApp().run()
    _cliente.desconectar()