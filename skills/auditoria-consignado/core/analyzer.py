"""Cálculos decimais e cruzamento conservador, baseado em identificadores explícitos."""
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal('0.01')

def money(value):
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)

def annual_rate(monthly_percent):
    return ((Decimal(1) + Decimal(str(monthly_percent)) / 100) ** 12 - 1) * 100

def analyze(case):
    findings = []
    contracts = case.get('contratos', [])
    movements = case.get('movimentos', [])
    ids = [c.get('id') for c in contracts]
    if any(not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('Cada contrato deve ter id único e não vazio')
    for c in contracts:
        cid = c['id']
        linked = [m for m in movements if m.get('contrato_id') == cid]
        for m in linked:
            if m.get('tipo') == 'desconto' and c.get('parcela') is not None and m.get('valor') is not None and money(m['valor']) != money(c['parcela']):
                findings.append({'descricao': f'Desconto diferente da parcela prevista no contrato {cid}', 'evidencias': [c.get('origem', 'origem não informada'), m.get('origem', 'origem não informada')], 'criterio': f"{money(m['valor'])} - {money(c['parcela'])} = {money(Decimal(str(m['valor'])) - Decimal(str(c['parcela'])))}", 'revisao': 'Conferir competência, encargos e documentos originais.'})
        if c.get('valor_contratado') is not None and c.get('valor_liberado') is not None:
            diff = money(Decimal(str(c['valor_contratado'])) - Decimal(str(c['valor_liberado'])))
            if diff > 0:
                findings.append({'descricao': f'Diferença entre valor contratado e liberado em {cid}', 'evidencias': [c.get('origem', 'origem não informada')], 'criterio': f'Contratado menos liberado = {diff}; valores podem incluir quitação ou encargos.', 'revisao': 'Conferir destinação da diferença e comprovantes.'})
    for m in movements:
        if m.get('tipo') == 'desconto' and (not m.get('contrato_id') or m['contrato_id'] not in ids):
            findings.append({'descricao': 'Desconto sem contrato correspondente informado', 'evidencias': [m.get('origem', 'origem não informada')], 'criterio': 'Nenhum identificador correspondente no conjunto recebido.', 'revisao': 'Buscar contrato e conferir identificação; ausência de correspondência não prova irregularidade.'})
    if not contracts:
        findings.append({'descricao': 'Nenhum contrato estruturado informado', 'evidencias': [], 'criterio': 'Dados insuficientes para cruzamento.', 'revisao': 'Adicionar contratos e respectivas origens.'})
    return findings
