import boto3
import json

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
actividades_table = dynamodb.Table('Actividades')

def lambda_handler(event, context):
    # Obtener el ID de la actividad del evento
    actividad_id = event.get('id')

    # Validar que se haya proporcionado el ID
    if not actividad_id:
        return {
            'statusCode': 400,
            'body': json.dumps('El campo "id" es obligatorio para eliminar una actividad.')
        }

    try:
        # Verificar si la actividad existe
        actividad_item = actividades_table.get_item(Key={'id': actividad_id})
        if 'Item' not in actividad_item:
            return {
                'statusCode': 404,
                'body': json.dumps('Actividad no encontrada.')
            }

        # Eliminar la actividad de la tabla
        actividades_table.delete_item(Key={'id': actividad_id})

        # Respuesta exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Actividad eliminada exitosamente.',
                'id': actividad_id
            })
        }

    except Exception as e:
        # Manejo de errores generales
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al eliminar la actividad: {str(e)}')
        }