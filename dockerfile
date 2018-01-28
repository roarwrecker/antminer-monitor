# Image with an installed watcher module
FROM python:3.6.3
COPY ./ ~/
WORKDIR ~/
RUN python -m pip install -r requirements.txt
ENV FLASK_APP="/~/run.py"
# Argument "-u" starts python with unbuffered binary stdout and stderr output. Therefore,
# output can be read via "docker logs <id>"
ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0" ]