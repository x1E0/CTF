import time
import socket
import tor_req as tor
import requests as req
from bs4 import BeautifulSoup

def answer_trivia():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('chall.2019.redpwn.net',6001))
    i = 0
    #grabs the intro phrase from the server
    # and skips it: "Welcome to Tux Trivia Show!!!"
    data = sock.recv(30)
    
    cache = {}
    
    while True:                
        data = sock.recv(1024)                    
        d = data.decode('utf-8').strip()
        print(d)
        #time.sleep(3)
        if "flag" in d:
            print(d)
        elif "Correct" in d:
            pass
        elif "INCORRECT" in d:
            pass
        else:
            country = d[d.index('of') + 3:d.index('?')]
            
            #I made a cache for the country:capital values bc I was pissing google off with too many queries
            if country in cache:
                reply = cache[country].encode('utf-8')
                print(reply)
                sock.send(reply)                

            #this block handles querying normally
            else:                
                reply = get_country_capital(d)
                print(reply)            
                try:
                    cache[country] = reply
                    sock.send(reply.encode('utf-8'))
                    i += 1
                except:
                    print(i)                
    
                    if (not data):
                        break

    

def get_country_capital(query):
    #handles all edge cases I seemd to have
    if query == "What is the capital of Kazakhstan?":
        return "Astana"
    
    if query == "What is the capital of Ukraine?":
        return "Kiev"
    
    if query == "What is the capital of Switzerland?":
        return "Bern"
    
    if query == "What is the capital of Minnesota?":
        return "St. Paul"
    
    if query == "What is the capital of Marshall Islands?":
        return "Majuro"
    
    if query == "What is the capital of New York?":
        return "Albany"

    if query == "What is the capital of Kuwait?":
        return "Kuwait City"
        
    
    r = req.get("https://www.google.com/search?q="+query)    
    soup = BeautifulSoup(r.text, "html.parser")
    divs = soup.find_all("div")    
    
    for item in divs:
        if(len(item.text) > 30):
            continue
        else:
            if "BNeawe" and "AP7Wnd" in str(item):                
                if "/" in item.text:
                    continue
                else:
                    if ("-" and "Wikipedia") in item.text:
                        return item.text[:item.text.index('-')]
                    else:
                        return item.text
            
answer_trivia()
#print(get_country_capital("What is the capital of California?"))
