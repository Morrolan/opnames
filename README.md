# opnames

Generates British military-style operation code names, from the command line or a small FastAPI app.

## Command line

```sh
uv run opnames                       # 5 modern-style names
uv run opnames -s ww2 -n 10          # styles: modern, ww2, exercise
uv run opnames -s exercise --seed 42 # repeatable output
```

## Web app

```sh
uv run uvicorn app:app --reload
```

- http://127.0.0.1:8000/ shows one name at a time, with a button for another
- http://127.0.0.1:8000/names?style=ww2&count=5 returns JSON
- http://127.0.0.1:8000/docs is the Swagger UI

## Licence

MIT — see [LICENSE.txt](LICENSE.txt).
