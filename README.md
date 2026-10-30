# Práctica de Sistemas Operativos: Sistema de Procesamiento de Documentos Concurrente

## Descripción
Sistema desarrollado en Python que simula el procesamiento concurrente de 24 documentos utilizando hilos (`threading`), una cola segura (`queue.Queue`) y exclusión mutua (`threading.Lock`).

---

## Preguntas de Análisis y Verificación

### 1. ¿Por qué `queue.Queue` es apropiada para compartir trabajos?
`queue.Queue` está diseñada específicamente para entornos concurrentes ( o multihilo) en Python. Es apropiada porque es **segura para hilos (thread-safe)**, gestionando automáticamente los bloqueos internos necesarios cuando muchos hilos intentan insertar o extraer elementos de forma simultánea. Además esto implementa un modelo FIFO (First-In, First-Out) que evita condiciones de carrera, garantizando que cuando un trabajador extrae un documento de la cola, este se elimina instantáneamente y ningún otro hilo puede tomarlo por duplicado.

### 2. ¿Qué protege `Lock` y qué pasaría si se actualizara el resumen sin él?
El objeto `threading.Lock` protege la sección crítica del código donde se actualiza el diccionario compartido de resultados (`resultados[nombre].append(doc_id)`). Si se intentara actualizar el resumen **sin un Lock**, se produciría una condición de carrera (*race condition*). Al ejecutarse muchos hilos de forma concurrente, dos de ellos podrían modificar o escribir en el diccionario al mismo milisegundo, corrompiendo la memoria interna del diccionario en Python y provocando pérdida de datos o los conteos incorrectos.

### 3. ¿Qué cambiarías si cada documento tuviera que guardarse en un archivo real?
Si los documentos tuvieran que guardarse físicamente en el disco duro, se requerirían los siguientes cambios:
* **Operaciones de Entrada/Salida (I/O):** Reemplazar el retraso simulado de `time.sleep()` por la lógica real de apertura, escritura y cierre de archivos.
* **Gestión de Excepciones:** Añadir bloques `try-except` para manejar posibles errores de disco lleno o permisos denegados.
* **Control de Concurrencia en Disco:** Asegurar que cada hilo escriba en archivos independientes o utilizar mecanismos de sincronización adicionales si se comparte un archivo de registro (*log*).