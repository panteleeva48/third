import urllib.request
import re
import os
import html

def download_main_page():
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request('https://news.rambler.ru/science/35453301-\
soyuz-s-gruzovikom-progress-ms-04-startoval-s-baykonura/items/', headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
#        print(html)
    return html

def other_pages():
    main_page = download_main_page()
    reg_site = re.compile('</div>\n<a\nhref="(.*?)"\nclass="j-metrics\
__clicks-out-source-subject article-sources__subject"\ntarget="_blank"\nrel="external">\n.*?\n</a>', flags=re.U | re.DOTALL)
    sites = reg_site.findall(main_page)
    sites = sites[:6]
    sites.pop(2)
    return sites

def download_other_pages(page):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(page, headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html

def cleaning(page):
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)  # это рег. выражение находит все тэги
    regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)  # все комментарии
    regFigur1 = re.compile('.*NASA Johnson ', flags=re.U | re.DOTALL)
    regFigur2 = re.compile('Подробнее »РИА Наука#Россия.*', flags=re.U | re.DOTALL)
    clean_t = regComment.sub('', page)
    clean_t = regTag.sub('', clean_t)
    clean_t = regScript.sub('', clean_t)
    clean_t = re.sub('\t','', clean_t)
    clean_t = regFigur1.sub('', clean_t)
    clean_t = regFigur2.sub('', clean_t)
    clean_t = re.sub('\n','', clean_t)
    clean_t = re.sub('  ','', clean_t)
    clean_t = re.sub(r'([а-яА-ЯЁё])([0-9])',r'\1 \2',clean_t)
    clean_t = re.sub(r'([0-9])([а-яА-ЯЁё])',r'\1 \2',clean_t)
    clean_t = re.sub('1034Комментировать\+','',clean_t)
    clean_t = re.sub('© Фото:.*?"РОСКОСМОС"','',clean_t)
    clean_t = re.sub(' МОСКВА, 1 декабря. /ТАСС/.','',clean_t)
    clean_t = re.sub('МОСКВА.*?Новости. ','',clean_t)
    return clean_t

def findingtext(page):
    textstr = ''
    headstr = ''
    htmlstr = download_other_pages(page)
    textreg = re.compile('<p>.*\.</p>', flags=re.U | re.DOTALL)
    headreg = re.compile('<h1.*?</h1>', flags=re.U | re.DOTALL)
    textlist = textreg.findall(htmlstr)
    headlist = headreg.findall(htmlstr)
    for i in textlist:
        textstr = headlist[0] + '. ' + textstr + '\n' + i
    return textstr
    
def makingdirs():
    sites = other_pages()
    i = 0
    for page in sites:
#        print(page)
        htmlstr = findingtext(page)
        htmlstr = cleaning(htmlstr)
        if not os.path.exists('D:\\new\\sites'):
            os.makedirs('D:\\new\\sites')
        filew = open('D:\\new\\sites\\' + str(i) + '.txt', 'w', encoding = 'utf-8')
        final = html.unescape(htmlstr)
        filew.write(final)
        filew.close()
        i += 1

def file(name):
    f = open(name, 'r', encoding = 'utf-8')
    fr = f.read()
    f.close()
    return fr

def setting(num_page):
    fr = file('D:\\new\\sites\\' + str(num_page) + '.txt')
    fr = re.sub('\"|\:|\.',' ', fr)
    fr = fr.split()
    list_fr = []
    for word in fr:
        word = word.strip(',.<>/\'":;?!~-[]{}©—()«»+')
        word = word.lower()
        if word != '':
                list_fr.append(word)
    x = set()
    for p in list_fr:
        x.add(p)
    return x

def making_all_settings():
    sites = other_pages()
    set0 = setting(0)
    set1 = setting(1)
    set2 = setting(2)
    set3 = setting(3)
    set4 = setting(4)
    return set0,set1,set2,set3,set4#множества из каждого сайта

