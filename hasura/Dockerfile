FROM hasura/graphql-engine:v1.3.2.cli-migrations-v2

# Add the hasura metadata to automatically apply
ADD ./metadata /hasura-metadata
# Uncomment in case of applying auto db migrations (Hasura)
# ADD ./migrations /hasura-migrations

# Enable the console
ENV HASURA_GRAPHQL_ENABLE_CONSOLE=true

# These two seem to be necessary for making migrations work
# ENV HASURA_GRAPHQL_CLI_ENVIRONMENT=default
ENV HASURA_GRAPHQL_MIGRATIONS_DATABASE_ENV_VAR=DATABASE_URL
# ENV HASURA_GRAPHQL_LOG_LEVEL=debug

# Change $DATABASE_URL to your heroku postgres URL if you're not using
# the primary postgres instance in your app
CMD graphql-engine \
    --database-url $DATABASE_URL \
    serve \
    --server-port $PORT \
    --query-plan-cache-size 100 \
    --retries 10
