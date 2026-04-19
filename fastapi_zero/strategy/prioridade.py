class PrioridadeStrategy:
    def executar(self):
        raise NotImplementedError()


class PrioridadeAlta(PrioridadeStrategy):
    def executar(self):
        return 'Alta prioridade - executar imediatamente'


class PrioridadeMedia(PrioridadeStrategy):
    def executar(self):
        return 'Prioridade média - planejar execução'


class PrioridadeBaixa(PrioridadeStrategy):
    def executar(self):
        return 'Baixa prioridade - pode aguardar'


def get_prioridade_strategy(prioridade: str) -> PrioridadeStrategy:
    if prioridade == 'alta':
        return PrioridadeAlta()
    if prioridade == 'media':
        return PrioridadeMedia()
    if prioridade == 'baixa':
        return PrioridadeBaixa()

    raise ValueError('Prioridade inválida')