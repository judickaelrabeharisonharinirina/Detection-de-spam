#!/bin/sh
# 1. On lance FastAPI en arrière-plan et on redirige ses logs pour qu'ils s'affichent
uvicorn src.fast:app --host 0.0.0.0 --port 8000 > /var/log/fastapi.log 2>&1 &

# 2. On attend 2 secondes que FastAPI s'initialise
sleep 2

# 3. On lance Streamlit au premier plan
streamlit run app.py --server.port 8501 --server.address 0.0.0.0