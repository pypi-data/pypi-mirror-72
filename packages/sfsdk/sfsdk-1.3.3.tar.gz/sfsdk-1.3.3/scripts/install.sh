cd "$(dirname "$0")"/..

echo y | pip3 uninstall sfsdk; \
  rm -rf dist build; \
  python3 setup.py sdist bdist_wheel && \
  pip3 install --user dist/sfsdk-*.whl
