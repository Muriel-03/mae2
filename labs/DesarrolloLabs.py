# ir guardando avance:  git add
# comentarlo: git commit -m "que fue lo que hice"
# para subirlo a mi git: git push origin muriel-tarea

# archivos de lab 1 descargados en carpeta creada llamada datalab1
# comandos profe:
# wget https://zenodo.org/records/7555181/files/cwlc.zip
# unzip cwlc.zip -d data/cwlc

# de prueba
# from pathlib import Path

# # Buscar todos los archivos .txt
# carpeta_datos = Path("datalab1/cwlc")
# archivos_txt = list(carpeta_datos.rglob("*.txt"))

# print(f"Encontrados {len(archivos_txt)} archivos .txt")

# Mostrar los primeros 10
# for archivo in archivos_txt[:10]:
#    print(archivo.name)

# PREGUNTA 1
# from pathlib import Path

# Buscar todos los archivos .txt
# archivos_txt = list(Path("datalab1/cwlc").rglob("*.txt"))

# print(f" Total de archivos: {len(archivos_txt)}")
# respuesta:  Total de archivos: 9000


# NORMALIZACION DEL .TXT

# import re
# from datasets import load_dataset

# ruta = "/workspaces/mae2/datalab1/cwlc"
# spanish_diagnostics = load_dataset("text", data_dir=ruta)

# Verificar tipo del primer texto
# type(spanish_diagnostics["train"]["text"][0])

# Ejemplo de procesamiento
# sample_sentence_lower = spanish_diagnostics["train"]["text"][0].lower()
# sample_sentence_lower

# Filtrar caracteres no alfabéticos
# sample_sentence_lower_alpha = re.sub(r'[^a-zñáéíóú]', ' ', sample_sentence_lower)
# sample_sentence_lower_alpha


# Función de normalización
# def normalize(text, remove_tildes=True):
#    """Normaliza una cadena de texto convirtiendo todo a minúsculas,
#    quitando los caracteres no alfabéticos y los tildes."""
#    text = text.lower()  # Convertir a minúsculas
#    text = re.sub(r"[^a-zñáéíóú]", " ", text)  # Quitar caracteres no alfabéticos
#    if remove_tildes:
#        text = re.sub("á", "a", text)
#        text = re.sub("é", "e", text)
#        text = re.sub("í", "i", text)
#        text = re.sub("ó", "o", text)
#        text = re.sub("ú", "u", text)
#    return text


# Aplicar normalización al conjunto de datos
# spanish_diagnostics_normalized = spanish_diagnostics["train"].map(
#    lambda x: {
#        "normalized_text": normalize(x["text"])
#    }
# )

# Mostrar ejemplo de texto normalizado
# import re
# from datasets import load_dataset

# Cargar únicamente los archivos .txt desde la ruta especificada
# ruta = "/workspaces/mae2/datalab1/cwlc"
# spanish_diagnostics = load_dataset("text", data_dir=ruta)

# Verificar tipo del primer texto
# type(spanish_diagnostics["train"]["text"][0])

# # Ejemplo de procesamiento
# sample_sentence_lower = spanish_diagnostics["train"]["text"][0].lower()
# sample_sentence_lower

# # Filtrar caracteres no alfabéticos
# sample_sentence_lower_alpha = re.sub(
#     r'[^a-zñáéíóú]', ' ', sample_sentence_lower)
# sample_sentence_lower_alpha


# # Función de normalización
# def normalize(text, remove_tildes=True):
#     """Normaliza una cadena de texto convirtiendo todo a minúsculas, 
#     quitando los caracteres no alfabéticos y los tildes."""
#     text = text.lower()  # Convertir a minúsculas
#     # Quitar caracteres no alfabéticos
#     text = re.sub(r"[^a-zñáéíóú]", " ", text)
#     if remove_tildes:
#         text = re.sub("á", "a", text)
#         text = re.sub("é", "e", text)
#         text = re.sub("í", "i", text)
#         text = re.sub("ó", "o", text)
#         text = re.sub("ú", "u", text)
#     return text


# # Aplicar normalización al conjunto de datos
# spanish_diagnostics_normalized = spanish_diagnostics["train"].map(
#     lambda x: {
#         "normalized_text": normalize(x["text"])
#     }
# )

