FROM python:3.12-alpine AS builder

WORKDIR /code


COPY pyproject.toml .

RUN python -m pip install hatch && \
    python -m hatch dep show requirements > requirements.txt && \
    python -m pip wheel -r requirements.txt --no-cache-dir --no-deps --wheel-dir wheels



FROM python:3.12-alpine AS runner

WORKDIR /code


COPY --from=builder /code/wheels wheels/
RUN python -m pip install --no-cache-dir wheels/* && \
    rm -r wheels

COPY security data/security
COPY app app


CMD [ "python", "-m", "app" ]


EXPOSE 443
