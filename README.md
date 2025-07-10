# Candelasoft - Gestión de Suscripciones

Este proyecto es un sistema de gestión de suscripciones desarrollado en **Django**. Permite registrar usuarios, crear suscripciones con información externa. En caso de inactividad detectada, se envía un correo de notificación.

---

##  Tecnologías principales

- Python
- Django
- Django REST Framework
- PostgreSQL
- Poetry (gestión de dependencias)
- Docker y Docker Compose

---

## ⚙️ Instalación local

### 1. Clona el repositorio

```bash
git clone https://github.com/Kalabuth/candelasoft.git
cd candelasoft
````

### 2. Instala Poetry (si no lo tienes)

```bash
pip install poetry
```

### 3. Instala dependencias

```bash
poetry install
```

### 4. Aplica migraciones y ejecuta el servidor

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🐳 Instalación con Docker

### 1. Construir la imagen y correr los contenedores

```bash
docker-compose up --build
```

Esto:

* Instala dependencias con `poetry`
* Ejecuta el servidor Django en `http://localhost:8000`

---

##  Correr tests

```bash
pytest
```

### Con Docker

```bash
docker-compose exec web pytest
```

---

##  Lógica de negocio actual

###  Objetivo

Permitir crear suscripciones para usuarios y, con base en información externa, enriquecer la respuesta con detalles adicionales.

###  Flujo principal

* Al listar o consultar una suscripción (`list` o `retrieve`):

  * Se consulta la API pública \[`https://gorest.co.in/public/v2/users?email={email}`].
  * Si la respuesta contiene al usuario y su estado es `"inactive"`, se envía un correo automático de notificación.
  * La respuesta de la API se incluye en un campo extra llamado `external_data`.

### Notificación por correo

Si un usuario es detectado como **inactivo** por la API externa, se ejecuta:

```python
send_email_notification(user.email)
```

> Este comportamiento se testea con `mock`.

### Tests automáticos

Se testean:

* Creación de usuario
* Creación de suscripción
* Listado y detalle con campo `external_data`
* Comportamiento diferente si `status` es `active` o `inactive`
* Envío de correo si el usuario externo está inactivo

---

## 🧾 Endpoints principales

| Método | URL                    | Descripción            |
| ------ | ---------------------- | ---------------------- |
| POST   | `/register/`           | Crear nuevo usuario    |
| POST   | `/subscriptions/`      | Crear una suscripción  |
| GET    | `/subscriptions/`      | Listar suscripciones   |
| GET    | `/subscriptions/<id>/` | Detalle de suscripción |

---

## 📁 Estructura

```
candelasoft/
├── apps/
│   ├── core/
│   │   ├── models/suscription.py
│   │   ├── views/suscripcion_view.py
│   │   ├── serializers/subscription_serializer.pytests/
│   │   └── test_subscription_api.py
│   └── common/
│       ├── external_services/jsonplaceholder.py
│       └── utils/email_utils.py
├
├── pyproject.toml
└── Dockerfile
```

---
