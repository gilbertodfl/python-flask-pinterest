from pinterest import app
## o app.run() inicia o servidor Flask e o modo debug=True permite que o servidor
## seja reiniciado automaticamente sempre que houver uma alteração no código-fonte
if __name__ == "__main__":
    app.run(debug=True)


