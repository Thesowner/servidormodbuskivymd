import os
import sys
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import kivymd
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.config import Config
from cliente_modbus import ClienteModbus


class MyWidget(MDBoxLayout):
    _clock_event = None
    _tipo = 'HR'  

    def selecionar_tipo(self, tipo):
        self._tipo = tipo
        _hints = {
            'HR':   'Ex: 42',
            'COIL': 'Ex: 1 ou 0',
            'FLOAT':'Ex: 3.14',
            'MB':   'Ex: 0:1,3:0,5:1 (bit:estado,bit:estado,...)',
        }
        self.ids.txt_escrita.hint_text = _hints.get(tipo, 'Ex: 42')

    def ler(self):
        end_txt = self.ids.txt_reg.text.strip()
        if not end_txt.isdigit():
            self.ids.lbl_valor.text = 'Endereco invalido'
            return

        end = int(end_txt)
        val = None

        if self._tipo == 'HR':
            val = self._cliente.ler_holding_register(end)
        elif self._tipo == 'COIL':
            val = self._cliente.ler_coil(end)
        elif self._tipo == 'FLOAT':
            val = self._cliente.ler_float(end)
        elif self._tipo == 'MB':
            val = self._cliente.ler_bits_register(end)

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
            if self._tipo == 'HR':
                ok = self._cliente.escrever_holding_register(end, int(val_txt))
            elif self._tipo == 'COIL':
                ok = self._cliente.escrever_coil(end, int(val_txt))
            elif self._tipo == 'FLOAT':
                ok = self._cliente.escrever_float(end, float(val_txt))
            elif self._tipo == 'MB':
                pares = []
                for par in val_txt.split(','):
                    b, e = par.strip().split(':')
                    pares.append((int(b), int(e)))
                ok = self._cliente.escrever_bits_register(end, pares)
            else:
                self.ids.lbl_valor.text = self._tipo + ' somente leitura'
                return
        except Exception as ex:
            self.ids.lbl_valor.text = 'Erro: ' + str(ex)
            return

        self.ids.lbl_valor.text = 'OK' if ok else 'Falha'

    def set_recorrente(self, active):
        if active:

            scan = self._cliente.get_scan_time() if hasattr(self, '_cliente') else 2.5
            self._clock_event = Clock.schedule_interval(lambda dt: self.ler(), scan)
        else:
            if self._clock_event is not None:
                self._clock_event.cancel()
                self._clock_event = None

    def connect(self):
        if self._clock_event is not None:
            self._clock_event.cancel()
            self._clock_event = None

        ip = self.ids.txt_ip.text.strip()
        porta = self.ids.txt_porta.text.strip()
        self._cliente = ClienteModbus(ip, porta, scan_time=2.5)
        self._cliente.conectar()



class ModbusApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return MyWidget()


if __name__ == '__main__':
    Config.set('graphics', 'resizable', True)
    ModbusApp().run()