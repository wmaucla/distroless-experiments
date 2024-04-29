# distroless-experiments

Experimentation with distroless containers for security, backed by python envs.

```bash
docker build -t myimage .
docker run myimage
docker run --entrypoint=sh -ti myimage
```

Thanks to example found [here](https://github.com/alexdmoss/distroless-python/blob/main/tests/gunicorn/app.py).