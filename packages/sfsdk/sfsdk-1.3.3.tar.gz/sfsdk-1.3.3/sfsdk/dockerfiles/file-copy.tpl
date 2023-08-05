{% for path in paths %}COPY --chown=sf:sf fs/{{path}} {{path}}
{% endfor %}
