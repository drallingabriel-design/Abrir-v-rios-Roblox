"""
multiroblox.py - permite abrir mais de um cliente Roblox (Windows) ao mesmo tempo.

Como funciona: o Roblox checa se ja existe uma "trava" do sistema com um nome
especifico. Este programa cria essa trava ANTES do Roblox abrir, entao os
clientes nao se bloqueiam. Ele nao mexe no Roblox, nao injeta nada e nao
acessa a internet.

Uso:
  1. Feche TODOS os Robloxes (olhe tambem no Gerenciador de Tarefas).
  2. Rode este arquivo e deixe a janela preta aberta.
  3. Abra o primeiro Roblox, depois o segundo.
  Para parar, feche a janela ou aperte Ctrl+C.
"""
import ctypes
import os
import sys
import time

os.system("")  # ativa os codigos ANSI (cores/cursor) no terminal do Windows

BRANCO = "\033[1;97m"
RESET = "\033[0m"
ESCONDE_CURSOR = "\033[?25l"
MOSTRA_CURSOR = "\033[?25h"

# Tons de cinza usados no "brilho" de cada letra, do escuro ao branco.
TONS = (238, 245, 252)


def escreve(texto):
    sys.stdout.write(texto)
    sys.stdout.flush()


def aparece(texto, atraso=0.05):
    """Faz cada letra surgir em cinza escuro e clarear ate ficar branca."""
    for letra in texto:
        if letra == " ":
            escreve(" ")
            time.sleep(atraso)
            continue
        for tom in TONS:
            escreve(f"\033[1;38;5;{tom}m{letra}\b")
            time.sleep(0.02)
        escreve(f"{BRANCO}{letra}{RESET}")
        time.sleep(atraso)


def linha_gradual(caractere, tamanho, atraso=0.012):
    """Desenha uma linha da esquerda para a direita."""
    escreve(BRANCO)
    for _ in range(tamanho):
        escreve(caractere)
        time.sleep(atraso)
    escreve(RESET)


def centralizado(texto, largura):
    return " " * ((largura - len(texto)) // 2)


def banner():
    largura = 44
    titulo = "P O R   J A R V A N"
    agradecimento = "Obrigado Por Utilizar"

    escreve(ESCONDE_CURSOR)
    try:
        print()
        linha_gradual("=", largura)
        print("\n")
        escreve(centralizado(titulo, largura))
        aparece(titulo, atraso=0.07)
        print("\n")
        time.sleep(0.3)
        escreve(centralizado(agradecimento, largura))
        aparece(agradecimento, atraso=0.05)
        print("\n")
        linha_gradual("=", largura)
        print("\n")
    finally:
        escreve(MOSTRA_CURSOR)


banner()

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
