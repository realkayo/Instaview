import os, time
import importlib.util


libraries = ['instaloader', 'Pillow', 'colorama', 'art', 're']

missing_libraries = [lib for lib in libraries if importlib.util.find_spec(lib) is None]

os.system('cls')
os.system('title Instaview by Kayo')
if missing_libraries:
    print("Instalando bibliotecas ausentes...")
    for lib in missing_libraries:
        os.system(f"pip install {lib}")
    print("Bibliotecas instaladas com sucesso!")

import instaloader
from PIL import Image
from colorama import Fore, Style
from art import *
import re


ig = instaloader.Instaloader()  # API


def criptografar(texto, chave):
    texto_criptografado = ''
    for char in texto:
        if char.isalpha():
            novo_char = chr((ord(char) + chave - 65) % 26 + 65) if char.isupper() else chr((ord(char) + chave - 97) % 26 + 97)
            texto_criptografado += novo_char
        else:
            texto_criptografado += char
    return texto_criptografado

def descriptografar(texto_criptografado, chave):
    return criptografar(texto_criptografado, -chave)


def salvar_credenciais(user, password):
    with open('auth.txt', 'w') as f:
        f.write(criptografar(user, 22) + f"\n{criptografar(password, 22)}")


def carregar_credenciais():
    if os.path.exists('auth.txt'):
        with open('auth.txt', 'r') as f:
            user = f.readline().strip()
            password = f.readline().strip()
        return descriptografar(user, 22), descriptografar(password, 22) # descriptografa e retorna
    return None, None

def salvar_informacoes(user, perfil):
    pasta_usuario = user
    os.makedirs(pasta_usuario, exist_ok=True)

    caminho_arquivo = os.path.join(pasta_usuario, "info.txt")

    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write('------ Perfil do Instagram ------\n')
            arquivo.write('\nNome: ' +  perfil.username)
            arquivo.write('\nNúmero de posts: '  + str(perfil.mediacount))
            arquivo.write('\nSeguidores: ' + str(perfil.followers))
            arquivo.write('\nSeguindo: ' + str(perfil.followees))
            arquivo.write('\n')
            arquivo.write('\nFoto de Perfil (link): '  + str(perfil.profile_pic_url))
            arquivo.write('\n')
            arquivo.write('\nPrivado : '  + str(perfil.is_private))
            arquivo.write('\nVerificado : ' + str(perfil.is_verified))
            arquivo.write('\n')
            arquivo.write('\nBio: ') 
            arquivo.write("\n" + perfil.biography)
            arquivo.write('\n')
            

    os.system('cls')
    print(Style.RESET_ALL + 'Informações salvas em', caminho_arquivo)
    print()

