from html import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from pathlib import Path

def report(case, findings, output, attachments=()):
    styles = getSampleStyleSheet()
    story = []
    def add(text, style='BodyText'):
        story.append(Paragraph(escape(str(text)).replace('\n', '<br/>'), styles[style])); story.append(Spacer(1, 8))
    add('Auditoria de crédito consignado — revisão profissional', 'Title')
    for label, key in [('Caso', 'caso'), ('Cliente ou beneficiário', 'cliente'), ('Auditor', 'auditor'), ('Data', 'data')]:
        add(f'{label}: {case.get(key) or "não informado"}')
    add('Sumário executivo', 'Heading1')
    add(case.get('escopo', 'Revisão limitada aos dados apresentados.'))
    add('Documentos: ' + ', '.join(case.get('documentos', [])) if case.get('documentos') else 'Documentos: não informados.')
    add('Limitações: dados e vínculos dependem de conferência humana; hipóteses não são conclusões de fraude ou ilegalidade. Não substitui análise profissional.')
    add(f'Achados para revisão: {len(findings)}')
    add('Achados detalhados', 'Heading1')
    for i, f in enumerate(findings, 1):
        add(f'{i}. {f["descricao"]}', 'Heading2')
        for label, value in [('Evidências', '; '.join(f.get('evidencias', [])) or 'não informadas'), ('Critério e cálculo', f.get('criterio', 'não informado')), ('Revisão', f.get('revisao', 'não informada'))]: add(f'{label}: {value}')
    add('Demonstrativo financeiro', 'Heading1')
    for c in case.get('contratos', []):
        add(f"Contrato {c.get('id')}: contratado {c.get('valor_contratado', 'não informado')}; liberado {c.get('valor_liberado', 'não informado')}; parcela {c.get('parcela', 'não informada')}; prazo {c.get('prazo', 'não informado')}; taxa {c.get('taxa', 'não informada')}; CET {c.get('cet', 'não informado')}. Origem: {c.get('origem', 'não informada')}")
    for attachment in attachments:
        p = Path(attachment)
        add('Anexo visual: ' + p.name, 'Heading2')
        image = Image(str(p)); image._restrictSize(480, 650); story.append(image)
    add('Profissional responsável: ________________________________________')
    SimpleDocTemplate(str(output), pagesize=A4).build(story)
