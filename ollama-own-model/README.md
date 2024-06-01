# Hugging Face safetensors models with Ollama


Download a model

```bash
hfdownloader -m NousResearch/Hermes-2-Theta-Llama-3-8B
```

Create model

```bash
ollama create \
  -f Modelfile NousResearch-Hermes-2-Theta-Llama-3-8B
```

Create quantized model

```bash
ollama create \
  -f Modelfile NousResearch-Hermes-2-Theta-Llama-3-8B:q4_0 \
--quantize q4_0
```

Run model

```bash
ollama run --verbose NousResearch-Hermes-2-Theta-Llama-3-8B:q4_0 \
  What would happen in a fight between a lion and a unicorn
```