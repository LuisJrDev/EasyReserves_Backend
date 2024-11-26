import json

def lambda_handler(event, context):
    actividades_disponibles = {
        "Tour en la playa": {},
        "Campamento en la montaña": {},
        "Excursión a las ruinas": {}
    }

    nombre_actividad = event.get("nombre_actividad")
    fecha = event.get("fecha")
    asientos = event.get("asientos")

    if not nombre_actividad or not fecha or not asientos:
        return {
            'statusCode': 400,
            'body': json.dumps('Faltan parámetros: nombre_actividad, fecha y asientos.')
        }

    if nombre_actividad in actividades_disponibles:
        return {
            'statusCode': 400,
            'body': json.dumps(f'La actividad "{nombre_actividad}" ya existe.')
        }

    actividades_disponibles[nombre_actividad] = {fecha: int(asientos)}

    return {
        'statusCode': 201,
        'body': json.dumps({
            "mensaje": "Actividad creada exitosamente",
            "actividad": actividades_disponibles[nombre_actividad]
        })
    }
