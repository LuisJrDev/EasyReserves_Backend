import json

def lambda_handler(event, context):
    actividades_disponibles = {
        "Tour en la playa": {
            "2024-12-01": 20,
            "2024-12-02": 18
        }
    }

    nombre_actividad = event.get("nombre_actividad")
    fecha = event.get("fecha")
    asientos = event.get("asientos")

    if not nombre_actividad or not fecha or not asientos:
        return {
            'statusCode': 400,
            'body': json.dumps('Faltan parámetros: nombre_actividad, fecha y asientos.')
        }

    if nombre_actividad not in actividades_disponibles:
        return {
            'statusCode': 404,
            'body': json.dumps(f'La actividad "{nombre_actividad}" no existe.')
        }

    actividades_disponibles[nombre_actividad][fecha] = int(asientos)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "mensaje": "Actividad actualizada",
            "actividad": actividades_disponibles[nombre_actividad]
        })
    }
