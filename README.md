# Инструкци по использованию
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

6) Переходи к самому интерессному! В файле embedder_model.py написан код, который загружает модель для создания эмбеддингов, и код, который разбивает текст документа на чанки а далее слхраняет его в БД. Но пока БД у нас нет 

7) Запускаем векторную БД! Для запуска БД нужно ввести команду 
```python
docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```
После чего docker сам установит и зпаустит её. Так же мы указываем ''-v qdrant_storage:/qdrant/storage'' тем самым мы будет сохранять нашу базу. После выполнения этой команды запускаем скрипт bd_settings.py. Он применет настройки к нашей БД

8) Осталось всё это слекить воедино. Для этого у нас есть скрипт rag.py
В нём:
- Создаётся приложение FastApi 
- Задаётся системный промт
- Создаётся вход для наших запросов 
После поступления запроса он превращается в вектор. 
После это твектор отправляется в БД, чтобы там нашли топ 5 самых близских по смыслу кусков.
hits - это список всех найденных текстов. Мы склеиваем его в один большой, который потом передаётся LLM.
Далее происходит генерация ответа:
system - всталяется инструкция, которая была в начале скрипта + найденный контекст.
user - передаёт оригинальный вопрос пользователя 
Далее в скрипте формируется итоговый JSON, который получает пользователь. В него входит ответ и ресурс откуда он был получен. 

9) И так мы проделали все шаги выше. Теперь, чтобы всё работало нужно:
- Запустить БД `docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant`
- добавить свой документ скриптом embedder_model.py
- Запустить llama `.\test.ps1`
- Запустить FastAPI server `uvicorn rag:app --host 0.0.0.0 --port 8000`
Теперь переходим по адрессу `http://localhost:8000/docs` и тестируем!