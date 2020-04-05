FROM hasura/graphql-engine:v1.2.0-beta.3.cli-migrations-v2

# Add the hasura metadata to automatically apply
ADD ./metadata /hasura-metadata
# Uncomment in case of applying auto db migrations (Hasura)
# ADD ./migrations /hasura-migrations

# Enable the console
ENV HASURA_GRAPHQL_ENABLE_CONSOLE=true

# Change $DATABASE_URL to your heroku postgres URL if you're not using
# the primary postgres instance in your app
CMD graphql-engine \
    --database-url $DATABASE_URL \
    serve \
    --server-port $PORT \
    --query-plan-cache-size 100 \
    --retries 10
