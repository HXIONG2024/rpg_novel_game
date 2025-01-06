from crewai import LLM

gpt_model_name = "gpt-4o-mini"
gemini_model_name = "gemini/gemini-2.0-flash-exp"
mistral_model_name = "mistral/mistral-large-latest"




novel_llm = LLM(
    model=gemini_model_name, # change your model here to see different novel writing by different models
    temperature=0.7
)

mistral_llm = LLM(
    model="mistral/mistral-large-latest",
    temperature=0.7
)

gemini_llm_15 = LLM(
    model="gemini/gemini-1.5-flash"
)
