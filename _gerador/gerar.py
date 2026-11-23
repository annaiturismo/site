# -*- coding: utf-8 -*-
# Gera as páginas individuais de destino a partir de destinos_dados.py.
# Uso: python3 _gerador/gerar.py   (rodar na raiz do site)
import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from destinos_dados import DESTINOS

E = html.escape
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base = open(os.path.join(RAIZ, 'destinos.html'), encoding='utf-8').read()
TOPO = base[base.index('<body>'):base.index('<main>') + 6]
RODAPE = base[base.index('</main>'):base.index('<script>')]
GRUPOS = 'https://annaiturismo.gruposcomguia.com.br'
MESES = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
TEMPO = {'A': ('alta', 'Alta'), 'M': ('media', 'Média'), 'B': ('baixa', 'Baixa')}
INDEXAR = '--publicar' in sys.argv   # sem essa opção, as páginas ficam fora do Google

def foto(d, i):
    p = d['passeios'][i]
    return 'img/%s.jpg' % (p[2] if len(p) > 2 and p[2] else '%s-%d' % (d['slug'], i + 1))

def pagina(d):
    nome = E(d['nome'])
    h = []
    h.append('''<!DOCTYPE html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s: o que fazer, onde ficar e quando ir | Annaí Turismo</title>
<meta name="description" content="%s Guia da Annaí Turismo com passeios, onde ficar e melhor época, com saída de Porto Alegre.">
%s<link rel="icon" href="img/selo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&amp;family=Nunito+Sans:ital,wght@0,400;0,700;0,800;1,400&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="estilo.css">
</head>''' % (nome, E(d['frase']), '' if INDEXAR else '<meta name="robots" content="noindex">\n'))
    h.append(TOPO)
    grupo_btn = '\n    <a class="btn btn-linha" href="%s" target="_blank" rel="noopener">Ver grupo com guia</a>' % GRUPOS if d.get('grupo') else ''
    h.append('''
<div class="capa-dest" style="--foto:url('img/%s-capa.jpg')"><div class="wrap">
  <a class="voltar" href="destinos.html#%s">← Guia de destinos</a>
  <span class="etiqueta">%s</span>
  <h1>%s</h1>
  <p>%s</p>
  <div class="acoes-capa">
    <a class="btn btn-ouro" href="#orcamento">Quero um orçamento</a>
    <a class="btn btn-linha" href="#quando">Quando ir</a>%s
  </div>
</div></div>
''' % (d['slug'], d['ancora'], E(d['tag']), nome, E(d['frase']), grupo_btn))
    h.append('''
<section><div class="wrap dois porque">
  <div>
    <div class="titulo" style="text-align:left;margin:0 0 20px"><small>Por que ir</small><h2>%s</h2></div>
    %s
  </div>
  <div class="caixa">
    <h3>Para quem é</h3>
    <ul class="lista">
      %s
    </ul>
  </div>
</div></section>
''' % (E(d['por_titulo']), '\n    '.join('<p>%s</p>' % E(p) for p in d['por']),
       '\n      '.join('<li><b>%s:</b> %s</li>' % (E(a), E(b)) for a, b in d['para'])))
    ps = ''.join('''
    <div class="passeio"><div class="foto" style="--foto:url('%s')"></div><div class="txt"><h3>%s</h3><p>%s</p></div></div>''' % (foto(d, i), E(p[0]), E(p[1])) for i, p in enumerate(d['passeios']))
    h.append('''
<section style="background:#fff"><div class="wrap">
  <div class="titulo"><small>O que fazer</small><h2>3 passeios que não podem faltar</h2><p>Os clássicos de %s, que cabem com folga na sua viagem.</p></div>
  <div class="passeios tres">%s
  </div>
</div></section>
''' % (nome, ps))
    regs = ''
    for r in d['regioes']:
        selo = r[2] if len(r) > 2 else ''
        cls = ' destaque-r' if selo.startswith('Mais procurad') else ''
        sc = ' calmo' if 'tranquil' in selo.lower() or 'sossego' in selo.lower() else ''
        regs += '\n    <div class="regiao-c%s">%s<h3>%s</h3><p>%s</p></div>' % (cls, ('<span class="selo-r%s">%s</span>' % (sc, E(selo))) if selo else '', E(r[0]), E(r[1]))
    if d.get('hoteis'):
        cols = ''.join('<div><h4>%s</h4><ul>%s</ul></div>' % (E(t), ''.join('<li>%s</li>' % E(n) for n in ns)) for t, ns in d['hoteis'])
        hot = '''
  <div class="hoteis">
    <h3>⭐ %s que a Annaí indica</h3>
    <div class="hoteis-cols%s">%s</div>
  </div>''' % ('Resorts' if d['hoteis'][0][0].startswith('Resort') else 'Hotéis', ' um' if len(d['hoteis']) == 1 else '', cols)
    else:
        hot = '''
  <div class="hoteis hoteis-cta">
    <h3>⭐ Hotéis que a Annaí indica</h3>
    <p>Selecionamos hotéis com bom custo-benefício e opções superiores. Conte o seu perfil que a gente indica o ideal.</p>
    <a class="btn btn-azul" href="#orcamento">Quero uma indicação de hotel</a>
  </div>'''
    h.append('''
<section><div class="wrap">
  <div class="titulo"><small>Onde ficar</small><h2>%s</h2><p>%s</p></div>
  <div class="regioes">%s
  </div>%s
</div></section>
''' % (E(d.get('regioes_titulo', 'Escolha a região que combina com você')), E(d.get('regioes_sub', 'A equipe da Annaí indica o hotel certo para o seu perfil.')), regs, hot))
    meses = ''.join('\n    <div class="mes %s"><b>%s</b><span>%s</span></div>' % (TEMPO[c][0], MESES[i], TEMPO[c][1]) for i, c in enumerate(d['temp']))
    h.append('''
<section id="quando" style="background:#fff"><div class="wrap">
  <div class="titulo"><small>Quando ir</small><h2>Planeje sua viagem</h2></div>
  <div class="infos">
    <div><span>☀️</span><b>Melhor época</b><p>%s</p></div>
    <div><span>🗓️</span><b>Quanto tempo</b><p>%s</p></div>
    <div><span>✈️</span><b>Saindo de Porto Alegre</b><p>%s</p></div>
  </div>
  <div class="meses">%s
  </div>
  <div class="legenda"><span><i class="q alta"></i>Alta temporada</span><span><i class="q media"></i>Média temporada</span><span><i class="q baixa"></i>Baixa temporada</span></div>
</div></section>
''' % (E(d['sol']), E(d['tempo']), E(d['voo']), meses))
    h.append('''
<section id="orcamento"><div class="wrap" style="max-width:720px">
  <div class="caixa">
    <h3>Quero um orçamento para %s</h3>
    <p class="nota" style="margin:0 0 18px">Preencha e envie pelo WhatsApp. A equipe da Annaí monta as opções de voo saindo de Porto Alegre e hotel para você.</p>
    <form id="form-dest">
      <div class="campo"><label for="nome">Seu nome</label><input id="nome" required placeholder="Nome do responsável"></div>
      <div class="linha">
        <div class="campo"><label for="cidade">Cidade</label><input id="cidade" placeholder="Ex.: Santiago"></div>
        <div class="campo"><label for="mes">Mês da viagem</label><select id="mes"><option>Ainda não sei</option><option>Janeiro</option><option>Fevereiro</option><option>Março</option><option>Abril</option><option>Maio</option><option>Junho</option><option>Julho</option><option>Agosto</option><option>Setembro</option><option>Outubro</option><option>Novembro</option><option>Dezembro</option></select></div>
      </div>
      <div class="linha">
        <div class="campo"><label for="adultos">Adultos</label><input id="adultos" type="number" min="1" value="2"></div>
        <div class="campo"><label for="criancas">Crianças (idades)</label><input id="criancas" placeholder="Ex.: 5 e 9 anos"></div>
      </div>
      <div class="campo"><label for="pref">Tipo de hotel</label><select id="pref"><option>Me ajudem a escolher</option><option>Econômico</option><option>Superior</option></select></div>
      <div class="campo"><label for="obs">Alguma dúvida?</label><textarea id="obs" rows="3"></textarea></div>
      <a id="enviar" class="btn btn-ouro" style="width:100%%;justify-content:center" href="https://wa.me/5555999207070" target="_blank" rel="noopener">Enviar pelo WhatsApp</a>
      <p class="nota">Ao tocar no botão, o WhatsApp abre com a mensagem pronta para a Annaí.</p>
    </form>
  </div>
</div></section>
''' % nome)
    h.append('\n' + RODAPE)
    h.append('''<script>
(function(){
  var DESTINO=%s;
  var b=document.getElementById('enviar');
  function v(id){return (document.getElementById(id).value||'').trim()}
  function monta(){
    var t='Olá! Vi o guia de *'+DESTINO+'* no site e quero um orçamento.\\n'+
      'Nome: '+(v('nome')||'-')+'\\nCidade: '+(v('cidade')||'-')+'\\nMês: '+v('mes')+
      '\\nAdultos: '+v('adultos')+(v('criancas')?'\\nCrianças: '+v('criancas'):'')+
      '\\nHotel: '+v('pref')+(v('obs')?'\\nDúvida: '+v('obs'):'');
    b.href='https://wa.me/5555999207070?text='+encodeURIComponent(t);
  }
  var f=document.getElementById('form-dest');
  f.addEventListener('input',monta);f.addEventListener('change',monta);f.addEventListener('submit',function(e){e.preventDefault()});monta();
})();
</script>
</body></html>
''' % ('"%s"' % d['nome'].replace('"', '')))
    return ''.join(h)

