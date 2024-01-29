#!/bin/zsh

export OPENAI_API_KEY="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"
export TAVILY_API_KEY="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"

conda run --no-capture-output -n gonswapGPT \
python app/run_svc.py \
  --host="127.0.0.1" \
  --port=8105 \
  --model-config=".config/model.json" \
  --chain-config=".config/chain.json"
