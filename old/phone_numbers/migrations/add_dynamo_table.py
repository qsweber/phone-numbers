import boto3

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    phone_numbers = dynamodb.create_table(
        TableName='phone_numbers',
        KeySchema=[
            {
                'AttributeName': 'phone_number',  # globally unique partition
                'KeyType': 'HASH',
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'phone_number',
                'AttributeType': 'S',
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    phone_numbers.meta.client.get_waiter('table_exists').wait(TableName='phone_numbers')
