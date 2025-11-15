# Plan de Desarrollo — Sistema de Gestión de Documentos y Procesos (Estilo ISO)

Autor: **Gustavo A. Sirtori (Insight Devs)**  
Stack base: **FastAPI + Supabase + React o Astro + Tailwind**  
Objetivo: construir un sistema modular, escalable y de bajo costo para documentación, procesos y calidad empresarial.

---

## 🔀 Enfoque de desarrollo por fases

| Fase | Nombre | Objetivo principal | Nivel de madurez |
|------|---------|--------------------|------------------|
| ✅ **Checkpoint 1** | **MVP — Documentos y Procesos** | Digitalizar documentación, tareas y organigramas. | Operativo mínimo |
| ⚙️ **Checkpoint 2** | **Versión Mediana — Calidad Lite** | Agregar auditorías, CAPA y entrenamiento básico. | Estructura ISO básica |
| 🚀 **Checkpoint 3** | **Versión Pro — Integración Total** | Flujo completo de calidad, permisos avanzados y analítica. | Nivel ISO completo |

---

## 🧠 0. Conceptos Base

### Multiempresa y costos

Podés desplegar **una única app frontend** y **distintas bases de datos Supabase**:

- Si las empresas son **independientes** (no comparten datos ni usuarios):  
  → conviene **una base Supabase por empresa** (más simple de aislar, menos RLS).  
- Si querés **gestión centralizada** (ver todas bajo un root global):  
  → una **única base con campo `company_id`** en todas las tablas y políticas RLS.  

💡 *Costo*:  
Supabase tiene plan gratuito + pago por uso. Podés repartirlo proporcionalmente según consumo (almacenamiento, invocaciones).  
En ambos casos, el **frontend es el mismo**, cambiando el `.env` o `api_url`.

---

## 💡 1. Comparativa React vs Astro

| Criterio | Astro | React (Vite/Next) |
|-----------|--------|------------------|
| **Rendimiento inicial** | Excelente (SSG/SSR híbrido) | Bueno (depende de SPA o SSR) |
| **Curva de complejidad** | Baja (componentes HTML+React opcional) | Media (hooks, context, router) |
| **Ideal para** | Portales documentales, contenido, dashboards simples | Apps interactivas, formularios dinámicos |
| **Futuro escalable (Pro)** | Posible, pero más trabajo para estados complejos | Más flexible para app compleja (training, CAPA, auditorías interactivas) |
| **Recomendación** | 🟢 **Astro para MVP + Medium** | 🔵 **React puro (Vite/Next) para Pro** |

✅ **Plan:** arrancar con **Astro + React islands** (te beneficia en SEO, carga rápida y reuso) y migrar gradualmente a full React si el nivel Pro lo exige.

---

## 📍 2. Checkpoint 1 — MVP (Documentos + Procesos + Diagramas)

### 🎯 Objetivos

- Tener estructura básica de documentación y procesos.  
- Permitir acceso multiusuario con roles.  
- Mostrar documentos (PDF, PPT, video) y marcar lectura.  
- Crear organigramas y flujos con branding.

---

### 🗃 Modelo de Datos (Supabase / Postgres)

El MVP ya cuenta con un esquema completo en Supabase. Incluye enums específicos y tablas ligadas por `company_id` para mantener el multi-tenant.

**Enums principales:**

```sql
create type user_role as enum ('root','admin','editor','user');
create type document_type as enum ('POE','Instructivo','Política','Plantilla','Presentación','Video');
create type document_status as enum ('borrador','aprobado','publicado','vigente','en_revision');
create type diagram_type as enum ('organigrama','flujo');
create type document_format as enum ('pdf','video');
create type processes_maturity as enum ('establecido','en_mejora','critico');
create type artifact_entity_type as enum ('document','process','task','diagram');
```

**Tablas actuales:**

