# F1 Lakehouse

Este projeto coleta dados de resultados de corridas da Fórmula 1 usando a biblioteca `fastf1` e os armazena em um data lake no Amazon S3. Os dados são salvos em formato Parquet, organizados por ano.

## Funcionalidades

- **Coleta de Dados**: Utiliza `fastf1` para obter resultados de corridas (R) e sprints (S) de anos específicos.
- **Armazenamento Local**: Salva os dados em arquivos Parquet na pasta `data/`.
- **Upload para S3**: Envia os arquivos para um bucket S3, organizados por ano, e remove os arquivos locais após o upload.

## Requisitos

- Python 3.8+
- Conta AWS com acesso a S3
- Bibliotecas: `fastf1`, `pandas`, `boto3`, `python-dotenv`, `tqdm`

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd f1-lakehouse
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install fastf1 pandas boto3 python-dotenv tqdm
   ```

4. Configure as variáveis de ambiente: Crie um arquivo `.env` na raiz do projeto com:
   ```
   AWS_KEY=your_aws_access_key
   AWS_SECRET_KEY=your_aws_secret_key
   BUCKET_NAME=your_s3_bucket_name
   BUCKET_FOLDER=raw/results
   ```
   **Atenção**: Nunca commite o arquivo `.env` no repositório. Ele está listado no `.gitignore`.

## Uso

### Coleta de Dados

Para coletar dados de anos específicos:
```bash
python src/collect.py --start 2010 --stop 2020 --modes R S
```

Ou para anos específicos:
```bash
python src/collect.py --years 2021 2022 --modes R
```

### Envio para S3

Para enviar os dados coletados:
```bash
python src/sender.py --bucket your_bucket_name --bucket_path raw/results --folder data
```

### Script Principal

O `main.py` executa a coleta e envio automaticamente para os anos configurados. Edite o script para ajustar os anos desejados.

## Regras do Projeto

- **Credenciais**: Nunca exponha chaves AWS ou outras credenciais no código ou commits. Use sempre variáveis de ambiente via `.env`.
- **Dados Sensíveis**: Não commite arquivos de dados ou logs que contenham informações sensíveis.
- **Contribuições**: Antes de contribuir, certifique-se de que o código segue as boas práticas e não inclui credenciais hardcoded.
- **Licença**: Este projeto é para uso pessoal/educacional. Verifique licenças das bibliotecas utilizadas.
- **Rate Limiting**: A coleta de dados usa delays para evitar sobrecarga na API do fastf1.

## Estrutura do Projeto

```
f1-lakehouse/
├── .env                 # Variáveis de ambiente (não commitar)
├── main.py              # Script principal; orquestra coleta e envio
├── src/
│   ├── collect.py       # Módulo de coleta de dados usando fastf1
│   └── sender.py        # Módulo de envio para S3
├── data/                # Dados locais (ignorados pelo git)
├── teste_aws.py         # Script de teste de acesso AWS (exemplo utilitário)
└── README.md            # Este arquivo
```

## Contribuição

1. Fork o projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto não possui licença específica. Use por sua conta e risco.
