import numpy as np
import nltk
import string
import random

#importing and initialising tkinter framework
from tkinter import *
from functools import partial
main = Tk()


#Importing and reading the corpus
f=open('chatbot.txt','r',errors='ignore')
doc=f.read()
doc=doc.lower()
nltk.download('punkt')
nltk.download('wordnet')
sent_tokens=nltk.sent_tokenize(doc)
word_tokens=nltk.word_tokenize(doc)


#Example of sentence tokens
#print(sent_tokens[:2])
#print(word_tokens[:2])


#Text Processing
lemmer=nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict=dict((ord(punct),None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


#define the greeting function
Greet_inputs=("hello","hi","greetings","what's up","hey")
Greet_responses=["hi","hey","nods","hi there","hello","I am glad!you are talking to me"]
def greet(sentence):

    for word in sentence.split():
        if word.lower() in Greet_inputs:
            return random.choice(Greet_responses)

#Response Generation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def response(user_response):
    robo_response=''
    TfidfVector=TfidfVectorizer(tokenizer=LemNormalize,stop_words='english')
    tfidf=TfidfVector.fit_transform(sent_tokens)
    vals=cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat=vals.flatten()
    flat.sort()
    req_tfidf=flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I dont understand you"
        return robo_response
    else:
        robo_response=robo_response+sent_tokens[idx]
        return robo_response



#defining conversation start/end protocols

flag=True
def ask_from_bot():
    user_response=textF.get()
    msg.insert(END, "you :"+user_response)
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you'):
            flag=False
            msg.insert(END,"BOT: You are Welcome...")

        else:
            if(greet(user_response)!=None):
                msg.insert(END,"BOT: "+greet(user_response))
            else:
                sent_tokens.append(user_response)
                word_tokens=nltk.word_tokenize(user_response)
                final_words=list(set(word_tokens))
                msg.insert(END,"BOT: "+response(user_response))
                sent_tokens.remove(user_response)
                msg.yview(END)


    else:
        flag=False
        msg.insert("BOT: Goodbye! Take Care...")


main.geometry("500x650")  # width*height
main.title("My Chat Bot")
img = PhotoImage(file="chatbot1.png")
photoL = Label(main, image=img,text='corona chatbot')
photoL.pack(pady=10)

frame = Frame(main)
label=Label(text="CORONA CHATBOT",font=("verdana",20))
label.pack()
sc = Scrollbar(frame)
#sc=Scrollbar(frame,orient='horizontal')
msg = Listbox(frame, width=200, height=20,yscrollcommand=sc.set)

sc.pack(side=RIGHT, fill=Y)
#sc.pack(side =BOTTOM, fill=X)
frame.pack()
msg.pack(side=LEFT, fill=BOTH, pady=10)

# creating text field

textF = Entry(main,width=20,font={"Verdana", 30})  # 20 is font size
textF.pack(fill=X, pady=10)

btn = Button(main, text="Ask from Bot", font=("Verdana", 20), command=ask_from_bot,pady=20)
btn.pack()


#creating an enter button so that we don't need to click the ask from bot button
def enter_key_press(event):
    btn.invoke()

#going to ind main window with enter key
main.bind('<Return>', enter_key_press)
main.mainloop()

