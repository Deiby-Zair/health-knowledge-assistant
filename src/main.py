from src.rag_chain import ask

question = input("¿Qué es la afiliación al sistema de salud?")

result = ask(question)

print("\nRESPUESTA:\n")
print(result["answer"])

print("\nFUENTES:\n")
for s in result["sources"]:
    print("-", s)