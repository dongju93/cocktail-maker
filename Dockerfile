FROM python:3.13.1-alpine

WORKDIR /maker

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

ENV UV_COMPILE_BYTECODE=1

RUN uv sync --frozen --no-group dev

COPY . .

WORKDIR /maker/app

CMD ["uv", "run", "fastapi", "run"]
