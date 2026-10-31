# veghe – imagine minimă, fără dependențe Python externe
FROM python:3.13-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends tzdata ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 10001 veghe

WORKDIR /app
COPY veghe/ ./veghe/
COPY config.example.toml ./config.example.toml
RUN mkdir -p /app/data && chown -R veghe:veghe /app

USER veghe
ENV PYTHONUNBUFFERED=1 TZ=Europe/Bucharest VEGHE_STATUS_BIND=0.0.0.0
VOLUME ["/app/data"]

HEALTHCHECK --interval=60s --timeout=5s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=4).status == 200 else 1)"

ENTRYPOINT ["python", "-m", "veghe", "--config", "/app/config.toml"]
CMD ["run"]
