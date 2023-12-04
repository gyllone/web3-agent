# Trading GPT

## Installation
```bash
conda install -y 'langchain[all]' -c conda-forge
conda install pydantic -c conda-forge
pip install web3
pip install fastapi
pip install uvicorn
pip install "redis[hiredis]"
```

## Export env
```bash
# win
conda env export --no-builds | findstr /v "prefix:" > environment.yml
# unix
conda env export --no-builds | grep -v "^prefix:" > environment.yml
```