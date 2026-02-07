FROM astral/uv:python3.14-trixie-slim

# TODO specify version tag
RUN uv tool install audx

WORKDIR /audx

ENTRYPOINT ["audx"]
