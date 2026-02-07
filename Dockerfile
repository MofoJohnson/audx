
FROM astral/uv:python3.14-trixie-slim

# install ffmpeg
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# TODO specify version tag
ARG AUDX_VERSION=0.1.2
RUN uv tool install "audx==${AUDX_VERSION}"

WORKDIR /audx

ENTRYPOINT ["audx"]
