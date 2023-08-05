# SDC Engine Helpers Package

### Description

Helper modules for interacting with the AWS Recommendation Engine services

### Requirements

- Redis-cli
- mysql client

### Quick Setup

1. Create a .env file and add the following:

```
DB_DATABASE='sdc'
REDIS_HOST='/your/redis/host'
REDIS_PORT=6379
RDS_HOST='/your/mysql/host'
RDS_USERNAME='/your/mysql/username'
RDS_PORT=3306
RDS_PASSWORD='/your/password/'
RDS_DB_NAME='/your/default/schema'
```

2. Run the `Makefile`:

```
make
```

## Helpers

General functions to get key components out of subscriptions properties/engine

Currently available:

`get_engine` - Get an engine out of the client's subscription properties passing the engine's slug as a parameter

`get_dataset` - Get a dataset of out of an engine's data using a dataset label

`get_campaign` - Get a campaign out an engine either using the campaign's arn or by passing the recipe and optionally, 
the event_type


## Personalize Engine

### Maintenance

The purpose of this module is to help ensure that Recommendation Engine solution versions
are created when required so that the latest tracked data is taken into account
for recommendation inferences.

When solution versions are ready, the campaigns (inference endpoints) are updated
to use the latest solution version.

The above actions are controlled by scheduling fields stored in our database i.e
frequency and next action times. We also ensure that statuses are kept in sync between 
the database and what they are in the Recommendation Engine

#### Code Analysis

| Class                | Description   |    
| -------------------- | ------------- |  
| MaintenanceManager   | For all active clients in the database, create Recommendation Engine solution versions and/or update Recommendation Engine campaigns if the Recommendation Engine states change
| SolutionStateManager | Given a solution defined in the database, determine whether it is time to create a new solution version or to sync the Recommendation Engine status with the database status 
| CampaignStateManager | Given a campaign defined in the database, determine whether it is time to update a campaign or to sync the Recommendation Engine status with the database status

### Event

The purpose of this module is to track real-time events to AWS Recommendation Engine

#### Code Analysis

| Class        | Description   |    
| -------------| ------------- |  
| EventManager | For a given client, determine the Recommendation Engine event tracking id from the database and track an event for the given item id and user id

### Recommendations

The purpose of this module is to provide recommendations from AWS Recommendation Engine campaigns

#### Code Analysis

| Class                  | Description   |    
| ---------------------- | ------------- |  
| RecommendationsManager | For a given client, determine the Recommendation Engine campaign from the database and provide recommendations for the given item id