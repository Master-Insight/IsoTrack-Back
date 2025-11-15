Autor: **Gustavo A. Sirtori (Insight Devs)**  
Stack base: **FastAPI + Supabase + React o Astro + Tailwind**  
Objetivo: construir un sistema modular, escalable y de bajo costo para documentación, procesos y calidad empresarial.

---

## ✅ Checkpoint 1 — MVP (Documentos + Procesos + Diagramas)

**Objetivo:** Base sólida para documentación y procesos, multiusuario y multiempresa sobre el esquema Supabase actual.

---

### 🔹 Fase 1.1 — Configuración del entorno (Back + Front)

**Backend (FastAPI):**

- ☐ Crear estructura modular `app/modules/{companies,users,documents,processes,tasks,diagrams,artifact_links}`.
- ☐ Definir `settings.py`, variables `.env` y clientes (`supabase`, `storage`).
- ☐ Replicar enums `user_role`, `document_type`, `document_status`, `diagram_type`, `document_format`, `processes_maturity`, `artifact_entity_type` en migraciones iniciales.
- ☐ Configurar políticas RLS mínimas (`company_id = auth.uid().company_id`).

**Frontend (Astro/React):**

- ☐ Crear proyecto Astro + Tailwind + shadcn/ui.
- ☐ Configurar `VITE_SUPABASE_URL`, `VITE_SUPABASE_KEY`, `VITE_API_URL`.
- ☐ Layout general con header multiempresa, sidebar y branding (`companies.theme`).

🧱 **Entregable:** stack base con login simulado, enums cargados y healthchecks contra Supabase.

---

### 🔹 Fase 1.2 — Módulo de Empresas y Usuarios (Back)

- ☐ Exponer tablas `companies` y `user_profiles` (perfil extendido de `auth.users`).
- ☐ Endpoints `/me`, `/companies`, `/companies/{id}` con `company_id` contextual.
- ☐ Seed inicial (empresa demo + usuarios root/admin) usando `sync_user_profile` trigger.
- ☐ RLS: `select/update` acotado a `company_id`, `insert` solo root/admin.

🧱 **Entregable:** autenticación + contexto empresa funcionando con control de roles `user_role`.

---

### 🔹 Fase 1.3 — Documentos (Back + Front)

**Backend:**

- ☐ Utilizar tablas `documents`, `document_versions`, `document_reads`.
- ☐ CRUD + lógica de versionado: `document_versions.status` (`borrador/aprobado/vigente`), `format` (`pdf/video`).
- ☐ Endpoint `POST /documents/{id}/versions/{version}/read` que registra en `document_reads` con `due_date` opcional.

**Frontend:**

- ☐ Vista “Documentos”: tabla multi-filtro (tipo, estado, etiquetas) + chips `tags`.
- ☐ Formulario “Nuevo documento” con `type`, `category`, `owner_id`, upload a storage (PDF/video) y vista previa (`preview_url`).
- ☐ Vista detalle con versión activa, notas, botón “Marcar leído” y histórico de lecturas.

🧱 **Entregable:** flujo crear → versionar → publicar → leer → acuse guardado en `document_reads`.

---

### 🔹 Fase 1.4 — Procesos, Tareas y vínculos (Back + Front)

**Backend:**

- ☐ CRUD sobre `processes` (maturity, inputs/outputs) y `tasks` (responsible_roles, frequency).
- ☐ Implementar `artifact_links` como matriz de relacionamiento (`from_id/from_type` ↔ `to_id/to_type`).
- ☐ Endpoints `/processes/{id}/links` y `/tasks/{id}/links` para crear/eliminar relaciones (p. ej. proceso ↔ documento ↔ tarea ↔ diagrama).

**Frontend:**

- ☐ Vista “Procesos” (lista + detalle) con secciones: datos generales, tareas asociadas, documentos vinculados.
- ☐ Subvista “Tareas del proceso” editable en línea y estado (`tasks.status`).
- ☐ Modal de vínculos que usa `artifact_links` para seleccionar cualquier artefacto disponible.

🧱 **Entregable:** árbol de procesos y tareas con vínculos cruzados persistidos en `artifact_links`.

---

### 🔹 Fase 1.5 — Diagramas / Organigramas (Front + Back)

**Frontend:**

- ☐ Integrar **React Flow** o librería similar con nodos custom (roles, áreas).
- ☐ Guardar el flujo como JSON (`diagrams.data`) y permitir exportar `svg_export` con branding de `companies.brand_logo`.

**Backend:**

- ☐ Tabla `diagrams` con tipos `diagram_type` (`organigrama`, `flujo`).
- ☐ Endpoints CRUD + `GET /diagrams/{id}/links` para mostrar conexiones con procesos/documentos via `artifact_links`.

🧱 **Entregable:** editor visual funcional con persistencia y vínculos a otros artefactos.

---

### 🔹 Fase 1.6 — Integración y migración

