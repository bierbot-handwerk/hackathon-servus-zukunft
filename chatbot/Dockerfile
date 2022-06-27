# Extend the official Rasa SDK image
FROM rasa/rasa-sdk

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY ./rasa_project/actions/requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r requirements-actions.txt

# Copy actions folder to working directory
COPY ./rasa_project/actions /app/actions

# ENTRYPOINT [ "/bin/sh" ]
# By best practices, don't run the code with root user
#USER 1001
