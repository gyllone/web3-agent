FROM condaforge/mambaforge

LABEL authors="Lone"

WORKDIR /tradingGPT

COPY . /tradingGPT

RUN mamba env create -f /tradingGPT/environment.yml

EXPOSE 8901

ENTRYPOINT [ \
    "conda", "run", "--no-capture-output", "-n", "tradingGPT", \
    "python", "/tradingGPT/app/run_svc.py" \
]