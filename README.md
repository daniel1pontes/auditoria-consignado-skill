# Auditoria de crédito consignado

Ferramenta inicial de apoio à revisão humana, não laudo e não detector de fraude. Uma skill orienta o ChatGPT; módulos Python também funcionam localmente. A ausência de achados não demonstra regularidade. Dados sintéticos em `examples/`.

## ChatGPT

A [documentação oficial de skills](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) descreve upload em **Plugins → Skills → Create → Upload from your computer**, sujeito a elegibilidade, configurações do workspace e verificação. Comprima o conteúdo de `skills/auditoria-consignado/` (incluindo `SKILL.md`, `core/` e `references/`) em ZIP e faça upload. O repositório ou manifesto por si só não instala a skill. A execução de Python, dependências e acesso a arquivos variam conforme o ambiente; a instalação e execução no ChatGPT não foram verificadas. A skill pode orientar análise manual quando scripts não estiverem disponíveis. A documentação foi consultada em 17/11/2026.

## Instalação e demonstração local

Python 3.11+:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install '.[test]'
python -m core.cli extrair arquivo.pdf -o extracao.json
python -m core.cli relatorio examples/caso-sintetico.json -o relatorio.pdf
pytest -q
```

Inspecione a extração e monte o JSON seguindo o exemplo, com origens específicas e valores decimais como strings. O programa cruza descontos identificados pelo `contrato_id`, compara parcela e diferença entre valor contratado e liberado, e indica desconto sem contrato informado. Os cálculos arredondam valores monetários a centavos pelo método half-up. `annual_rate` converte taxa mensal efetiva para anual por `(1 + taxa_mensal/100)^12 - 1`; o resultado é percentual, sem arredondamento interno. O PDF apresenta dados informados e achados; inspecione-o antes de usar. `signature_check.comparison` cria prancha de imagens e origens explicitamente fornecidas. `report(..., attachments=[...])` permite incluí-la no relatório. Não há score.

## Limites e integrações

- PDF extrai texto, não OCR: páginas sem texto são indicadas. CSV usa UTF-8; XLSX mostra fórmulas, não as recalcula. Extração não compreende automaticamente contratos, imagens, campos financeiros ou tabelas complexas. Dados devem ser revisados e estruturados por profissional; PDF protegido precisa ser desbloqueado pelo usuário. OCR e provedores de IA são possibilidades futuras, sem implementação integrada.
- A comparação de valores não identifica automaticamente refinanciamento, portabilidade, recorrência ou ilegalidade; análise documental e pesquisa adicional são necessárias. O relatório não gera gráficos. Não há inferência biométrica ou detecção automática de edição; imagens são pranchas para revisão visual.
- `core.rates.fetch_sgs(codigo, inicio, fim, authorized=True)` consulta opcionalmente a [API SGS do BCB](https://dadosabertos.bcb.gov.br/dataset/11-taxa-de-juros---selic) (datas `DD/MM/AAAA`). A seleção da série correta, unidade, modalidade e período é responsabilidade do usuário. A resposta registra URL, série e data de consulta; indisponibilidade é reportada. A série citada é apenas documentação da API, não referência para consignado. O programa não escolhe referência automaticamente nem declara abusividade.
- `core.inss_automation.next_step` orienta interrupção e upload manual; não controla navegador, autentica ou baixa dados. Uma eventual coleta deve respeitar as regras do portal e ocorrer com usuário presente. Login, MFA e CAPTCHA são do usuário. Não faça contratações nem alterações.
- A prancha visual não estabelece autenticidade, falsificação, pressão da escrita ou probabilidade; confirmar por perícia documentoscópica/grafotécnica. Qualidade, resolução, quantidade e proveniência das amostras devem ser avaliadas.

## Privacidade e segurança

Arquivos e saídas permanecem onde o usuário os salvar; a ferramenta não faz upload, telemetria, logs de conteúdo ou exclusão automática. Não envie arquivos reais ao repositório; `.gitignore` não substitui revisão de conteúdo. Proteja acesso, backups e retenção e apague entradas e saídas ao término conforme acordo e política aplicável. Não inclua dados pessoais ou tokens em nomes de arquivo, erros, issues ou logs. Dependências são obtidas do índice configurado do pip. A consulta opcional ao BCB envia série e datas, não documentos. Usar a skill no ChatGPT implica processamento dos dados enviados pelos serviços e configurações aplicáveis à conta; verifique-os e obtenha autorização apropriada antes do envio. Sem provedor externo de OCR/IA configurado pelo código. A LGPD pode exigir definição de base legal, finalidade, medidas de segurança, retenção e direitos dos titulares; busque revisão especializada. Nenhuma conformidade é garantida.

Licença MIT; bibliotecas externas têm licenças próprias. Resultados são subsídios, sujeitos à revisão jurídica, financeira, contábil ou pericial.
