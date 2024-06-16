if [ ! -f ./data/llava-llama-3-8b-v1_1-mmproj-f16.gguf ]; then
    wget -P ./data https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf/resolve/main/llava-llama-3-8b-v1_1-mmproj-f16.gguf
fi

if [ ! -f ./data/llava-llama-3-8b-v1_1-int4.gguf ]; then
    wget -P ./data https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf/resolve/main/llava-llama-3-8b-v1_1-int4.gguf
fi

if [ ! -f ./data/OLLAMA_MODELFILE_INT4 ]; then
    wget -P ./data https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf/resolve/main/OLLAMA_MODELFILE_INT4
fi

sudo docker compose -f docker-compose-api-prod.yaml exec ollama ollama create llava-llama3-int4 -f ./root/.ollama/OLLAMA_MODELFILE_INT4
sudo docker compose -f docker-compose-api-prod.yaml exec ollama ollama run llava-llama3-int4
