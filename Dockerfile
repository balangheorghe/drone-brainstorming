# veghe – imagine minimă, fără dependențe Python externe
FROM python:3.13-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends tzdata ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 10001 veghe

WORKDIR /app
# codul rămâne al lui root (needitabil de procesul care rulează); doar data/ e scriibil
COPY veghe/ ./veghe/
COPY config.example.toml ./config.example.toml
RUN mkdir -p /app/data && chown veghe:veghe /app/data && chmod 700 /app/data

USER veghe
ENV PYTHONUNBUFFERED=1 TZ=Europe/Bucharest VEGHE_STATUS_BIND=0.0.0.0 VEGHE_STATUS_PORT=8080
VOLUME ["/app/data"]

# Dacă bucla se blochează, procesul iese singur (watchdog) și Docker îl repornește (restart policy).
HEALTHCHECK --interval=60s --timeout=5s --start-period=60s --retries=3 \
  CMD python -c "import os,urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:%s/health' % os.environ.get('VEGHE_STATUS_PORT','8080'), timeout=4).status == 200 else 1)"

ENTRYPOINT ["python", "-m", "veghe", "--config", "/app/config.toml"]
CMD ["run"]