def revisao():
    linhas = []
    for d in DESTINOS:
        fotos = ['%s-capa.jpg' % d['slug']] + [foto(d, i)[4:] for i in range(3)]
        existe = [os.path.exists(os.path.join(RAIZ, 'img', f)) for f in fotos]
        fs = ''.join('<li class="%s">%s</li>' % ('ok' if e else 'falta', f) for f, e in zip(fotos, existe))
        linhas.append('<tr><td><a href="%s.html" target="_blank">%s</a></td><td><ul>%s</ul></td><td>%s</td></tr>' % (d['slug'], E(d['nome']), fs, 'Sim' if d.get('hoteis') else '<b>Falta</b>'))
    return '''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Revisão das páginas de destino | Annaí</title><link rel="stylesheet" href="estilo.css">
<style>body{padding:30px}table{width:100%%;border-collapse:collapse;background:#fff}td,th{border-bottom:1px solid #e3e7ef;padding:10px;text-align:left;vertical-align:top;font-size:15px}ul{list-style:none}li.ok{color:#2f7d3a}li.ok::before{content:"✓ "}li.falta{color:#c0392b}li.falta::before{content:"✕ "}</style></head><body>
<div class="wrap"><h1>Revisão das páginas de destino</h1><p class="nota">Página interna (fora do Google). %d destinos. Fotos em verde já estão na pasta img; em vermelho, ainda faltam. Os nomes dos arquivos precisam ser exatamente estes.</p>
<table><tr><th>Página</th><th>Fotos (pasta img)</th><th>Hotéis indicados</th></tr>%s</table></div></body></html>''' % (len(DESTINOS), ''.join(linhas))

for d in DESTINOS:
    assert len(d['temp']) == 12 and len(d['passeios']) == 3, d['slug']
    open(os.path.join(RAIZ, d['slug'] + '.html'), 'w', encoding='utf-8').write(pagina(d))
open(os.path.join(RAIZ, 'revisao.html'), 'w', encoding='utf-8').write(revisao())
print(len(DESTINOS), 'páginas geradas')