```sql
-- Empresas
create table companies (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  brand_logo text,
  theme jsonb,
  created_at timestamptz default now()
);

-- Usuarios (perfil extendido del usuario de auth)
create table user_profiles (
  id uuid primary key references auth.users(id),
  company_id uuid references companies(id),
  email text unique not null,
  role user_role default 'user',
  full_name text,
  position text,
  created_at timestamptz default now()
);

-- Documentos y metadatos
create table documents (
  id uuid primary key default uuid_generate_v4(),
  company_id uuid references companies(id),
  code text,
  title text not null,
  type document_type not null,
  process_id uuid null,
  owner_id uuid references user_profiles(id),
  active boolean default true,
  created_at timestamptz default now(),
  description varchar,
  category varchar,
  tags text[],
  "updatedAt" timestamptz default now(),
  "nextReviewAt" timestamptz
);

-- Versiones
create table document_versions (
  id uuid primary key default uuid_generate_v4(),
  document_id uuid references documents(id),
  version varchar,
  status document_status default 'borrador',
  file_url text,
  external_url text,
  notes text,
  approved_by uuid references user_profiles(id),
  approved_at timestamptz,
  created_at timestamptz default now(),
  format document_format,
  preview_url text
);

-- Lecturas
create table document_reads (
  id uuid primary key default uuid_generate_v4(),
  document_id uuid references documents(id),
  user_id uuid references user_profiles(id),
  version varchar,
  read_at timestamptz,
  due_date date
);

-- Procesos y tareas
create table processes (
  id uuid primary key default uuid_generate_v4(),
  company_id uuid references companies(id),
  code text,
  name text,
  area text,
  owner_id uuid references user_profiles(id),
  objective varchar,
  inputs text[],
  outputs text[],
  maturity processes_maturity,
  updated_at timestamptz default now(),
  created_at timestamptz default now(),
  description varchar
);

create table tasks (
  id uuid primary key default uuid_generate_v4(),
  company_id uuid references companies(id),
  code text,
  name text,
  purpose text,
  scope text,
  frequency text,
  responsible_roles text[],
  owner_id uuid references user_profiles(id),
  status text,
  updated_at timestamptz default now()
);

-- Diagramas (organigramas / flujos)
create table diagrams (
  id uuid primary key default uuid_generate_v4(),
  company_id uuid references companies(id),
  title text,
  type diagram_type not null
  data jsonb,
  svg_export text
);


-- Relaciones entre artefactos (documento ↔ proceso ↔ tarea ↔ diagrama)
create table artifact_links (
  id uuid primary key default uuid_generate_v4(),
  company_id uuid references companies(id),
  from_id uuid not null,
  from_type artifact_entity_type not null,
  to_id uuid not null,
  to_type artifact_entity_type not null,
  relation_type text,
  created_at timestamptz default now()
);
```

> 🔗 `artifact_links` permite conectar cualquier combinación de artefactos del MVP (por ejemplo, relacionar un documento con el proceso al que pertenece o con un diagrama específico) y facilita las vistas cruzadas.

---

### ⚙️ API (FastAPI)

**Endpoints clave (esqueleto):**

```python
# /app/modules/documents/routes.py
@router.get("/documents")
def list_documents(current_user=Depends(auth_user)):
    return service.list_documents(current_user)

@router.post("/documents")
def create_document(payload: DocumentCreate, current_user=Depends(require_role(["admin","editor"]))):
    return service.create_document(payload, current_user)

@router.post("/documents/{id}/versions")
def add_version(document_id: str, payload: DocumentVersionCreate, current_user=Depends(require_role(["admin","editor"]))):
    return service.add_version(document_id, payload, current_user)

@router.post("/documents/{id}/reads/ack")
def mark_read(document_id: str, current_user=Depends(require_role(["user","editor","admin"]))):
    return service.mark_read(document_id, current_user)
```

**Otros módulos MVP:**

- `/processes` y `/tasks`
- `/diagrams` (guardar y exportar)
- `/companies/config`
- `/auth/me` (perfil y rol actual)

---

### 🧱 Entregables del Checkpoint 1

- ✅ Estructura Supabase con RLS por `company_id`.  
- ✅ API FastAPI con CRUD Documentos, Procesos, Diagramas.  
- ✅ Front (Astro + Tailwind) con login, listado de documentos, vista de proceso, editor de organigramas.  
- ✅ Script Python para importar tu Excel existente.

---

## ⚙️ 3. Checkpoint 2 — Versión Mediana (Calidad Lite)

### 🎯 Objetivos

- Estructura base de auditorías y hallazgos.  
- No conformidades (NCR) y CAPA básicas.  
- Entrenamiento y competencias (lecturas + mini evaluaciones).  
- Dashboards simples con KPIs.

---

### 🗃 Modelo de Datos (Extensión)

