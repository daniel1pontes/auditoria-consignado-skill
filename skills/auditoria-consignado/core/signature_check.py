"""Cria prancha de amostras, sem classificação biométrica."""
from PIL import Image, ImageOps, ImageDraw

def comparison(samples, output):
    if len(samples) < 2:
        raise ValueError('Forneça ao menos duas imagens autorizadas')
    canvas = Image.new('RGB', (800, len(samples)*250), 'white')
    draw = ImageDraw.Draw(canvas)
    for i, sample in enumerate(samples):
        with Image.open(sample['arquivo']) as source:
            img = ImageOps.contain(source.convert('RGB'), (760, 200))
            canvas.paste(img, (20, i*250+35))
            draw.text((20, i*250+10), str(sample['origem'])[:100], fill='black')
    canvas.save(output)
    return 'Comparação visual para revisão: não determina autenticidade, falsificação ou pressão da escrita.'
