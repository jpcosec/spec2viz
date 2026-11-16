REFORMULACION
Encargo en el repo IR: ejecutar la tarea task-ir13e para portar a IR, contra sldb y sin importar spec2viz, las pruebas de notaciones, paletas y vistas de spec2viz. El resultado es tests/visual/test_notations_parity.py con 42 pruebas portadas y 9 comparaciones «valida igual» (51 funciones), fixtures copiados, reexportaciones en src/specir/visual/notation_style.py y 16 filas de «Acreditación (IR13)» actualizadas, más el resumen y el acta. Límites: no cambiar sldb ni spec2viz, no implementar capacidades visuales, no cambiar condiciones de IR07, no declarar el retiro; quedan fuera G5, SV-K09/K16/K21/K26/K29 y el store spec2viz/.sldb.

AMBIGUEDADES
1. «40 casos» frente a «Quedan 42 pruebas a portar» y «42 pruebas portadas (40, más test_notation_load_gives_typed_errors y test_palette_check_is_typed)». Obliga a decidir si el total base es 40 o 42 y qué significa el paréntesis; la precisión (f) dice 42+9=51.
2. «se agregan ahí como reexportaciones los nombres que falten» no enumera los nombres. Obliga a inventar o inferir el conjunto exacto de reexportaciones si no se inspecciona sldb.api.
3. «test_notation_validate_gives_typed_errors (load_notation lanza el error tipado, 7 casos)» y luego «sale de test_notation_validate_gives_typed_errors de test_style_palette.py». Obliga a decidir en qué archivo fuente está y si el nombre citado es correcto.

DRY-RUN
Lecturas: TaskDoc, matriz y acta, pruebas fuente de spec2viz en b624b75, notation_style.py, tests/test_imports.py, API pública de sldb y fixtures. Cambios previstos: copiar 8 notaciones y la paleta default con README; crear test_notations_parity.py; añadir reexportaciones; editar matriz y acta. Dependencias: exports de sldb.api, deskops, revisión de spec2viz y entorno .venv. Validaciones futuras: pytest del archivo nuevo, test_imports, matriz, retirement gate, test_catalog, grep de imports, specir retirement check, suite completa con flock y deskops graph missing. Nada se ejecuta aquí.

FUTURO
sldb debe entregar exports o corregir diferencias; su desk recibe las notas. Un humano aprueba la acreditación de filas y el retiro, que esta tarea no declara. El ejecutor futuro corre las validaciones y registra resultados.
