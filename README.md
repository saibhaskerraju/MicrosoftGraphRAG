# MicrosoftGraphRAG
First GraphRAG using Azure Cloud Services

#### How to run locally

- make sure you have `.env.local` file. replace all valeus from `.env`.
- run `docker compose up --build` in your terminal.

### uv commands

#### activate environment

- as of now it is mentioned in `postStartCommand` of `devcontainer.json`

- another way is, type in terminal `source .venv/bin/activate`

#### list packages

- ` uv pip list`

#### install from lock file only

- `uv sync --frozen --no-cache`
