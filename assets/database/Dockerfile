FROM postgres:15-alpine

# Set the timezone
RUN apk add --no-cache tzdata
ENV TZ=UTC

# Create a directory for initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Optional: Copy custom initialization scripts
# COPY init.sql /docker-entrypoint-initdb.d/

# Optional: Copy custom PostgreSQL configuration
# COPY postgresql.conf /etc/postgresql/postgresql.conf

# Set default environment variables (can be overridden by docker-compose)
ENV POSTGRES_DB=realtor
ENV POSTGRES_USER=db_user
ENV POSTGRES_PASSWORD=secure_password

# Expose the PostgreSQL port
EXPOSE 5432

# The postgres image already has the correct CMD, so we don't need to override it