"""Gerenciador de objetos e etiquetas do AUdi.

A leitura NFC e a reprodução de áudio são simuladas por texto.
Execute dentro desta pasta: python main.py (Python 3.10 ou superior).
"""
import json

ARQUIVO = 'objetos.json'
CAMPOS = ('etiqueta', 'nome', 'descricao', 'audio')
OPCOES = ('Cadastrar objeto', 'Listar objetos', 'Consultar etiqueta',
          'Editar objeto', 'Excluir objeto', 'Simular leitura NFC',
          'Mostrar pendências', 'Mostrar resumo')


def normalizar_codigo(codigo: str) -> str:
    """Remove espaços nas extremidades e converte o código para maiúsculas.

    Args:
        codigo: identificador digitado ou lido do cadastro.
    Returns:
        Código padronizado para comparação.
    """
    return codigo.strip().upper()


def buscar_indice(objetos: list[dict], codigo: str) -> int:
    """Busca uma etiqueta linearmente, conforme a Aula 13.

    Args:
        objetos: lista de cadastros.
        codigo: etiqueta procurada.
    Returns:
        Índice encontrado ou -1 quando não houver correspondência.
    """
    codigo = normalizar_codigo(codigo)
    for indice in range(len(objetos)):
        if objetos[indice]['etiqueta'] == codigo:
            return indice
    return -1


def validar_dados(objetos: list[dict]) -> None:
    """Verifica a estrutura do JSON e impede códigos duplicados.

    Args:
        objetos: dados carregados do arquivo.
    Returns:
        None. Gera ValueError quando o conteúdo não é válido.
    """
    if not isinstance(objetos, list):
        raise ValueError('O conteúdo precisa ser uma lista de objetos.')
    codigos = []
    for objeto in objetos:
        if not isinstance(objeto, dict):
            raise ValueError('Cada objeto precisa ser um dicionário.')
        for campo in CAMPOS:
            if campo not in objeto or not isinstance(objeto[campo], str):
                raise ValueError(f'Campo ausente ou inválido: {campo}.')
        codigo = objeto['etiqueta']
        if not codigo or codigo != normalizar_codigo(codigo):
            raise ValueError('Etiqueta vazia ou fora do padrão de maiúsculas.')
        if not objeto['nome'].strip():
            raise ValueError('O nome do objeto não pode ficar vazio.')
        if codigo in codigos:
            raise ValueError('Há etiquetas repetidas no arquivo.')
        codigos.append(codigo)


def carregar_dados(caminho: str = ARQUIVO) -> list[dict]:
    """Carrega JSON; arquivo ausente inicia um catálogo vazio.

    Args:
        caminho: nome do arquivo de dados.
    Returns:
        Lista de objetos validada. Outros erros são tratados pelo menu.
    """
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            objetos = json.load(arquivo)
    except FileNotFoundError:
        return []
    validar_dados(objetos)
    return objetos


def salvar_dados(objetos: list[dict], caminho: str = ARQUIVO) -> bool:
    """Salva os cadastros e mantém backup do arquivo anterior.

    Args:
        objetos: lista a persistir.
        caminho: arquivo de destino.
    Returns:
        True se salvou ou False se houve erro.
    """
    try:
        validar_dados(objetos)
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                anterior = arquivo.read()
        except FileNotFoundError:
            anterior = None
        if anterior is not None:
            with open(caminho + '.bak', 'w', encoding='utf-8') as backup:
                backup.write(anterior)
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(objetos, arquivo, indent=4, ensure_ascii=False)
    except (OSError, ValueError) as erro:
        print(f'Falha ao salvar: {erro}')
        print('Alteração não confirmada. Preserve o arquivo .bak, se existir.')
        return False
    return True


def ler_texto(mensagem: str, obrigatorio: bool = True) -> str:
    """Lê uma entrada e repete caso um campo obrigatório esteja vazio.

    Args:
        mensagem: orientação para o usuário.
        obrigatorio: permite ou não uma resposta vazia.
    Returns:
        Texto sem espaços nas extremidades.
    """
    while True:
        texto = input(mensagem).strip()
        if texto or not obrigatorio:
            return texto
        print('Preencha este campo para continuar.')


