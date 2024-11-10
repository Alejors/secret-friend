# Amigo Secreto

## Descripción

El objetivo de este proyecto es poder gestionar concursos de amigo secreto.

### Funcionamiento

#### Creación Sorteo

Un usuario se debe registrar, iniciar sesión y luego crear un Concurso.
El concurso puede tener opcionalmente montos mínimos y máximos como valor del regalo.
A este concurso le agregará participantes a través de su email (y nombre en caso que el usuario no exista).

#### Lista de Deseos

Cada usuario puede agregar regalos deseados para el concurso, de manera que otros puedan saber qué poder regalar a la persona u obtener ideas.
Al momento de agregar elementos a la lista de deseos recibirán un recordatorio del monto que deberán respetar.

##### Consideraciones

En una primera instancia no hay cómo verificar el precio del objeto, pero se espera más adelante poder consultar por API los objetos deseados y obtener el valor de éstos, generando una alerta antes de agregar elementos que estén fuera de los parámetros establecidos.

#### Sortear

El dueño del concurso puede realizar el sorteo una vez que se hayan agregado todos los usuarios deseados. 
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
curl --location 'localhost:8000/v1'
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
