# artichoqe

## Prerequisite

### Docker

[Prometheus](https://hub.docker.com/r/prom/prometheus/)

Bind-mount your prometheus.yml from the host by running:

```bash
docker run \
    -p 9090:9090 \
    -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```

Or use an additional volume for the config:

```bash
docker run \
    -p 9090:9090 \
    -v /path/to/config:/etc/prometheus \
    prom/prometheus
```

[Grafana](https://hub.docker.com/r/grafana/grafana)

Start your container binding the external port 3000.

`docker run -d --name=grafana -p 3000:3000 grafana/grafana`
