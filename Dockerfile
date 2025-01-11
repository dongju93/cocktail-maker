FROM python:3.13.1-alpine

WORKDIR /maker

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . /maker

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
    
RUN rm -f /maker/uv.lock /maker/pyproject.toml

ENV PATH="/maker/.venv/bin:$PATH"

WORKDIR /maker/app

ENTRYPOINT []

CMD ["fastapi", "run"]
