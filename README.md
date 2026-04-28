# Shopify Notifier PWA

Simulador de notificaciones de Shopify para iPhone. Notificaciones nativas del sistema con ícono, título, subtítulo y cuerpo personalizables, con contador de órdenes automático.

## Despliegue en Vercel (5 minutos)

### Opción A — Vercel CLI

```bash
npm install -g vercel
cd shopify-notifier
vercel --prod
```

### Opción B — GitHub + Vercel (recomendado)

1. Sube el proyecto a un repositorio de GitHub
2. Ve a [vercel.com](https://vercel.com) → "New Project"
3. Importa tu repositorio
4. En la configuración del proyecto:
   - **Framework**: Other
   - **Root Directory**: `./` (raíz)
   - **Output Directory**: `public`
5. Click en "Deploy"

Vercel te dará una URL tipo `https://shopify-notifier-xxx.vercel.app`

---

## Instalar en iPhone

1. Abre la URL en **Safari** (no Chrome ni Firefox)
2. Toca el botón de compartir ↑
3. Selecciona **"Añadir a pantalla de inicio"**
4. Dale el nombre que quieras → "Añadir"
5. Abre la app desde el ícono de la pantalla de inicio
6. Cuando pida permisos de notificación → **"Permitir"**

> ⚠️ Requiere iOS 16.4 o superior para notificaciones push en PWAs.

---

## Estructura del proyecto

```
shopify-notifier/
├── public/
│   ├── index.html        ← App principal
│   ├── manifest.json     ← Configuración PWA
│   ├── sw.js             ← Service Worker
│   └── icons/
│       ├── icon-192.png  ← Ícono app
│       ├── icon-512.png  ← Ícono splash
│       └── shopify-icon.png ← Ícono notificación
├── vercel.json           ← Configuración Vercel
├── generate_icons.py     ← Script para regenerar íconos
└── generate-icons.js     ← Script alternativo (Node.js)
```

---

## Regenerar íconos

Si quieres personalizar el color o diseño del ícono:

**Python (recomendado):**
```bash
pip install Pillow
python3 generate_icons.py
```

**Node.js:**
```bash
npm install canvas
node generate-icons.js
```

---

## Limitaciones en iOS

| Característica | Estado |
|---|---|
| Notificaciones mientras la app está abierta | ✅ Funciona |
| Notificaciones en segundo plano | ⚠️ iOS las suspende tras un tiempo |
| Notificaciones con la app cerrada | ❌ Requiere servidor push (VAPID) |
| iOS 16.4+ instalada desde Safari | ✅ Requerido |

Para notificaciones con la app cerrada necesitarías un servidor con Web Push Protocol (VAPID), que está fuera del scope de esta versión local.
