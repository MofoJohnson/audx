FROM astral/uv:python3.14-trixie-slim

# install ffmpeg
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# TODO specify version tag
RUN uv tool install audx

WORKDIR /audx

ENTRYPOINT ["audx"]
