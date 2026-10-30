import queue
import random
import threading
import time

trabajos = queue.Queue()
nombres_trabajadores = ["Juan", "Julio", "Daniel", "Pedro"]

# Inicializar los 4 trabajadores antes de lanzar hilos
resultados = {nombre: [] for nombre in nombres_trabajadores}
lock = threading.Lock()

# Cargar aleatoriamente los 24 documentos
lista_docs = list(range(1, 25))
random.shuffle(lista_docs)

for doc_id in lista_docs:
  trabajos.put((doc_id, random.randint(1, 5)))


def trabajador(nombre):
  while True:
    try:
      doc_id, tamano = trabajos.get(timeout=1)
    except queue.Empty:
      break

    # Mostrar la concurrencia y el tamaño simulado
    print(f"-> {nombre} procesando doc {doc_id} (tamaño {tamano})")

    # Simular con time.sleep
    time.sleep(tamano * 0.1)

    # Actualizar resultados con lock
    with lock:
      resultados[nombre].append(doc_id)

    trabajos.task_done()


def main():
  hilos = []

  for nombre in nombres_trabajadores:
    hilo = threading.Thread(target=trabajador, args=(nombre,), name=nombre)
    hilos.append(hilo)
    hilo.start()

  trabajos.join()

  for hilo in hilos:
    hilo.join()


  print("\n" + "=" * 55)
  print("         RESUMEN DETALLADO POR TRABAJADOR           ")
  print("=" * 55)
  total_general = 0
  for nombre in nombres_trabajadores:
    docs = resultados[nombre]
    docs.sort()  # Ordenar los documentos 
    print(f"-> Trabajador {nombre} procesó {len(docs)} documentos: {docs}")
    total_general += len(docs)

  print("=" * 55)
  print(f"Total general de documentos procesados: {total_general} / 24")
  print("=" * 55 + "\n")


if __name__ == "__main__":
  main()