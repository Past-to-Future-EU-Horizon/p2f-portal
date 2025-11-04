FROM ghcr.io/astral-sh/uv:python3.13-trixie

WORKDIR /p2f/portal

ADD . .

EXPOSE 8082

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/ uv sync --locked

ENV PATH="/p2f/portal/.venv/bin/:$PATH"

CMD [ "streamlit", "run", "/p2f-api/Past_2_Future_Portal.py" ]