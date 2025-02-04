from time import time_ns
import json
import sys

from mcap.mcap0.writer import Writer

with open(sys.argv[1], "wb") as stream:
    writer = Writer(stream)

    # The library argument helps identify what tool wrote the file.
    writer.start(profile="x-custom", library="my-writer-v1")

    schema_id = writer.register_schema(
        name="sample",
        encoding="jsonschema",
        data=json.dumps(
            {
                "type": "object",
                "properties": {
                    "sample": {
                        "type": "string",
                    }
                },
            }
        ).encode(),
    )

    channel_id = writer.register_channel(
        schema_id=schema_id,
        topic="sample_topic",
        message_encoding="json",
    )

    writer.add_message(
        channel_id=channel_id,
        log_time=time_ns(),
        data=json.dumps({"sample": "test"}).encode("utf-8"),
        publish_time=time_ns(),
    )

    writer.finish()
