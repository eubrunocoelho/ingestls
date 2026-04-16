import os

# Pede o diretório ao usuário
while True:
    path = input('Digite o caminho do diretório: ')

    if os.path.isdir(path):
        break

    print('Caminho inválido, tente novamente')

# Arquivo de saída (no diretório autal do script)
output_file = os.path.join(os.getcwd(), 'resultado.txt')

with open(output_file, 'w', encoding='utf-8') as output:
    for file in os.listdir(path):
        full_path = os.path.join(path, file)

        # Garante que é arquivo
        if os.path.isfile(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    output.write(f'-- {file} --\n')  # identifica o arquivo
                    output.write(f.read())
                    output.write('\n\n')  # separação entre arquivos

                print(f'Adicionado: {file}')

            except Exception as e:
                print(f'Erro ao ler {file}: {e}')

print(f'\nArquivo gerado em: {output_file}')
