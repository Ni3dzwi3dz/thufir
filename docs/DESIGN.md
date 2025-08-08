# Thufir

Thufir should be an AI-boosted RSS reader. Not only it will provide access to articles
from RSS streams, but will also be
## Basic requirements

### Reader
* Can read subscribed channels from config
* Can retrieve single article from feed
* Can mark article as seen
* Can mark article as interesting

### AI Agent
* Can create synopsis for a single article
* Can create summary for daily articles
* Can choose most interesting articles based on previously starred ones
* Can create a summary of the topic selected by user, based on all feeds
* Can find articles on the same topic

### REST API
* Allows to retrieve single article
* Allows to retrieve feed articles
* Allows to retrieve article summary by id
* Allows to retrieve daily summary by date
* Allows to perform lookup in summaries by topic

### Frontend
TBC

## Future additions
### Multiple users
* Allow user creation
* Allow profile management
* Choose, add and delete feeds

## Architecture decisions and coding style

## General
* Abstractions will be used to define each object expected behaviour
* There will be a clear division of app into layers
* Each layer will explicitly accept all needed layers as dependency injection

## Components

### RSS Reader

### LLM Summary

### REST API
