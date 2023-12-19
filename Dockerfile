FROM condaforge/mambaforge

LABEL authors="Lone"

WORKDIR /gonswapGPT

COPY . /gonswapGPT

RUN mamba env create -f /gonswapGPT/environment.yml

EXPOSE 8901

ENTRYPOINT [ \
    "conda", "run", "--no-capture-output", "-n", "gonswapGPT", \
    "python", "/gonswapGPT/app/run_svc.py", "--host=127.0.0.1", "--port=8901", \
    "--model-config=/gonswapGPT/.config/model.json", "--chain-config=/gonswapGPT/.config/chain.json"  \
]