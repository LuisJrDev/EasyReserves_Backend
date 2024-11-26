import json

def lambda_handler(event, context):
    actividades_disponibles = {
        "Tour en la playa": {
            "2024-12-01": 20,
            "2024-12-02": 18
        },
        "Campamento en la montaña": {
            "2024-12-01": 15,
            "2024-12-02": 0
        },
        "Excursión a las ruinas": {
            "2024-12-01": 25,
            "2024-12-02": 20
        }
    }

    disponibilidad_actividades = {}
    for actividad, fechas in actividades_disponibles.items():
        disponibilidad_actividad = {}
        for fecha, cantidad in fechas.items():
            disponibilidad_actividad[fecha] = {
                "estado": "Disponible" if cantidad > 0 else "No disponible",
                "asientos_disponibles": cantidad
            }
        disponibilidad_actividades[actividad] = disponibilidad_actividad

    return {
        'statusCode': 200,
        'body': json.dumps(disponibilidad_actividades)
    }
