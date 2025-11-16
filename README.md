# Framework de Pruebas de API para Bagisto
Framework de pruebas automatizadas para la API REST del panel administrativo de Bagisto (Clientes y Grupos), utilizando Python y Pytest. Allure para los reportes, GitHub Actions para CI, y Github Pages para el despliegue el reporte.

## Manual de Usuario

### 1. Configuración del Entorno de Bagisto con Docker

Para ejecutar las pruebas, primero es necesario tener una instancia de Bagisto con la API REST de administración instalada y funcionando esto lo haremos con Docker. 

#### Requisitos Previos:
*   **Docker**: Tener Docker Desktop instalado y funcionando en tu máquina. Puedes descargarlo desde [Docker Desktop](https://www.docker.com/products/docker-desktop).

#### Pasos de Configuración:

1.  **Descargar la imagen de Bagisto**:
    Abre tu terminal o línea de comandos y ejecuta el siguiente comando para descargar la imagen oficial de Bagisto `2.3.0`:

    ```bash
    docker pull webkul/bagisto:2.3.0
    ```

2.  **Ejecutar el contenedor de Bagisto**:
    Inicia un contenedor Docker con la imagen descargada. El puerto `8000` de tu máquina local se mapeará al puerto `80` del contenedor.

    ```bash
    docker run -it -d -p 8000:80 --name mi_bagisto webkul/bagisto:2.3.0
    ```
    *   `-p 8000:80`: Mapea el puerto 8000 de tu host al puerto 80 del contenedor
    *   `--name mi_bagisto`: Asigna el nombre "mi_bagisto" al contenedor

3.  **Gestión del Contenedor (comandos útiles)**:
    *   **Iniciar contenedor**:
        ```bash
        docker start mi_bagisto
        ```
    *   **Detener contenedor**:
        ```bash
        docker stop mi_bagisto
        ```
    *   **Acceder al contenedor (cuando está ejecutándose)**:
        ```bash
        docker exec -it mi_bagisto /bin/bash
        ```

4.  **Instalar la REST API de Administración dentro del contenedor**:
    Este es un paso clave. Una vez que Bagisto esté en línea, es necesario acceder al contenedor e instalar el paquete de la API REST.

    Primero, accede al contenedor:
    ```bash
    docker exec -it mi_bagisto /bin/bash
    ```
    Una vez dentro del contenedor, ejecuta los siguientes comandos:
    ```bash
    cd /var/www/html
    composer require bagisto/rest-api
    echo "SANCTUM_STATEFUL_DOMAINS=http://localhost:8000" >> .env
    php artisan bagisto-rest-api:install
    exit
    ```
    *   `composer require bagisto/rest-api`: Instala el paquete de la API REST de Bagisto.
    *   `echo "SANCTUM_STATEFUL_DOMAINS=http://localhost:8000" >> .env`: Agrega la configuración necesaria para Laravel Sanctum en el archivo `.env`.
    *   `php artisan bagisto-rest-api:install`: Ejecuta el comando de instalación de la API REST, que también generará la documentación Swagger.
    *   `exit`: Sale del shell del contenedor.

### 2. Acceso a Bagisto y la API
Después de la instalación y configuración, es posible acceder a la documentacion de api rest
*   **Documentación de la API REST Admin (Swagger)**: http://localhost:8000/api/admin/documentation#/

### 3. Ejecución de los Tests de la API
Este framework utiliza `pytest` para ejecutar las pruebas y `allure-pytest` para generar informes detallados.

#### Requisitos Previos:
*   **Python 3.11+**: Asegúrate de tener Python 3.11 o superior instalado en tu máquina local.
*   **Java Runtime Environment (JRE)**: Necesario para generar los informes de Allure. Se puede descargar desde el sitio oficial de Oracle/OpenJDK.
*   **Node.js y npm**: Necesario para instalar `allure-commandline`. Puedes descargarlos desde Node.js.

#### Pasos para Ejecutar las Pruebas:

1.  **Clonar el repositorio del framework**:
    Clona este repositorio en tu máquina local:

    ```bash
    git clone https://github.com/BiancaFernandezQ/bagisto-api-test-framework.git
    cd bagisto-api-test-framework
    ```

2.  **Configurar un entorno virtual (recomendado)**:
    Es una buena práctica aislar las dependencias de tu proyecto.

    ```bash
    # Para crear un entorno virtual en Python:
    python -m venv venv
    # Para activar en Linux/macOS:
    source venv/bin/activate
    # Para activar en Windows:
    .\venv\Scripts\activate
    ```

3.  **Instalar dependencias de Python**:
    Instala las bibliotecas necesarias para el framework de pruebas listadas en el archivo requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar las pruebas de la API**:
    Asegúrate de que el contenedor de Bagisto esté corriendo y la API REST esté instalada (ver sección 1). Luego, ejecuta las pruebas con `pytest` en modo verbose:
    - Puedes ejecutar todas la pruebas con el comando:
        ```bash
        pytest -v test/ -vvvv
        ```
    - Es posible ejecutar por modulo ya sea customers o groups
        - Modulo de Grupos o Groups  
        ```bash
        pytest -v test/groups -vvvv
       ```
       - Modulo de Clientes o Customers
       ```bash
        pytest -v test/customers -vvvv
       ```
    - Tambien es posible ejecutar por mark, [marcas definidas en pytest.ini](./pytest.ini) para más detalles.
        - Ejemplo, ejecucion de pruebas con mark "positivas"
        ```bash
            pytest -v test/ -m positivas
        ```
5.  **Generar y ver el informe de Allure**:
    Después de ejecutar las pruebas, puedes generar un informe HTML
    ```bash
    npm install -g allure-commandline --save-dev
    python -m pytest --alluredir allure-results
    allure serve allure-results
    ```
    * `npm install -g allure-commandline --save-dev` Transforma los resultados de la carpeta allure-results en un reporte HTML
    * `python -m pytest --alluredir allure-results` Ejecutar los Test Cases en Allure
    * `allure serve allure-results` Generar el reporte Allure

## Manual Técnico

Esta sección describe la arquitectura y el flujo de trabajo de integración continua (CI) del framework de pruebas.

### Estructura del Proyecto

El framework está organizado de la siguiente manera:

*   `bagisto-api-test-framework/`
    *   `.github/workflows/bagisto-tests.yml`: Archivo de configuración para GitHub Actions, que define el flujo de trabajo de CI
    * `config/`: Contiene archivos de configuración y credenciales de acceso.
    *   `test/`: Contiene los archivos de prueba de Pytest, organizados por módulos (ej. `customers/`, `groups/`) y marks (`pytest.ini`).
    *   `bagisto_api/`: comunicación con la API REST, centralizando las funciones get, post, put y delete en api_request.py y gestionando las rutas en endpoint.py
    * `src/`: Compone la lógica principal y los componentes reutilizables:
        * `helpers/`tareas o funciones de ayuda que asisten a un módulo específico
        * `assertions/` define las aserciones personalizadas para validar los resultados esperados.
        * `Schemas/` contiene los esquemas JSON para validar las estructuras de respuesta.
        * `services/` abstrae la interacción directa con los endpoints.
        * `utils/` tareas generales y reutilizables en cualquier parte de tu proyecto, implementa el logger reutilizable.
        * `requirements.txt` Lista de dependencias necesarias para el proyecto.

### Flujo de Trabajo CI (GitHub Actions) y reportes (Github Pages)

El archivo `.github/workflows/bagisto-tests.yml` define un flujo de trabajo de integración continua (CI) que se ejecuta automáticamente en GitHub para asegurar la calidad del código y la funcionalidad de la API.
Contenido en `bagisto-tests.yml`
[Contenido en bagisto-tests.yml](.github/workflows/bagisto-tests.yml) para más detalles.
Flujo de trabajo:
* Checkout del repositorio: Se obtiene el código fuente actualizado
* Configuración de Python: Se instala la versión necesaria para ejecutar las pruebas
* Instalación de dependencias: Se instalan los paquetes especificados en requirements.txt, incluyendo herramientas de reporte como Allure.
* Inicio del contenedor Bagisto: Se despliega la aplicación Bagisto en un contenedor Docker para simular el entorno de pruebas.
* Esperar disponibilidad: Se verifica que Bagisto esté listo antes de continuar.
* Ejecución de pruebas: Se ejecutan los tests automatizados sobre la API, validando todos los endpoints de los módulos de Clientes y Grupos
* Generación de reportes: Se instala Java y Allure para generar reportes visuales de los resultados de las pruebas ejecutadas.
* Despliegue de reportes: El reporte generado se publica automáticamente en GitHub Pages para su posterior consulta

El proceso completo de generación y publicación de los reportes de Allure está integrado en el pipeline de GitHub Actions. Cada vez que se ejecuta este, los nuevos reportes son generados y desplegados automáticamente