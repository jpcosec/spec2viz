#!/usr/bin/env bash
# Prueba integrada de la suite SLDB_1 (sldb, pron, deskops, spec2viz, graph_ui), sin deploy.
#
#   tools/suite-check.sh [--fresh] [--from-origin] [--skip-install] [--skip-suites] [--skip-e2e]
#
# --from-origin: clona cada repo desde su origin (git clone --depth 1, rama principal) en
#    SUITE_CLONES (por defecto <SUITE_REPORT>/origin) y usa esos clones como ROOT, sin tocar
#    los checkouts de trabajo; es la corrida que vale para decidir un deploy. Los origin se
#    leen de los checkouts bajo SLDB1_ROOT (o de SUITE_ORIGIN_<name> si se exporta).
#
# 1. Crea un venv limpio (SUITE_VENV, por defecto /tmp/suite-venv) con SUITE_PYTHON (por
#    defecto /usr/bin/python3) e instala los cinco repos desde sus checkouts (SLDB1_ROOT,
#    por defecto el padre del checkout de spec2viz). kgdb no se instala: ya no existe.
# 2. Corre la suite de cada repo en ese venv (logs en SUITE_REPORT, por defecto /tmp/suite-check).
# 3. Corre un flujo de punta a punta en un repo temporal: deskops init -> add task -> advance
#    -> closeout commit; spec2viz diagram sync + notation sync + notation view contra ese
#    store; graph_ui sirviendo ese store con /api/schema, /api/graph y /api/notation/view en 200.
# 4. Imprime la tabla repo x resultado y sale con 1 si algo fallo.
set -u

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
ROOT=${SLDB1_ROOT:-$(cd "$HERE/.." && pwd)}
VENV=${SUITE_VENV:-/tmp/suite-venv}
PY=${SUITE_PYTHON:-/usr/bin/python3}
REPORT=${SUITE_REPORT:-/tmp/suite-check}
PORT=${SUITE_PORT:-8123}
FRESH=0; DO_INSTALL=1; DO_SUITES=1; DO_E2E=1; FROM_ORIGIN=0
for arg in "$@"; do
  case "$arg" in
    --fresh) FRESH=1 ;;
    --from-origin) FROM_ORIGIN=1 ;;
    --skip-install) DO_INSTALL=0 ;;
    --skip-suites) DO_SUITES=0 ;;
    --skip-e2e) DO_E2E=0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done
mkdir -p "$REPORT"
VPY="$VENV/bin/python"
declare -A RESULT NOTE
FAILED=0

say() { printf '\n== %s\n' "$*"; }
record() { RESULT[$1]=$2; NOTE[$1]=${3:-}; [ "$2" = ok ] || FAILED=1; }
last_line() { tail -n 1 "$1" 2>/dev/null | cut -c1-110; }

REPOS=(sldb pron deskops spec2viz UIs/graph_ui)

# --- 0. clones desde origin (--from-origin) -----------------------------------------------------
declare -A HASH
if [ "$FROM_ORIGIN" = 1 ]; then
  CLONES=${SUITE_CLONES:-$REPORT/origin}
  say "clones desde origin en $CLONES"
  rm -rf "$CLONES"; mkdir -p "$CLONES"
  for repo in "${REPOS[@]}"; do
    name=$(basename "$repo")
    var="SUITE_ORIGIN_$name"
    url=${!var:-$(git -C "$ROOT/$repo" remote get-url origin 2>/dev/null)}
    branch=$(git ls-remote --symref "$url" HEAD 2>/dev/null | sed -n 's|^ref: refs/heads/\(.*\)\tHEAD|\1|p')
    if [ -z "$url" ] || [ -z "$branch" ]; then record "clone:$name" FAIL "sin origin o sin rama principal ($url)"; continue; fi
    if git clone -q --depth 1 --branch "$branch" "$url" "$CLONES/$repo" > "$REPORT/clone-$name.log" 2>&1; then
      HASH[$name]=$(git -C "$CLONES/$repo" rev-parse --short HEAD)
      record "clone:$name" ok "$branch@${HASH[$name]} $url"
    else
      record "clone:$name" FAIL "$(last_line "$REPORT/clone-$name.log")"
    fi
  done
  ROOT=$CLONES
fi

