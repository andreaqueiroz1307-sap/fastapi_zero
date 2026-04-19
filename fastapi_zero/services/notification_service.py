from fastapi_zero.models.task import Task


def descrever_frequencia(frequencia: str | None) -> str:
    if frequencia is None:
        return 'Sem lembrete configurado'

    descricoes = {
        '30min': 'Lembrete a cada 30 minutos',
        '1h': 'Lembrete a cada 1 hora',
        '2h': 'Lembrete a cada 2 horas',
        '1x_dia': 'Lembrete 1 vez ao dia',
        '2x_dia': 'Lembrete 2 vezes ao dia',
        '3x_dia': 'Lembrete 3 vezes ao dia',
        'no_dia_limite': 'Lembrete apenas no dia da data limite',
    }

    return descricoes.get(frequencia, 'Frequência de lembrete desconhecida')


def montar_mensagem_lembrete(task: Task) -> str:
    descricao = descrever_frequencia(task.frequencia_lembrete)

    return f'Tarefa: {task.titulo} | {descricao}'