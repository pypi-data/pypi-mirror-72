FROM sf-solidity

COPY --chown=sf:sf app /home/sf/exercise/app

{% include 'file-copy.tpl' %}
