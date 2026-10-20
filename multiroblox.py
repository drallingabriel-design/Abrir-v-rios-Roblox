"""
Uso:
  1. Feche TODOS os Robloxes (olhe tambem no Gerenciador de Tarefas).
  2. Rode este arquivo e deixe a janela preta aberta.
  3. Abra o primeiro Roblox, depois o segundo.
  Para parar, feche a janela ou aperte Ctrl+C.
"""
import ctypes
import sys
import time

if sys.platform != "win32":
    print("Este programa so funciona no Windows.")
    input("Aperte Enter para sair...")
    sys.exit(1)

kernel32 = ctypes.windll.kernel32
kernel32.CreateMutexW.restype = ctypes.c_void_p
kernel32.CreateEventW.restype = ctypes.c_void_p

ERROR_ALREADY_EXISTS = 183

# Versoes antigas do cliente checam um mutex, as atuais um evento.
# Seguramos os dois para cobrir os casos.
mutex = kernel32.CreateMutexW(None, True, "ROBLOX_singletonMutex")
erro_mutex = kernel32.GetLastError()

evento = kernel32.CreateEventW(None, True, False, "ROBLOX_singletonEvent")
erro_evento = kernel32.GetLastError()

if not mutex and not evento:
    print("Nao consegui criar as travas. Tente rodar como administrador.")
    input("Aperte Enter para sair...")
    sys.exit(1)

if erro_mutex == ERROR_ALREADY_EXISTS or erro_evento == ERROR_ALREADY_EXISTS:
    print("ATENCAO: ja existe um Roblox aberto (ou outro programa segurando a trava).")
    print("Feche todos os Robloxes, feche esta janela e rode de novo.")
    input("Aperte Enter para sair...")
    sys.exit(1)

print("Ativo! Deixe esta janela aberta.")
print("Agora abra o primeiro Roblox, depois o segundo.")
print("(Ctrl+C para parar)")

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("Encerrado.")
