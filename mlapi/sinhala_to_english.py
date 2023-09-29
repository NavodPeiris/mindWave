from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_1.2B")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_1.2B")

def sinhala_to_english(text):

    # translate sinhala to english
    tokenizer.src_lang = "si"
    encoded_si = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(**encoded_si, forced_bos_token_id=tokenizer.get_lang_id("en"))
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return result[0]

'''
ans = sinhala_to_english("මට මානසික ලෙඩක්ද?")
print(ans)
'''