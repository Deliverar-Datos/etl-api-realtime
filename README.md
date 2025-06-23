# etl-api-realtime

For running the app

uvicorn main:app --reload


To delete PyCache if generated 

Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force