import boto3
import json

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
actividades_table = dynamodb.Table('Actividades')

def lambda_handler(event, context):
    # Obtener datos del evento
    actividad_id = event.get('id')  # ID de la actividad a editar
    nombre = event.get('nombre')
    fecha = event.get('fecha')
    asientos = event.get('asientos')

    # Validación de datos de entrada
    if not actividad_id:
        return {
            'statusCode': 400,
            'body': json.dumps('El campo "id" es obligatorio para editar una actividad.')
        }

    if not any([nombre, fecha, asientos]):
        return {
            'statusCode': 400,
            'body': json.dumps('Debe proporcionar al menos uno de los campos: nombre, fecha o asientos para actualizar.')
        }

    try:
        # Verificar si la actividad existe
        actividad_item = actividades_table.get_item(Key={'id': actividad_id})
        if 'Item' not in actividad_item:
            return {
                'statusCode': 404,
                'body': json.dumps('Actividad no encontrada.')
            }

        # Crear expresión de actualización dinámicamente
        update_expression = []
        expression_values = {}
        if nombre:
            update_expression.append("nombre = :nombre")
            expression_values[':nombre'] = nombre
        if fecha:
            update_expression.append("fecha = :fecha")
            expression_values[':fecha'] = fecha
        if asientos:
            update_expression.append("asientos = :asientos")
            expression_values[':asientos'] = int(asientos)

        # Concatenar la expresión de actualización
        update_expression_str = "SET " + ", ".join(update_expression)

        # Actualizar la actividad en DynamoDB
        actividades_table.update_item(
            Key={'id': actividad_id},
            UpdateExpression=update_expression_str,
            ExpressionAttributeValues=expression_values
        )

        # Respuesta exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Actividad actualizada exitosamente.',
                'id': actividad_id
            })
        }

    except Exception as e:
        # Manejo de errores generales
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al editar la actividad: {str(e)}')
        }
