$pyCode = 'import bootstrap; from llama_cpp.server.__main__ import main; main()'

$pyArgs = @(
    '-c', $pyCode,
    '--model', 'C:/myRAG/models/GigaChat3.1-10B-A1.8B-q4_K_M.gguf',
    '--n_gpu_layers', '999',
    '--n_ctx', '8192',
    '--port', '8080'
)

python @pyArgs