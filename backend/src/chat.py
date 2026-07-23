from backend.src.rag.rag_chain import ask

print("Asistente RAG - Ministerio de Salud")
print("Escribe 'salir' para terminar.\n")

while True:
    question = input("Tú: ")

    if question.lower() == "salir":
        break

    result = ask(question)

    print("\nAsistente:")
    print(result["answer"])

    print("\nFuentes:")
    for s in result["sources"]:
        print("-", s)

    print()