def mostrar_objeto(objeto: dict) -> None:
    """Exibe o cadastro e diferencia descrição de referência de áudio.

    Args:
        objeto: dicionário de um cadastro.
    Returns:
        None.
    """
    print(f"\nEtiqueta: {objeto['etiqueta']} | Objeto: {objeto['nome']}")
    print('Descrição:', objeto['descricao'] or 'Pendente')
    print('Referência de áudio:', objeto['audio'] or 'Pendente')


def cadastrar(objetos: list[dict]) -> bool:
    """Solicita um objeto, rejeitando etiquetas já cadastradas.

    Args:
        objetos: lista que receberá o cadastro.
    Returns:
        True se cadastrou; False se a etiqueta já existir.
    """
    codigo = normalizar_codigo(ler_texto('Código da etiqueta: '))
    if buscar_indice(objetos, codigo) != -1:
        print('Etiqueta já cadastrada. Use a opção de edição.')
        return False
    nome = ler_texto('Nome do objeto: ')
    descricao = ler_texto('Descrição (opcional): ', obrigatorio=False)
    audio = ler_texto('Nome do arquivo de áudio (opcional): ', obrigatorio=False)
    objetos.append({'etiqueta': codigo, 'nome': nome,
                    'descricao': descricao, 'audio': audio})
    return True


def listar(objetos: list[dict]) -> None:
    """Exibe todos os cadastros ou informa que a lista está vazia.

    Args:
        objetos: lista de cadastros.
    Returns:
        None.
    """
    if not objetos:
        print('Nenhum objeto cadastrado.')
    for objeto in objetos:
        mostrar_objeto(objeto)


def consultar(objetos: list[dict]) -> None:
    """Procura e exibe um cadastro pelo código informado.

    Args:
        objetos: lista de cadastros.
    Returns:
        None.
    """
    indice = buscar_indice(objetos, ler_texto('Código da etiqueta: '))
    if indice == -1:
        print('Etiqueta não cadastrada.')
    else:
        mostrar_objeto(objetos[indice])


def editar(objetos: list[dict]) -> bool:
    """Altera o cadastro mantendo o código original da etiqueta.

    Args:
        objetos: lista de cadastros.
    Returns:
        True se mudou algo; False se não houve alteração.
    """
    indice = buscar_indice(objetos, ler_texto('Código da etiqueta: '))
    if indice == -1:
        print('Etiqueta não cadastrada.')
        return False
    objeto = objetos[indice]
    mostrar_objeto(objeto)
    print('Enter mantém o valor. /limpar apaga descrição ou referência de áudio.')
    anterior = objeto.copy()
    nome = ler_texto('Novo nome: ', obrigatorio=False)
    descricao = ler_texto('Nova descrição: ', obrigatorio=False)
    audio = ler_texto('Nova referência de áudio: ', obrigatorio=False)
    if nome:
        objeto['nome'] = nome
    if descricao == '/limpar':
        objeto['descricao'] = ''
    elif descricao:
        objeto['descricao'] = descricao
    if audio == '/limpar':
        objeto['audio'] = ''
    elif audio:
        objeto['audio'] = audio
    return objeto != anterior


def excluir(objetos: list[dict]) -> bool:
    """Exclui somente após confirmação explícita.

    Args:
        objetos: lista de cadastros.
    Returns:
        True se excluiu; False se cancelou ou não encontrou.
    """
    indice = buscar_indice(objetos, ler_texto('Código da etiqueta: '))
    if indice == -1:
        print('Etiqueta não cadastrada.')
        return False
    mostrar_objeto(objetos[indice])
    if ler_texto('Digite SIM para excluir: ').upper() == 'SIM':
        objetos.pop(indice)
        return True
    print('Exclusão cancelada.')
    return False


