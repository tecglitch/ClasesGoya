# Flujo de login OAuth con Google

```mermaid
sequenceDiagram
    actor U as Usuario
    participant B as Navegador
    participant T as TaskFlow
    participant G as Google

    U->>B: Elige Ingresar con Google
    B->>T: GET /accounts/google/login/
    T-->>B: Redirección con client_id, redirect_uri, scope y state aleatorio
    B->>G: Abre la autorización de Google
    U->>G: Inicia sesión y acepta compartir perfil/email
    G-->>B: Redirige a la callback con code y state
    B->>T: Entrega code a /accounts/google/login/callback/
    T->>T: Verifica state y redirect_uri
    T->>G: Canjea code usando client_secret (servidor a servidor)
    G-->>T: Devuelve tokens y datos de identidad (servidor a servidor)
    T->>T: Allauth vincula/crea el usuario y abre sesión Django
    T-->>B: Redirige a /api/auth/social/jwt/
    B->>T: Pide el JWT de TaskFlow mediante la sesión
    T-->>B: Devuelve access y refresh propios de TaskFlow
```

El navegador transporta el código de autorización de un solo uso; el `client_secret` y el canje de tokens quedan entre los servidores. `state` protege la vuelta contra solicitudes inyectadas y los scopes se limitan a `profile` y `email`. La URL de callback local es `http://127.0.0.1:8000/accounts/google/login/callback/`.

Para completar el login real falta crear una aplicación OAuth en Google Cloud y copiar su Client ID y Client Secret al `.env` local. Esos valores no se guardan en el repositorio.
