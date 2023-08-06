FROM cbaxter1988/vse:base

COPY env.py /
COPY run.py /


COPY vse /vse


CMD python run.py --serve_rest