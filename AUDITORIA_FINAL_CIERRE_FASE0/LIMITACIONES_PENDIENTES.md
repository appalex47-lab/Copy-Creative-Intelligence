# Limitaciones pendientes
1. Sin custodio externo del hash → verificación no operativa hasta configurarlo.
2. Guarda falsa + hash controlado por el atacante (E2/M) — estructural.
3. AG-18: clon físico indistinguible; endpoints aprobados sólo mitigan.
4. stdin no soportado.
5. Operadores no calificados: protección sólo por chequeo de search_path.
6. Pooler simulado; Supabase no validado (TEMP, pg_control_system, PGOPTIONS).
7. 05A/05B dependientes; batería no paralelizable; orden de los 22 pasos no probado independiente.
8. 5 controles V26 NO VERIFICADO, 4 PARCIAL, LR-22 parcialmente resuelta; 26 PARTIAL previos intactos.
9. Listas allow/deny de DEV/PROD vacías (no se inventan identificadores).
