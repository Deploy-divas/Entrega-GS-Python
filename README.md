# AUdi — gerenciador de objetos e etiquetas

**Global Solution 2026.2 · CitizenTech · Python**

O **AUdi** é uma proposta de chaveiro assistivo para apoiar pessoas cegas ou com baixa visão na identificação de objetos pessoais. Uma etiqueta NFC associada ao objeto fornece um identificador; o dispositivo proposto recupera a descrição correspondente e a apresenta em áudio. O gerenciador em Python organiza esse catálogo e simula, no terminal, os resultados de uma leitura.

## Equipe

| Integrante | RM |
|---|---:|
| Amanda Silva da Mata | 572585 |
| Beatriz Mantovani da Cruz | 573824 |
| Laura Sampaio Neves | 570802 |

## O que o programa faz

O aplicativo permite cadastrar, consultar, listar, editar e excluir objetos associados a etiquetas. Cada cadastro contém um código de etiqueta, nome do objeto, descrição e referência textual a um arquivo de áudio. Os dados ficam salvos em `objetos.json` e permanecem disponíveis nas próximas execuções.

A opção **Simular leitura NFC** recebe um código digitado e apresenta um dos três resultados: etiqueta desconhecida, descrição pendente ou objeto identificado. Essa etapa demonstra a lógica de identificação do AUdi. A leitura física da etiqueta e a reprodução do áudio pertencem à implementação do dispositivo, enquanto este programa executa o gerenciamento e a simulação pelo terminal.

## Arquivos

| Arquivo | Finalidade |
|---|---|
| `main.py` | Programa principal, menu e operações sobre os cadastros. |
| `objetos.json` | Catálogo inicial com cinco objetos fictícios para demonstração. |
| `README.md` | Apresentação do projeto e instruções de uso. |

O programa cria `objetos.json.bak` ao salvar uma alteração quando já existe um arquivo de dados. Esse backup contém a versão imediatamente anterior do catálogo.

## Requisitos e execução

- Python **3.10 ou superior**.
- Nenhuma biblioteca externa. O programa usa apenas o módulo `json` da biblioteca padrão.

Abra um terminal na pasta `entrega_python` e execute:

```bash
python main.py
```

Se o executável do Python no sistema for `python3`, use:

```bash
python3 main.py
```

O arquivo `objetos.json` é acessado a partir da pasta em que o comando é executado. Por isso, inicie o programa dentro de `entrega_python`.

## Menu

| Opção | Ação |
|---:|---|
| 1 | Cadastrar objeto e código de etiqueta. |
| 2 | Listar todos os objetos cadastrados. |
| 3 | Consultar um objeto pelo código da etiqueta. |
| 4 | Editar nome, descrição ou referência de áudio. |
| 5 | Excluir um cadastro após confirmação. |
| 6 | Simular uma leitura NFC pelo código digitado. |
| 7 | Mostrar cadastros com descrição ou referência de áudio pendente. |
| 8 | Mostrar totais e percentual de cadastros completos. |
| 0 | Encerrar o programa. |

Na edição, **Enter** mantém o valor atual. Digitar `/limpar` no campo de descrição ou de referência de áudio apaga esse valor. O código da etiqueta permanece associado ao mesmo cadastro. As etiquetas são comparadas sem diferenciar maiúsculas de minúsculas e mantêm zeros à esquerda, como em `001`.

## Demonstração com o catálogo inicial

1. Consulte `TAG001` para visualizar o cadastro do pote de café.
2. Simule `TAG004` para observar o resultado de uma descrição pendente.
3. Simule `TAG999` para observar o resultado de uma etiqueta desconhecida.
4. Edite `TAG001`, alterando a descrição para `Açúcar` e a referência de áudio para `acucar.mp3`.
5. Simule novamente `TAG001`: a descrição atualizada aparece no terminal.
6. Encerre e reabra o programa para confirmar que a alteração foi salva em `objetos.json`.

O programa salva cada alteração confirmada. Códigos de etiqueta duplicados são rejeitados; a exclusão exige a confirmação `SIM`.

## Organização dos dados

`objetos.json` contém uma lista de registros com os campos `etiqueta`, `nome`, `descricao` e `audio`. A busca é feita pelo código normalizado da etiqueta. O campo `audio` guarda o nome de referência da gravação associada ao objeto; os arquivos de áudio não fazem parte deste módulo de gerenciamento.

Se o catálogo ainda não existir, o programa inicia com uma lista vazia. Se o JSON estiver inválido, a execução é interrompida para preservar o arquivo. Os dados de demonstração são fictícios.

## Recursos de Python utilizados

O projeto aplica funções, anotações de tipo, listas, tuplas, dicionários, strings, estruturas de decisão, laços, `match/case`, tratamento de exceções, busca linear, leitura e escrita de arquivos e persistência em JSON. A separação em funções permite acompanhar cada etapa do cadastro e da simulação de leitura.
