FROM python:3.14.0-slim-trixie
ARG INSTALL_DEV_DEPENDENCIES

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
RUN apt update && apt install -y sudo git

# User
RUN groupadd -g 1000 -o debian
RUN useradd -m -u 1000 -g 1000 -o -s /bin/bash debian
RUN echo "debian ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
ENV PATH "/home/debian/.local/bin:${PATH}"

ENV WORKDIR /app
WORKDIR $WORKDIR
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

RUN rm /usr/local/bin/pip
COPY --from=ghcr.io/astral-sh/uv:0.9.5-python3.14-trixie-slim /usr/local/bin/uv /usr/local/bin/uv

COPY . $WORKDIR/
RUN uv pip install --system -r pyproject.toml ${INSTALL_DEV_DEPENDENCIES}

RUN rm -rf /tmp/*

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]