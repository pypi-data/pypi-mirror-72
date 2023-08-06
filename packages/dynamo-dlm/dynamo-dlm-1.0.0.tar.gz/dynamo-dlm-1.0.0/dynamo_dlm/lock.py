import logging
import time
import uuid

import backoff
import boto3
from boto3.dynamodb.conditions import Attr

# Import own module to ensure we get user-defined custom table names defined there
import dynamo_dlm as dlm


# Adds default logging for backoff algorithm. Leaving this at the default log level of WARNING will log backoff events
logging.getLogger('backoff').addHandler(logging.StreamHandler())
_logger = logging.getLogger('dynamo_dlm')
_dynamo_db = boto3.resource('dynamodb')


class DynamoDbLock:

    def __init__(self, resource_id: str, duration: int=10, table_name: str=None):
        self._table = _dynamo_db.Table(table_name or dlm.DEFAULT_TABLE_NAME)
        self._resource_id = resource_id
        self._duration = duration or dlm.DEFAULT_DURATION
        self._release_code = None


    def __enter__(self):
        self.acquire()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


    def acquire(self):
        self._release_code = uuid.uuid4().hex
        lock_confirmation = self._acquire_lock()
        while lock_confirmation is None:
            lock_confirmation = self._acquire_lock()


    def release(self):
        if not self._release_code:
            raise LockNotAcquiredError()
        self._release_lock()


    def _acquire_lock(self):
        try:
            return self._put_lock_item()
        except _dynamo_db.meta.client.exceptions.ConditionalCheckFailedException:
            pass


    def _release_lock(self):
        try:
            self._delete_lock_item()
        except _dynamo_db.meta.client.exceptions.ConditionalCheckFailedException:
            _logger.warning(
                f'Warning: DynamoDbLock for resource {self._resource_id} attempted to release after '
                f'it was already acquired. This means the caller took too long to release '
                f'the lock, it expired, and was subsequently acquired by another caller.'
            )


    @backoff.on_predicate(backoff.expo, jitter=backoff.full_jitter)
    def _put_lock_item(self):
        now = int(time.time())
        try:
            return self._table.put_item(
                Item={
                    'resource_id': self._resource_id,
                    'release_code': self._release_code,
                    'expires': now + self._duration
                },
                ConditionExpression=Attr('resource_id').not_exists() | Attr('expires').lte(now)
            )
        except _dynamo_db.meta.client.exceptions.ClientError as error:
            if error.response['Error']['Code'] != 'ProvisionedThroughputExceededException':
                raise error


    @backoff.on_predicate(backoff.expo, jitter=backoff.full_jitter)
    def _delete_lock_item(self):
        try:
            return self._table.delete_item(
                Key={'resource_id': self._resource_id},
                ConditionExpression=Attr('release_code').eq(self._release_code)
            )
        except _dynamo_db.meta.client.exceptions.ClientError as error:
            if error.response['Error']['Code'] != 'ProvisionedThroughputExceededException':
                raise error




class LockNotAcquiredError(RuntimeError):

    def __str__(self):
        return 'LockNotAcquiredError: Cannot release a lock that was never acquired'

    def __repr__(self):
        return str(self)
