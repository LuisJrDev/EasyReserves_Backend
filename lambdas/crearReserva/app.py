import json
import uuid

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

    nombre = event.get("nombre")
    correo = event.get("correo")
    actividad = event.get("actividad")
    fecha = event.get("fecha")
    asientos = event.get("asientos")

    if not nombre or not correo or not actividad or not fecha or not asientos:
        return {
            'statusCode': 400,
            'body': json.dumps('Faltan parámetros: nombre, correo, actividad, fecha y asientos.')
        }

    if actividad not in actividades_disponibles:
        return {
            'statusCode': 404,
            'body': json.dumps(f'La actividad "{actividad}" no está disponible.')
        }

    if fecha not in actividades_disponibles[actividad]:
        return {
            'statusCode': 404,
            'body': json.dumps(f'No hay disponibilidad para la fecha "{fecha}" en la actividad "{actividad}".')
        }

    disponibilidad = actividades_disponibles[actividad][fecha]
    asientos = int(asientos)

    if asientos > disponibilidad:
        return {
            'statusCode': 400,
            'body': json.dumps(f'No hay suficientes asientos disponibles. Solo quedan {disponibilidad}.')
        }

    actividades_disponibles[actividad][fecha] -= asientos
    id_reserva = str(uuid.uuid4())
    reserva = {
        "id_reserva": id_reserva,
        "nombre": nombre,
        "correo": correo,
        "actividad": actividad,
        "fecha": fecha,
        "asientos": asientos,
        "estado": "confirmada"
    }

    return {
        'statusCode': 200,
        'body': json.dumps({
            "mensaje": "Reserva confirmada",
            "reserva": reserva,
            "disponibilidad_restante": actividades_disponibles[actividad][fecha]
        })
    }
