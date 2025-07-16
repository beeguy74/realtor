FROM rabbitmq:management

# Expose the default RabbitMQ ports for documentational purposes only
EXPOSE 5672 15672 


# Optional: Enable management plugin (already enabled in rabbitmq:management)
# RUN rabbitmq-plugins enable rabbitmq_management

# Optional: Copy custom configuration files
# COPY rabbitmq.conf /etc/rabbitmq/
# COPY definitions.json /etc/rabbitmq/

CMD ["rabbitmq-server"]