FROM python:3.14.0-slim-trixie
ARG INSTALL_DEV_DEPENDENCIES

ENV UV_PROJECT_ENVIRONMENT=/usr/local/ \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy

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

COPY pyproject.toml uv.lock $WORKDIR/
RUN uv sync --frozen ${INSTALL_DEV_DEPENDENCIES}


COPY . $WORKDIR/
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]