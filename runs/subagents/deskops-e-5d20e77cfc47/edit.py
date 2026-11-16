import re,sys
p='docs/spec2viz/acta-de-retiro.md'; s=open(p).read()
def rep(old,new):
    global s
    assert s.count(old)==1,(old[:60],s.count(old)); s=s.replace(old,new)
rep("""quedan 85
dependencias de spec2viz en el universo auditado y 9 filas de la matriz sin acreditar (corrida del
2026-11-16 de IR13g, que acreditó SV-H03 y SV-K22 tras la migración de graph_ui en `79d63ee`; eran 11""",
"""quedan 63
dependencias de spec2viz en el universo auditado y 9 filas de la matriz sin acreditar (corrida del
2026-11-16 de IR13h, con 0 dependencias de deskops tras su migración a specir; la de IR13g acreditó
SV-H03 y SV-K22 tras la migración de graph_ui en `79d63ee`; eran 11""")
block = """porque SV-H03 y SV-K22 pasan a cumplidas.
"""
rep(block, block + """
rc 1; 63 dependencias; 9 filas no acreditadas (SV-A17, H01, K09, K16, K18, K21, K23, K26 y K29), las
mismas que quedan abiertas en «Acreditación (IR13)» de la matriz. Corrida del 2026-11-16 a las 19:33
(-03:00), IR13h
(`task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4`), con el mismo
comando y `timeout 300`, sobre IR `4f1e108` (con el acta y la matriz de IR13h sin commitear), sldb
`12e9b191`, graph_ui `824c135` (39 rutas sin commitear en su árbol), deskops `12c5c2ce` (origin/main
`ee9bc3cd`), pron `39ea972` y spec2viz `91ba1d0`. Por repo o store: deskops 0, sldb 1, IR 43,
`spec2viz/.sldb` 19, graph_ui 0 y pron 0. deskops ya no depende de spec2viz: `git -C ../deskops
merge-base --is-ancestor` de `2421ca29`, `74ffdb63` y `b716bf85` contra `origin/main` sale con rc 0, y
`../deskops/.sldb/core/store_index.yaml` solo federa sldb, pron y scion (la única coincidencia de
`grep -n spec2viz` es la etiqueta semántica `system.spec2viz` del modelo `ViewDoc` de sldb, línea 308, no un
enlace de store; ver «Consumidores»). Las dependencias bajan de 85 a 63 porque desaparecen las 22 de
deskops; las 63 son las de la salida de abajo.
""")
old_row = re.search(r"^\| deskops \|.*\| pendiente \|\n", s, re.M).group(0)
new_row = ("| deskops | 22: 20 de habilidad de agente (`.claude/skills/deskops-workflow/SKILL.md`, `references/spec2viz-cli.md`, "
 "`.opencode/skills/use-spec2viz/SKILL.md`), 2 invocaciones (`desk/drawer/plans/workspace-documental/render_diagram.py:7`, `:9`), "
 "corrida del 2026-11-15 (y las de IR13e, IR13f e IR13g); 0 desde la del 2026-11-16 de IR13h (HEAD `12c5c2ce`, origin/main `ee9bc3cd`). "
 "Además, la regla de rutas `deskops/graph/desk_graph.py:75` (no es dependencia; decidida, ver «Decisiones» 4) "
 "| `deskops/desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md` "
 "| resuelto: deskops origin/main `ee9bc3cd` (aviso de su coordinador del 2026-11-16), en tres pares de commit y closeout, todos en origin: "
 "el enlace federado al store de spec2viz sale de su `.sldb` (`421d6a27`, closeout `74ffdb63`; G5 opción b), "
 "la regla de `deskops/graph/desk_graph.py:75` deja de nombrar spec2viz y reconoce los specs YAML sincronizados (`42b752ea`, closeout `b716bf85`) "
 "y las skills y el script `render_diagram.py` dejan de invocar spec2viz y usan specir (`ce66f69e`, closeout `2421ca29`). "
 "Comprobado desde IR el 2026-11-16 (IR13h): `git -C ../deskops merge-base --is-ancestor` de `2421ca29`, `74ffdb63` y `b716bf85` "
 "(y de `421d6a27`, `42b752ea` y `ce66f69e`) contra `origin/main` rc 0; `../deskops/.sldb/core/store_index.yaml` federa solo sldb, pron y scion "
 "(`grep -n spec2viz` solo encuentra la etiqueta `system.spec2viz` del modelo `ViewDoc` de sldb, línea 308); la corrida de IR13h no tiene filas de deskops. "
 "Quedan menciones en prosa (la remisión de `.opencode/skills/use-spec2viz/SKILL.md` a use-specir), que no cuentan para el comprobador |\n")
rep(old_row,new_row)
old_g4 = re.search(r"^\| G4 Consumidores \|.*\n", s, re.M).group(0)
rep(old_g4, "| G4 Consumidores | abierto | 63 dependencias (abajo; corrida del 2026-11-16 de IR13h): sldb 1 (`runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5`), IR 43 (los oráculos de paridad en pruebas, que se retiran al declarar) y `spec2viz/.sldb` 19 (G5). graph_ui (`79d63ee`), pron (`4224186`) y deskops (`ee9bc3cd`; closeouts `74ffdb63`, `b716bf85` y `2421ca29`) están resueltos y salen con 0 (ver «Consumidores»). |\n")
rep("""1. Consumidores (G4): que deskops y sldb resuelvan sus pedidos y respondan con el commit (pron quedó
   resuelto con `4224186` y graph_ui con `79d63ee`).""",
"""1. Consumidores (G4): que sldb resuelva su pedido y responda con el commit
   (`runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5`); lo demás que queda en G4 es de IR (los
   oráculos de paridad en pruebas, punto 6, que se retiran al declarar) y `spec2viz/.sldb` (G5, punto 2).
   pron quedó resuelto con `4224186`, graph_ui con `79d63ee` y deskops con `ee9bc3cd` (closeouts
   `74ffdb63`, `b716bf85` y `2421ca29`).""")
# salida del comprobador
deps=[l.strip() for l in open(sys.argv[1]) if l.count('\t')>=3]
assert len(deps)==63
m=re.search(r"(## Salida del comprobador \(dependencias\)\n\n```\n)(.*?)(```\n)", s, re.S)
s=s[:m.start(2)]+"\n".join(deps)+"\n"+s[m.end(2):]
open(p,'w').write(s)
q='docs/spec2viz/matriz-de-cobertura.md'; t=open(q).read()
o="  Estado IR13: **abierto**. `specir retirement check` lista dependencias en graph_ui, deskops, pron, sldb y en las pruebas de paridad de IR (acta).\n"
assert t.count(o)==1
t=t.replace(o,"  Estado IR13: **abierto**. `specir retirement check` (corrida del 2026-11-16 de IR13h, acta) lista 63 dependencias: sldb 1, las pruebas de paridad de IR 43 y el store `spec2viz/.sldb` 19 (G5); graph_ui, deskops y pron salen con 0.\n")
open(q,'w').write(t)
