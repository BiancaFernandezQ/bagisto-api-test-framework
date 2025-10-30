utils - Clase estática que se puede mover e importar libremente en cualquier lugar.

Realizar tareas generales que podrían ser útiles en diferentes módulos. Como dijo Peter Lawrey, es útil usar nombres más específicos .

helpers - Clase que ayuda a otra clase o a un módulo.

Tareas que solo se usan en el módulo donde se ubican y no tienen sentido importarlas a otro lugar. Por lo tanto, el nombre podría ser más específico: ModuleName Helper (p. ej. , AdministrationHelper , LoginHelper ).



utils: Como bien describes, son para tareas generales y reutilizables en cualquier parte de tu proyecto (ej: un formateador de fechas, un generador de strings aleatorios, etc.). Crear un cliente es una acción muy específica de tu dominio.
helpers: Son perfectos para tareas que asisten a un módulo específico. En este caso, necesitas una función que "ayude" a tus tests de clientes a tener los datos necesarios para ejecutarse. Crear un cliente es una tarea de ayuda directamente ligada al módulo de customers.