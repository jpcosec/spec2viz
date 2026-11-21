# Script de grabación de los goldens de spec2viz

record_goldens.py (importaba spec2viz para grabar tests/visual/goldens/spec2viz-2de1056-*.json) se movió fuera del repo, a /mnt/ssd/proyectos/SLDB_1/reports/spec2viz-goldens/record_goldens.py, porque specir retirement check audita también runs/ y contaba sus 23 importaciones como dependencias de IR. Se grabó desde spec2viz HEAD 91ba1d0, con código idéntico a 2de1056. Movido por el coordinador el 2026-11-21.
