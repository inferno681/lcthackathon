ARG PG_MAJOR=16
FROM postgres:$PG_MAJOR
ARG PG_MAJOR

RUN apt-get update && \
apt-mark hold locales && \
apt-get install -y --no-install-recommends build-essential postgresql-server-dev-$PG_MAJOR git ca-certificates && \
cd /tmp && \
git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git && \
cd /tmp/pgvector && \
make clean && \
make OPTFLAGS="" && \
make install && \
mkdir /usr/share/doc/pgvector && \
cp LICENSE README.md /usr/share/doc/pgvector && \
rm -r /tmp/pgvector && \
apt-get remove -y build-essential postgresql-server-dev-$PG_MAJOR && \
apt-get autoremove -y && \
apt-mark unhold locales && \
rm -rf /var/lib/apt/lists/*

CMD ["postgres"]
