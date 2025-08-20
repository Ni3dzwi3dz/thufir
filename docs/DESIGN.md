# Thufir

Thufir should be an AI-boosted RSS reader. Not only it will provide access to articles
from RSS streams, but will also be
## Basic requirements

## Architecture

### Frontend
Vue.js

### Domain layer
* Includes abstractions and datatypes for rest of the system
* Does not depend on anything
* Data models independent from database models

### Presentation(Api) Layer
* Provides logic to handle requests, serialize data etc.
* Classes like FeedAPI depend on Manager abstraction to create data to be returned to client.

### Business layer
* Provides business logic for operations on feed, articles etc. It encapsulates most of the logic connected
to features visible by user i.e. "get all articles from feed X" or  "get summary for article Y"
* Classes like FeedManager depend on Repository abstraction and Provider abstraction

### Provider Layer
* Provides operations for retreiving new data- parsing feed, scraping article etc.
* Providers depend on Repository abstraction to put results to db

### Repository Layer
* Depends on persistence layer,
* Provides model-specific persistence operations

### Persistence Layer
* Creates an interface for a database
* Provides basic CRUD operations



## Feature actions

### Reader
* Should i use Celery to read feeds periodically?
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
