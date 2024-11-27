import uuid
import json

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
reservas_table = dynamodb.Table('Reservas')

def lambda_handler(event, context):
    # Obtener datos del evento
    nombre = event.get('nombre')
    correo = event.get('correo')
    actividad = event.get('actividad')
    fecha = event.get('fecha')
    asientos = event.get('asientos')

    # Validación de datos de entrada
    if not nombre or not correo or not actividad or not fecha or not asientos:
        return {
            'statusCode': 400,
            'body': json.dumps('Faltan parámetros: nombre, correo, actividad, fecha y asientos.')
        }

    # Generar ID único para la reserva
    reserva_id = str(uuid.uuid4())

    # Crear ítem para insertar en DynamoDB
    item = {
        'id': reserva_id,           # ID único de la reserva
        'nombre': nombre,
        'correo': correo,
        'actividad': actividad,
        'fecha': fecha,
        'asientos': int(asientos),  # Convertir a número
        'estado': 'confirmada'      # Estado inicial de la reserva
    }

    try:
        # Guardar en DynamoDB
        reservas_table.put_item(Item=item)

        # Respuesta exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Reserva creada exitosamente.',
                'reserva': item
            })
        }

    except Exception as e:
        # Manejar errores
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al crear la reserva: {str(e)}')
        }
