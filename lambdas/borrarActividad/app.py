import json



def lambda_handler(event, context):
    actividades_disponibles = {
        "Tour en la playa": {
            "2024-12-01": 20,
            "2024-12-02": 18
        }
    }

    nombre_actividad = event.get("nombre_actividad")

    if not nombre_actividad:
        return {
            'statusCode': 400,
            'body': json.dumps('Falta el parámetro: nombre_actividad.')
        }

    if nombre_actividad not in actividades_disponibles:
        return {
            'statusCode': 404,
            'body': json.dumps(f'La actividad "{nombre_actividad}" no existe.')
        }

    del actividades_disponibles[nombre_actividad]

    return {
        'statusCode': 200,
        'body': json.dumps({
            "mensaje": f'Actividad "{nombre_actividad}" eliminada con éxito.'
        })
    }
