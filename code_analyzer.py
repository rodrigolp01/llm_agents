from transformers import AutoModelForCausalLM, AutoTokenizer, GemmaForCausalLM
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import numpy as np

class CodeOptimizerLLM:
    #EleutherAI/gpt-neo-125M, "EleutherAI/gpt-neo-2.7B", Salesforce/codegen-2B-multi, "google/gemma-2-9b", 
    #meta-llama/LLaMA-3.2, gemma, DeepSeek-R1
    def __init__(self, model_name="EleutherAI/gpt-neo-2.7B"):
        # Carregando o modelo LLM e de embedding
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    # função para gerar sugestões
    def generate_suggestions(self, code_snippet):
        prompt = f"Analyze the following Python code and provide suggestions for improvements:\n\n{code_snippet}\n\nSuggestions:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, 
                                      max_length=512, 
                                      num_return_sequences=1,
                                      temperature=0.6,
                                      top_k=50,
                                      top_p=0.95,
                                      do_sample=True)
        
        suggestions = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return suggestions.split("Suggestions:")[1].strip() if "Suggestions:" in suggestions else ""
    

# class CodeOptimizerBERT:
#     def __init__(self):
#         # Carregando o modelo CodeBERT para classificação
#         self.model_name = "microsoft/codebert-base"  # Alternativa: "microsoft/graphcodebert-base" para GraphCodeBERT
#         self.tokenizer = RobertaTokenizer.from_pretrained(self.model_name)
#         self.model = RobertaForSequenceClassification.from_pretrained(self.model_name, num_labels=2)  # Altere num_labels conforme necessário

#     def generate_suggestions(self, code_snippet):
#         # Tokenizando o código de entrada
#         inputs = self.tokenizer(code_snippet, return_tensors='pt', padding=True, truncation=True, max_length=512)

#         with torch.no_grad():
#             outputs = self.model(**inputs)
        
#         # Pegando as probabilidades e a classe prevista
#         probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
#         predicted_class = np.argmax(probs.numpy(), axis=1)

#         return predicted_class[0], probs.numpy()