def common():
    set0,set1,set2,set3,set4 = making_all_settings()
    commonwords = set0 & set1 & set2 & set3 & set4
#    print(commonwords)
#    print(set0,set1,set2,set3,set4)
    return commonwords#пересечение множеств

def own():
    set0,set1,set2,set3,set4 = making_all_settings()    
    sum0 = set1 | set2 | set3 | set4
    sum1 = set0 | set2 | set3 | set4
    sum2 = set0 | set1 | set3 | set4
    sum3 = set0 | set1 | set2 | set4
    sum4 = set0 | set1 | set2 | set3
    own0 = set0 - sum0
    own1 = set1 - sum1
    own2 = set2 - sum2
    own3 = set3 - sum3
    own4 = set4 - sum4
#    print(own0,own1,own2,own3,own4)
    return own0,own1,own2,own3,own4#разности множеств

def transform(setting):
    res = ''
    for el in sorted(setting):
        res = res + ', ' + el
    return res

def result():
    commonwords = common()
    commonwords_res = transform(commonwords)
    own0,own1,own2,own3,own4 = own()
    own0_res = transform(own0)
    own1_res = transform(own1)
    own2_res = transform(own2)
    own3_res = transform(own3)
    own4_res = transform(own4) 
    filew = open('D:\\new\\' + 'result.txt', 'w', encoding = 'utf-8')
    result = commonwords_res + '\n' + own0_res + '\n' + own1_res + '\n' + own2_res + '\n' + own3_res + '\n' + own4_res + '\n'
    result = re.sub('^, ','', result)
    result = re.sub('\n, ','\n', result)
    filew.write(result)
    filew.close()

def prepare_freq(num_page):
    fr = file('D:\\new\\sites\\' + str(num_page) + '.txt')
    fr = re.sub('\"|\:|\.',' ', fr)
    fr = fr.split()
    list_fr = []
    for word in fr:
        word = word.strip(',.<>/\'":;?!~-[]{}©—()«»+')
        word = word.lower()
        if word != '':
                list_fr.append(word)
#    print(list_fr)
    return list_fr

def diction(numpage):
    list_fr = prepare_freq(numpage)
    freq_dict = {}
    for key in list_fr:
        if key in freq_dict:
            value = freq_dict[key]
            freq_dict[key] = value + 1
        else:
            freq_dict[key] = 1
    return freq_dict

def freq(num,own):
    dicti = diction(num)
    freq_list = []
    p = 0
    for k in dicti:
        i = 0
        for el in own:
            if el == k and dicti[k] > 1:
                freq_list.append(k)
            i += 1
        p += 1
    return freq_list
        

def againfreq():
    own0,own1,own2,own3,own4 = own()
    freq0 = freq(0,own0)
    freq1 = freq(1,own1)
    freq2 = freq(2,own2)
    freq3 = freq(3,own3)
    freq4 = freq(4,own4)
#    print (freq0,freq1,freq2,freq3,freq4)
    return freq0,freq1,freq2,freq3,freq4

def result2():
    commonwords = common()
    commonwords_res = transform(commonwords)
    freq0,freq1,freq2,freq3,freq4 = againfreq()
    own0_freq_res = transform(freq0)
    own1_freq_res = transform(freq1)
    own2_freq_res = transform(freq2)
    own3_freq_res = transform(freq3)
    own4_freq_res = transform(freq4) 
    filew = open('D:\\new\\' + 'result_freq.txt', 'w', encoding = 'utf-8')
    result = commonwords_res + '\n' + own0_freq_res + '\n' + own1_freq_res + '\n' + own2_freq_res + '\n' + own3_freq_res + '\n' + own4_freq_res + '\n'
    result = re.sub('^, ','', result)
    result = re.sub('\n, ','\n', result)
    result = re.sub('\n\n','\nНе встречаются слова с частотностью больше 1, которые присутсвуют только в этом тексте.\n', result)
    filew.write(result)
    filew.close()
    
def main():
    makingdirs()
    result()
    result2()
    
if __name__ == '__main__':
    main()
