1) Создаём проект и помещаем туда веса модели в формате .gguf в моём случае это `GigaChat3.1-10B-A1.8B-q4_K_M`
2) Создаём виртуальное окружение проекта и начинаем скачивать нужные нам библиотеки:
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124
```
- pip install llama-cpp-python - стандартная установка Python-обвязки для `llama.cpp`
- **`--extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu132`** — ключевой модификатор. 
Так же для работы необходимо скачать CUDA 
```bash
winget install -e --id Nvidia.CUDA
```
Сама моделька качается 
```bash
huggingface-cli download ai-sage/GigaChat3.1-10B-A1.8B-GGUF --include "*Q4_K_M.gguf" --local-dir C:\myRAG\models
```

На будущее стоит установить сами библиотеки для RAG системы:
**`qdrant-client`** — клиент для векторной базы данных **Qdrant**
**`sentence-transformers`** — библиотека для создания **эмбеддингов**
**`fastapi`** — современный веб-фреймворк для создания **API**
**`uvicorn`** — **ASGI-сервер**, который запускает приложение на FastAPI
**`pymupdf`** — библиотека для **извлечения текста и данных из PDF**
**`python-docx`** — библиотека для **чтения и создания файлов Microsoft Word**
```bash
pip install qdrant-client sentence-transformers fastapi uvicorn pymupdf python-docx
```

Устанавливаем дополнительные зависимости для сервера 
```bash
pip install 'llama-cpp-python[server]'
```
Эта команда подтянет `sse-starlette` (для Server-Sent Events, которые использует сервер) и другие недостающие пакеты, например `fastapi`, `uvicorn`, `pydantic-settings`.

3) Пишем небольшой скрипт, который будет загружать нужные DLL пакеты до запуска сервера. В репо он называется bootstrap.py
4) Теперь всё готово и можно запускать сервер одной командой
```bash
python -c "import bootstrap; import runpy; runpy.run_module('llama_cpp.server', run_name='__main__')" --model C:/myRAG/models/GigaChat3.1-10B-A1.8B-q4_K_M.gguf --n_gpu_layers 999 --n_ctx 8192 --port 8080
```
5) Переходим в браузере на http://localhost:8080/docs открывается Swagger. Там находим POST запрос `v1/chat/completions` 
Меняем в нём промт и контекст роли модели на нужные нам. Отправляем запрос и ждём ответа. 
```
   {
  "model": "GigaChat3.1-10B-A1.8B-q4_K_M.gguf",
  "messages": [
    {
      "role": "system",
      "content": "Ты добрый друг, который всем всегда помогает"
    },
    {
      "role": "user",
      "content": "Как дела?"
    }
  ]
}
```