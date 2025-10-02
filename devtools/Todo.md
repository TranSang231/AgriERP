# Rasa 
* Checkout Rasa open source, keep rasa-nlu, replace rasa-server and rasa-core by our implementation to make it compatible with our authentication, chatting modules, and can serve multiple models at the same time.
* Replace rasa docker pre-build image by yourself implement image.

# Open search
* Replace vector search by model search.

# Website builder
* Use queue, such as [RabbitMQ](https://www.rabbitmq.com/), [Celery](https://docs.celeryq.dev), [Kafka](https://kafka.apache.org) to communicate with website service instead of calling APIs directly.
