#!/usr/bin/env python3
# (1) Cataloga TODOS los bloques `except Exception` de modelo_estructural.py (AST) y clasifica su efecto sobre el resultado; (2) demuestra por ejecución que las tres ramas muertas
# (`if False`, `if True`) no cambian ningún resultado, comparando la salida de las funciones afectadas con y sin ellas (copia en memoria; el original NO se modifica).
# Uso: python3 -I -B ct_catalogo_except_y_ramas_muertas.py <modelo_estructural.py> <salida_catalogo.csv>
import ast, sys, csv, types, importlib.util
sys.dont_write_bytecode = True
ruta, out = sys.argv[1], sys.argv[2]; src = open(ruta, encoding="utf-8").read(); T = ast.parse(src)
padres = {}
for n in ast.walk(T):
    for c in ast.iter_child_nodes(n): padres[c] = n
def func(n):
    while n in padres:
        n = padres[n]
        if isinstance(n, ast.FunctionDef): return n.name
    return "(módulo)"
filas = []
for n in ast.walk(T):
    if isinstance(n, ast.ExceptHandler) and (n.type is None or (isinstance(n.type, ast.Name) and n.type.id == "Exception")):
        f = func(n); h = " ".join((ast.get_source_segment(src, b) or "").strip() for b in n.body)[:140]
        riesgo = f == "_baterias14"
        if n.type is None: cls = "REVISAR (except desnudo)"
        elif riesgo: cls = "RIESGO_TECNICO: la excepción se registra como fallo ('EXC', False) y en correr_mutaciones_modelo14 un fallo cuenta como DETECCIÓN (podría ser detección espuria por caída)"
        elif "True" in h: cls = "REVISAR (el manejador asigna True)"
        else: cls = "SEGURO: la excepción deja el caso en FAIL/ERROR (nunca PASS)"
        filas.append((n.lineno, f, h, cls))
filas.sort()
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["Linea", "Funcion_envolvente", "Manejador", "Clasificacion"]); w.writerows(filas)
print("bloques except Exception: %d ; SEGURO=%d ; RIESGO_TECNICO=%d ; REVISAR=%d" % (len(filas), sum(f[3].startswith("SEGURO") for f in filas), sum(f[3].startswith("RIESGO") for f in filas), sum(f[3].startswith("REVISAR") for f in filas)))
# (2) ramas muertas: equivalencia por ejecución
def modulo(texto, nombre):
    m = types.ModuleType(nombre); m.__file__ = ruta; exec(compile(texto, ruta, "exec"), m.__dict__); return m
reemp = [('x0.E("ca") if False else calcular_E_verificado(m0, "ca")', 'calcular_E_verificado(m0, "ca")'), ('(ev["source_root_asset_id"] if False else ev["source_root_asset_version_id"], ', '(ev["source_root_asset_version_id"], '), (' if True else False\n            det_campos', '\n            det_campos')]
src2 = src
for a, b in reemp:
    c = src2.count(a); print("rama muerta localizada %d vez: %s" % (c, a[:60]));
    assert c == 1, "patrón no único"; src2 = src2.replace(a, b)
M0 = modulo(src, "m_orig"); M1 = modulo(src2, "m_sin_ramas")
ok = True
for fn in ("correr_mutaciones_rechazo", "correr_positivos_arte", "correr_adversariales15"):
    a = repr(getattr(M0, fn)()); b = repr(getattr(M1, fn)()); ok &= a == b; print("%s: resultado idéntico con y sin la rama muerta: %s" % (fn, a == b))
print("EQUIVALENCIA_RAMAS_MUERTAS=%s" % ok)
