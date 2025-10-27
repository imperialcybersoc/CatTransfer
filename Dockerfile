FROM python:3.11-slim
ENV LOG_DIR=".hidden"
ENV PORT=8080
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir Flask==2.3.2 werkzeug==3.0.0
RUN printf 'ICCYBERSOC{lf1_2_rc3_bruh_41424344}\n' > /another_flag.txt
RUN useradd -m -s /bin/bash www
RUN printf 'ICCYBERSOC{whoopsies}\n' > /root/omds_its_a_flag.txt && chmod 400 /root/omds_its_a_flag.txt
WORKDIR /srv
RUN mkdir -p ${LOG_DIR} /srv/uploads
COPY . /srv
RUN chown -R www:www /srv
EXPOSE 8080 6969
CMD sh -c "python3 /srv/admin.py 6969 & su -c 'python3 /srv/app.py' www"