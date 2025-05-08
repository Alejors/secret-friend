# Amigo Secreto

## Descripción

El objetivo de este proyecto es poder gestionar concursos de amigo secreto.

## Tecnologías:

- Python
- Flask
- Jinja2
- MySQL
- Docker

### Funcionamiento

#### Creación Sorteo

Un usuario se debe registrar, iniciar sesión y luego crear un Concurso en la pestaña **Manage Events**.
El concurso puede tener opcionalmente montos mínimos y máximos como valor del regalo.
A este concurso le agregará participantes a través de su email (y nombre en caso que el usuario no exista).

**Nota**: *Existe un mínimo de 3 participantes para crear un evento (menos de eso no tiene sentido).*

#### Lista de Deseos

Cada usuario puede agregar regalos deseados en su lista, de manera que otros puedan saber qué poder regalar a la persona u obtener ideas.
Esta lista servirá cuando el evento se sortee, mostrando los regalos que estén dentro de los criterios del evento, en caso que haya límites.

#### Sortear

El administrador del concurso puede realizar el sorteo una vez que se hayan agregado todos los usuarios deseados. 
Esto busca todos los usuarios registrados para ese concurso, escoge un usuario diferente para cada uno (sin incluirse a si mismo) y lo asigna.

Cuando los usuarios participantes inicien sesión y seleccionen el concurso que ya se sorteó, deberían ver si el sorteo se efectuó, quién se seleccionó para ellos y la lista de deseos de ese usuario en caso que ya la haya creado.

## Despliegue

Una vez clonado el repositorio, se debe crear un archivo _.env_, se puede tomar como ejemplo _.env.example_ que está configurado para funcionar de manera local con el contenedor de mysql. 

**Nota**: Se debe agregar un valor a *JWT_SECRET_KEY* como llave para la creación de JWT.

Una vez realizado lo anterior, en el directorio donde se clonó el repositorio, ejecutar:

```
docker-compose up --build
```

Esto descargará las imágenes necesarias, compilará los contenedores en orden y levantará el proyecto.

### Verificación

Para poder verificar que la API está corriendo se puede ejecuta:

```
curl --location 'localhost:8000/healthcheck'
```

## Migraciones

### Correr

Con el servicio levantado se necesita correr las migraciones para que se creen las tablas en la DB.
Para esto se debe ejecutar:

```
docker-compose exec api alembic upgrade head
```

### Crear Nuevas

En caso que se modifiquen los modelos de las DB, se debe ejecutar los comandos de Alembic para poder crear nuevas migraciones.

```
docker-compose exec api alembic revision --autogenerate -m"<Mensaje descriptivo>"
```

Esto creará un nuevo documento en el directorio *migrations/versions*. Es necesario revisar que la migración esté correcta y corregir lo que sea necesario.
Una vez realizado esto, se debe [correr migración](#correr).

## Poblar Bases de Datos

Con las tablas ya pobladas, se puede ejecutar el comando propio *seed* agregado a la app de Flask.
Para esto se debe ejecutar:

```
docker-compose exec api flask --app src.main:app seed
```

Esto correrá los scripts SQL definidos en el comando:

- init-data.sql

La contraseña definida para los usuarios de prueba es Hola1234, considerando que se use el *JWT_SECRET_KEY* **MyM3g45up3r53cr3tK3y!**. 

*nota*: por favor no usar este secret key en ambientes productivos.
