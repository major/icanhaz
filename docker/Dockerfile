FROM fedora:20

RUN yum -y install httpd mod_wsgi python-flask traceroute && yum clean all
RUN mkdir -vp /var/www/html/icanhaz-app/icanhaz/

RUN useradd icanhaz

ADD icanhaz.wsgi /var/www/html/icanhaz-app/icanhaz.wsgi
ADD icanhaz-app.conf /etc/httpd/conf.d/icanhaz-app.conf
ADD icanhaz-config.stub /etc/httpd/conf.d/icanhaz-config.stub
ADD icanhaz.py /var/www/html/icanhaz-app/icanhaz/icanhaz.py
RUN echo "ServerTokens Prod" >> /etc/httpd/conf.d/servertokens.conf
RUN echo "ServerName icanhazip.com" >> /etc/httpd/conf.d/servername.conf

EXPOSE 80
ENTRYPOINT ["/usr/sbin/httpd"]
CMD ["-D", "FOREGROUND"]
