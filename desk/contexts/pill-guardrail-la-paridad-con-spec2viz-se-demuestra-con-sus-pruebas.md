---
sldb:
  by: agent
  at: '2026-11-25T14:20:33Z'
  authority: generated
  via: save_document_payload
# pill-xxx
id: pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas
status: active
summary: Una capacidad esta cubierta cuando su prueba de aceptacion pasa; sin goldens
  de spec2viz.
# e.g., language:python, library:pydantic
tags:
- system:specir
---

# Guardrail: la paridad con spec2viz se demuestra con sus pruebas

## What

_Define the context or guardrail this pill carries._

Una capacidad (de las que tenia spec2viz o de las que pide la paridad de la UI) se considera cubierta cuando su prueba de aceptacion pasa contra specIR o graph_ui. Se cumple con features, no con codigo: no hay goldens de spec2viz ni comparacion de salida contra el.

## Why

_Explain why this context matters for safe execution._

Decision de JP (2026-11-25): mantener goldens de spec2viz solo genera ruido; lo que importa es que cada capacidad funcione, demostrado por una prueba de aceptacion.

## When

_Describe when an agent should apply this pill._

En toda tarea que migre, reemplace o agregue una capacidad de visualizacion de specIR o de su UI.

## Where

_Name the files, surfaces, or scope this pill applies to._

Las pruebas de aceptacion de specIR (tests/) y de graph_ui (tests/e2e_*.py, tests/*.test.mjs). La matriz docs/spec2viz/matriz-de-cobertura.md y el acta quedan como documentos historicos.

## How

_Describe the correct way to apply this guidance._

Escribir para cada capacidad una prueba de aceptacion que ejercite el comportamiento (entrada real o fixture del repo, salida observable) y registrar en la tarea cual es.

## How Not

_Describe the shortcut or failure mode to avoid._

No portar ni regenerar goldens de spec2viz; no comparar salida byte a byte contra spec2viz; no declarar cubierta una capacidad sin una prueba de aceptacion que pase.
