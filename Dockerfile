FROM condaforge/mambaforge

LABEL authors="Lone"

WORKDIR /tradingGPT

COPY . /tradingGPT

RUN conda env create -f /tradingGPT/environment.yml

EXPOSE 8901

ENTRYPOINT [
    "conda", "run", "-n", "tradingGPT", \
    "/tradingGPT/app/run_svc.py", \
    "--host=127.0.0.1", \
    "--port=8901", \
    "--env=dev" \
]