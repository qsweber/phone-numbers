from datetime import datetime
from decimal import Decimal
import json
from uuid import UUID

import boto3
from boto3.dynamodb.conditions import Key


class Dao(object):
    def __init__(self, model_class, table_name):
        self.model_class = model_class
        self.table_name = table_name

        self.to_dynamo = {
            dict: json.dumps,
            list: json.dumps,
            datetime: lambda v: Decimal(v.timestamp()),
            UUID: str,
            str: str,
            int: int,
            Decimal: Decimal,
        }

        self.from_dynamo = {
            dict: json.loads,
            list: json.loads,
            datetime: lambda v: datetime.fromtimestamp(float(v)),
            UUID: UUID,
            str: str,
            int: int,
            Decimal: Decimal,
        }

    def _get_dynamo_table(self):
        dynamodb = boto3.resource('dynamodb')
        return dynamodb.Table(self.table_name)

    def _create_internal(self, object_for_dynamo):
        dynamo_table = self._get_dynamo_table()
        return dynamo_table.put_item(Item=object_for_dynamo)

    def _to_dynamo_object(self, model_instance):
        return {
            field: self.to_dynamo[field_type](getattr(model_instance, field))
            for field, field_type in model_instance._field_types.items()
        }

    def _from_dynamo_object(self, dynamo_object):
        return self.model_class(**{
            field: self.from_dynamo[field_type](dynamo_object.get(field)) if dynamo_object.get(field) else None
            for field, field_type in self.model_class._field_types.items()
        })

    def create(self, model_instance):
        object_for_dynamo = self._to_dynamo_object(model_instance)

        self._create_internal(object_for_dynamo)

        return True

    def _read_internal(self, key, value):
        dynamo_table = self._get_dynamo_table()
        if not key:
            return dynamo_table.scan().get('Items')
        else:
            return dynamo_table.query(KeyConditionExpression=Key(key).eq(value)).get('Items')

    def read(self, key=None, value=None):
        result = self._read_internal(key, value)

        if not result:
            return None

        return self._from_dynamo_object(result[0])
