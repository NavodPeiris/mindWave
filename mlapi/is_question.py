from langchain import PromptTemplate
from langchain import LLMChain
from langchain.llms import CTransformers

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

CUSTOM_SYSTEM_PROMPT="You are an advanced assistant that tells whether a text is a question or not. you only return True or False as a response"

def is_question(text):
    print("text : ", text)
    instruction = f"is following text a question" + ": \n\n {text}"

    SYSTEM_PROMPT = B_SYS + CUSTOM_SYSTEM_PROMPT + E_SYS

    template = B_INST + SYSTEM_PROMPT + instruction + E_INST

    print(template)
    prompt = PromptTemplate(template=template, input_variables=["text"])

    llm = CTransformers(model='llama2\llama-2-7b-chat.ggmlv3.q4_0.bin',
                        model_type='llama',
                        config={'max_new_tokens': 128,
                                'temperature': 0.01}
                    )
    LLM_Chain=LLMChain(prompt=prompt, llm=llm)

    return LLM_Chain.run(text)

'''
ans = is_question("The medicine was drank")
print(ans)
'''