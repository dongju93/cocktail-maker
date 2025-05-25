FROM python:3.13.3-alpine

WORKDIR /cocktail-maker

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . /cocktail-maker

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

RUN rm -f /cocktail-maker/uv.lock /cocktail-maker/pyproject.toml

ENV PATH="/cocktail-maker/.venv/bin:$PATH"

WORKDIR /cocktail-maker/app

ENTRYPOINT []

CMD ["gunicorn", "main:cocktail_maker", "--config", "gunicorn.conf.py"]
