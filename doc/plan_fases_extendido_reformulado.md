
# 📘 Plan de Desarrollo — IsoTrack (Extendido y Reformulado)
Versión centrada en flujos visuales como núcleo del sistema.

---

# ✅ Checkpoint 1 — MVP (Documentos + Procesos + Diagramas)
*(se mantiene exactamente igual al archivo original)*

➡ Este checkpoint representa el sistema base de documentos, procesos, tareas y primeros diagramas.

---

# 🟦 Checkpoint 2 — Flujos Visuales + Migración a React
Transformación del sistema para adoptar **ReactFlow** + migración completa del frontend.

## 🎯 Objetivo General
Convertir IsoTrack en una plataforma cuya navegación central sea el **flujo visual**, reemplazando la lógica basada en módulos por un enfoque visual, dinámico y contextual.

---

## 2.1 — Migración del Frontend: Astro → React
### Incluye:
- Creación del nuevo proyecto **React + Vite + Tailwind**
- Migración de:
  - `AppShell`
  - `AuthProvider`
  - Layouts
  - Componentes de Documentos / Procesos / Tareas
- Reemplazo de islands Astro por componentes React
- Creación del sistema de routing (TanStack Router recomendado)
- Manejo de estado global (Zustand o Context API)

---

## 2.2 — Nuevo módulo Backend: Flujos (Flow / Nodes / Edges)

### Tablas nuevas:
- **flows**
- **flow_nodes**
- **flow_edges**

### Modelo de un nodo:
```
Node {
  id: string
  label: string
  type: "step" | "decision" | "event" | "process" | "integration"
  system?: string

  metadata: {
    notes?: string
    artifacts?: [{ type, id }]
    roles?: string[]
    userAssigned?: string
    visibleFor?: string[]
  }

  position: { x, y }
}
```

### Endpoints nuevos:
- `GET /flows`
- `POST /flows`
- `POST /flows/import`
- `POST /flows/{id}/nodes`
- `POST /flows/{id}/edges`

---

## 2.3 — Visualizador ReactFlow
Implementación del canvas visual:
- Nodos custom
- Conexiones interactivas
- Minimapa
- Panel lateral con:
  - Información del nodo
  - Documentos
  - Procesos
  - Tareas
  - Notas
  - Roles responsabiles

---

## 2.4 — Editor de Flujos (modo edición)
- Crear/editar nodos
- Conectar edges
- Drag & drop
- Guardado de layout
- Importación desde CSV

---

## 2.5 — Clasificación de flujos
- **principales**
- **auxiliares**
- **por área**
- visibilidad por rol

---

## 2.6 — Vista “Mis flujos”
- Muestra solo flujos donde el usuario participa
- Resalta nodos asignados
- Estados de tareas/documentos por nodo

---

# 🟩 Checkpoint 3 — Calidad Lite Basada en Flujos
Antes se hacía con módulos separados.  
Ahora **todo es flujo**.

## 3.1 — Auditorías como flujos visuales
Nodos:
- planificación
- ejecución
- hallazgos
- revisión
- cierre

## 3.2 — NCR / CAPA como flujos
- detección
- análisis causa raíz
- acción correctiva
- verificación
- cierre

Cada etapa = nodo con evidencia adjunta.

---

## 3.3 — Entrenamientos como flujos
Nodos = módulos o pasos de capacitación:
- lectura
- video
- evaluación
- cierre

---

## 3.4 — Dashboard Lite
KPIs:
- % avance por flujo
- NCR abiertas
- CAPA en verificación
- Auditorías activas

---

# 🟧 Checkpoint 4 — Editor de Contenidos
Nuevo módulo para crear contenido desde nodos.

Incluye:
- Editor WYSIWYG (TipTap/Lexical)
- Subida de PDF
- Creación de:
  - documentos
  - procesos
  - tareas
- Versionado desde el nodo
- Previsualización integrada

---

# 🚀 Checkpoint 5 — Pro (Automatización + BI + Integraciones Avanzadas)
Extensión del sistema visual:

- Workflows automáticos entre nodos
- Aprobaciones multi-etapa
- Notificaciones internas y externas
- Exportación a BI
- Webhooks entre flujos y sistemas externos
- Multiempresa avanzado

---

# 🧩 Conclusión
Este plan reformulado coloca a **ReactFlow** y los **flujos visuales** como el centro conceptual, funcional y técnico de IsoTrack.