- ☐ Script `import_excel.py` / `import_supabase.py` para cargar hojas CSV (Companies, Users, Documents, Processes, Tasks, Artifact Links).
- ☐ Validar consistencia de `company_id` y deduplicar relaciones antes de insertar en `artifact_links` (trigger `artifact_links_check_references`).
- ☐ Smoke tests end-to-end: crear documento, vincularlo a proceso/tarea, marcar lectura y mostrarlo en diagrama.

🧱 **Entregable Checkpoint 1:** sistema operativo (usuarios, docs, procesos, tareas, organigramas, lecturas, vínculos).

---

## ⚙️ Checkpoint 2 — Versión Mediana (Calidad Lite)

**Objetivo:** incorporar seguimiento de calidad (auditorías, NCR, CAPA) y entrenamiento.

---

### 🔹 Fase 2.1 — Auditorías (Back + Front)

**Backend:**

- ☐ Tablas `audits`, `audit_findings`.
- ☐ Endpoints CRUD y validaciones.

**Frontend:**

- ☐ Vista “Auditorías”: plan anual, agregar hallazgo.
- ☐ Modal de hallazgos con severidad/responsable.

🧱 **Entregable:** registro y visualización de auditorías.

---

### 🔹 Fase 2.2 — No Conformidades y CAPA (Back + Front)

**Backend:**

- ☐ Tablas `ncr`, `capa`.
- ☐ Endpoints CRUD y `/capa/{id}/verify`.

**Frontend:**

- ☐ Vista “CAPA y NCR”: tablero tipo **kanban**.
- ☐ Formularios de acción y verificación.

🧱 **Entregable:** control completo de acciones correctivas.

---

### 🔹 Fase 2.3 — Entrenamiento y competencias (Back + Front)

**Backend:**

- ☐ Tablas `trainings`, `training_assignments`, `training_quizzes`.
- ☐ Endpoints CRUD + `/training-attempts`.

**Frontend:**

- ☐ Vista “Capacitaciones”: mis asignaciones, tests, lecturas.
- ☐ Evaluación interactiva 3–5 preguntas.

🧱 **Entregable:** módulo de formación activo con evaluaciones básicas.

---

### 🔹 Fase 2.4 — Dashboard e indicadores

**Backend:**

- ☐ Endpoint `/reports/overview` con KPIs (lecturas, CAPA, auditorías).

**Frontend:**

- ☐ Dashboard con tarjetas y gráficos (`recharts`).

🧱 **Entregable:** panel de gestión ISO-lite visible al admin.

---

## 🚀 Checkpoint 3 — Versión Pro (Flujos + Analítica + Integraciones)

**Objetivo:** sistema de calidad integral con notificaciones, BI y automatización.

---

### 🔹 Fase 3.1 — Flujos de aprobación multi-etapa (Back + Front)

**Backend:**

- ☐ Tabla `approvals`.
- ☐ Endpoint `/workflow/advance` con control de pasos.

**Frontend:**

- ☐ UI “Aprobaciones pendientes”.
- ☐ Botón “Aprobar / Rechazar”.

🧱 **Entregable:** circuito de aprobación multi-etapa.

---

### 🔹 Fase 3.2 — Notificaciones y automatización

**Backend:**

- ☐ Servicio `notifications_service.py` (Resend / WhatsApp Cloud).
- ☐ Eventos: documento nuevo, CAPA vencida, auditoría próxima.

**Frontend:**

- ☐ Banner de notificaciones internas.
- ☐ Configuración de preferencias.

🧱 **Entregable:** alertas automáticas de eventos clave.

---

### 🔹 Fase 3.3 — Analítica y BI

**Backend:**

- ☐ Tablas `metrics_cache`, `attachments`.
- ☐ Endpoint `/reports/kpis` para BI externo.

**Frontend:**

- ☐ Panel avanzado de KPIs.
- ☐ Gráficos dinámicos y export CSV/PDF.

🧱 **Entregable:** tablero ISO con KPIs y exportables.

---

### 🔹 Fase 3.4 — Multiempresa avanzada y roles raíz

**Backend:**

- ☐ Endpoint `/admin/companies/manage`.
- ☐ Permitir al `root` crear empresas y admins.
- ☐ Refactor de RLS global.

**Frontend:**

- ☐ Vista “Panel raíz”: listado de empresas y botón “Entrar como admin”.

🧱 **Entregable:** sistema SaaS interno multiempresa con control global.

---

## 📅 Cronograma sugerido

| Checkpoint | Fases | Duración | Ámbito |
|-------------|--------|----------|--------|
| ✅ MVP | 1.1 → 1.6 | 4–6 semanas | Base de procesos y docs |
| ⚙️ Mediana | 2.1 → 2.4 | 5–7 semanas | Calidad lite y dashboard |
| 🚀 Pro | 3.1 → 3.4 | 6–8 semanas | Automatización y BI |

---

## 🧩 Distribución de esfuerzo

- **Back y DB:** FastAPI + Supabase → 60%
- **Front (Astro/React):** UI funcional → 40%
- **Docs:** `docs/plan_fases_detallado.md` actualizado tras cada checkpoint
- **Hosting:** Supabase (DB/Auth/Storage) + Vercel (Front)
