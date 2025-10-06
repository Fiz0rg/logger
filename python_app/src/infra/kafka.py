from confluent_kafka import Consumer, Producer
from src.domain.exeption.kafka import ProducerError
from src.domain.interfaces.event_bus import iEventBus
from src.infra.config import settings


class EventBus(iEventBus):
    _server = {"bootstrap.servers": f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}"}

    def __init__(self) -> None:
        __producer_config = dict(self._server)

        self.producer = Producer(__producer_config)

        # Consumer
        __consumer_config = {
            **self._server,
            "group.id": "mygroup",
            "auto.offset.reset": "earliest",
        }

        self.consumer = Consumer(__consumer_config)

    def publish(self, topic: str, message: str) -> None:
        self.producer.poll(0)
        try:
            self.producer.produce(
                topic=topic,
                value=message.encode("utf-8"),
                callback=self.delivery_report,
            )
            # self.producer.flush()
        except Exception as err:
            raise ProducerError(message="Error sending to event bus") from err
        self.healthcheck()

    def consume(self, topic: str) -> None:
        self.consumer.subscribe([topic])

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    raise NotImplementedError("Not implemented if block")
                elif msg.error():
                    raise NotImplementedError("Not implemented elif block")
                else:
                    raise NotImplementedError("Not implemented else block")

        except KeyboardInterrupt as err:
            raise NotImplementedError("KeyboardInterrupt") from err
        finally:
            self.consumer.close()
        return

    def flush(self):
        self.producer.flush()

    def healthcheck(self) -> None:
        try:
            self.producer.poll(0)
            self.producer.produce(
                topic="test",
                value=b"ping",
                callback=self.delivery_report,
            )
            self.producer.flush(timeout=3)
            print("Healthcheck OK")
        except Exception as e:
            print(f"Healthcheck failed: {e}")
            raise

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            print("Message delivery failed")
        else:
            print("Message delivered")
