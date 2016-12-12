import urllib.request as ur, re, os, time, html.parser, json, math
from flask import Flask
from flask import url_for, render_template, request, redirect

def phrase(text):
    whole_phrase = re.findall("(-lexeme.+?trans_ru:.+?)-", text, flags=re.DOTALL)
    return whole_phrase

def udmword(whole_phrase):
    udm = re.findall("lex: (.+?)\n", whole_phrase, flags=re.DOTALL)
    return udm

def rusdef(whole_phrase):
    rus = re.findall("trans_ru: (.+?)\n", whole_phrase, flags=re.DOTALL)
    return rus

def part(whole_phrase):
    part = re.findall("gramm: (.+?)\n", whole_phrase, flags=re.DOTALL)
    return part

def file(namefile,dictionary):
    s = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii = False)
    file = open(namefile, "w", encoding = "utf-8")
    file.write(s)
    file.close()
    return file

def main():
    i = 1
    d = {}
    d3 = {}
    for x in range(1,3):
        rou = 'D:\\proga\\cr\\' + 'dict' + str(i) + '.txt'
        f = open(rou, 'r', encoding = 'utf-8')
        text = f.read()
        phrases = phrase(text)
        for one in phrases:
            udm = ''.join(udmword(one))
            rus = ''.join(rusdef(one))
            par = ''.join(part(one))
            mass = [rus, par]
            if rus != '':
                d[udm] = mass
                udmstr = str(udm) + '%%%' + str(par)
                d3[udmstr] = rus
        i += 1
        f.close()
    file('first.txt',d)
    return d3

def main2():
    d2 = {}
    d3 = main()
    for udm in d3:
        russep = re.split('[0-9].|, ',d3[udm])
        for x in russep:
            x.strip()
        for n in russep:
            if n == '':
                russep.remove(n)
        d3[udm] = russep
        mas = ''
        for word in russep:
            if str(d2.get(word)) == 'None':
                d2[word] = udm
            else:
                if mas == '':
                    mas = str(d2.get(word)) + '***' + str(udm)
                else:
                    mas = mas + '***' + str(d2.get(word)) + '***' + str(udm)
                d2[word] = mas
                mas = ''
    for p in d2:
        sep = d2[p].split('***')
        d2[p] = sep
    for r in range(0,len(d2[p])):
        d2[p][r] = d2[p][r].split('%%%')
    file('third.txt',d3)
    file('second.txt',d2)

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/search')
def search():
    file = open('first.txt', "r", encoding = "utf-8")
    results = file.read()
    data = json.loads(results)
    file.close()
    if request.args:
        name = request.args['name']
        rus = str(data[name][0])
        return render_template("result.html", name = name, rus = rus)
    else:
        return render_template("main_page.html")

if __name__ == '__main__':
    main()
    main2()
    app.run(port = 5004, debug=True)
