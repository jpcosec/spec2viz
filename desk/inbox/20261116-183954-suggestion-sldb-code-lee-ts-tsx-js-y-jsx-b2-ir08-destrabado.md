---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T18:39:54'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb.code lee TS, TSX, JS y JSX (B2, IR08 destrabado)

_Describe the incoming message with enough evidence to triage._

En sldb quedó cerrada B2: código 600b51a9 y closeout 34b26a50, sobre origin c5cb52f0; wA:p1 lo integra y avisa del push. Con el extra code (incluye tree-sitter-typescript 0.23.2), sldb.code lee .ts con la gramática typescript y .tsx, .js y .jsx con la gramática tsx, en un mismo reader. Los hechos tienen la misma forma que los de Python. kind:
- component: nombre en mayúscula y JSX en el cuerpo, también con memo y forwardRef;
- hook: use seguido de mayúscula;
- type: type o interface, solo en TS;
- function;
- module.
El docstring es el JSDoc adyacente. Las anclas code:<ruta>.<ext>::<símbolo> pasan por intact, changed, lost y reconnected. find_files no recorre node_modules. La salida de .py no cambia. Sigue B2-SQL (dialecto PostgreSQL), que destraba IR09.
