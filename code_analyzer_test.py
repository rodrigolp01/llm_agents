# test_llm.py
from code_analyzer import CodeOptimizerLLM

def main():
    # Cria uma instância do otimizador de código LLM
    code_optimizer = CodeOptimizerLLM()
    #code_optimizer_bert = CodeOptimizerBERT()
    
    # Trecho de código para teste
    code_snippet = """
n = input('Digite o texto todo em maiúscula: ')
res = n.isupper()

while res != True:
  n = input('Texto errado, digite tudo em maiúscula: ')
  res= n.isupper()
  continue

if res == True:

  print('Texto correto!'
"""
    # Gera sugestões a partir do código
    suggestions = code_optimizer.generate_suggestions(code_snippet)

    #predicted_class, probabilities = code_optimizer_bert.generate_suggestions(code_snippet)

    # Imprime as sugestões
    print("Código de entrada:")
    print(code_snippet)
    print("\nSugestões:")
    print(suggestions)

    #print("\nSugestões bert:")
    #print(predicted_class)

if __name__ == "__main__":
    main()
