import requests
from tabulate import tabulate
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# URL del servicio
url = "https://sicoexa.midagri.gob.pe/SICOEXA/Exportaciones/lstRanking"

headers = {
    "Content-Type": "application/json"
}

def fetch_anio(anio):
    payload = {
        "Annio": str(anio),
        "MesIni": "01",
        "MesFin": "12",
        "Tipo": "3"
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            detalles = data.get("RecDetalle", [])
            resultados = []
            for d in detalles:
                if d.get("strIde_arancel") and d.get("strPais_ant"):
                    fob = float(d["decFob"]) if d.get("decFob") else 0.0
                    neto = float(d["decNeto"]) if d.get("decNeto") else 0.0
                    resultados.append([
                        anio,
                        d["strIde_arancel"],
                        d["strPais_ant"],
                        f"{fob:,.2f}",
                        f"{neto:,.2f}"
                    ])
            return resultados
        else:
            print(f"Error al conectar para el año {anio}. Código HTTP: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error en el año {anio}: {e}")
        return []

tabla_resultados = []

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(fetch_anio, anio) for anio in range(2000, 2025)]
    for future in as_completed(futures):
        tabla_resultados.extend(future.result())

# Exportar a CSV
with open("exportaciones.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Año", "Ranking", "País", "Valor FOB (USD)", "Valor Neto"])
    writer.writerows(tabla_resultados)

# Mostrar resultados en formato tabla
print(tabulate(
    tabla_resultados,
    headers=["Año", "Ranking", "País", "Valor FOB (USD)", "Valor Neto"],
    tablefmt="grid"
))