# # Mostrar ejemplo de texto normalizado
# spanish_diagnostics_normalized[0]

# spanish_diagnostics_normalized.save_to_disk(
#     "/workspaces/mae2/datalab1/cwlc_normalized")

# # PREGUNTA 2
# import re
# from datasets import load_from_disk

# # Cargar el dataset procesado
# dataset_normalized = load_from_disk("/workspaces/mae2/datalab1/cwlc_normalized")

# # Patrón para buscar términos relacionados con hipertensión
# patron_hipertension = r'(hipertens|hta|presión alta|tensión arterial)'

# # Contador y lista para guardar los resultados
# contador_hipertension = 0
# resultados = []

# # Recorrer cada ejemplo del dataset
# for i, ejemplo in enumerate(dataset_normalized):
#     texto = ejemplo.get("normalized_text", "") or ejemplo.get("text", "")
    
#     # Buscar el patrón
#     if re.search(patron_hipertension, texto, re.IGNORECASE):
#         contador_hipertension += 1
#         resultados.append({
#             "registro": i,
#             "texto_completo": ejemplo.get("text", ""),  # texto original
#             "texto_normalizado": ejemplo.get("normalized_text", "")
#         })
#         print(f"Hipertensión encontrada en el registro número: {i}")

# # Mostrar resumen final
# print(f"\nTotal de registros con hipertensión: {contador_hipertension}")

# # Guardar los resultados en un archivo
# ruta_salida = "/workspaces/mae2/datalab1/resultados_hipertension.txt"

# with open(ruta_salida, "w", encoding="utf-8") as f:
#     for resultado in resultados:
#         f.write(f"Registro número: {resultado['registro']}\n")
#         f.write(f"Texto original:\n{resultado['texto_completo']}\n")
#         f.write(f"Texto normalizado:\n{resultado['texto_normalizado']}\n")
#         f.write("-" * 80 + "\n")

# print(f"\nResultados guardados en: {ruta_salida}")

import re
from datasets import load_from_disk

# Cargar el dataset desde la carpeta
dataset = load_from_disk("/workspaces/mae2/datalab1/cwlc_normalized")

# Patrón para buscar términos relacionados con hipertensión
patron_hipertension = r'(hipertens|hta|presión alta|tensión arterial)'

# Lista para guardar apariciones por línea (en todos los registros)
apariciones_por_linea = []

# Contador global de líneas
linea_global = 0

# Recorrer cada registro del dataset
for idx, ejemplo in enumerate(dataset):
    texto = ejemplo.get("text", "")  # Usamos el texto original

    if texto.strip() == "":
        continue  # Saltar textos vacíos

    # Dividir el texto por líneas
    lineas = texto.splitlines()

    for linea in lineas:
        coincidencias = re.findall(patron_hipertension, linea, re.IGNORECASE)
        cantidad = len(coincidencias)

        if cantidad > 0:
            apariciones_por_linea.append((linea_global, cantidad))
            print(f"Línea {linea_global}: Se encontraron {cantidad} aparición(es) de hipertensión")

        linea_global += 1

# Resumen final
print("\n=== Resumen ===")
print(f"Total de líneas analizadas: {linea_global}")
print(f"Total de líneas con hipertensión: {len(apariciones_por_linea)}")

total_apariciones = sum(cant for _, cant in apariciones_por_linea)
print(f"Total de apariciones totales: {total_apariciones}")

# Guardar resultados en archivo
ruta_salida = "/workspaces/mae2/datalab1/apariciones_hipertension_por_linea.txt"
with open(ruta_salida, "w", encoding="utf-8") as f:
    f.write("=== Resultados de búsqueda de hipertensión ===\n")
    f.write(f"Total de líneas analizadas: {linea_global}\n")
    f.write(f"Total de líneas con hipertensión: {len(apariciones_por_linea)}\n")
    f.write(f"Total de apariciones totales: {total_apariciones}\n\n")
    f.write("Línea - Apariciones\n")
    for linea_num, cant in apariciones_por_linea:
        f.write(f"Línea {linea_num}: {cant} vez(s)\n")

print(f"\nResultados guardados en: {ruta_salida}")