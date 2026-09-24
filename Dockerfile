FROM docker.io/library/python@sha256:53739acebd52a300f19f52d93f2a6165f63300689bdf6f8af2bff0d63780e5e6

ARG ROBOTNIC_UID=10001
ARG ROBOTNIC_GID=10001
ARG VCS_REF=unknown
ARG ROBOTNIC_VERSION=dev

LABEL org.opencontainers.image.source="https://github.com/g-633/robotnic-trivium" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.version="${ROBOTNIC_VERSION}" \
      org.opencontainers.image.licenses="AGPL-3.0-only"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.lock /app/requirements.lock

RUN python -m pip install --no-cache-dir --no-deps -r /app/requirements.lock \
    && addgroup -S -g "${ROBOTNIC_GID}" robotnic \
    && adduser -S -D -H -u "${ROBOTNIC_UID}" -G robotnic robotnic \
    && mkdir -p /var/lib/robotnic/logs /etc/robotnic \
    && chown -R "${ROBOTNIC_UID}:${ROBOTNIC_GID}" /var/lib/robotnic \
    && ln -s /var/lib/robotnic/database.db /app/database.db \
    && ln -s /var/lib/robotnic/logs /app/logs \
    && ln -s /etc/robotnic/settings.json /app/settings.json \
    && ln -s /etc/robotnic/robotnic.env /app/.env

COPY api /app/api
COPY bot /app/bot
COPY cogs /app/cogs
COPY config /app/config
COPY database /app/database
COPY locales /app/locales
COPY default_settings.json main.py /app/

USER 10001:10001

CMD ["python", "main.py"]
