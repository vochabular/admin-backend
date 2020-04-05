# Hasura GraphQL Engine

## Setup:

- (Installation of Hasura CLI)[https://hasura.io/docs/1.0/graphql/manual/hasura-cli/install-hasura-cli.html#install-hasura-cli] - Important: Install the lateest version via `curl -L https://github.com/hasura/graphql-engine/raw/master/cli/get.sh | bash` or `npm install --global hasura-cli@beta`
- Make sure that the `config.yaml` values are set correctly

## How to work with Hasura and multiple environments (dev, staging, production):

Hasura provides a web interface to manage the metadata (which DB tables and columns should be exposed and such as role based access rights). It can be accessed via http://localhost:8080 (if you are running docker...). 

Since any changes done through this need to get tracked somewhere so they can be applied also upstream in the staging or production environment, it is important to track all changes to the metadata (and the db if applicable...):

### Track changes

- Connect hasura-cli to the engine to track changes: `hasura console`
- Any changes to the database (when you run a a change through the SQL editor...) will now be stored in the `hasura/migrations` directory
- Any changes to the metadata (permissions, which tables arre tracked etc.) will now be updated in the `hasura/metadata` dir. 
- Upstream, the migrations will automatically be applied to the instances once the code is checked in and released as the docker image contains such a stage

