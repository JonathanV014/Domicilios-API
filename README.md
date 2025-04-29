# Domicilios API

Este proyecto fue desarrollado por mi **Jonathan Vizcaíno Macías** como parte de la prueba técnica de Alfred. Es una API para la gestión de domicilios que encuentra el conductor más cercano, construida con **Django**, **Django REST Framework**, y **PostgreSQL**.
La API sigue una **arquitectura en capas**, lo que facilita la separación de responsabilidades y el mantenimiento del código. Además, incluye las siguientes características clave:

- **Autenticación con JWT**: Para garantizar la seguridad de las solicitudes y el acceso a los recursos.
- **Paginación**: Implementada al momento de obtener datos, para manejar grandes volúmenes de información de manera eficiente.
- **Documentación interactiva**: Disponible a través de Swagger para facilitar la exploración y prueba de los endpoints.

---

## **Poner en marcha el proyecto**

## **Notas importantes**
Asegurate de tener los siguientes puertos disponibles:
- **Puertos predeterminados**:
  - `8000`: Puerto para la API.
  - `3000`: Puerto para la base de datos PostgreSQL.


### **Requisitos previos**
Antes de comenzar, asegúrate de tener instalado lo siguiente:
- **Docker** y **Docker Compose**: Para construir y ejecutar los contenedores.
  - [Guía de instalación de Docker](https://www.docker.com/products/docker-desktop)

### **Pasos para iniciar**
1. **Construir la imagen Docker**  
   Ejecuta el siguiente comando para construir las imágenes:
   ```bash
   docker-compose build
   ```

2. **Iniciar los contenedores**  
   Una vez construidas las imágenes, inicia los contenedores:
   ```bash
   docker-compose up -d
   ```

   **Nota:** Asegúrate de que los puertos `8000` (API) y `3000` (base de datos) estén libres en tu máquina.

3. **Acceder a la API**  
   Una vez que los contenedores estén corriendo, puedes acceder a la API y ver la documentacion en:  
   [http://localhost:8000/](http://localhost:8000/)
   
   o 

   [http://localhost:8000/](http://localhost:8000/docs/)

---

## **Crear un superusuario**

Para crear un superusuario, ejecuta el siguiente comando:

```bash
docker-compose exec domiciliosapi pipenv run python manage.py createsuperuser
```

Sigue las instrucciones para configurar el nombre de usuario, correo electrónico y contraseña.

---

## **Autenticación y uso del token**

1. **Obtener un token**  
   Ve a la ruta `/api/token/` y realiza un POST con el siguiente cuerpo:

   ```json
   {
       "username": "usernameSuperUsuarioCreado",
       "password": "passwordSuperUsuarioCreado"
   }
   ```

   Esto devolverá un `access` token y un `refresh` token.

2. **Usar el token en la documentación interactiva**  
   - Ve a [http://localhost:8000/docs/](http://localhost:8000/docs/).
   - Haz clic en el botón **Authorize**.
   - En el campo que aparece, ingresa:  
     ```
     Bearer tokenGenerado
     ```
   - Una vez autorizado, podrás usar la documentación interactiva para probar las rutas de la API.

---

## **Crear recursos**

### **Crear un conductor (Driver)**

Para crear un conductor, realiza un POST a `/api/drivers/` con el siguiente cuerpo:

```json
{
    "name": "Nombre del conductor",
    "phone": "+123456789",
    "address": 1,
    "is_available": true
}
```

**Campos requeridos:**
- `name` (string): Nombre del conductor. Longitud entre 1 y 100 caracteres.
- `phone` (string): Número de teléfono. Debe seguir el patrón `^\+?\d{9,15}$`.
- `address` (integer): ID de la dirección asociada.
- `is_available` (boolean): Indica si el conductor está disponible.

---

### **Crear una dirección (Address)**

Para crear una dirección, realiza un POST a `/api/addresses/` con el siguiente cuerpo:

```json
{
    "name": "Casa",
    "country": "Colombia",
    "city": "Bogotá",
    "street": "Calle 123",
    "latitude": 4.711,
    "longitude": -74.072
}
```

**Campos requeridos:**
- `name` (string): Nombre de la dirección. Longitud entre 1 y 255 caracteres.
- `country` (string): País. Longitud entre 1 y 100 caracteres.
- `city` (string): Ciudad. Longitud entre 1 y 100 caracteres.
- `latitude` (number): Latitud. Valor entre -90 y 90.
- `longitude` (number): Longitud. Valor entre -180 y 180.

---

### **Crear un cliente (Client)**

Para crear un cliente, realiza un POST a `/api/clients/` con el siguiente cuerpo:

```json
{
    "name": "Juan Pérez",
    "phone": "+123456789",
    "email": "juan.perez@example.com",
    "address": 1
}
```

**Campos requeridos:**
- `name` (string): Nombre del cliente. Longitud entre 1 y 100 caracteres.
- `phone` (string): Número de teléfono. Debe seguir el patrón `^\+?1?\d{9,15}$`.
- `email` (string): Correo electrónico válido.
- `address` (integer): ID de la dirección asociada.

---

### **Crear un servicio (Service)**

Para crear un servicio, realiza un POST a `/api/services/` con el siguiente cuerpo:

```json
{
    "pickup_address": 1,
    "client": 1
}
```

**Campos requeridos:**
- `pickup_address` (integer): ID de la dirección de recogida.
- `client` (integer): ID del cliente asociado.

**Respuesta esperada (si hay conductores disponibles):**

```json
{
    "pickup_address": 1,
    "client": 1,
    "driver": 1,
    "status": "in_progress",
    "estimated_time": 15,
    "distance": 5.2,
    "created_at": "2025-04-28T20:00:00Z",
    "updated_at": "2025-04-28T20:00:00Z"
}
```

---

## **Completar un servicio**

Para que un conductor marque un servicio como completado, realiza un POST a:

```
/api/drivers/<driver_id>/complete/
```

Con el siguiente cuerpo:

```json
{
    "service_id": 1
}
```

Esto marcará el servicio como completado siempre en cuando el conductor lo tenga asignado.

---

---

### **Notas adicionales**
- **Paginación**: Todos los endpoints de lectura (`GET`) devuelven datos paginados. Puedes usar los parámetros `?page=` para navegar.
- **Autenticación**: Todos los endpoints requieren un token JWT válido en el encabezado `Authorization` como `Bearer <token>`. Con Driver podras usar endpoints de lectura (`GET`) sin necesidad de un token 

---

## **Ejecutar tests**

Puedes ejecutar los tests del proyecto con el siguiente comando:

```bash
docker-compose exec domiciliosapi pipenv run python manage.py test asignacion_servicios.test --verbosity 2
```

Si deseas ejecutar solo los tests de un módulo específico, puedes especificarlo:

- **Tests de repositories**:
  ```bash
  docker-compose exec domiciliosapi pipenv run python manage.py test asignacion_servicios.test.repositories --verbosity 2
  ```

- **Tests de services**:
  ```bash
  docker-compose exec domiciliosapi pipenv run python manage.py test asignacion_servicios.test.services --verbosity 2
  ```

- **Tests de views**:
  ```bash
  docker-compose exec domiciliosapi pipenv run python manage.py test asignacion_servicios.test.views --verbosity 2
  ```
---

## **Despliegue en la Nube (AWS/GCP)**

### **Cómo desplegar en AWS**
Para subir este proyecto a AWS, usaría los siguientes servicios:

1. **Elastic Beanstalk**:  
   Este servicio me permite desplegar aplicaciones Docker fácilmente. Subiría mi proyecto como una imagen Docker y Elastic Beanstalk se encargaría de manejar la infraestructura, como el balanceo de carga y el escalado automático.

   - Primero, construiría la imagen Docker de mi proyecto y la subiría a **Elastic Container Registry (ECR)**.
   - Luego, configuraría un entorno en Elastic Beanstalk para que use esa imagen.

2. **RDS (Relational Database Service)**:  
   Usaría RDS para manejar la base de datos PostgreSQL. Esto me permite tener una base de datos gestionada, con backups automáticos y alta disponibilidad.

   - Configuraría una instancia de PostgreSQL en RDS con las credenciales necesarias.
   - En mi archivo `.env`, pondría las credenciales de conexión a la base de datos.

3. **Seguridad**:  
   - Configuraría **Security Groups** para restringir el acceso a la base de datos y a la aplicación.
   - Usaría **IAM Roles** para limitar los permisos de acceso a los servicios.
---

### **Cómo desplegar en GCP**
Si quisiera desplegar este proyecto en GCP, usaría los siguientes servicios:

1. **Cloud Run**:  
   Este servicio es ideal para ejecutar aplicaciones Docker sin necesidad de gestionar servidores. Subiría mi imagen Docker a **Artifact Registry** y luego la desplegaría en Cloud Run.

   - Primero, construiría la imagen Docker de mi proyecto y la subiría a Artifact Registry.
   - Luego, configuraría Cloud Run para que use esa imagen.

2. **Cloud SQL**:  
   Para la base de datos PostgreSQL, usaría Cloud SQL. Es un servicio gestionado que facilita la configuración y el mantenimiento de la base de datos.

   - Configuraría una instancia de PostgreSQL en Cloud SQL.
   - En mi archivo `.env`, pondría las credenciales de conexión a la base de datos.

4. **Seguridad**:  
   - Configuraría **Firewall Rules** para restringir el acceso a la base de datos y a la aplicación.
   - Usaría **IAM Roles** para limitar los permisos de acceso a los servicios.

---

### **Consideraciones de Escalabilidad y Seguridad**
1. **Escalabilidad**:
   - Tanto AWS como GCP ofrecen escalado automático, lo que significa que mi aplicación puede manejar aumentos repentinos de tráfico sin problemas.
   - Configuraría límites mínimos y máximos para evitar costos innecesarios.

2. **Seguridad**:
   - Usaría HTTPS para todas las comunicaciones, configurando certificados SSL en **AWS Certificate Manager** o directamente en GCP.
   - Almacenaré las credenciales sensibles (como las de la base de datos) en servicios como **AWS Secrets Manager** o **GCP Secret Manager**.
   - Restringiría el acceso a la base de datos y a la aplicación mediante reglas de firewall o grupos de seguridad.

---

## **Contacto **

Si tienes preguntas o sugerencias, puedes contactarme en:  
**Correo:** jonayma0110@gmail.com