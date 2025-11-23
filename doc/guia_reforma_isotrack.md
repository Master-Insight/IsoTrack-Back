# Guía de Reformulación de IsoTrack: Flujos Visuales como Núcleo del Sistema

## Objetivo General
Reemplazar completamente la estructura tradicional basada en documentos estáticos (`plan_fases_extendido.md` y `plan_fases_qms.md`) por un **sistema centrado en flujos visuales** utilizando **React Flow** como eje de navegación, representación, documentación y trazabilidad.

Esta guía sirve como:
- Documento de diseño conceptual
- Plan de migración
- Prompt base para futuras consultas y desarrollos
- Base para nuevos colaboradores del proyecto

---

# 1. Cambios conceptuales generales

## Antes:
- El proyecto se estructuraba en fases textuales.
- Los procesos ISO eran vistos como módulos independientes.
- Se priorizaba la documentación como listas o estructuras jerárquicas.

## Después:
- El **FLUJO VISUAL** es el centro del sistema.
- Todo comienza desde **mapas de nodos y conexiones**.
- Cada nodo representa:
  - Un paso del flujo
  - Un evento
  - Un punto de decisión
  - Un sistema externo (Vtex, Easy, Gateway)
  - Un responsable
  - Una tarea ISO
  - Un documento relacionado
  - Una acción del usuario
- El usuario navega el sistema mediante flujos y no mediante menús.

---

# 2. Nueva estructura conceptual

## Entidad central: `Flow`
Un flujo es un “mapa” completo:
- Flujo de cliente
- Flujo de pago
- Flujo de producto
- Onboarding del colaborador
- Ciclo de formación
- Ciclo de vida del pedido
- Gestión QMS

Cada flujo contiene:
- Nodos (`FlowNode`)
- Conexiones (`FlowEdge`)

---

# 3. Estructura sugerida para `FlowNode`

```ts
FlowNode {
  id: string
  code?: string
  label: string
  system?: string
  type: "step" | "decision" | "event" | "process" | "integration"
  metadata?: {
    documents?: Document[],
    tasks?: Task[],
    roles?: string[],
    notes?: string,
    userAssigned?: string
  }
  position: { x: number, y: number }
}
```

---

# 4. Cambios requeridos en `plan_fases_extendido.md`

## ❌ Eliminar/modificar:
- Secciones que describen fases lineales.
- Partes que explican módulos como bloques estáticos independientes.
- Listado tradicional de funcionalidades en seco.

## ✔ Reemplazar por:
### 1. Nueva Fase 1: “Sistema Visual de Flujos”
Debe incluir:
- Objetivo: implementar ReactFlow como núcleo del proyecto.
- Modelo de datos: Flow, FlowNode, FlowEdge.
- Pantalla principal: “Flujos”.
- Visualizador interactivo.
- Panel lateral detallado.
- Integración con documentos y tareas.
- Roles y asignaciones por nodo.
- Importador desde CSV/Excel para construir flujos.

### 2. Nueva Fase 2: “Integración con QMS”
Debe incluir:
- Asociar documentos a nodos.
- Asociar tareas ISO a nodos.
- Asociar roles y responsabilidades.
- Vista de documentos desde nodos.

### 3. Nueva Fase 3: “Edición interactiva”
Debe incluir:
- Drag & drop de nodos.
- Creación de conexiones.
- Editor de metadatos del nodo.
- Guardado en Supabase.

### 4. Nueva Fase 4: “Gestión de estados y workflows”
Debe incluir:
- Estados del nodo.
- Reglas automáticas.
- Acciones automáticas.
- Alertas y notificaciones.

### 5. Nueva Fase 5: “Expansión multi-flujo”
Debe incluir:
- Varios flujos por empresa.
- Relaciones entre flujos.
- Templates de flujos.

---

# 5. Cambios requeridos en `plan_fases_qms.md`

## ❌ Eliminar/modificar:
- Linealidad típica del QMS.
- Representación de procesos como listas separadas.

## ✔ Reemplazar por:

### 1. “QMS basado en flujos”
- Cada proceso ISO debe representarse como un flujo visual.
- Ejemplos:
  - Gestión documental → flujo
  - No conformidades → flujo
  - Acciones correctivas → flujo
  - Auditorías → flujo
  - Procesos operativos → flujo
  - Gestión de capacitación → flujo

### 2. “Evidencia y documentación por nodo”
- Cada nodo del flujo contiene documentos, registros o tareas QMS.

### 3. “RACI por nodo”
- R: Responsable
- A: Accountable
- C: Consultado
- I: Informado

### 4. “Trazabilidad automática”
- Cada nodo registra:
  - Cambios
  - Aprobaciones
  - Estados
  - Seguimiento

---

# 6. Plantilla para flujos (para clientes)

```
ID | Texto | Conecta desde | Sistema
101 | Cliente decide pagar carrito |  | Vtex
102 | Cliente elije pago | 101 | Vtex
103 | Vtex se comunica con Gateway | 102 | Vtex
...
```

Convertido a JSON compatible con ReactFlow:

```json
{
  "nodes": [
    { "id": "101", "data": { "label": "Cliente decide pagar carrito", "system": "Vtex" }, "position": { "x": 0, "y": 0 } }
  ],
  "edges": [
    { "id": "e101-102", "source": "101", "target": "102" }
  ]
}
```

---

# 7. Prompt sugerido para próximas consultas (MUY IMPORTANTE)

```
Estoy desarrollando IsoTrack, un sistema basado en flujos visuales donde ReactFlow es el centro del proyecto. 
Los flujos reemplazan completamente a la documentación tradicional. 
Cada flujo contiene nodos que representan pasos del proceso, decisiones, eventos o tareas ISO. 
Cada nodo puede tener documentos asociados, tareas, roles responsables, notas, y asignaciones de usuarios. 
Necesito que cada respuesta que me brindes respete este nuevo enfoque y esté alineada al modelo de datos Flow, FlowNode y FlowEdge. 
Siempre que me ayudes a desarrollar algo nuevo, asumí que el usuario navega el sistema por flujos y no por menús.
```

---

# 8. Checklist final de migración

### ✔ Migrar concepto de proyecto a flujos  
### ✔ Redefinir fases principales  
### ✔ Reescribir documentación QMS  
### ✔ Integrar ReactFlow  
### ✔ Crear importador CSV → Flow  
### ✔ Crear template de flujos  
### ✔ Asociar documentos/tareas/roles por nodo  
### ✔ Crear panel lateral  
### ✔ Preparar modos: Viewer / Editor  
### ✔ Adaptar onboarding del usuario al sistema visual  

---

# Archivo generado automáticamente  
Este archivo sirve como guía general y como prompt base para futuras implementaciones del nuevo núcleo visual de IsoTrack.
