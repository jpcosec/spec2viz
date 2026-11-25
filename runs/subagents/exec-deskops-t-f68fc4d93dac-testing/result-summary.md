PASA

# Resultado del tester — U1b: cascarón de la UI con tokens de papel

- Tarea: `task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta`.
- Commit del ejecutor: `9e0ca79cc2b806c480b07ae4ab28e7c858e7c76c` — *U1b: cascaron de la UI con tokens de papel*.
- Archivos del commit: `ui/index.html`, `ui/src/Shell.tsx`, `ui/src/shell.css`. Todos bajo `ui/`; no toca Python ni `sldb/`.
- No hay archivos `tests/*.py` en el commit ni módulos Python tocados, así que la validación aplicable es la de la tarea (UI): `tsc` + `vitest` sobre `Shell.test.tsx`.

## Comprobaciones exigidas

| Comprobación | Resultado |
|---|---|
| `cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx` | **rc 0**: tsc sin errores y `Shell.test.tsx` con **4/4 tests passed** |
| `npx vitest run` (suite completa de `ui/` como regresión) | **2 archivos, 6/6 tests passed**, rc 0 |
| `Shell.test.tsx` sin cambios | OK; los roles/nombres accesibles no cambiaron y los 4 tests siguen pasando |

Log completo: `runs/subagents/exec-deskops-t-f68fc4d93dac-testing/validation.log`.

## Contrato visual revisado en el código

| Requisito | Evidencia |
|---|---|
| Tokens `--wb-*`, sin colores a mano | `ui/src/shell.css` usa variables `--wb-*` en todas sus reglas (31 usos); `grep` de `#hex`, `rgb()` y `hsl()` no encuentra ninguno. |
| Botones sin apariencia nativa | `shell.css:5` resetea `button` (fondo, borde, padding); pestañas y lentes tienen reglas propias en `shell.css:15-22`. |
| Pestañas y lentes monoespaciadas, borde de 2 px, activa en piedra | `shell.css:15-21`: `font: 12px var(--wb-font-mono)`, `border: 2px solid transparent`; activa con `background: var(--wb-stone)` y `border-color: var(--wb-border)`. |
| Explorador con fondo piedra y borde | `shell.css:24`: `background: var(--wb-stone)` y `border-right`. |
| Panel de documento con borde | `shell.css:25`: borde izquierdo `var(--wb-border)`. |
| Títulos en serif (Newsreader) | `shell.css:6-7` y `.brand` en `shell.css:12` usan `var(--wb-font-serif)`; `index.html` carga Newsreader. |
| Rail inferior | `Shell.tsx:42-45` y `shell.css:27-30` (fila de 24 px, fondo piedra, borde superior). |
| Miga en la cabecera | `Shell.tsx:17` inserta `.crumb`; `shell.css:13` la estiliza en mono. Usa el valor por defecto `"store"` (ver diferencias). |

## Capturas y comparación en Chrome real

- `runs/subagents/exec-deskops-e-c5a02bd67c2b/captura-app.png` (app) y `captura-maqueta.png` (maqueta), ambas de 1400×800.
- Reproduje las dos capturas de forma independiente con `chromium --headless` sobre `vite dev` en `127.0.0.1:5199` (HEAD `de5cfbae`, que contiene el commit del ejecutor) y sobre `maqueta-ui.html#grafo`:
  - app: SHA-256 `61741f666de6576376b23a5e1c9be224deb24c3b620493bf2a8d25e9f35b31ae`, **idéntico** al del ejecutor;
  - maqueta: SHA-256 `3b4011174c913d82d2afdbc2918c0d0e274bcae4815f820f07ca2fa5b1bf41b6`, **idéntico** al del ejecutor.
- Las capturas muestran el mismo cascarón: cabecera con marca, miga, pestañas y lentes; explorador en piedra con borde; columna central sobre papel; panel de documento con borde; rail inferior.

## Diferencias observadas (no bloqueantes)

- El borde de pestañas/lentes es de **2 px** como pide esta tarea; `maqueta-ui.html` usa 1 px. Es una diferencia deliberada a favor del encargo.
- La miga muestra el placeholder `store` porque el Shell aún no carga datos del store; la prop `storeName` ya existe (`Shell.tsx:8`) para cablearla en U2. La estructura de miga sí está presente y visible.
- El contenido de las pestañas y del explorador no existe todavía: queda fuera de alcance (U2-U9). Las fuentes se cargan de Google Fonts; sin red caen a los fallbacks declarados en los tokens.

## Veredicto

PASA. El cascarón cumple el contrato visual solicitado, `shell.css` usa los tokens `--wb-*` sin colores literales, las capturas son reproducibles e idénticas a las del ejecutor, y la validación `tsc` + `vitest src/Shell.test.tsx` pasa.
