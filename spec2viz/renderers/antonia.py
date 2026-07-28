from __future__ import annotations
from spec2viz.renderers.mermaid import MermaidRenderer

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>antonIA Diagram</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;1,400&family=Manrope:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.min.js"></script>
<style>
  :root{{--bg:#0a0a0f;--amber:#d4a574;--bone:#f5f0e8;--bone-dim:rgba(245,240,232,.6);--line:rgba(212,165,116,.25);--card:#12121a;}}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{background:var(--bg);color:var(--bone);font-family:'Manrope',sans-serif;}}
  section{{padding:44px 6%;}}
  .board{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:26px;overflow-x:auto;}}
  .mermaid{{display:flex;justify-content:center;min-width:600px;}}
</style>
</head>
<body>
<section>
  <div class="board"><pre class="mermaid">
{MERMAID_CONTENT}
  </pre></div>
</section>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'base',
    themeVariables: {{
      darkMode: true,
      background: '#12121a',
      primaryColor: '#1a1a24',
      primaryTextColor: '#f5f0e8',
      primaryBorderColor: '#d4a574',
      lineColor: '#d4a574',
      secondaryColor: '#22222e',
      tertiaryColor: '#12121a',
      fontFamily: 'Manrope, sans-serif',
      fontSize: '14px',
      noteBkgColor: '#2a2233',
      noteTextColor: '#f5f0e8',
      noteBorderColor: '#7c5d94',
      actorBkg: '#1a1a24',
      actorBorder: '#d4a574',
      actorTextColor: '#f5f0e8',
      signalColor: '#d4a574',
      signalTextColor: '#f5f0e8',
      labelBoxBkgColor: '#2a2233',
      labelTextColor: '#f5f0e8',
      loopTextColor: '#f5f0e8',
      altSectionBkgColor: 'rgba(212,165,116,0.06)',
      clusterBkg: 'rgba(245,240,232,0.03)',
      clusterBorder: 'rgba(212,165,116,0.35)',
      edgeLabelBackground: '#12121a',
      titleColor: '#f5f0e8'
    }},
    flowchart: {{ curve: 'basis', htmlLabels: true }},
    sequence: {{ mirrorActors: false, actorMargin: 40 }}
  }});
</script>
</body>
</html>
"""

class AntoniaHtmlRenderer:
    def render(self, ir) -> str:
        mermaid_content = MermaidRenderer().render(ir)
        return TEMPLATE.format(MERMAID_CONTENT=mermaid_content)
