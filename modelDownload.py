from transformers import MarianTokenizer, MarianMTModel
model_name = "Helsinki-NLP/opus-mt-nl-en"
tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir="./models")
model = MarianMTModel.from_pretrained(model_name, cache_dir="./models")