# --- 1. venv e instalacion ------------------------------------------------------------------
# SUITE_REPOS="deskops UIs/graph_ui" limita las suites del paso 2 (la instalacion siempre es completa)
read -r -a SUITE_REPOS_ARR <<< "${SUITE_REPOS:-${REPOS[*]}}"
if [ "$DO_INSTALL" = 1 ]; then
  say "venv $VENV ($PY)"
  [ "$FRESH" = 1 ] && rm -rf "$VENV"
  if [ ! -x "$VPY" ]; then "$PY" -m venv "$VENV" || { echo "no pude crear el venv"; exit 1; }; fi
  "$VPY" -m pip install -q --upgrade pip > "$REPORT/pip.log" 2>&1
  for repo in "${REPOS[@]}"; do
    name=$(basename "$repo")
    extras=""
    case "$name" in
      sldb) extras="[click,graph]" ;;
      deskops|spec2viz) extras="[dev]" ;;
      pron) extras="[mcp,dev]" ;;  # tests/mcp_* importan mcp/anyio
      graph_ui) extras="[test,notation]" ;;
    esac
    if "$VPY" -m pip install -q -e "$ROOT/$repo$extras" >> "$REPORT/pip.log" 2>&1; then
      record "install:$name" ok
    else
      record "install:$name" FAIL "$(grep -i 'error' "$REPORT/pip.log" | tail -n 1 | cut -c1-110)"
    fi
  done
  # pron pide structuredLanguageDB>=0.1.12 y pip puede traer una rueda de PyPI por encima del
  # checkout: se reinstala sldb editable al final y se comprueba que los cinco vienen de ROOT
  "$VPY" -m pip install -q --no-deps -e "$ROOT/sldb[click,graph]" >> "$REPORT/pip.log" 2>&1 || true
  "$VPY" -m pip install -q pytest playwright >> "$REPORT/pip.log" 2>&1 || true
  for pkg in structuredLanguageDB pron deskops spec2viz graph-ui; do
    loc=$("$VPY" -m pip show "$pkg" 2>/dev/null | sed -n 's/^Editable project location: //p')
    case "$loc" in "$ROOT"/*) record "local:$pkg" ok "$loc" ;; *) record "local:$pkg" FAIL "no es el checkout: ${loc:-no editable} ($("$VPY" -m pip show "$pkg" 2>/dev/null | sed -n 's/^Version: //p'))" ;; esac
  done
  # los e2e de graph_ui lanzan chromium con playwright; sin navegador fallan los 16
  if "$VPY" -m playwright install chromium >> "$REPORT/pip.log" 2>&1; then record "install:chromium" ok; else record "install:chromium" FAIL "playwright install chromium fallo"; fi
  "$VPY" -m pip freeze > "$REPORT/freeze.txt" 2>/dev/null
  if grep -qi "^kgdb" "$REPORT/freeze.txt"; then record "install:no-kgdb" FAIL "kgdb quedo instalado"; else record "install:no-kgdb" ok; fi
fi

# --- 2. suites ------------------------------------------------------------------------------
if [ "$DO_SUITES" = 1 ]; then
  for repo in "${SUITE_REPOS_ARR[@]}"; do
    name=$(basename "$repo")
    say "suite $name"
    log="$REPORT/suite-$name.log"
    ( cd "$ROOT/$repo" && "$VPY" -m pytest tests -q -p no:cacheprovider --ignore=tests/e2e > "$log" 2>&1 )
    rc=$?
    summary=$(grep -E "passed|failed|error" "$log" | tail -n 1 | cut -c1-110)
    if [ $rc -eq 0 ]; then record "suite:$name" ok "$summary"; else record "suite:$name" FAIL "${summary:-$(last_line "$log")}"; fi
  done
fi

# --- 3. punta a punta ---------------------------------------------------------------------------
if [ "$DO_E2E" = 1 ]; then
  say "e2e en repo temporal"
  TMP=$(mktemp -d /tmp/suite-e2e.XXXXXX)
  E2E="$REPORT/e2e.log"; : > "$E2E"
  run() { echo "\$ $*" >> "$E2E"; "$@" >> "$E2E" 2>&1; }
  export PATH="$VENV/bin:$PATH"
  (
    cd "$TMP" || exit 1
    git init -q . && git config user.email suite@example.invalid && git config user.name suite
    mkdir -p tests && printf 'def test_ok():\n    assert True\n' > tests/test_ok.py
    git add -A && git commit -q -m "init"
    # deskops: init -> task -> advance -> closeout commit
    run deskops init . || exit 10
    BASE=$(git rev-parse --short HEAD)
    run deskops add task --root . --title "Suite check task" --goal "Cerrar por el ciclo completo" --scope "tests/test_ok.py" --validation "python -m pytest tests -q" --done-when "cerrada por closeout commit" || exit 11
    TASK=$(ls desk/tasks | grep '^task-suite-check' | sed 's/\.md$//' | head -n 1)
    [ -n "$TASK" ] || { echo "no task file"; exit 11; }
    run deskops add atom --root . --title "Suite check atom" --five-wh-one-plus what --answer "Un atomo de prueba para el flujo integrado." --tags system:suite || exit 12
    ATOM=$(ls desk/atoms | grep -i 'suite' | head -n 1)
    git add -A && git commit -q -m "desk: task and atom" && SHA=$(git rev-parse --short HEAD)
    run deskops edit task "$TASK" references "[\"$SHA\", \"tests/test_ok.py\", \"desk/atoms/$ATOM\"]" || exit 13
    run deskops advance task "$TASK" --root . || exit 14
    run deskops advance task "$TASK" --root . || exit 14
    run deskops closeout verify --root . --task "$TASK" || exit 15
    PATHS=("desk/tasks/$TASK.md" desk .sldb); for extra in .deskops.log runs; do [ -e "$extra" ] && PATHS+=("$extra"); done
    run deskops closeout commit --root . --task "$TASK" --no-run --reason "suite check" -m "closeout(task): suite check" --paths "${PATHS[@]}" || exit 16
    [ "$(deskops list tasks --root . 2>/dev/null | grep -c '^task-')" = 0 ] || { echo "task still listed"; exit 17; }
    echo "deskops e2e ok" >> "$E2E"
  )
  rc=$?; [ $rc -eq 0 ] && record "e2e:deskops" ok || record "e2e:deskops" FAIL "exit $rc: $(last_line "$E2E")"

  (
    cd "$TMP" || exit 1
    mkdir -p docs
    cat > docs/shapes.yml <<'YML'
id: shapes
title: Shapes
type: class
version: "1"
data:
  classes:
    Shape: {kind: interface, methods: [{name: area, returns: float}]}
    Circle: {attributes: [{name: r, type: float}]}
  relations:
    - {from: Circle, to: Shape, relation: realization}
YML
    cat > docs/door.yml <<'YML'
id: door
title: Door
type: state
version: "1"
data:
  entity: Door
  initial: closed
  states:
    - {id: closed, label: Closed}
    - {id: open, label: Open, contains: [ajar, wide]}
    - {id: ajar, label: Ajar}
    - {id: wide, label: Wide}
  transitions:
    - {from: closed, to: open, "on": push, guard: unlocked}
    - {from: wide, to: closed, "on": slam}
YML
    run spec2viz diagram validate docs/shapes.yml docs/door.yml || exit 20
    run spec2viz diagram sync docs/shapes.yml docs/door.yml --store .sldb --strict || exit 21
    run spec2viz notation sync uml-class statechart --store .sldb --strict || exit 22
    run spec2viz notation view door --store .sldb --out "$TMP/door-view.json" || exit 23
    "$VPY" - "$TMP/door-view.json" <<'PYV' >> "$E2E" 2>&1 || exit 24
import json, sys
v = json.load(open(sys.argv[1]))
nests = [l for l in v["links"] if l["draw"] == "nest"]
assert v["notation"] == "NotationDoc:statechart" and len(v["nodes"]) == 4 and len(nests) == 2 and not v["skipped"], v
print("spec2viz view ok:", len(v["nodes"]), "nodes", len(v["links"]), "links")
PYV
    run "$VPY" -m sldb edges check --store .sldb || exit 25
  )
  rc=$?; [ $rc -eq 0 ] && record "e2e:spec2viz" ok || record "e2e:spec2viz" FAIL "exit $rc: $(last_line "$E2E")"

  (
    cd "$ROOT/UIs/graph_ui" || exit 1
    SLDB_STORE="$TMP/.sldb" "$VPY" frontends/mindmap/serve.py "$PORT" > "$REPORT/graph_ui-serve.log" 2>&1 &
    SRV=$!
    for _ in $(seq 1 40); do curl -s -o /dev/null "http://127.0.0.1:$PORT/" && break; sleep 0.5; done
    fail=0
    i=0
    for path in /api/schema /api/graph "/api/notation/view?spec=door" "/api/notation/view?spec=shapes"; do
      i=$((i + 1))
      code=$(curl -s -o "$REPORT/gui-$i.json" -w '%{http_code}' "http://127.0.0.1:$PORT$path")
      echo "GET $path -> $code (gui-$i.json)" >> "$E2E"
      [ "$code" = 200 ] || fail=1
    done
    kill $SRV 2>/dev/null; wait $SRV 2>/dev/null
    [ $fail = 0 ] || exit 30
    "$VPY" - "$REPORT/gui-3.json" "$TMP/door-view.json" <<'PYV' >> "$E2E" 2>&1 || exit 31
import json, sys
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
assert a == b, "graph_ui /api/notation/view differs from spec2viz notation view"
print("graph_ui view parity ok")
PYV
  )
  rc=$?; [ $rc -eq 0 ] && record "e2e:graph_ui" ok || record "e2e:graph_ui" FAIL "exit $rc: $(last_line "$E2E")"
  echo "e2e tmp repo: $TMP" >> "$E2E"
fi

# --- 4. tabla -------------------------------------------------------------------------------------
say "resultado"
printf '%-22s %-5s %s\n' "paso" "ok?" "nota"
for key in $(printf '%s\n' "${!RESULT[@]}" | sort); do
  printf '%-22s %-5s %s\n' "$key" "${RESULT[$key]}" "${NOTE[$key]}"
done
if [ "$FROM_ORIGIN" = 1 ]; then
  echo; echo "origin HEAD por repo:"
  for repo in "${REPOS[@]}"; do name=$(basename "$repo"); printf '  %-10s %s\n' "$name" "${HASH[$name]:-?}"; done
fi
echo "logs: $REPORT"
exit $FAILED
