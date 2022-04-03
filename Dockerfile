FROM python:3.6.15


ENV TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"

RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

COPY . /app
WORKDIR /app

RUN pip install -i ${PIPURL} --upgrade pip \
    && pip install -i ${PIPURL} -r requirements.txt \
    && chmod +x start.sh

CMD ./start.sh
