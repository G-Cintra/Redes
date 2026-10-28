from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
raiz=Path.cwd()
pasta=raiz/'entrega_final/entrega'
main=(pasta/'main.tex').read_text(encoding='utf-8')
preambulo=main.split(r'\begin{document}',1)[0]
corpo=main[main.index(r'\input{introducao.tex}'):]
corpo=corpo.split(r'{\renewcommand*{\bibfont}',1)[0]
def incluir(m):
    return (pasta/m.group(1)).read_text(encoding='utf-8')
corpo=re.sub(r'\\input\{([^}]+)\}', incluir, corpo)
assert r'\input' not in corpo
assert r'\begin{abstract}' not in corpo and r'\appendix' not in corpo
corpo,n_floats=re.subn(r'\\begin\{(figure|table)\}.*?\\end\{\1\}', '', corpo, flags=re.S)
assert n_floats==11, n_floats  # seis imagens no corpo e cinco tabelas; anexos excluídos antes.
caminho=raiz/'tmp/corpo_revisado_para_texcount.tex'
caminho.write_text(preambulo+'\n'+r'\begin{document}'+'\n'+corpo+'\n'+r'\end{document}'+'\n',encoding='utf-8')
cmd=['texcount','-utf8','-sub=section','-sum=1,0,0,0,0,0,0',str(caminho)]
resultado=subprocess.run(cmd,capture_output=True,encoding='utf-8',errors='replace',check=True)
print(resultado.stdout)
achado=re.search(r'Words in text:\s*(\d+)',resultado.stdout)
assert achado
registro={'palavras_corpo':int(achado.group(1)), 'metodo':'TeXcount; peso apenas Words in text',
 'exclusoes':['títulos e subtítulos','abstract','palavras-chave','figuras e tabelas completas, incluindo legendas, fontes e notas',
              'notas de rodapé','referências bibliográficas','anexos/apêndices','fórmulas'],
 'comando':cmd,'saida':resultado.stdout,
 'sha256_fontes':{nome:hashlib.sha256((pasta/nome).read_bytes()).hexdigest() for nome in
                   ['main.tex','introducao.tex','dados.tex','modelo_atribuicao.tex','resultados.tex']}}
(raiz/'tmp/contagem_corpo_revisado.json').write_text(json.dumps(registro,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('TOTAL CORPO:',registro['palavras_corpo'])
