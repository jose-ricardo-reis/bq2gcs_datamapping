import os
import csv
import zipfile
from google.cloud import bigquery
from datetime import date

def exportar_informacoes_do_dataset(id_projeto):
    # Cria um cliente BigQuery com o projeto fornecido
    cliente = bigquery.Client(project=id_projeto)
    # Lista todos os datasets no projeto
    datasets = cliente.list_datasets()

    # Lista para armazenar as informações do dataset
    informacoes_do_dataset = [['Nome do Dataset', 'Quantidade de Tabelas']]

    # Itera sobre os datasets encontrados
    for dataset in datasets:
        # Obtém o nome do dataset
        nome_dataset = dataset.dataset_id
        # Lista todas as tabelas do dataset
        quantidade_tabelas = len(list(cliente.list_tables(dataset.reference)))
        # Armazena o nome do dataset e a quantidade de tabelas
        informacoes_do_dataset.append([nome_dataset, quantidade_tabelas])

    return informacoes_do_dataset

def exportar_esquema_da_tabela(id_projeto, nome_dataset):
    # Cria um cliente BigQuery com o projeto fornecido
    cliente = bigquery.Client(project=id_projeto)
    # Obtém uma referência para o dataset específico
    referencia_dataset = cliente.dataset(nome_dataset)
    # Lista todas as tabelas do dataset
    tabelas = cliente.list_tables(referencia_dataset)

    # Lista para armazenar os esquemas das tabelas
    esquemas_das_tabelas = [['Nome do Dataset', 'Nome da Tabela', 'Campo (Coluna)', 'Descrição', 'Tipo de Campo']]

    # Itera sobre as tabelas encontradas
    for tabela in tabelas:
        # Obtém o nome da tabela
        nome_tabela = tabela.table_id
        # Obtém uma referência para a tabela específica
        referencia_tabela = referencia_dataset.table(nome_tabela)
        # Obtém as informações da tabela
        tabela = cliente.get_table(referencia_tabela)
        # Itera sobre os campos (campos) da tabela
        for campo in tabela.schema:
            # Armazena as informações do dataset, tabela, campo (coluna), descrição e tipo de campo
            esquemas_das_tabelas.append([nome_dataset, nome_tabela, campo.name, campo.description, campo.field_type])

    return esquemas_das_tabelas

def exportar_quantidade_de_colunas(id_projeto, nome_dataset):
    # Cria um cliente BigQuery com o projeto fornecido
    cliente = bigquery.Client(project=id_projeto)
    # Obtém uma referência para o dataset específico
    referencia_dataset = cliente.dataset(nome_dataset)
    # Lista todas as tabelas do dataset
    tabelas = cliente.list_tables(referencia_dataset)

    # Lista para armazenar a quantidade de colunas das tabelas
    lista_quantidade_colunas = [['Nome do Dataset', 'Nome da Tabela', 'Quantidade de Colunas']]

    # Itera sobre as tabelas encontradas
    for tabela in tabelas:
        # Obtém o nome da tabela
        nome_tabela = tabela.table_id
        # Obtém uma referência para a tabela específica
        referencia_tabela = referencia_dataset.table(nome_tabela)
        # Obtém as informações da tabela
        tabela = cliente.get_table(referencia_tabela)
        # Armazena o nome do dataset, nome da tabela e quantidade de colunas da tabela
        lista_quantidade_colunas.append([nome_dataset, nome_tabela, len(tabela.schema)])

    return lista_quantidade_colunas

def exportar_para_csv(data, nome_arquivo):
    # Exporta os dados para um arquivo CSV
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerows(data)

def deletar_arquivos(nomes_arquivos):
    # Deleta os arquivos especificados
    for nome_arquivo in nomes_arquivos:
        os.remove(nome_arquivo)

def compactar_pastas(pastas, nome_arquivo_zip):
    # Compacta as pastas em um arquivo ZIP
    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        for pasta in pastas:
            for raiz, _, arquivos in os.walk(pasta):
                for arquivo in arquivos:
                    caminho_arquivo = os.path.join(raiz, arquivo)
                    zipf.write(caminho_arquivo, os.path.relpath(caminho_arquivo, pasta))

def compactar_arquivos(nomes_arquivos, nome_arquivo_zip):
    # Compacta os arquivos em um arquivo ZIP
    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        for nome_arquivo in nomes_arquivos:
            zipf.write(nome_arquivo, os.path.basename(nome_arquivo))

