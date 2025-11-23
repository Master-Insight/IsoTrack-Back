
# 📗 Plan QMS — Reformulado (Basado 100% en Flujos Visuales)

Este documento reemplaza la estructura ISO tradicional por un concepto moderno donde **cada proceso, cada etapa QMS y cada evidencia** se representa mediante **flujos visuales interactivos**.

---

# 🔵 1. QMS como conjunto de flujos

## Cada proceso ISO se convierte en un flujo:
- Auditorías internas
- No conformidades
- CAPA
- Acciones de mejora
- Formación y competencias
- Gestión documental
- Procesos operativos
- Seguridad y ambiente (si aplica)

---

# 🔵 2. Estructura general de un flujo QMS
Un flujo QMS contiene nodos con:

```
Node {
  label
  state (abierto/en curso/completado)
  roles responsables
  documentos vinculados
  evidencias
  checklist
  notas
  visibilidad por rol
}
```

---

# 🔵 3. Auditorías internas — como flujo visual
Nodos ejemplos:
- Planificación
- Ejecución
- Hallazgos
- Análisis
- Revisión directiva
- Cierre

Cada hallazgo → evidencia adjunta.

---

# 🔵 4. NCR — como flujo visual
Nodos:
- Detección
- Registro
- Análisis causa raíz
- Acción inmediata
- Acciones correctivas
- Verificación
- Cierre

---

# 🔵 5. CAPA — como flujo visual
Nodos:
- Planificación
- Ejecución
- Seguimiento
- Verificación de efectividad
- Cierre

---

# 🔵 6. Formación — como flujo
Nodos:
- Módulo 1
- Módulo 2
- Video
- Evaluación
- Validación final

---

# 🔵 7. Roles y visibilidad por nodo
Cada nodo define:
- `roles` responsables
- `visibleFor` (roles que pueden verlo)
- `userAssigned` si corresponde

---

# 🔵 8. Evidencias por nodo
Cada nodo puede contener:
- Documentos
- Imágenes
- PDFs
- Enlaces
- Notas
- Checklists

---

# 🔵 9. Integración con artifact_links
No se crea un módulo nuevo.  
Se reutiliza el sistema existente de `artifact_links` para asociar:

- documentos
- procesos
- tareas
- otros flujos

---

# 🔵 10. Trazabilidad
Cada nodo registra:
- cambios
- usuario
- fecha
- estado
- adjuntos
- decisiones tomadas

---

# 🔵 11. Vista general del QMS
Se representa mediante:
- Lista de flujos QMS
- Dashboard de avance y cumplimiento
- Accesos directos por área o rol

---

# 📌 Conclusión
El QMS deja de ser un conjunto de módulos dispersos y se convierte en un sistema **visual, interactivo, trazable y modular**, donde cada elemento ISO se representa como un flujo o como un nodo dentro de uno.