def simular_leitura(objetos: list[dict]) -> None:
    """Decide o estado de uma leitura simulada, exibindo apenas texto.

    Args:
        objetos: cadastros conhecidos pelo programa.
    Returns:
        None.
    """
    print('SIMULAÇÃO: o código digitado representa uma leitura NFC.')
    indice = buscar_indice(objetos, ler_texto('Código simulado: '))
    if indice == -1:
        print('ETIQUETA DESCONHECIDA: cadastre o objeto no menu.')
    elif not objetos[indice]['descricao'].strip():
        print('DESCRIÇÃO PENDENTE: edite o objeto antes de utilizá-lo.')
    else:
        print('OBJETO IDENTIFICADO.')
        mostrar_objeto(objetos[indice])
    print('Não houve leitura física, gravação nem reprodução de áudio.')


def listar_pendencias(objetos: list[dict]) -> None:
    """Aponta campos de descrição e referência de áudio não preenchidos.

    Args:
        objetos: lista de cadastros.
    Returns:
        None.
    """
    total = 0
    for objeto in objetos:
        faltas = []
        if not objeto['descricao'].strip():
            faltas.append('descrição')
        if not objeto['audio'].strip():
            faltas.append('referência de áudio')
        if faltas:
            total += 1
            print(f"{objeto['etiqueta']} - {objeto['nome']}: falta " + ' e '.join(faltas))
    if total == 0:
        print('Nenhuma pendência de cadastro.')
    print('A existência e o conteúdo dos arquivos de áudio não são verificados.')


def mostrar_resumo(objetos: list[dict]) -> None:
    """Conta registros completos e pendentes, evitando divisão por zero.

    Args:
        objetos: lista de cadastros.
    Returns:
        None.
    """
    completos = 0
    for objeto in objetos:
        if objeto['descricao'].strip() and objeto['audio'].strip():
            completos += 1
    total = len(objetos)
    print(f'Total: {total} | Completos: {completos} | Pendentes: {total - completos}')
    if total > 0:
        print(f'Cadastros completos: {completos / total * 100:.1f}%')
    else:
        print('Cadastre o primeiro objeto para começar.')


def executar(caminho: str = ARQUIVO) -> None:
    """Controla o menu e confirma alterações somente após salvar.

    Args:
        caminho: arquivo JSON usado pela sessão.
    Returns:
        None.
    """
    try:
        objetos = carregar_dados(caminho)
    except (OSError, ValueError) as erro:
        print(f'Não foi possível carregar os dados: {erro}')
        print('Execução interrompida para não sobrescrever o arquivo inválido.')
        return
    while True:
        print('\nAUDI - GERENCIADOR DE OBJETOS')
        for indice in range(len(OPCOES)):
            print(f'{indice + 1}. {OPCOES[indice]}')
        print('0. Sair')
        try:
            opcao = int(ler_texto('Opção: '))
        except ValueError:
            print('Digite um número inteiro do menu.')
            continue
        novos = []
        for objeto in objetos:
            novos.append(objeto.copy())
        alterou = False
        match opcao:
            case 1:
                alterou = cadastrar(novos)
            case 2:
                listar(objetos)
            case 3:
                consultar(objetos)
            case 4:
                alterou = editar(novos)
            case 5:
                alterou = excluir(novos)
            case 6:
                simular_leitura(objetos)
            case 7:
                listar_pendencias(objetos)
            case 8:
                mostrar_resumo(objetos)
            case 0:
                print('Programa encerrado. Alterações confirmadas foram salvas.')
                break
            case _:
                print('Opção inválida. Escolha de 0 a 8.')
        if alterou:
            if salvar_dados(novos, caminho):
                objetos = novos
                print('Alteração salva com sucesso.')
        elif opcao == 4:
            print('Nenhuma alteração aplicada.')


if __name__ == '__main__':
    try:
        executar()
    except (KeyboardInterrupt, EOFError):
        print('\nSessão interrompida. Dados já confirmados permanecem salvos.')
