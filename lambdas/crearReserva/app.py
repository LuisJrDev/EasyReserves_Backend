import boto3
import uuid
import json

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
actividades_table = dynamodb.Table('Actividades')
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

    try:
        # Paso 1: Validar que haya asientos disponibles para la actividad
        actividad_item = actividades_table.get_item(Key={'id': actividad})
        
        if 'Item' not in actividad_item:
            return {
                'statusCode': 404,
                'body': json.dumps('Actividad no encontrada.')
            }

        actividad_data = actividad_item['Item']
        if int(asientos) > actividad_data['asientos']:
            return {
                'statusCode': 400,
                'body': json.dumps('No hay suficientes asientos disponibles para la actividad.')
            }

        # Paso 2: Generar un UUID como ID para la reserva
        reserva_id = str(uuid.uuid4())  # Genera un UUID único para la reserva

        # Paso 3: Crear ítem para insertar en DynamoDB
        item = {
            'id': reserva_id,           # UUID como ID único de la reserva
            'nombre': nombre,
            'correo': correo,
            'actividad': actividad,
            'fecha': fecha,
            'asientos': int(asientos),  # Convertir a número
            'estado': 'confirmada'      # Estado inicial de la reserva
        }

        # Paso 4: Guardar la reserva en la tabla DynamoDB
        reservas_table.put_item(Item=item)

        # Paso 5: Actualizar la cantidad de asientos en la actividad
        new_asientos = actividad_data['asientos'] - int(asientos)
        actividades_table.update_item(
            Key={'id': actividad},
            UpdateExpression="SET asientos = :new_asientos",
            ExpressionAttributeValues={':new_asientos': new_asientos}
        )

        # Respuesta exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Reserva creada exitosamente.',
                'reserva': item
            })
        }

    except Exception as e:
        # Manejar errores generales
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al crear la reserva: {str(e)}')
        }
