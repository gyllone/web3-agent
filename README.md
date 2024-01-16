# Trading GPT

## Installation
```bash
conda create -n gonswapGPT python=3.11
conda activate gonswapGPT
conda install -y 'langchain[all]' -c conda-forge
conda install pydantic -c conda-forge
pip install langchain-experimental
pip install tavily-python
pip install httpx
pip install openai
pip install web3
pip install fastapi
pip install uvicorn
pip install argparse
pip install nest_asyncio
pip install mypy
pip install "redis[hiredis]"
```

## Export env
```bash
# win
conda env export --no-builds | findstr /v "prefix:" > environment.yml
# unix
conda env export --no-builds | grep -v "^prefix:" > environment.yml
```

## Import env
```bash
conda env create -f environment.yml
```

# TODO
- [ ] Refactor function modules to BaseModel