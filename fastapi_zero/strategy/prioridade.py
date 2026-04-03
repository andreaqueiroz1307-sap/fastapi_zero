from typing import override


class PrioridadeStrategy:
    def executar(self):
        raise NotImplementedError()


class PrioridadeAlta(PrioridadeStrategy):
    @override
    def executar(self):
        return "Alta prioridade - executar imediatamente"


class PrioridadeMedia(PrioridadeStrategy):
    @override
    def executar(self):
        return "Prioridade média - planejar execução"


class PrioridadeBaixa(PrioridadeStrategy):
    @override
    def executar(self):
        return "Baixa prioridade - pode aguardar"


def get_prioridade_strategy(prioridade: str) -> PrioridadeStrategy:
    if prioridade == "alta":
        return PrioridadeAlta()
    elif prioridade == "media":
        return PrioridadeMedia()
    elif prioridade == "baixa":
        return PrioridadeBaixa()
    else:
        raise ValueError("Prioridade inválida")
