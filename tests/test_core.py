import io
import json
from decimal import Decimal
from pathlib import Path
import fitz
import pytest
from openpyxl import Workbook
from PIL import Image
from core.extraction import extract
from core.analyzer import analyze, annual_rate
from core.inss_automation import next_step
from core.rates import fetch_sgs
from core.reporter import report
from core.signature_check import comparison


def test_extract_formats_and_missing_text(tmp_path):
    pdf = tmp_path / 'scan.pdf'
    doc = fitz.open(); doc.new_page(); doc.save(pdf); doc.close()
    assert 'OCR' in extract(pdf)['avisos'][0]
    csv = tmp_path / 'a.csv'; csv.write_text('x,y\n1,2', encoding='utf8')
    assert extract(csv)['trechos'][1]['local'] == 'linha 2'
    book = Workbook(); book.active['B2'] = 'parcela'; book.save(tmp_path / 'a.xlsx')
    assert 'B2' in extract(tmp_path / 'a.xlsx')['trechos'][0]['local']
    with pytest.raises(ValueError): extract(tmp_path / 'x.txt')


def test_finance_and_matching():
    assert annual_rate('1').quantize(Decimal('.0001')) == Decimal('12.6825')
    case = json.loads(Path('examples/caso-sintetico.json').read_text())
    findings = analyze(case)
    assert len(findings) == 3
    assert '20.00' in findings[0]['criterio']
    assert 'linha 3' in findings[0]['evidencias'][1]
    assert analyze({})[0]['descricao'].startswith('Nenhum')
    with pytest.raises(ValueError): analyze({'contratos': [{'id': 'x'}, {'id': 'x'}]})


def test_rates_authorization_success_failure():
    with pytest.raises(PermissionError): fetch_sgs(123, '01/01/2020', '01/02/2020')
    def ok(url, timeout): return io.BytesIO(b'[{"data":"01/01/2020","valor":"1.2"}]')
    assert fetch_sgs(123, '01/01/2020', '01/02/2020', authorized=True, opener=ok)['dados'][0]['valor'] == '1.2'
    def fail(url, timeout): raise OSError('offline')
    assert fetch_sgs(123, '01/01/2020', '01/02/2020', authorized=True, opener=fail)['status'] == 'indisponível'


def test_human_intervention():
    assert 'autorização' in next_step()
    assert 'Interromper' in next_step(authorized=True, human_check=True)
    assert 'manualmente' in next_step(authorized=True, portal_available=False)


def test_report_and_visual(tmp_path):
    samples = []
    for i in range(2):
        p = tmp_path / f'{i}.png'; Image.new('RGB', (100, 50), 'white').save(p)
        samples.append({'arquivo': str(p), 'origem': f'documento fictício página {i+1}'})
    image = tmp_path / 'comparacao.png'; comparison(samples, image)
    output = tmp_path / 'relatorio.pdf'
    report({'caso': 'Caso sintético'}, analyze({}), output, [image])
    with fitz.open(output) as doc:
        assert 'Caso sintético' in ''.join(p.get_text() for p in doc)
        assert len(doc) >= 1
