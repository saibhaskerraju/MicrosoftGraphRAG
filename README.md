# MicrosoftGraphRAG
First GraphRAG using Neo4j

#### How to run locally in PRD mode

- make sure you have `.env.local` file. replace all valeus from `.env`.
- run `docker compose up --build` in your terminal.

#### How to run in devContainer mode

- open in dev container mode using command pallete `ctrl+shift+p`
- the `postStartCommand` will take care of initial steps
- once setup is ready, in your terminal, navigate to `backend` and type
`source .venv/bin/activate`


### uv commands

#### activate environment

- as of now it is mentioned in `postStartCommand` of `devcontainer.json`

- another way is, type in terminal `source .venv/bin/activate`

#### list packages

- ` uv pip list`

#### install from lock file only

- `uv sync --frozen --no-cache`


#### Notes on Docker Pre-commit

- Tried developing `pre-commit` in docker rather than host system.
- able to get `staged` file names from `pre-commit` hook.
- figured out a way to pass to docker compose
- `pre-commit.yaml` will do the required stuff and finally able to move the files back to org dest using volumes.
- the problem here is, developers need to stage them again and then commit it and it is a long process.