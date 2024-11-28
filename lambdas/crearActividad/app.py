import boto3
import uuid
import json

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
actividades_table = dynamodb.Table('Actividades')

def lambda_handler(event, context):
    # Obtener datos del evento
    nombre = event.get('nombre')
    fecha = event.get('fecha')
    asientos = event.get('asientos')

    # Validación de datos de entrada
    if not nombre or not fecha or not asientos:
        return {
            'statusCode': 400,
            'body': json.dumps('Faltan parámetros: nombre, fecha y asientos.')
        }

    try:
        # Generar un UUID como ID para la actividad
        actividad_id = str(uuid.uuid4())  # Genera un UUID único para la actividad

        # Crear ítem para insertar en DynamoDB
        item = {
            'id': actividad_id,          # UUID como ID único de la actividad
            'nombre': nombre,
            'fecha': fecha,
            'asientos': int(asientos)    # Convertir a número
        }

        # Guardar la actividad en la tabla DynamoDB
        actividades_table.put_item(Item=item)

        # Respuesta exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Actividad creada exitosamente.',
                'actividad': item
            })
        }

    except Exception as e:
        # Manejar errores generales
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al crear la actividad: {str(e)}')
        }
