#https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest
from django.http import HttpResponse
from . import preprocess
from django.shortcuts import redirect
from . import lemmatization

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax

from sentiment_api.models import Positive,Negative,Neutral
from sentiment_api.serializers import PositiveSerializer,NegativeSerializer,NeutralSerializer
# Preprocess text (username and link placeholders)
#print("%%%%%%%%%%%%%%%%%%%%%%%%%%% : ",preprocess.sum(4,5))


from django.shortcuts import render

def home(request):

    # mydata = ProductDescription.objects.all().values()
    # template = loader.get_template('display.html')
    # context = {
    #     'mymembers': mydata,
    # }
    # return HttpResponse(template.render(context, request))
    return render(request,'home.html')

# def large_text_area(request):
#     if request.method == 'POST':
#         form = LargeTextAreaForm(request.POST)
#         #https://stackoverflow.com/questions/4706255/how-to-get-value-from-form-field-in-django-framework
#         print("Form ############# : ",form.data['content'])
#         #return render(request, 'thank_you.html')
#         text=form.data['content']
#         #preprocess_index(text)
#         #return redirect('/nlp/')
    
#         # if form.is_valid():
#         #     form.save()
#         #     return render(request, 'thank_you.html')

#     else:
#         form = LargeTextAreaForm()
    
#     return render(request, 'large_text_area.html', {'form': form})


def preprocess_index(request):
    new_text = []
    if(request.method=='POST'):
        text=request.POST["search"]
        text_store=text
        print("Search &&&&&&&&&&&&&&&&&&&& ",text)
    else:
        print("ERORRRRRRRRRRRRRRRRRRRRRRRRR")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ : ",text)
    def preprocess1(text):
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    # PT
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    #model.save_pretrained(MODEL)
    #text = "This is herrrrrrrrrrrrr can't \\ first day K-a-j-a-l. Thi*s is $100.05 at this place.\n Please,\t Be nice to her.\\n"
    #"Covid cases are incrosing"
    
    #print("text BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",text)
    text = preprocess.text_preprocess(text)
    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBB  :  ",text)
    text = lemmatization.text_lemmatization(text)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA :  ",text)
    encoded_input = tokenizer(text=text,padding=True, truncation=True,return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    # # TF
    # model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)
    # model.save_pretrained(MODEL)
    # text = "Covid cases are increasing fast!"
    # encoded_input = tokenizer(text, return_tensors='tf')
    # output = model(encoded_input)
    # scores = output[0][0].numpy()
    # scores = softmax(scores)
    # Print labels and scores
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    list_=[]
    senti=[]
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        senti.append(l)
        list_.append(s)
        #print("YYYYYYYYYYYYYYYYYYYYYYYYYYY : ",s)
        print(f"sent  {i+1}) {l} {np.round(float(s), 4)}")
    print("********************* : ",list_,"\n",senti)
    if(senti[0]=='neutral'):
        values_=Neutral(text=text,sentiment='neutral')
        values_.save()
        #print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSS")

    if(senti[0]=='negative'):
        values_=Negative(text=text,sentiment='neutral')
        values_.save()

    if(senti[0]=='positive'):
        values_=Positive(text=text,sentiment='neutral')
        values_.save()

    return HttpResponse("Hello, world. You're at the polls index.")