def abrir_imagem(user):
    pasta_usuario = user
    padrao = re.compile(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_UTC_profile_pic\.jpg")
    for nome_arquivo in os.listdir(pasta_usuario):
        if padrao.match(nome_arquivo):
            caminho_imagem = os.path.join(pasta_usuario, nome_arquivo)
            imagem = Image.open(caminho_imagem)
            imagem.show()
            return
    print(Fore.LIGHTRED_EX + "Nenhuma imagem de perfil encontrada para ", user)

def input_valido(mensagem, opcoes):
    while True:
        entrada = input(mensagem).strip().lower()
        if entrada in opcoes:
            return entrada
        else:
            
            print(Fore.LIGHTRED_EX + "Opção inválida. Por favor, escolha entre", opcoes)


def login(user, password):
    try:
        ig.login(user, password)
    except Exception as err:
        print(Fore.LIGHTRED_EX + '--> Erro no login: ' + str(err))
        print()
        return False
    return True
    
def iniciar(userlogado):
    os.system('cls')
    print( Fore.LIGHTRED_EX + text2art('Instaview', font="small"))
    if userlogado != 'nao_logado':
            print(Fore.CYAN + '|' + Fore.RESET + '  Logado como: ' + Fore.LIGHTRED_EX + '|  ' + Fore.RESET + str(userlogado))
    else:
        print(Fore.CYAN + '|' + Fore.RESET + '  Logado como: ' + Fore.LIGHTRED_EX + '| ' + Fore.RESET + "nao_logado")
    print('')
    print('')
    print('Coloque o User: '+  Fore.CYAN)
    user = input('-->  ' + Fore.RESET + '@')
    perfil = instaloader.Profile.from_username(ig.context, user)
    os.system('cls')

    print(Fore.LIGHTRED_EX + '------ Perfil do Instagram ------')
    print()
    print(Fore.LIGHTRED_EX+ 'Nome: ' + Fore.RESET + perfil.username)
    print(Fore.LIGHTRED_EX + 'Número de posts: '  + Fore.RESET + str(perfil.mediacount))
    print(Fore.LIGHTRED_EX + 'Seguidores: '  + Fore.RESET + str(perfil.followers))
    print(Fore.LIGHTRED_EX + 'Seguindo: '  + Fore.RESET + str(perfil.followees))
    print()
    print(Fore.LIGHTRED_EX+ 'Foto de Perfil (link): '  + Fore.RESET + str(perfil.profile_pic_url))
    print()
    print(Fore.LIGHTRED_EX+ 'Privado : '  + Fore.RESET + str(perfil.is_private))
    print(Fore.LIGHTRED_EX+ 'Verificado : '  + Fore.RESET + str(perfil.is_verified))
    print()
    print(Fore.LIGHTRED_EX + 'Bio: '  + Fore.RESET) 
    print(perfil.biography)
    print()

    opcoes_salvar = ['s', 'n']
    resposta_salvar = input_valido(Fore.LIGHTRED_EX + 'Deseja salvar as informações? (s/n): ' + Fore.RESET, opcoes_salvar)
    if resposta_salvar == 's':
        salvar_informacoes(user, perfil)
    os.system('cls')
    opcoes_baixar = ['s', 'n']
    resposta_baixar = input_valido(Fore.LIGHTRED_EX + 'Deseja baixar a foto de perfil da pessoa? (Alta qualidade) (s/n): ' + Fore.RESET, opcoes_baixar)
    if resposta_baixar == 's':
        os.system('cls')
        print(Fore.LIGHTGREEN_EX + 'Baixando foto de perfil...')
        ig.download_profile(user, profile_pic_only=True)
        print(Fore.LIGHTGREEN_EX + 'Perfil baixado.')
        os.system('cls')

    opcoes_abrir = ['s', 'n']
    resposta_abrir = input_valido(Fore.CYAN + 'Deseja abrir a imagem baixada? (s/n): ' + Fore.RESET, opcoes_abrir)
    if resposta_abrir == 's':
        os.system('cls')
        abrir_imagem(user)

def main():
    os.system("cls")
    user, password = carregar_credenciais()
    if not user or not password:
        print()
        print(Fore.LIGHTRED_EX + '------       login' + Fore.RESET)
        print(Fore.YELLOW + '[!] ' + Fore.RESET + 'voce deve logar na sua conta do instagram para evitar erros no programa.')
        print(Fore.YELLOW + '[!] ' + Fore.RESET + 'caso nao queira logar, coloque o usuario e senha como "a" ')
        print(Fore.LIGHTYELLOW_EX + '[+] ' + Fore.RESET + 'depois de logar o programa vai salvar seu login, para fazer login automatico da proxima vez.')
        print()
        username = input(Fore.CYAN + "Usuário --> " + Fore.RESET)
        password = input(Fore.CYAN + "Senha --> " + Fore.RESET)
        if username.lower() == 'a' and password.lower() == 'a':
            iniciar('nao_logado')
            return
        login_success = login(username, password)
        if login_success:
            salvar_credenciais(username, password)
            iniciar(username)
        else:
            time.sleep(3)
            main()

    else:
        print(Fore.YELLOW + '[!] ' + Fore.RESET + f" tentando logar na conta: ({user})")
       # print(user) 
       # print(password)
        tentarLogar = login(user, password)
        if tentarLogar:
            print(Fore.GREEN + "Login automático realizado com sucesso." + Fore.RESET)
            time.sleep(1)
            iniciar(user)
        else:
            print(Fore.LIGHTRED_EX + '--> ocorreu um erro no login automatico')
            os.system("del auth.txt")
            time.sleep(3)
            main()



if __name__ == "__main__":
    os.system('cls')
    main()
