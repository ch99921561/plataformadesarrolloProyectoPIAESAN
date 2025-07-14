import sys
import requests
import json
import csv
from multiprocessing import Pool, cpu_count
from urllib.parse import urlencode

API_URL = "https://checatusenal.osiptel.gob.pe/get_informacion_cobertura"
TECNOLOGIAS = ["2g", "3g", "4g", "5g"]

BASE_PAYLOAD = {
    "dist": "TODOS",
    "tipoDeCobertura": "cobertura_adicional",
    "tiposDeCobActivosArray": "cobertura_adicional,cobertura_garantizada",
    "operadoras": "`0"
}

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}
def fetch_for_dep_prov_ubigeo_tech(args):
    # args puede tener 5 o 6 elementos según el modo
    if len(args) == 5:
        depa, prov, ubigeo, tecnologia, usar_api = args
        distrito = None
    else:
        depa, prov, distrito, ubigeo, tecnologia, usar_api = args

    payload = {**BASE_PAYLOAD, "depa": depa, "prov": prov, "ubigeo": ubigeo, "tecnologiaActiva": tecnologia}
    payload_encoded = urlencode(payload)
    resp = requests.post(API_URL, headers=HEADERS, data=payload_encoded)
    # Guardar siempre la respuesta, incluso si hay error
    #with open(f"respuesta_{depa}_{prov}_{ubigeo}_{tecnologia}.txt", "w", encoding="utf-8") as f:
    #    f.write(resp.text)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"Error HTTP para {depa}-{prov}-{ubigeo}-{tecnologia}: {e}")
        return []
    data = resp.json()

    area_cubierta = data.get("areaCubierta", {})
    #with open(f"area_cubierta_{depa}_{prov}_{ubigeo}_{tecnologia}.json", "w", encoding="utf-8") as f:
    #    json.dump(area_cubierta, f, ensure_ascii=False, indent=2)
    area_adicional = area_cubierta.get(f"{tecnologia}-cobertura_adicional", "")
    area_garantizada = area_cubierta.get(f"{tecnologia}-cobertura_garantizada", "")

    registros = []
    info_cobertura = data.get("infoDeCobertura", {})
    area_total_km = data.get("areaTotalKM", "")

    for empresa, tecnologias in info_cobertura.items():
        for tech, valores in tecnologias.items():
            if tech.lower() == tecnologia.lower():
                registro = {
                    "departamento": depa,
                    "provincia": prov,
                    "ubigeo": ubigeo,
                    "tecnologia_consultada": tecnologia,
                    "empresa": empresa,
                    "tecnologia_operador": tech,
                    "info_de_cobertura": json.dumps(valores, ensure_ascii=False),
                    "area_total_cubierta": area_total_km,
                    "area_garantizada": valores.get("area_garant", ""),
                    "area_adicional": valores.get("area_adicio", ""),
                    "area_total_cubierta_global": area_adicional,
                    "area_total_garantizada_global": area_garantizada
                }
                if distrito is not None:
                    registro["distrito"] = distrito
                registros.append(registro)
    if not registros:
        registro = {
            "departamento": depa,
            "provincia": prov,
            "ubigeo": ubigeo,
            "tecnologia_consultada": tecnologia,
            "empresa": "",
            "tecnologia_operador": "",
            "info_de_cobertura": "",
            "area_total_cubierta": area_total_km,
            "area_garantizada": "",
            "area_adicional": "",
            "area_total_cubierta_global": area_adicional,
            "area_total_garantizada_global": area_garantizada
        }
        if distrito is not None:
            registro["distrito"] = distrito
        registros.append(registro)
    return registros
def leer_ubigeos_csv(path_csv, modo):
    combinaciones = []
    with open(path_csv, encoding="latin-1") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            depa = row.get("DEPARTAMENTO") or row.get("Departamento")
            prov = row.get("PROVINCIA") or row.get("Provincia")
            ubigeo = row.get("UBIGEO")
            if not (depa and prov and ubigeo):
                continue
            if modo == "distrital":
                distrito = row.get("DISTRITO") or row.get("Distrito")
                if not distrito:
                    continue
                combinaciones.append((depa.strip(), prov.strip(), distrito.strip(), ubigeo.strip()))
            else:
                combinaciones.append((depa.strip(), prov.strip(), ubigeo.strip()))
    return combinaciones

