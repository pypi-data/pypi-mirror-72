FROM sf-ruby

COPY --chown=sf:sf app /home/sf/exercise/app

# Uncomment the next lines to setup rvm environment and gem files
#RUN cd /home/sf/exercise/app/ \
#  && /usr/local/rvm/bin/rvm install 2.6.2 \
#  && gosu sf bash -l -c 'rvm use 2.6.2 --default'

{% include 'file-copy.tpl' %}
