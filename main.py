import os
import fnmatch


# Função para detectar arquivo binário
def is_binary(file_path):
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)  # Lê só os primeiros 1kb

            if b'\x00' in chunk:
                return True  # binário (tem byte nulo)

        return False  # provavelmente texto
    except:
        return True  # se deu erro, trate como binário


# Função para determinar os arquivos que devem ser ignorados
def should_ignore(file_path, ignore_patterns, base_path):
    rel_path = os.path.relpath(file_path, start=base_path)

    for pattern in ignore_patterns:
        pattern = pattern.strip()

        # Ignorar diretórios (ex: node_modules/)
        if pattern.endswith('/'):
            if pattern[:-1] in rel_path.split(os.sep):
                return True

        # Ignorar por padrão (*.md)
        elif fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True

        # Ignorar arquivo exato
        elif os.path.basename(file_path) == pattern:
            return True

    return False


# 1. Pergunta o que ignorar
ignore_input = input('Digite o que deseja ignorar (ex: *.md, node_modules/, arquivo.txt): ')
ignore_patterns = [p.strip() for p in ignore_input.split(',') if p.strip()]

# 2. Pede o diretório ao usuário
while True:
    path = input('Digite o caminho do diretório: ')

    if os.path.isdir(path):
        break

    print('Caminho inválido, tente novamente')

# Arquivo de saída (no diretório autal do script)
output_file = os.path.join(os.getcwd(), 'resultado.txt')

with open(output_file, 'w', encoding='utf-8') as output:
    for root, dirs, files in os.walk(path):

        # Remove diretórios ignorados da varredura
        dirs[:] = [
            d for d in dirs
            if not should_ignore(os.path.join(root, d), ignore_patterns, path)
        ]

        for file in files:
            full_path = os.path.join(root, file)

            # Evita ler o próprio arquivo de saída
            if os.path.abspath(full_path) == os.path.abspath(output_file):
                continue

            # Ignora padrões
            if should_ignore(full_path, ignore_patterns, path):
                print(f'Ignorado (regra): {full_path}')
                continue

            # Ignora binários
            if is_binary(full_path):
                print(f'Ignorado (binário): {full_path}')
                continue

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    output.write(f'-- {full_path} --\n')
                    output.write(f.read())
                    output.write('\n\n')

                print(f'Adicionado: {full_path}')

            except Exception as e:
                print(f'Erro ao ler {full_path}: {e}')

print(f'\nArquivo gerado em: {output_file}')
