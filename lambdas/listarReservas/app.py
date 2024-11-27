import boto3
import json

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
actividades_table = dynamodb.Table('Actividades')

def lambda_handler(event, context):
    try:
        # Realizar una scan a la tabla de actividades
        response = actividades_table.scan()
        
        # Filtrar actividades con asientos disponibles
        actividades_disponibles = {}

        for item in response.get('Items', []):
            actividad = item['nombre']  # Nombre de la actividad
            for fecha, asientos_disponibles in item.items():
                # Ignorar el campo 'nombre' que no es una fecha
                if fecha != 'nombre' and isinstance(asientos_disponibles, int) and asientos_disponibles > 0:
                    # Si hay asientos disponibles, añadir a la lista
                    if actividad not in actividades_disponibles:
                        actividades_disponibles[actividad] = []
                    actividades_disponibles[actividad].append({
                        'fecha': fecha,
                        'asientos_disponibles': asientos_disponibles
                    })

        # Si no se encuentran actividades disponibles
        if not actividades_disponibles:
            return {
                'statusCode': 404,
                'body': json.dumps('No hay actividades disponibles en las fechas indicadas.')
            }

        # Devolver la lista de actividades disponibles
        return {
            'statusCode': 200,
            'body': json.dumps(actividades_disponibles)
        }

    except Exception as e:
        # Manejo de errores
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al consultar las actividades: {str(e)}')
        }
