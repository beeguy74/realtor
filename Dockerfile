FROM rabbitmq:management

# Expose the default RabbitMQ ports
EXPOSE 5672 15672

# Optional: Set environment variables
ENV RABBITMQ_DEFAULT_USER=admin
ENV RABBITMQ_DEFAULT_PASS=password

# Optional: Enable management plugin (already enabled in rabbitmq:management)
# RUN rabbitmq-plugins enable rabbitmq_management

# Optional: Copy custom configuration files
# COPY rabbitmq.conf /etc/rabbitmq/
# COPY definitions.json /etc/rabbitmq/

CMD ["rabbitmq-server"]