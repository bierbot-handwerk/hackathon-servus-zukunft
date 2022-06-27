# hackathon-servus-zukunft
A fork of the hackathon project 'bierthron'

# Requirements for happy developing on your local host
- Docker
- Docker-Compose

# Necessary .env file to place on root level of this repo

If you want to make use of telegram bot (see credentials.yml)

    TELEGRAM_TOKEN=example:example

If you use a real mongodb, make sure to hide the envs aswell somewhere. We leave this up to you.

# Getting started

Make sure the build is successful

`docker-compose build`

For the first time you start the bot you need to train the underlying models

On M1 Macbook:

```
    docker-compose -f docker-compose.yml -f docker-compose.dev-m1.yml run rasa-server 'rasa train'

```

Other:

```
    docker-compose run rasa-server 'rasa train'
```
        
As a next step you can start the deployment as usual with `docker-compose -f docker-compose.yml -f docker-compose.dev-m1.yml`




