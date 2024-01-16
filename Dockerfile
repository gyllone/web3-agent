FROM condaforge/mambaforge

LABEL authors="Lone"

WORKDIR /gonswapGPT

COPY . /gonswapGPT

RUN mamba env create -f /gonswapGPT/environment.yml

EXPOSE 8901

ENV OPENAI_API_KEY="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" \
    TAVILY_API_KEY="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"

ENTRYPOINT [ \
    "conda", "run", "--no-capture-output", "-n", "gonswapGPT", \
    "python", "/gonswapGPT/app/run_svc.py", "--host=127.0.0.1", "--port=8901", \
    "--model-config=/gonswapGPT/.config/model.json", "--chain-config=/gonswapGPT/.config/chain.json"  \
]