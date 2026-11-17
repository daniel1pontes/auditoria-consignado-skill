"""Consulta opt-in ao SGS; a escolha e a comparabilidade da série são humanas."""
import json
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import date


def fetch_sgs(series, start, end, *, authorized=False, opener=urlopen):
    if not authorized:
        raise PermissionError('A consulta externa requer autorização explícita')
    if not str(series).isdigit():
        raise ValueError('Código da série deve ser numérico')
    query = urlencode({'formato': 'json', 'dataInicial': start, 'dataFinal': end})
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series}/dados?{query}'
    try:
        with opener(url, timeout=15) as response:
            data = json.load(response)
        if not isinstance(data, list):
            raise ValueError('Resposta inesperada')
    except (OSError, ValueError) as exc:
        return {'status': 'indisponível', 'serie': str(series), 'fonte': url, 'consulta': date.today().isoformat(), 'motivo': type(exc).__name__}
    return {'status': 'ok' if data else 'sem dados', 'serie': str(series), 'fonte': url, 'consulta': date.today().isoformat(), 'dados': data, 'limitação': 'Verificar modalidade, unidade, período e comparabilidade antes de usar; não conclui abusividade.'}
