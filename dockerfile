FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /p2f/portal

RUN apk update
RUN apk upgrade
RUN apk add git

ADD . .

EXPOSE 8082

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/ uv sync 

ENV PATH="/p2f/portal/.venv/bin/:$PATH"

# CMD ["/bin/bash"]
CMD [ "streamlit", "run", "p2f-portal/entry.py" ]