def fetch_for_dep_prov_ubigeo_tech(args):
    # args puede tener 5 o 6 elementos según el modo
    if len(args) == 5:
        depa, prov, ubigeo, tecnologia, usar_api = args
        distrito = None
    else:
        depa, prov, distrito, ubigeo, tecnologia, usar_api = args

    payload = {**BASE_PAYLOAD, "depa": depa, "prov": prov, "ubigeo": ubigeo, "tecnologiaActiva": tecnologia}
    payload_encoded = urlencode(payload)
    resp = requests.post(API_URL, headers=HEADERS, data=payload_encoded)
    # Guardar siempre la respuesta, incluso si hay error
    with open(f"respuesta_{depa}_{prov}_{ubigeo}_{tecnologia}.txt", "w", encoding="utf-8") as f:
        f.write(resp.text)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"Error HTTP para {depa}-{prov}-{ubigeo}-{tecnologia}: {e}")
        return []
    data = resp.json()

    area_cubierta = data.get("areaCubierta", {})
    with open(f"area_cubierta_{depa}_{prov}_{ubigeo}_{tecnologia}.json", "w", encoding="utf-8") as f:
        json.dump(area_cubierta, f, ensure_ascii=False, indent=2)
    area_adicional = area_cubierta.get(f"{tecnologia}-cobertura_adicional", "")
    area_garantizada = area_cubierta.get(f"{tecnologia}-cobertura_garantizada", "")

    registros = []
    info_cobertura = data.get("infoDeCobertura", {})
    area_total_km = data.get("areaTotalKM", "")

    for empresa, tecnologias in info_cobertura.items():
        for tech, valores in tecnologias.items():
            if tech.lower() == tecnologia.lower():
                registro = {
                    "departamento": depa,
                    "provincia": prov,
                    "ubigeo": ubigeo,
                    "tecnologia_consultada": tecnologia,
                    "empresa": empresa,
                    "tecnologia_operador": tech,
                    "info_de_cobertura": json.dumps(valores, ensure_ascii=False),
                    "area_total_cubierta": area_total_km,
                    "area_garantizada": valores.get("area_garant", ""),
                    "area_adicional": valores.get("area_adicio", ""),
                    "area_total_cubierta_global": area_adicional,
                    "area_total_garantizada_global": area_garantizada
                }
                if distrito is not None:
                    registro["distrito"] = distrito
                registros.append(registro)
    if not registros:
        registro = {
            "departamento": depa,
            "provincia": prov,
            "ubigeo": ubigeo,
            "tecnologia_consultada": tecnologia,
            "empresa": "",
            "tecnologia_operador": "",
            "info_de_cobertura": "",
            "area_total_cubierta": area_total_km,
            "area_garantizada": "",
            "area_adicional": "",
            "area_total_cubierta_global": area_adicional,
            "area_total_garantizada_global": area_garantizada
        }
        if distrito is not None:
            registro["distrito"] = distrito
        registros.append(registro)
    return registros

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("provincial", "distrital"):
        print("Uso: python main_coberturaredesmoviles.py [provincial|distrital]")
        return

    modo = sys.argv[1]
    usar_api = True

    if modo == "provincial":
        combinaciones = leer_ubigeos_csv("input/lista_ubigeo_peru_relaciondepartamento_provincia.csv", modo)
        tasks = [(depa, prov, ubigeo, tecnologia, usar_api) for depa, prov, ubigeo in combinaciones for tecnologia in TECNOLOGIAS]
        salida_csv = "cobertura_provincial.csv"
        salida_json = "cobertura_provincial.json"
    else:
        combinaciones = leer_ubigeos_csv("input/lista_ubigeoperu_relaciondepartamento_provincia_distrito.csv", modo)
        tasks = [(depa, prov, distrito, ubigeo, tecnologia, usar_api) for depa, prov, distrito, ubigeo in combinaciones for tecnologia in TECNOLOGIAS]
        salida_csv = "cobertura_distrital.csv"
        salida_json = "cobertura_distrital.json"

    workers = min(cpu_count(), len(tasks))
    with Pool(workers) as pool:
        results = pool.map(fetch_for_dep_prov_ubigeo_tech, tasks)

    all_records = [rec for sublist in results for rec in sublist]

    if all_records:
        with open(salida_json, "w", encoding="utf-8") as jsonfile:
            json.dump(all_records, jsonfile, ensure_ascii=False, indent=2)
        fieldnames = list(all_records[0].keys())
        with open(salida_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(all_records)
        print(f"Generados: {salida_json} y {salida_csv} ({len(all_records)} registros)")
    else:
        print("No se obtuvieron registros de cobertura.")

if __name__ == "__main__":
    main()