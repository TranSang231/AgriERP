# Alpha Development tools
To provide development environment for local environment (such as database, caching service,..), we provide these services as containers.
The [docker-compose.yml](./docker-compose.yml) file in this section will include all needed services.

To run these services:
* First, you need to download and install [Docker Desktop](https://docs.docker.com/desktop/) on your pc.
* Copy [env.example](./env.example) file to `.env`, open it and change environment variables as your own.
* Copy [builder/env.example](./builder/env.example) file to `builder/.env`, open it and change environment variables as your own.
* Run the command below to start the services:
    ```
    docker compose --env-file .env up -d --build
    ```
    For Apple Silicon Macbook, use this command instead:
    ```
    docker compose --env-file .env -f docker-compose-apple-silicon.yml up -d --build
    ```

To stop the services, run the command below:

```
docker compose down
```

For Apple Silicon Macbook, use this command instead:

```
docker compose -f docker-compose-apple-silicon.yml down
```

## Additional tools
After running the above services, you can use these tools to connect and manage them.
- Use [Nosql Workbench](https://aws.amazon.com/dynamodb/nosql-workbench/) to connect and manage Dynamodb
- Use [MySQL Workbench](https://www.mysql.com/products/workbench/) to connect and manate MySQL databases.
- Use [Mongo express](https://github.com/mongo-express/mongo-express), available at http://localhost:8091, to manage mongo db
- Use [OpenSearch Dashboard](https://docs.opensearch.org/docs/latest/dashboards/quickstart/), available at http://127.0.0.1:5901, to manage [OpenSearch](https://opensearch.org/). You can login with the username `admmin`. The password can be found in environment variable `OPENSEARCH_INITIAL_ADMIN_PASSWORD`, in [.env](./env.example) file.
- Use [Kibana](https://www.elastic.co/kibana), available at http://localhost:<KIBANA_PORT>, to manage elastic search. You can login with the username `elastic`. The password can be found in environment variable `ELASTIC_PASSWORD`, in [.env](./env.example) file.