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

Nuestro objetivo es, aparte de ver sus resultados, analizar cómo es el rendimiento de cada uno de ellos y las máquinas en donde los estamos ejecutando. Se tendrá en cuenta factores como el tiempo de ejecución, el uso de memoria, sensibilidad a min support, el uso de CPUs, etc.

Para el análisis haremos uso del dataset "online_retail_2.xlsx" presente en este repositorio, usando diferentes tamaños de muestras para evaluar la escalabilidad de cada algoritmo.

La explicación de la limpieza inicial de los datos y de la creación del dataset para los algoritmos se puede ver en el notebook llamado `preprocessing.ipynb`.

Cada algoritmo tiene su propio archivo .py en el cual se hace el análisis de rendimiento del mismo. Los resultados de performance se listan a continuación.

