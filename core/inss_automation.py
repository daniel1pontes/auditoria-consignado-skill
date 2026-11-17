"""Máquina de orientação: não acessa nem controla o portal."""
def next_step(*, authorized=False, portal_available=True, human_check=False):
    if not authorized:
        return 'Solicitar autorização do titular ou representante antes de acessar dados; upload manual disponível.'
    if not portal_available:
        return 'Portal ou navegação indisponível: obtenha o extrato manualmente e envie o arquivo.'
    if human_check:
        return 'Interromper e aguardar o usuário concluir autenticação, MFA, CAPTCHA ou verificação no portal.'
    return 'Com navegador visível disponível, usuário acessa Meu INSS e obtém o Extrato de Empréstimo Consignado; não alterar operações.'
