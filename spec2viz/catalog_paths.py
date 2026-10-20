"""Rutas de un `vistas.yml` (o de los items de un diagram store): una sola regla para `src`/`mmd`,
`specs` y `notation`.

Una ruta relativa se busca primero junto al archivo de configuracion (la carpeta del
`vistas.yml`) y, si ahi no existe, desde la raiz del repositorio (el ancestro mas cercano con
`.git`, o con `.sldb` si no hay git). Si existen las dos y son archivos distintos, la ruta es
ambigua (`AmbiguousPathError`); si no existe ninguna, el error lista las rutas que se probaron.
Una ruta absoluta se usa tal cual. En `src`, un `#fragmento` final no es parte de la ruta.
"""

from __future__ import annotations

from pathlib import Path

from spec2viz.exceptions import AmbiguousPathError, UnknownReferenceError


def repo_root(start: Path) -> Path | None:
    """El ancestro mas cercano de `start` con `.git` (archivo o carpeta) o, si no hay, con `.sldb`."""
    start = Path(start).resolve()
    chain = [start, *start.parents]
    for marker in (".git", ".sldb"):
        for directory in chain:
            if (directory / marker).exists():
                return directory
    return None


def candidates(value: str | Path, config_dir: Path) -> list[Path]:
    """Las rutas que la regla prueba, en orden y sin repetir."""
    path = Path(str(value))
    if path.is_absolute():
        return [path]
    config_dir = Path(config_dir).resolve()
    out = [(config_dir / path).resolve()]
    root = repo_root(config_dir)
    if root is not None:
        from_root = (root / path).resolve()
        if from_root != out[0]:
            out.append(from_root)
    return out


def resolve_catalog_path(value: str | Path, config_dir: Path, field: str = "path",
                         missing: type[Exception] = UnknownReferenceError) -> Path:
    """La ruta de `value` segun la regla del catalogo.

    `AmbiguousPathError` si existen las dos candidatas y son archivos distintos; `missing`
    (por defecto `UnknownReferenceError`) con las rutas probadas si no existe ninguna.
    """
    tried = candidates(value, config_dir)
    found = [p for p in tried if p.exists()]
    if len(found) == 2 and not found[0].samefile(found[1]):
        raise AmbiguousPathError(
            f"{field} {str(value)!r} is ambiguous: it exists next to the config ({found[0]}) and from the repo root ({found[1]}); "
            "make it unambiguous (a path from the repo root that does not also exist next to the config, or the reverse)"
        )
    if found:
        return found[0]
    raise missing(f"{field} {str(value)!r} not found; tried: {', '.join(str(p) for p in tried)}")


def split_fragment(value: str) -> tuple[str, str]:
    """`archivo.html#seccion` -> (`archivo.html`, `seccion`)."""
    path, _, fragment = str(value).partition("#")
    return path, fragment


__all__ = ["repo_root", "candidates", "resolve_catalog_path", "split_fragment"]
