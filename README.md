# Data Mapping: Exportação de Dados do BigQuery para o Cloud Storage

Este repositório contém um script em Python que permite exportar dados do BigQuery para o Cloud Storage. O script fornece funcionalidades para exportar informações sobre conjuntos de dados, esquemas de tabelas e quantidades de colunas.

## Requisitos
- Python 3.x
- Biblioteca google-cloud-bigquery
- Biblioteca google-cloud-storage

## Configuração
Antes de executar o script, verifique o seguinte:

1. Configure um projeto no Google Cloud e ative as APIs do BigQuery e Cloud Storage.
2. Crie uma conta de serviço e faça o download do arquivo de chave JSON.
3. Conceda as permissões adequadas à conta de serviço para acessar conjuntos de dados do BigQuery e buckets do Cloud Storage.
4. Instale as bibliotecas Python necessárias executando o comando: `pip install google-cloud-bigquery google-cloud-storage`.

## Uso
Siga as etapas abaixo para exportar dados do BigQuery para o Cloud Storage:

1. Abra o arquivo de script (`data_mapping.py`) em um editor de texto.
2. Defina a variável `id_projeto` com o ID do seu projeto no Google Cloud.
3. Defina a variável `bucket` com o bucket de destino no Cloud Storage.
4. Salve as alterações.

## Guia Passo a Passo
1. Instale as bibliotecas Python necessárias (se ainda não estiverem instaladas).
2. Configure seu projeto e conta de serviço no Google Cloud.
3. Defina o ID do projeto e o bucket de destino no script.
4. Execute o script usando o comando: `python data_mapping.py`.
5. O script exportará informações sobre conjuntos de dados, esquemas de tabelas e quantidades de colunas para arquivos CSV.
6. Os arquivos gerados serão compactados em um arquivo ZIP (`[id_projeto]_data_mapping_[data].zip`).
7. O arquivo ZIP será enviado para o bucket especificado no Cloud Storage.

## Script Python
O script `data_mapping.py` contém as seguintes funções:
- `exportar_informacoes_do_dataset`: Exporta informações sobre conjuntos de dados e quantidades de tabelas.
- `exportar_esquema_da_tabela`: Exporta os esquemas das tabelas, incluindo nomes de campo, descrições e tipos de campo.
- `exportar_quantidade_de_colunas`: Exporta a quantidade de colunas em cada tabela.
- `exportar_para_csv`: Exporta os dados para um arquivo CSV.
- `deletar_arquivos`: Exclui os arquivos especificados.
- `compactar_pastas`: Compacta pastas em um arquivo ZIP.
- `compactar_arquivos`: Compacta arquivos em um arquivo ZIP.
- `upload_para_bucket`: Faz upload de um arquivo para um bucket do Cloud Storage.
- `main`: A função principal que orquestra o processo de exportação de dados.

## Executando o Código
Para executar o código:

1. Verifique se as dependências necessárias estão instaladas.
2. Substitua a variável `id_projeto` pelo ID do seu projeto no Google Cloud.
3. Defina a variável `bucket` com o bucket do Cloud Storage desejado.
4. Execute o script usando o comando: `python data_mapping.py`.

Observação: O script pressupõe que você tenha autenticação válida e

 acesso aos conjuntos de dados especificados no BigQuery e ao bucket do Cloud Storage.

Sinta-se à vontade para modificar o script de acordo com o seu caso de uso específico ou integrá-lo ao seu código existente.

Por favor, avise-me se precisar de mais alguma ajuda.
