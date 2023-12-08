# Trading GPT

## Installation
```bash
conda install -y 'langchain[all]' -c conda-forge
conda install pydantic -c conda-forge
pip install openai
pip install web3
pip install fastapi
pip install uvicorn
pip install argparse
pip install nest_asyncio
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

# TestExecutor
Nothing
## Input
- **a** `string` *required*

	This is a description of a.
- **b** `integer` *optional*

	This is a description of b.
- **c** `number` *optional*

	This is a description of c.
- **d** `array` *required*

	This is a description of d.
- **e** `object` *required*

	Nothing

Example:
```json
{
  "a": "hello",
  "b": 123,
  "c": 1.23,
  "d": [
    "hello"
  ],
  "e": {
    "foo": "hello",
    "bar": "hello"
  }
}
```
## Output
- **a** `string`

	This is a description of a.
- **b** `integer`

	This is a description of b.
- **c** `number`

	This is a description of c.
- **d** `array`

	This is a description of d.
- **e** `object`

	Nothing

Example:
```json
{
  "a": "hello",
  "b": 123,
  "c": 1.23,
  "d": [
    "hello"
  ],
  "e": {
    "foo": "hello",
    "bar": "hello"
  }
}
```