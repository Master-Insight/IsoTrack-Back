Autor: **Gustavo A. Sirtori (Insight Devs)**  
Stack base: **FastAPI + Supabase + React o Astro + Tailwind**  
Objetivo: construir un sistema modular, escalable y de bajo costo para documentación, procesos y calidad empresarial.

---

## ✅ Checkpoint 1 — MVP (Documentos + Procesos + Diagramas)

**Objetivo:** Base sólida para documentación y procesos, multiusuario y multiempresa.

---

### 🔹 Fase 1.1 — Configuración del entorno (Back + Front)

**Backend (FastAPI):**
- ☐ Crear estructura modular `app/modules/{documents,processes,diagrams,companies,auth}`.
- ☐ Definir `settings.py` y variables `.env`.
- ☐ Configurar cliente Supabase y RLS policies mínimas.

**Frontend (Astro/React):**
- ☐ Crear proyecto Astro.
- ☐ Instalar Tailwind y shadcn/ui.
- ☐ Configurar `VITE_API_URL` y `.env`.
- ☐ Layout general con header, sidebar y branding.

🧱 **Entregable:** stack base con login simulado y endpoints de prueba.

---

### 🔹 Fase 1.2 — Módulo de Empresas y Usuarios (Back)

- ☐ Crear tablas `companies`, `user_profiles`.
- ☐ Endpoints `/me`, `/companies`, `/companies/{id}`.
- ☐ RLS: usuarios ven solo su `company_id`.
- ☐ Seeds iniciales (1 empresa + admin/user).

🧱 **Entregable:** autenticación + contexto empresa funcionando.

---

### 🔹 Fase 1.3 — Documentos (Back + Front)

**Backend:**
- ☐ Tablas: `documents`, `document_versions`, `document_reads`.
- ☐ Endpoints CRUD + lógica de versionado.

**Frontend:**
- ☐ Vista “Documentos”: tabla, filtros, búsqueda.
- ☐ Formulario “Nuevo documento”.
- ☐ Vista detalle con PDF/video y botón “Marcar leído”.

🧱 **Entregable:** flujo crear → publicar → leer → acuse guardado.

---

### 🔹 Fase 1.4 — Procesos y Tareas (Back + Front)

**Backend:**
- ☐ Tablas `processes`, `tasks`, `links_process_artifacts`.
- ☐ Endpoints CRUD.

**Frontend:**
- ☐ Vista “Procesos” (lista y detalle).
- ☐ Subvista “Tareas del proceso”.
- ☐ Relación visible con documentos.

🧱 **Entregable:** árbol de procesos con vínculos a documentos.

---

### 🔹 Fase 1.5 — Diagramas / Organigramas (Front + Back opcional)

**Frontend:**
- ☐ Integrar **React Flow**.
- ☐ Guardar flujo en JSON y exportar SVG/PNG con branding.

**Backend:**
- ☐ Tabla `diagrams`.
- ☐ Endpoints CRUD.

🧱 **Entregable:** editor visual funcional.

---

### 🔹 Fase 1.6 — Integración y migración

- ☐ Script `import_excel.py` para cargar hojas (Procesos, Tareas, Docs, Relaciones).
- ☐ Pruebas de vinculación completa.

🧱 **Entregable Checkpoint 1:** sistema operativo (usuarios, docs, procesos, organigramas, lecturas).

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
