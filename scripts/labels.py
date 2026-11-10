"""Shared display labels and tolerant lookup keys for profile generators."""
import re
import unicodedata

_TRANSLATION=str.maketrans({'ı':'i','İ':'I','ş':'s','Ş':'S','ğ':'g','Ğ':'G','ç':'c','Ç':'C','ö':'o','Ö':'O','ü':'u','Ü':'U'})
def match_key(value):
 value=unicodedata.normalize('NFKC',str(value)).translate(_TRANSLATION).casefold()
 value=''.join(ch for ch in unicodedata.normalize('NFKD',value) if not unicodedata.combining(ch))
 value=value.replace('&','and')
 return re.sub(r'[^a-z0-9+#]+','',value)

def lookup_index(mapping):
 result={}
 for label,value in mapping.items():
  key=match_key(label)
  if key in result and result[key]!=value:raise ValueError(f'Conflicting normalized label: {label}')
  result[key]=value
 return result

_SPECIAL=['MQTT','OpenSCAD','UART','I²C','SPI','CAN','C','C++','C#','MATLAB','Simulink','PSIM','LTspice','Proteus','STM32','ESP32','KiCad','EAGLE','Quartus','ModelSim','Linux','Python','VHDL','Verilog','ROS 2','FreeRTOS','Raspberry Pi','NanoEdge AI Studio','Git','Gazebo','SolidWorks','Fusion','CAD','3D Printing','TinyML','DSP','PLC','IoT','AI','PV','HVAC','GitHub','LinkedIn','Microsoft Office','Windows','PowerShell','Inno Setup']
_SPECIAL={match_key(label):label for label in _SPECIAL}
_SMALL={'and','or','of','the','in','on','at','to','for','with','a','an','as','but','nor','ve','veya','ile'}
def display_label(value):
 value=unicodedata.normalize('NFC',str(value))
 if match_key(value) in _SPECIAL:return _SPECIAL[match_key(value)]
 # Repository identifiers, URLs and date/data strings are not editorial labels.
 if '://' in value or re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+){2,}',value):return value
 def word(m):
  token=m.group();key=match_key(token)
  if key in _SPECIAL:return _SPECIAL[key]
  if token.casefold() in _SMALL:return token[:1].upper()+token[1:].lower() if m.start()==0 else token.lower()
  return token[:1].upper()+token[1:].lower()
 return re.sub(r"[^\W_]+(?:[+#]+)?",word,value,flags=re.UNICODE)
