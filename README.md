# Conjuntos de items frecuentes - 3er Parcial

### Inteligencia Empresarial y Datamining
#### Universidad Tecnológica Nacional - Facultad Regional Tucumán

Alumnos:
* Pulido, Luciano Nicolás - 53397
* Sarmiento, Joaquín Esteban - 50152

## Introducción

En este trabajo haremos un análisis de rendimiento de los modelos de itemsets frecuentes vistos durante el cursado de la materia. Vamos a utilizar tres algoritmos:

- Apriori: funciona mediante una estrategia de generación y prueba de candidatos. Parte identificando los ítems individuales más frecuentes y luego, en cada iteración, genera combinaciones de ítems más grandes (k-itemsets) a partir de los que ya han sido considerados frecuentes. Cada conjunto candidato es evaluado contra la base de datos completa para calcular su soporte, repitiendo el proceso hasta que no se puedan generar más combinaciones frecuentes.
- FP-Growth: elimina la necesidad de generar candidatos de forma explícita. En su lugar, realiza un primer escaneo del dataset para identificar los ítems más frecuentes y luego construye una estructura compacta llamada FP-Tree, que almacena las transacciones en forma comprimida. A partir de este árbol, el algoritmo explora patrones frecuentes de manera recursiva, dividiendo el problema en subconjuntos condicionales sin tener que volver a escanear la base de datos completa.
- ECLAT: adopta un enfoque vertical, asociando cada ítem con una lista de transacciones (TID-list) en las que aparece. A partir de estas listas, construye itemsets más grandes mediante la intersección de TID-lists, lo que permite calcular el soporte sin escanear el dataset original.

Nuestro objetivo es, aparte de ver sus resultados, analizar cómo es el rendimiento de cada uno de ellos y las máquinas en donde los estamos ejecutando. Se tendrá en cuenta factores como el tiempo de ejecución, el uso de memoria y sensibilidad a min support.

Para el análisis haremos uso del dataset "online_retail_2.xlsx" presente en este repositorio, usando diferentes valores de soporte mínimo para generar diferente cantidad de itemsets y candidatos en caso de los algoritmos que los generan.

La explicación de la limpieza inicial de los datos y de la creación del dataset para los algoritmos se puede ver en el notebook llamado `preprocessing.ipynb`. En ella se explica cuales son las instancias eliminadas del dataset y como se preparan los datos para cada algoritmo.

Los algoritmos de Apriori y FP-Growth utilizados son de la biblioteca mlxtend, que reciben dataframes one hot encoded. Por otro lado, ECLAT es una implementación nuestra. Mlxtend no cuenta con la opción de usar este algoritmo y el paquete de pyEclat no nos funcionaba. pyEclat tomaba el dataset y ejecutaba durante horas incluso con valores de soporte mínimo elevado, por lo que consideramos injusto usar esta implementación para la comparación. Esto nos llevó a hacer la propia que se puede ver en el script correspondiente.

Cada algoritmo tiene su propio archivo .py en el cual se ejecuta el algoritmo dentro de una función llamada benchmark, que básicamente toma los datos necesarios para el análisis de rendimiento.

Todo esto es ejecutable a través del archivo `main.py`, que recibe parámetros para poder ejecutar los diferentes algoritmos con diferentes soportes mínimos y guadar los resultados en la carpeta `results` con formato csv, tanto del benchmark como de los itemsets encontrados.

En los archivos de benchmark, con cada ejecución se agrega una fila correspondiente a la misma. Los resultados de itemsets son sobre escritos porque con los mismos valores son siempre iguales.

Desde la consola se pueden pasar los parametros para hacer las ejecuciones de la siguiente manera.

```
$ python main.py --algorithm fp_growth --min_support 0.015
Dataframe cargado. Tamaño: (19773, 3912)
Ejecutando dataframe de tamaño: (19773, 3912)
Ejecutando benchmark...
```

Los resultados encontrados luego de las ejecuciones son analizados en la notebook llamada `results.ipynb` presente en la carpeta raíz del proyecto.

Las dependencias fueron gestionadas con poetry, por lo que con un `poetry install` debería ser suficiente para poder correr el código.



