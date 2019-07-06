#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Deka crawler
import requests
from requests import Session
from bs4 import BeautifulSoup


# In[2]:


def crawlSubmitForm():
    # gen session 
    session = Session()
    
    r = session.post(
        url='http://deka.supremecourt.or.th/search',
        data={
            # show keys
            'show_item_remark': 0,
            'show_item_primartcourt_deka_no': 0,
            'show_item_deka_black_no': 0,
            'show_item_department': 0,
            'show_item_primarycourt': 1,
            'show_item_judge': 1,
            'show_item_source': 1,
            'show_item_long_text': 0,
            'show_item_short_text': 1,
            'show_item_law': 1,
            'show_item_litigant': 1,
            'show_result_state': 1,
            'search_form_type': 'basic',
            'search_type': 1,
            'start': True,
            # doctype 1 = คำพิพากศาศาลฏีกา
            'search_doctype': 1,
            # search keyword
            'search_word': 'ทุจริต .และ. อาญา',
            'search_deka_no_ref': '',
            'search_deka_no': '',
            # select years
            'search_deka_start_year': 2553,
            'search_deka_end_year': 2553,
            },
            # no header
            headers={}
        )
    return r


# In[3]:


def extractLaws(B4sentences):
    p_tag = []
    for i in range(100):
        if B4sentences == 'จำเลย':
            break
        else : 
            p_tag.append(B4sentences.previous_element)
            B4sentences = B4sentences.previous_element

    List_laws = p_tag[::-1]
    
    text = ''
    for txt in List_laws:
        if(str(txt)[0]!='<'):
            text = text + txt
        else: 
            continue

    L = text.split('จำเลย')
    # set unique value
    return set(L)


# In[4]:


def crawlExample(ArticleName,RightDetails,judges,Deka_conslusion_rank,Sentences):
    for i in range(0,len(ArticleName)):
        
        # Extract data
        # 1 Article name
        print(ArticleName[i].text)

        # 2 Parties
        parties = RightDetails[i].text
        p = parties.split('โจทก์')
        defendant = p[-1]
        prosecutor = p[:-1]
        print('โจทก์ ',prosecutor,' จำเลย ', defendant)

        # 3 judges
        print("ผู้ตัดสิน :",judges[i].text)

        # 4 Conclusion
        print('คำพิพากษา :',Deka_conslusion_rank[i].find_previous('p').text)

        # 5 Sentences
        print('ประมวลที่พิจารณา :',extractLaws(Sentences[i]))
        print('################')


# In[6]:


if __name__ == "__main__":
    r = crawlSubmitForm();
    # get response text
    r.encoding = 'utf-8'
    r_text = r.text
    soup = BeautifulSoup(r_text, 'html.parser')
    # print(soup.prettify())
    
    ArticleName = soup.findAll("li", {"class": "item show-display-left print_item_deka_no"})

    RightDetails = soup.findAll("li", {"class": "item show-display-right print_item_litigant"})

    judges = soup.findAll("li", {"class": "item_judge content-option"})

    Deka_conslusion_rank = soup.findAll("li", {"class": "item print_item_judge"})

    Sentences = soup.findAll("li", {"class": "item print_item_short_text"})
    
    # print result
    crawlExample(ArticleName,RightDetails,judges,Deka_conslusion_rank,Sentences)

