FROM ubuntu:16.04

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
&& sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
&& apt-get clean \
&& apt-get update \
&& apt-get install -y python3-pip python3-dev supervisor \
&& python3 -m pip install --upgrade pip -i https://pypi.douban.com/simple

COPY supervisord.conf /etc/supervisord.conf
COPY printyun.conf /etc/supervisor/
COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
&& rm -rf /etc/supervisor/supervisord.conf


EXPOSE 8001
CMD ["supervisord", "-c", "/etc/supervisord.conf"]