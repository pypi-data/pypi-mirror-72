# Prometheus ECS SD (Wrap)

![Version](https://img.shields.io/github/v/release/trallnag/prometheus-ecs-sd-wrap?label=Release)

**Important: This is currently just a small flavor of / wrapper around 
<https://github.com/signal-ai/prometheus-ecs-sd> Copyright 2018, 2019 Signal 
Media Ltd**

Reason for this fork: Does not work out of the box run as ECS task. The only 
change made is the initialization of the ECS and EC2 clients using the session 
object instead of creating the clients directly.

This work makes the script work with the credential environment variable 
injected by AWS into the container. Only additional configuration required 
is the region provided by `AWS_DEFAULT_REGION`.

## Usage

See documentation at <https://github.com/signal-ai/prometheus-ecs-sd>

Install from PyPI with:

    pip install prometheus-ecs-discoverer

Or use the provided Docker image:

    docker run trallnag/prometheus-ecs-sd-wrap:wrapped-latest