```sql
-- Auditorías
create table audits (
  id uuid primary key default uuid_generate_v4(),
  company_id uuid references companies(id),
  year int,
  scope text,
  lead_auditor uuid references user_profiles(id),
  status text check (status in ('planificada','en_progreso','cerrada')) default 'planificada',
  planned_on date
);

create table audit_findings (
  id uuid primary key default uuid_generate_v4(),
  audit_id uuid references audits(id),
  description text,
  severity text check (severity in ('menor','mayor','observación')) default 'menor'
);

-- NCR / CAPA
create table ncr (
  id uuid primary key default uuid_generate_v4(),
  company_id uuid references companies(id),
  description text,
  detected_on date,
  responsible_id uuid references user_profiles(id),
  status text check (status in ('abierta','en_accion','verificacion','cerrada')) default 'abierta'
);

create table capa (
  id uuid primary key default uuid_generate_v4(),
  ncr_id uuid references ncr(id),
  root_cause text,
  action text,
  owner_id uuid references user_profiles(id),
  due_date date,
  effectiveness_verified bool default false,
  verified_at timestamptz
);

-- Entrenamiento
create table trainings (
  id uuid primary key default uuid_generate_v4(),
  company_id uuid references companies(id),
  title text,
  description text
);

create table training_assignments (
  id uuid primary key default uuid_generate_v4(),
  training_id uuid references trainings(id),
  document_id uuid null,
  user_id uuid null,
  role_target text null,
  due_date date,
  completed_at timestamptz
);

create table training_quizzes (
  id uuid primary key default uuid_generate_v4(),
  training_id uuid references trainings(id),
  data jsonb
);
```

---

### ⚙️ API (FastAPI)

```python
# /modules/audits/routes.py
@router.post("/audits")
def create_audit(payload: AuditCreate, current_user=Depends(require_role(["admin"]))):
    return service.create_audit(payload, current_user)

@router.post("/audit-findings")
def create_finding(payload: AuditFindingCreate, current_user=Depends(require_role(["editor","admin"]))):
    return service.create_finding(payload, current_user)

# /modules/capa/routes.py
@router.post("/ncr")
def create_ncr(payload: NCRCreate, current_user=Depends(require_role(["editor","admin"]))):
    return service.create_ncr(payload, current_user)

@router.post("/capa")
def create_capa(payload: CAPACreate, current_user=Depends(require_role(["editor","admin"]))):
    return service.create_capa(payload, current_user)
```

---

### 🧱 Entregables del Checkpoint 2

- ✅ Base de datos extendida con Auditorías, CAPA y Entrenamiento.  
- ✅ API y servicios asociados.  
- ✅ UI para NCR y CAPA (tablero kanban básico).  
- ✅ Dashboard inicial con métricas (lecturas pendientes, CAPA abiertas, etc.).  

---

## 🚀 4. Checkpoint 3 — Versión Pro (Completa / Analítica / Integración)

### 🎯 Objetivos

- Flujos completos de aprobación multi-etapa.  
- Auditorías con seguimiento de acciones.  
- Competencias + tests con calificaciones.  
- Integración con BI externo (Metabase, Looker o GA4).  
- Roles avanzados (multiempresa raíz + delegados).  

---

### 🗃 Modelo de Datos (Ampliado)

- `approvals` → flujo multi-etapa (`step`, `role_required`, `signed_by`, `signed_at`)  
- `notifications` → colas de avisos por evento (documento, CAPA, vencimiento)  
- `metrics_cache` → almacenamiento de KPIs diarios/semanales  
- `attachments` → repositorio general de archivos con `entity_type` + `entity_id`

---

### ⚙️ API (FastAPI)

- `/workflow` → engine para cambio de estado con validaciones.  
- `/notifications` → correo o webhook (Resend, WhatsApp).  
- `/reports/*` → endpoints agregados para BI.  

---

### 🧱 Entregables del Checkpoint 3

- ✅ Sistema 100% multiempresa y multirol.  
- ✅ Auditorías integradas con CAPA y verificación.  
- ✅ Entrenamiento con resultados y reportes.  
- ✅ Panel de métricas y cumplimiento ISO-like.  
- ✅ Integración con correo/BI externos.  

---

## 💰 Plan de Recupero de Costo

| Modelo | Descripción | Cuándo aplicarlo |
|---------|--------------|------------------|
| **Costo compartido** | Cada empresa paga un % del hosting (Supabase/Vercel). | Si se hospedan bases separadas. |
| **SaaS interno** | App única con multiempresa y roles administrados. | Si querés escalar a más clientes. |
| **Servicio Insight Devs** | Te convertís en proveedor del sistema. | Fase Pro (licencia mensual o mantenimiento). |

---

## 📅 Resumen visual por fases

```
[Checkpoint 1] MVP
 ├── Documentos (versionado, lectura)
 ├── Procesos / Tareas
 └── Diagramas / Organigramas

[Checkpoint 2] Versión Mediana
 ├── Auditorías (estructura)
 ├── NCR / CAPA lite
 ├── Entrenamiento / Lecturas / Mini test
 └── Dashboard básico

[Checkpoint 3] Versión Pro
 ├── Flujos de aprobación multi-etapa
 ├── Auditorías integradas y métricas
 ├── Competencias + evaluaciones
 ├── Integración con BI / Resend
 └── Multiempresa avanzada
```
