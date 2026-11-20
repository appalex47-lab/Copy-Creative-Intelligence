#!/usr/bin/env python3
"""V20 (H-09): prueba estructural EXTERNA, de solo lectura, de cobertura referencial de la especificación.
Toda columna *_id / source_* de las tablas nuevas debe figurar en una FK (sección «Claves foráneas» del bloque, o fila del contrato 4.4.9 / inventario
«columna agregada» cuyo origen es esa tabla) o estar en la lista EXPLÍCITA de excepciones justificadas. Incluye controles negativos: al quitar una FK
de una copia en memoria, la prueba debe detectarla. Uso: python3 -I este.py <especificacion.md>"""
import re, sys
S = open(sys.argv[1], encoding="utf-8").read()
EXC = {  # (tabla, columna): justificación (todas con fuente en la especificación)
 ("impact_evaluations", "correlation_id"): "identificador de correlación generado; no es referencia",
 ("impact_evaluations", "client_correlation_id"): "identificador de correlación del cliente; no es referencia",
 ("publication_attempts", "correlation_id"): "identificador de correlación generado; no es referencia",
 ("publication_attempts", "client_correlation_id"): "identificador de correlación del cliente; no es referencia",
 ("attribution_discard_resolutions", "evidence_attribution_id"): "CHECK evidence_attribution_id = coalesce(...atribución) (alternativa declarada)",
 ("attribution_discard_resolutions", "evidence_version_id"): "trigger de versión (alternativa declarada, IG5-93)",
 ("attribution_discard_resolutions", "source_kind"): "enumeración, no referencia",
 ("contribution_events", "source_hash"): "huella, no referencia", ("contribution_events", "operation_id"): "identificador de operación generado",
 ("contribution_events", "source_attribution_relation"): "enumeración, no referencia",
}
def bloques(txt):
    L = txt.split("\n"); h = [(i, re.match(r"#### `(\w+)`", l).group(1)) for i, l in enumerate(L) if re.match(r"#### `(\w+)`", l)]
    for k, (i, n) in enumerate(h): yield n, "\n".join(L[i:(h[k+1][0] if k+1 < len(h) else len(L))])
def cols(b):
    out = []; m = False
    for l in b.split("\n"):
        if l.startswith("| Columna |"): m = True; continue
        if m and l.startswith("|---"): continue
        if m and l.startswith("|"): out.append(l.strip("|").split("|")[0].strip())
        elif m and not l.startswith("|"): m = False
    return out
def fks(b):
    seg = b.split("**Claves foráneas:**")
    return seg[1].split("**Restricciones")[0] if len(seg) > 1 else ""
def agregadas(txt, tabla):  # filas de contrato 4.4.9 e inventario de columnas agregadas con origen en la tabla
    return "\n".join(l for l in txt.split("\n") if l.startswith("| ") and re.match(r"\|[^|]*\|\s*%s\s*\|" % tabla, l.replace("→", "→")) or l.startswith("| %s → " % tabla))
def falta(txt):
    res = []
    for n, b in bloques(txt):
        cobertura = fks(b) + "\n" + agregadas(txt, n)
        for c in cols(b):
            if (c.endswith("_id") or c.startswith("source_")) and c not in ("id", "organization_id") and (n, c) not in EXC and not re.search(r"\b%s\b" % re.escape(c), cobertura): res.append((n, c))
    return res
f = falta(S); print("tablas con bloque:", sum(1 for _ in bloques(S)), "| columnas sin FK ni excepción:", f)
ok = []
ok.append(("E1 toda columna *_id/source_* de las tablas nuevas tiene FK o excepción justificada", not f))
# controles negativos: quitar una FK de una copia en memoria debe ser detectado
for tabla, col, patron in [("impact_evaluations", "master_basis_creative_asset_id", r"\| \(organization_id, master_piece_id, master_basis_creative_asset_id[^\n]*\n"),
                           ("publication_attempts", "master_current_copy_version_id", r"\| \(organization_id, master_piece_id, master_current_copy_version_id[^\n]*\n"),
                           ("brief_field_attributions", "brief_id", r"\| \(organization_id, brief_id, brief_version_id\)[^\n]*V20: FK añadida; `brief_id`[^\n]*\n")]:
    mut = re.sub(patron, "", S, count=1);
    mut = "\n".join(l for l in mut.split("\n") if not (l.startswith("| %s → " % tabla) and col in l)); d = (mut != S) and (tabla, col) in falta(mut)
    ok.append(("N %s.%s: al quitar su FK la prueba lo detecta" % (tabla, col), d))
for nom, v in ok: print("%s | %s" % ("PASS" if v else "FAIL", nom))
print("TOTAL pruebas=%d fallos=%d" % (len(ok), sum(1 for _, v in ok if not v))); sys.exit(0 if all(v for _, v in ok) else 1)
