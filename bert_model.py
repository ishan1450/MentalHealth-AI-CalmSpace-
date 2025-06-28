from transformers import BertTokenizer, BertForSequenceClassification
import torch
import logging
tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

def sentiment_analysis(user_input):
    input = tokenizer(user_input,return_tensors="pt",truncation=True,padding=True)
    output = model(**input)
    prob = torch.nn.functional.softmax(output.logits,dim=1)
    score = torch.argmax(prob,dim=1).item()
    

    if score<=2:
        return "negative"
    
    elif score==3:
        return "neutral"

    else:
        return "positive"

        