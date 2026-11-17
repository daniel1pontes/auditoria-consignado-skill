import argparse
import json
from pathlib import Path
from .extraction import extract
from .analyzer import analyze
from .reporter import report

def main():
    p = argparse.ArgumentParser(description='Revisão assistida de crédito consignado')
    sub = p.add_subparsers(dest='command', required=True)
    e = sub.add_parser('extrair'); e.add_argument('arquivo'); e.add_argument('-o', '--saida', required=True)
    a = sub.add_parser('relatorio'); a.add_argument('caso'); a.add_argument('-o', '--saida', required=True)
    args = p.parse_args()
    if args.command == 'extrair':
        Path(args.saida).write_text(json.dumps(extract(args.arquivo), ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        case = json.loads(Path(args.caso).read_text(encoding='utf-8'))
        report(case, analyze(case), args.saida)
if __name__ == '__main__': main()
