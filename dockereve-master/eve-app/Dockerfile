FROM python:3.4-onbuild

WORKDIR /usr/src/app

ADD . /usr/src/app

RUN pip3 install -r requirements.txt
RUN pip3 install pytest pyjwt bcrypt requests flask_cors
RUN sed -i 's/\[scheme\]/\["https"\]/' /usr/local/lib/python3.4/site-packages/eve_swagger/objects.py

RUN cp /usr/src/app/*.cfg /usr/local/lib/python3.4/site-packages/eve/
RUN cat /usr/local/lib/python3.4/site-packages/eve/*.cfg

#EXPOSE 5000
#CMD ["python3", "server.py"]

