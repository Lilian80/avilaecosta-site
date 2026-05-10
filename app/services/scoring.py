PONTOS_RESPOSTA = {
    "Satisfatório": 1.0,
    "Parcial": 0.5,
    "Insatisfatório": 0.0,
    "Não se aplica": None,
}


def calcular_nivel(percentual):
    if percentual >= 85:
        return "Excelente"
    if percentual >= 70:
        return "Controlado"
    if percentual >= 50:
        return "Atenção"
    return "Crítico"


def calcular_percentual(respostas):
    pontos = 0.0
    avaliaveis = 0
    for resposta in respostas:
        valor = PONTOS_RESPOSTA.get(resposta)
        if valor is not None:
            pontos += valor
            avaliaveis += 1
    percentual = round((pontos / avaliaveis) * 100, 1) if avaliaveis else 0
    return pontos, avaliaveis, percentual, calcular_nivel(percentual)
