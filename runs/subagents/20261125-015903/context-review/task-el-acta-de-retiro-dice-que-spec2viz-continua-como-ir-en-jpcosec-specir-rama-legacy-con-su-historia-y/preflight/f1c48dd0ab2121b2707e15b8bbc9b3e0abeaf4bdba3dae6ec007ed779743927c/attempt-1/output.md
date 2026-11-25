REFORMULACION
Propósito: actualizar el acta de retiro de spec2viz para reflejar que no quedó archivado, sino que continúa como IR en jpcosec/specir (main=IR; legacy=historia de spec2viz), y marcar el punto 9 como hecho con salvedad fechada 2026-11-24 y decisión de JP. Resultado: `docs/spec2viz/acta-de-retiro.md` contiene esa salvedad, nombra jpcosec/specir y la rama legacy, y el punto 9 está marcado; `gate-de-retiro.md` se ajusta solo si nombra el archivo; sin cambios de código. Repo: checkout actual (`/mnt/ssd/proyectos/SLDB_1/IR`), aunque el input solo da rutas relativas. Límites: solo esos documentos; nada de código; la única validación prevista es el grep indicado. No es agregado ni paquete: es una tarea documental ejecutable.

AMBIGUEDADES
1. "El acta dice que el repo quedo archivado" frente a "registra el cambio: spec2viz no queda archivado sino que continua..." no aclara si debe corregirse/eliminarse la frase previa o solo añadirse una salvedad; obliga a inventar el tratamiento editorial.
2. "docs/spec2viz/acta-de-retiro.md (y gate-de-retiro.md si nombra el archivo)" no da la ruta del gate ni el criterio exacto para editarlo; obliga a inventar ubicación y alcance.
3. "Agregar la salvedad fechada 2026-11-24 y marcar el punto 9" no incluye el texto actual ni el formato de marca (checkbox, "hecho", tachado) ni la redacción literal de la salvedad; obliga a inventar contenido y representación.

DRY-RUN
Lecturas: acta y, si existe y el acta lo nombra, gate. Cambios previstos: añadir salvedad fechada 2026-11-24 con main=IR, legacy=historia y decisión de JP; marcar punto 9; tocar gate solo si nombra el archivo. Dependencias: contenido y ubicación reales de ambos documentos; no hay código. Validaciones futuras: ejecutar `grep -n 'jpcosec/specir' docs/spec2viz/acta-de-retiro.md` y revisar que nombre rama legacy, fecha y decisión, y que el punto 9 esté marcado. Nada se ejecuta ahora.

FUTURO
Un humano aprueba la redacción final y el commit; un nodo validador ejecutará el grep. No se identifica artefacto externo pendiente.
