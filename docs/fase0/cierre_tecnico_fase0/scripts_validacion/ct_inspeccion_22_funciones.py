#!/usr/bin/env python3
# Inspección estática (AST) de las 22 funciones de ejecución. NO ejecuta ni modifica modelo_estructural.py. Uso: python3 -I -B ct_inspeccion_22_funciones.py <modelo_estructural.py> [salida.json]
import ast, sys, json, hashlib, builtins
p = sys.argv[1]; src = open(p, encoding="utf-8").read(); tree = ast.parse(src); L = src.split("\n")
F = ["pruebas_guarda","pruebas_atomicidad","correr_mutaciones_rechazo","correr_adversariales","correr_escenarios","correr_mutaciones_k47","correr_mutaciones_resoluciones","correr_mutaciones_assets","correr_positivos_arte","correr_mutaciones_k45","correr_mutaciones_cadena","correr_adversariales_cadena","correr_mutaciones_atribucion","pruebas_atomicidad14","pruebas_E14","correr_mutaciones_av","correr_mutaciones_cf","correr_mutaciones_ac","correr_positivos15","correr_adversariales15","pruebas_atomicidad15","correr_mutaciones_modelo14"]
defs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
mod_names = {}
for n in tree.body:
    if isinstance(n, (ast.Assign,)):
        for t in n.targets:
            if isinstance(t, ast.Name): mod_names[t.id] = n.lineno
    elif isinstance(n, (ast.FunctionDef, ast.ClassDef)): mod_names[n.name] = n.lineno
def prof(n):
    calls, names, attrs = set(), set(), set(); trys = excs = asserts = raises = loops = 0; glob_writes = set(); deep = False
    for x in ast.walk(n):
        if isinstance(x, ast.Call):
            f = x.func
            if isinstance(f, ast.Name): calls.add(f.id)
            elif isinstance(f, ast.Attribute): attrs.add(f.attr)
        if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load): names.add(x.id)
        if isinstance(x, ast.Try): trys += 1; excs += sum(1 for h in x.handlers if h.type is None or (isinstance(h.type, ast.Name) and h.type.id in ("Exception", "BaseException")))
        if isinstance(x, ast.Assert): asserts += 1
        if isinstance(x, ast.Raise): raises += 1
        if isinstance(x, (ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)): loops += 1
        if isinstance(x, ast.Global): glob_writes |= set(x.names)
    deep = "deepcopy" in attrs
    dep_mod = sorted(c for c in (calls | names) if c in mod_names and c != n.name)
    return dict(calls=sorted(calls), attrs=sorted(attrs), dep_mod=dep_mod, try_blocks=trys, except_amplio=excs, asserts=asserts, raises=raises, bucles=loops, global_writes=sorted(glob_writes), deepcopy=deep)
out = []
for f in F:
    n = defs[f]; end = n.end_lineno; body = "\n".join(L[n.lineno - 1:end])
    pr = prof(n); doc = ast.get_docstring(n)
    out.append(dict(funcion=f, linea_ini=n.lineno, linea_fin=end, n_lineas=end - n.lineno + 1, args=[a.arg for a in n.args.args], docstring=doc, sha256_fuente=hashlib.sha256(body.encode()).hexdigest()[:16], **pr))
if len(sys.argv) > 2: json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for o in out: print("%-34s L%-5d-%-5d n=%-4d args=%s try=%d exc_amplio=%d raises=%d deep=%s deps=%s" % (o["funcion"], o["linea_ini"], o["linea_fin"], o["n_lineas"], o["args"], o["try_blocks"], o["except_amplio"], o["raises"], o["deepcopy"], o["dep_mod"][:7]))
