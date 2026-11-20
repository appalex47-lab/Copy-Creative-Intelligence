#!/usr/bin/env python3
"""V20 (H-07): prueba EXTERNA y de solo lectura de independencia del auditor respecto del motor.
1) Estático: cierre transitivo de llamadas del auditor independiente; no debe invocar métodos de la clase Motor ni instanciarla.
2) Dinámico: durante cada llamada al auditor, TODOS los métodos del Motor que calculan resultados se sustituyen por funciones que lanzan excepción;
   los casos adversariales/cadena/E14 deben dar el mismo resultado que sin sustituir (si el auditor usara el motor, fallaría).
3) Control: la sustitución realmente lanza si algo llama al motor.
Uso: python3 -I este.py <dir herramientas>"""
import ast, importlib.util, os, sys
sys.dont_write_bytecode = True
H = sys.argv[1]; sys.path.insert(0, H)
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); sys.modules[n] = m; s.loader.exec_module(m); return m
V = load("verificar_expediente", os.path.join(H, "verificar_expediente.py")); MS = load("modelo_estructural_i", os.path.join(H, "modelo_estructural.py"))
res = []
def chk(nom, ok): res.append(ok); print("%s | %s" % ("PASS" if ok else "FAIL", nom))
t = ast.parse(open(os.path.join(H, "modelo_estructural.py"), encoding="utf-8").read())
fn = {n.name: n for n in t.body if isinstance(n, ast.FunctionDef)}
motor = {m.name for c in t.body if isinstance(c, ast.ClassDef) and c.name == "Motor" for m in c.body if isinstance(m, ast.FunctionDef)}
AUD = ["auditar", "auditar_E", "cadena_identidad_independiente", "validar_resolucion_independiente"]
def callees(f):
    o, a = set(), set()
    for n in ast.walk(f):
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name): o.add(n.func.id)
            elif isinstance(n.func, ast.Attribute): a.add(n.func.attr)
    return o, a
seen, stack, attrs, inst = set(), list(AUD), set(), False
while stack:
    k = stack.pop()
    if k in seen or k not in fn: continue
    seen.add(k); o, a = callees(fn[k]); attrs |= a; inst |= ("Motor" in o); stack += [x for x in o if x in fn]
print("cierre del auditor independiente:", ", ".join(sorted(seen)))
chk("S1 el auditor no invoca ningún método de la clase Motor (cierre transitivo: %s)" % (sorted(attrs & motor) or "ninguno"), not (attrs & motor))
chk("S2 el auditor no instancia Motor", not inst)
# Dinámico
Mc = MS.Motor; calls = {"n": 0, "aud": 0}; orig = {}
def boom(*a, **k): calls["n"] += 1; raise RuntimeError("el auditor llamó al motor")
CALC = [n for n in motor if not n.startswith("__") and n not in ("nid", "tick")]
def con_motor_roto(f):
    def w(*a, **k):
        calls["aud"] += 1; guard = {}
        for n in CALC:
            if callable(getattr(Mc, n, None)): guard[n] = Mc.__dict__[n]; setattr(Mc, n, boom)
        try: return f(*a, **k)
        finally:
            for n, v in guard.items(): setattr(Mc, n, v)
    return w
def run(): return [bool(x["ok"]) if "ok" in x else bool(x.get("det")) for x in MS.correr_adversariales()] + [bool(x["ok"]) if "ok" in x else bool(x.get("det")) for x in MS.correr_adversariales_cadena()] + [bool(x["ok"]) if "ok" in x else bool(x.get("det")) for x in MS.correr_adversariales15()]
base = run()
for nom in AUD: orig[nom] = getattr(MS, nom); setattr(MS, nom, con_motor_roto(orig[nom]))
try: roto = run()
except Exception as e: roto = None; print("excepción:", e)
finally:
    for nom in AUD: setattr(MS, nom, orig[nom])
chk("D1 adversariales (%d casos, motor forzado) dan el mismo resultado con TODOS los métodos del motor rotos durante el auditor" % len(base), roto == base and all(base))
chk("D3 el auditor se invocó realmente durante la prueba (invocaciones = %d > 0)" % calls["aud"], calls["aud"] > 0)
chk("D2 el auditor no llamó al motor ni una vez (llamadas al stub = %d)" % calls["n"], calls["n"] == 0)
# Control: el stub sí detecta una llamada
guard = {n: Mc.__dict__[n] for n in CALC if callable(getattr(Mc, n, None))}
try:
    for n in guard: setattr(Mc, n, boom)
    try: m = Mc(); m.calcular_E("x"); ctrl = False
    except Exception: ctrl = True
finally:
    for n, v in guard.items(): setattr(Mc, n, v)
chk("C1 control negativo: llamar a un método del motor roto lanza excepción (la prueba sí detectaría dependencia)", ctrl)
print("TOTAL pruebas=%d fallos=%d" % (len(res), res.count(False))); sys.exit(1 if False in res else 0)