def upload_para_bucket(bucket, nome_arquivo):
    comando_gsutil = f"gsutil cp {nome_arquivo} gs://{bucket}/{nome_arquivo}"
    os.system(comando_gsutil)

def main(id_projeto):
    # Obtém a data atual
    data_atual = date.today().strftime("%d-%m-%y")
    # Define o nome do arquivo ZIP final
    nome_arquivo_zip_final = f"{id_projeto}_{data_atual}.zip"

    # Exporta as informações do dataset para um arquivo CSV
    datasets = exportar_informacoes_do_dataset(id_projeto)
    arquivo_csv_datasets = f'{id_projeto}_datasets_{data_atual}.csv'
    exportar_para_csv(datasets, arquivo_csv_datasets)

    # Lista para armazenar as tabelas dos datasets e as pastas dos datasets
    tabelas_do_dataset = []
    pastas_datasets = []

    # Itera sobre os datasets a partir do segundo elemento (o primeiro é o cabeçalho)
    for dataset in datasets[1:]:
        # Obtém o nome do dataset
        nome_dataset = dataset[0]
        # Exporta o esquema da tabela para um arquivo CSV
        esquemas_tabelas = exportar_esquema_da_tabela(id_projeto, nome_dataset)
        arquivo_csv_tabelas = f'{id_projeto}_{nome_dataset}_tabelas_{data_atual}.csv'
        exportar_para_csv(esquemas_tabelas, arquivo_csv_tabelas)
        # Armazena o nome do dataset e o arquivo CSV das tabelas na lista correspondente
        tabelas_do_dataset.append((nome_dataset, arquivo_csv_tabelas))
        # Armazena o nome do dataset na lista de pastas dos datasets
        pastas_datasets.append(nome_dataset)

    # Lista para armazenar os arquivos CSV com a quantidade de colunas
    arquivos_quantidade_colunas = []

    # Itera sobre os datasets a partir do segundo elemento
    for dataset in datasets[1:]:
        # Obtém o nome do dataset
        nome_dataset = dataset[0]
        # Exporta a quantidade de colunas para um arquivo CSV
        quantidade_colunas = exportar_quantidade_de_colunas(id_projeto, nome_dataset)
        arquivo_csv_quantidade_colunas = f'{id_projeto}_{nome_dataset}_{data_atual}.csv'
        exportar_para_csv(quantidade_colunas, arquivo_csv_quantidade_colunas)
        # Adiciona o arquivo CSV à lista correspondente
        arquivos_quantidade_colunas.append(arquivo_csv_quantidade_colunas)

    # Define os nomes dos arquivos ZIP
    arquivo_zip_tabelas_dataset = f'{id_projeto}_tabelas_dataset_{data_atual}.zip'
    arquivo_zip_quantidade_colunas = f'{id_projeto}_quantidade_colunas_{data_atual}.zip'
    arquivo_zip_data_mapping = f'{id_projeto}_data_mapping_{data_atual}.zip'

    # Compacta os arquivos das tabelas dos datasets em um arquivo ZIP
    compactar_arquivos([arquivo_csv_tabelas for _, arquivo_csv_tabelas in tabelas_do_dataset], arquivo_zip_tabelas_dataset)

    # Compacta os arquivos CSV com a quantidade de colunas em um arquivo ZIP
    compactar_arquivos(arquivos_quantidade_colunas, arquivo_zip_quantidade_colunas)

    # Compacta os arquivos CSV, o arquivo ZIP das tabelas dos datasets e o arquivo ZIP da quantidade de colunas em um arquivo ZIP final
    compactar_arquivos([arquivo_csv_datasets, arquivo_zip_tabelas_dataset, arquivo_zip_quantidade_colunas], arquivo_zip_data_mapping)

    # Deleta os arquivos CSV, os arquivos ZIP das tabelas dos datasets e o arquivo ZIP da quantidade de colunas
    deletar_arquivos([arquivo_csv_datasets] + arquivos_quantidade_colunas + [arquivo_zip_tabelas_dataset, arquivo_zip_quantidade_colunas] + [nome_arquivo_tabela for _, nome_arquivo_tabela in tabelas_do_dataset])

    # Envia o arquivo ZIP final para o bucket GCS
    upload_para_bucket('staging-datahub-provider-dsv', arquivo_zip_data_mapping)

    print(f"Informações do dataset e tabelas exportadas para {arquivo_zip_data_mapping}")

if __name__ == '__main__':
    # Define o ID do projeto
    id_projeto = 'Project_Id'
    # Define o caminho do bucket
    bucket = 'Bucket_path/To_path'
    # Chama a função principal
    main(id_projeto)
