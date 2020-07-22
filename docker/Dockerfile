FROM debian:buster-slim

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        clamav-daemon \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt-/lists/* && \
    freshclam --user clamav
EXPOSE 3310
RUN rm -rf /var/log/clamav/* && \
    ln -s /dev/stdout /var/log/clamav/clamav.log && \
    rm -f /etc/clamav/clamd.conf && \
    mkdir /var/run/clamav && \
    chown clamav:clamav /var/run/clamav
COPY conf.d/clamav.conf /etc/clamav/clamd.conf
    # chown clamav:clamav /var/log/clamav/clamav.log
CMD clamd
