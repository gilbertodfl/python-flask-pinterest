print(">>> MAIN.PY FOI EXECUTADO <<<", flush=True)

from pinterest import app

print(">>> PINTEREST FOI IMPORTADO <<<", flush=True)

if __name__ == "__main__":
    app.run(debug=True)