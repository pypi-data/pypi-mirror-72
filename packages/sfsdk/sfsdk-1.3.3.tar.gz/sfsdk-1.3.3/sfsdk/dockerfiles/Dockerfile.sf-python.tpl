FROM sf-python

COPY --chown=sf:sf app /home/sf/exercise/app

# Uncomment the next line to install your project requirements
#RUN pip3 install -r /home/sf/exercise/app/requirements.txt

{% include 'file-copy.tpl' %}
