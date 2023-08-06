import uuid
from functools import cached_property
from typing import Iterable, Optional, TypedDict, TypeVar

import boto3
from boto3_type_annotations.sqs import Client as SQSClient

from platonic_queue.chunkify import chunkify
from platonic_queue.queue import Queue
from platonic_queue.serde import SerdeStringMixin

# We only can send 10 messages at once to SQS.
MAX_ENTRIES_PER_BATCH = 10

T = TypeVar('T')  # noqa: WPS111


class SQSMessage(TypedDict):
    """Representation of SQS message."""

    Id: str   # noqa: WPS115
    MessageBody: str  # noqa: WPS115


class SQSQueue(SerdeStringMixin[T], Queue[T]):
    """SQS queue."""

    url: str

    def __init__(self, url: Optional[str] = None):
        if url is not None:
            self.url = url

        if not getattr(self, 'url', None):
            raise ValueError(f'Please specify {self.__class__.__name__}.url')

    def get_client(self) -> SQSClient:
        """Create boto3 SQS client."""
        return boto3.client('sqs')

    @cached_property
    def client(self) -> SQSClient:
        """Create boto3 SQS client and cache it."""
        return self.get_client()

    def create_sqs_message_id(self, instance: T) -> str:
        """Unique SQS message id."""
        # As per boto3 docs:
        # > The Id s of a batch request need to be unique within a request.
        # > This identifier can have up to 80 characters. The following
        # characters are accepted: alphanumeric characters, hyphens(-),
        # and underscores (_).
        return uuid.uuid4().hex

    def create_sqs_message(self, instance: T) -> SQSMessage:
        """Create a valid SQS message."""
        return SQSMessage(
            Id=self.create_sqs_message_id(instance),
            MessageBody=self.serialize(instance),
        )

    def put(self, instance: T) -> None:
        """Put a message into the queue."""
        message_body = self.serialize(instance)

        self.client.send_message(
            QueueUrl=self.url,
            MessageBody=message_body,
        )

    def put_many(self, instances: Iterable[T]):  # noqa: WPS110
        """Send multiple objects to SQS queue."""
        messages = map(self.create_sqs_message, instances)

        # We only can send MAX_ENTRIES_PER_BATCH messages at once.
        chunks = chunkify(messages, MAX_ENTRIES_PER_BATCH)

        for entries in chunks:
            self.client.send_message_batch(
                QueueUrl=self.url,
                Entries=entries,
            )

    def get(self) -> T:
        """Fetch a message from queue."""
        raise NotImplementedError()
