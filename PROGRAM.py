import pandas as pd
import os,re

import time,traceback

from path import Path
from datetime import date

from pdf_read import generate
from CAPTCHA import decaptcha
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException,UnexpectedAlertPresentException,ElementClickInterceptedException


verify_bids_gem={"BID NO":[]}
def ele(X_path):
    return browser.find_element(By.XPATH,X_path)

options= ChromeOptions()
options.binary_location="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
options.add_argument("start-maximized")
options.add_argument("user-data-dir=C:/Users/SIWAN/AppData/Local/Google/Chrome/User Data/Default")
browser=webdriver.Chrome(options=options)
browser.implicitly_wait(50)
ignored_exceptions=(NoSuchElementException,UnexpectedAlertPresentException,StaleElementReferenceException,
ElementClickInterceptedException)
waiter=WebDriverWait(browser,3000,ignored_exceptions=ignored_exceptions)

alert=Alert(browser)
def login(user_id="sa_india11",password="Rsharma@2010"):#pass for gem=Rsharma@2010
    global browser
    browser.get("https://sso.gem.gov.in/ARXSSO/oauth/login")
    
    ele("//*[@id='loginid']").send_keys(user_id)  #ENTER USER ID
    ele("//*[@id='captcha1']").screenshot("Captcha.png") #CAPTCHA COVER
    
    cap_inp=ele("//*[@id='captcha_math']")
    time.sleep(1)                                       #ENTER THE CAPTCHA
    cap_inp.send_keys(decaptcha("Captcha.png")[0:6])


    ele("//*[@id='loginFrm']/div[4]/div[2]/button").click()
    os.remove("Captcha.png")
    ele("//*[@id='password']").send_keys(password) #ENTER PASS

    ele("//*[@id='loginFrm']/div[4]/div[1]/button").click()
    
    waiter.until(EC.title_contains("Fulfilment"))
    
    waiter.until(EC.number_of_windows_to_be(2)) 
    browser.switch_to.window(browser.window_handles[1])
    waiter.until(EC.url_to_be("https://bidplus.gem.gov.in/seller-bids"))
    ele('//*[@id="old_bid_dash"]').click()

    ele('/html/body/div[2]/div[1]/div[1]/div/div[2]/a[1]/button').click()



def Technical(inplace=True):
    if "https://bidplus.gem.gov.in/bidding/sellerbid/participate" in browser.current_url:
        #PARTICIPATION PHASE
        #ele('//*[@id="accordion"]/div/div[1]/h4/a').click()
        down_bid_doc=ele('//*[@id="pagi_content row"]/div[1]/div[1]/p/a').click()
        
        ext=input("Enter Extension")
        generate(ext)
        #os.remove(f"F:\\NABARD\\GeM-Bidding-{ext}.pdf")
        '//*[@id="participate_seller"]/table/tbody/tr[2]/td[3]/div/button'
        #print(browser.find_elements_by_class_name('btn dropdown-toggle'))
        global tech_flag
        print("INTO TECHNICAL")
        parts=browser.find_elements(By.CLASS_NAME,"participateTag")
        tech_flag=len(parts)
        try:
            for part in range(1,len(parts)+1):
                ele(f'//*[@id="content"]/div[1]/div[1]/div[{part}]/div/a').click()
                #ele('//*[@id="content"]/div[1]/div[1]/div/div/a').click()# CLICKING ON PARTICIPATION BUTTON
                #print(ele('//*[@id="participate_seller"]/table/tbody/tr[5]/td[3]/div/button').get_attribute("class"))
                browser.implicitly_wait(5)
                #print(browser.find_elements_by_class_name("btn dropdown-toggle"))#REMEMBER THAT THE SPACE B/W CLASS NAME MEANS
                                                                                #THAT THEY ARE 3 DIFF CLASSES
                #print(browser.find_elements_by_css_selector('btn.dropdown-toggle'))
                #print(browser.find_elements_by_class_name('btn'))
                drop=browser.find_elements(By.CLASS_NAME,"selectpicker")
                #TECHNICAL BID TABLE
                for buts in drop:
                    try:
                        inp=''
                        name=buts.get_attribute("name")
                        care=name[5:name.find("]")].replace("_"," ")
                        if(care=="[certifications trainings"):
                            print()
                            inp="No"
                        e=browser.find_elements(By.TAG_NAME,"td")
                        for i in range(len(e)):
                            t=e[i].text.lower()
                            if t==care:
                                inp=e[i+1].text
                        sel=Select(buts)
                        sel.select_by_visible_text(inp)
                    except Exception as e:
                        print("BOY THERE IS AN EXCEPTION WAIT!!!! ",e)
                        time.sleep(10)
                time.sleep(0.5)
                '//*[@id="participate_seller"]/div/button'
                browser.find_element(By.CLASS_NAME,"saveserSpecs.btn.btn-md.btn-primary").click()
                #browser.find_element_by_partial_link_text("Save & Continue").click() #SAVE AND CONTINUE
            time.sleep(0.5)
            ele('//*[@id="continue_button"]').click()#CONTINUE ON THE NEXT PAGE
        except Exception as e:
            print("There was an error in TECHNICAL, waiting until you end this.")
    Price(tech_flag,inplace)


def Price(div_len=1,inplace=True):
    if "https://bidplus.gem.gov.in/bidding/sellerbid/finalize" in browser.current_url:
        try:#INCASE THE PRICE HAS ALREADY BEEN ENTERED
            print("INTO THE PRICE")
            global pr_flag
            pr_flag=True
            browser.implicitly_wait(5)
            time.sleep(0.5)
            for i in range(div_len):
                k=2
                price=ele(f'/html/body/div[2]/div/div/div[3]/div[2]/div/div/form/div[{k}]/div[2]/div[1]/input')
                
                if(i>0):
                    time.sleep(1)
                price.send_keys("0.01")
                price.send_keys(Keys.ENTER)
                pr=browser.find_element(By.XPATH,f'//*[@id="sellerfinancial"]/div[{k}]/div[2]/div[1]/span/p').text
                p1=re.findall('\d+\.\d+',pr) #FIRST TRIES TO FIND DECIMAL NUMBERS
                if(len(p1)==0):
                    p1=re.findall("\d+",pr)[0]#IF NOT THEN FINDS INTEGERS
                else:
                    p1="0"+p1[0]
                print("ENTERING PRICE")
                price.clear()
                price.send_keys(p1)
                price.send_keys(Keys.ENTER)
                k+=2
            
            browser.find_element(By.XPATH,'//*[@id="showEstPrice"]').click()
            browser.find_element(By.XPATH,'//*[@id="showEstPriceModal"]/div/div/div[3]/button').click()
            browser.find_element(By.XPATH,'//*[@id="saveParticipate"]').click()
            alert.accept()
        except Exception as e:
            print("Price has been entered or you have the following exception")
            print(e)
            traceback.print_tb(e.__traceback__)
    if inplace:
        Upload()

def Upload():
    waiter.until(EC.url_contains("https://bidplus.gem.gov.in/bidding/sellerbid/biddoc"))
    if "https://bidplus.gem.gov.in/bidding/sellerbid/biddoc" in browser.current_url:
        print("Inside upload section")
        global up_flag,bid_no,l
        up_flag=True
        browser.implicitly_wait(10)
        ele('//*[@id="accordion"]/div/div[1]/h4/a').click()
        requirement=browser.find_element(By.ID,"collapseBuyer")
        time.sleep(1)
        l=requirement.text.replace("\n",":").split(":")
        browser.implicitly_wait(2)
        #MSME IMPUT
        try:
            browser.find_element(By.CSS_SELECTOR,"input[type='radio'][value='msmeopt_yes']").click()
            browser.find_element(By.CSS_SELECTOR,"input#fumsmecer").send_keys(get_file(file_dict["MSME"]))
        except Exception as e:
            print("NO MSME REQUIRED")
        but_keys='/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[{}]/div[2]/div[1]'
        label_key="/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[{}]/div[1]/label"
        p1='/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[{}]/div[2]/div[1]/p[1]'
        p2='/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[{}]/div[2]/div[1]/p[2]'

        #'/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[CHANGINGGGGGG]/div[2]/div[1]/input'  
    
        size=ele('/html/body/div[2]/div/div/div[4]/div[2]/div/form').get_attribute("length")
        for i in range(1,int(size)):
            file_size=10
            num_pages=102
            browser.implicitly_wait(5)
            try:
                label=browser.find_element(By.XPATH,label_key.format(i)).text
                browser.implicitly_wait(5)
                """try:
                    file_size=ele(p1.format(i)).text[15:17]
                    num_pages=ele(p2.format(i)).text[18:21]
                except:
                    pass"""
                browser.find_element(By.XPATH,but_keys.format(i)+"/input").send_keys(get_file(file_dict[label],file_size,num_pages))

            except Exception as e:
                pass
                #print("Error in uploading file for ",label,"and the error is ",e)
            
    Verify(True)            
        
def Verify(up_flag=False):
    if up_flag:
        waiter.until(EC.title_contains("GeM | Verfy & Sign"))
        global tender_doc,update_dict
        try:
            ele('/html/body/div[2]/div/div/div[1]/div/div[1]/h4/a/i').click()
        except:
            pass
        bid_no=l[1].strip()
        if not(bid_no.strip() in tender_doc["BID NO"].values):
            update_dict["QTY"]=l[-1][-3:-1].replace("(","")
            update_dict["BID NO"]=bid_no
            update_dict["DURATION"]=l[l.index("Contract Duration")+1].strip()
            update_dict["ORGANIZATION"]=l[l.index("Department")+1] if len(l[l.index("Department")+1].strip())>3 else l[l.index("Organisation")+1].strip()
            update_dict["STATE"]=input("ENTER THE STATE PLEASE")
            print("TENDER DETAILS:")
            print(update_dict)
            tender_doc=tender_doc.append(update_dict,ignore_index=True)
            tender_doc.to_excel("TENDER-GEM1.xlsx")
            verify_bids_gem["BID NO"].append(bid_no)
            pd.DataFrame(verify_bids_gem).to_excel("VERIFY_GEM.xlsx")
            ele('//*[@id="verify_undertaking"]').click()
            ele('/html/body/header/section[2]/section/div[2]/div/div/div[2]/div/ul/li[4]/a').click() #CLICK ON BIDS OPTIONS
            time.sleep(0.5)
            ele('/html/body/header/section[2]/section/div[2]/div/div/div[2]/div/ul/li[4]/ul/li[1]/a').click() #CLICK ON 
                                                                                    #BID LISTS BUTTON 
             

def get_file(file,size=10,num_pages=101):
    file=path+f"/{file}"
    if size==2:
        print("THE SIZE FOR THE FILE:",file.name," Is ",size)
        return get_100_pages(path+"\\"+(file.stem+"2.pdf"))
    return file.abspath()



def get_100_pages(file,num_pages):
    if num_pages==100:
        print("DOC RECIEIVED:",file.stem,"for page removal")
        output_pdf=path+"/"+(file.stem+"_removed.pdf")
        if output_pdf.exists():
            return output_pdf.abspath()
        else:
            print("UPLOAD FAILED!! ",output_pdf.stem ,"Doesnot exist")
    else:
        return file.abspath()

if __name__=="__main__": #RUN ALL THIS ONLY WHEN CALLED DIRECTLY FROM THE CMD
    tender_doc=pd.read_excel("TENDER-GEM1.xlsx")
    tender_doc=tender_doc[tender_doc.filter(regex='^(?!Unnamed)').columns]
    init_tender_count=tender_doc["BID NO"].count()
    try:
        
        path=Path("E:\\ANACONDA\\Scripts\\New Folder") 

        update_dict={"DATE":str(date.today()),"BID NO":'',"ORGANIZATION":'',"STATE":'',"QTY":'',
                    "DURATION":'',"STATUS":'',"KIND":''}

        
        down_bid_doc=''
        if "y" in input("LOGIN REQUIRED??").lower():
            login()
            
            ele("//*[@id='exTab2']/div[1]/div[1]/div/div[1]/div/ul/li[2]/a").click() #SERVICE BIDS

            ele("//*[@id='category_selection']").click() #VIEW CATEGORIES

            """ele("//*[@id='service']").click() #SELECTING SERVICE BIDS                                    
            ele("/html/body/div[2]/div[5]/div[1]/div[5]/span/div/button").click() #SELECTING CATEGORIES    NEW BID SELECTION 
            ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[2]/a/label/input').click()          PAGE KE LIYE  
            ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[2]/a/label/input').click()"""

            ele('//*[@id="catList"]/p[16]/label/input')
            buts_sai=[ele('//*[@id="catList"]/p[16]/label/input'),ele('//*[@id="catList"]/p[15]/label/input'),
            ele('//*[@id="catList"]/p[4]/label/input'),ele('//*[@id="catList"]/p[6]/label/input'),
            ele('//*[@id="catList"]/p[8]/label/input'),ele('//*[@id="catList"]/p[7]/label/input'),
            ele('//*[@id="catList"]/p[13]/label/input')]
            #[ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[2]/a/label/input'),
            #ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[3]/a/label/input'),ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[4]/a/label/input'),
            #ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[5]/a/label/input'),ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[6]/a/label/input'),
            #ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[8]/a/label/input'),ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[9]/a/label/input'),
            #ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[10]/a/label/input')]
            #ele("/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[7]/a/label/input"),ele("/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[17]/a/label/input"),
            #ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[19]/a/label/input'),ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[23]/a/label/input')
            #,ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[26]/a/label/input'),ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[27]/a/label/input')
            #,ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[29]/a/label/input'),ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[30]/a/label/input'),
            #ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[32]/a/label/input')]
            
            #check_buts=[7,19,26,29,32,17,23,27,30] FOR NEW PAGE
            
            time.sleep(1)#FOR ALL-PVT,RESOURCES,GEM
            for i in buts_sai:
                i.click()

            ele("/html/body/div[3]/div/div/form/div[3]/button[1]").click() #SEARCH FOR THE CATS 
            ele('//*[@id="high_value_bids"]').click()

        #NEW PAGE CODE
        #ele("/html/body/div[2]/div[5]/div[1]/div[5]/span/div/button").click() #SEARCH FOR SELECTED CATEGORIES
        #ele('//*[@id="highValue"]').click() #TO SEARCH FOR HIGH VALUE BIDS


        page_nos=20
        
        file_dict={
        "Statutory Auditor Certificate:":'Statutory.pdf',
        "Bidder Turnover:":'Bidder.pdf',
        "OEM Authorization Certificate:":'OEM.pdf',
        "OEM Annual Turnover:":'Bidder.pdf',
        "Copy Of Certificate For Incorporation/Registration Of Bidding Entity Under Appropriateact/Authority In India:":"Incorporation.pdf",
        "Copy Of Labour Licence/PF/EPF/ESI Registration Letter/Certificate:":'Labour.pdf',
        "Copy Of Certificate For Incorporation/Registration Of Bidding Entity Under Appropriate Act/Authority In India:":'Incorporation.pdf',
        "Auditor Certificate For Profit Making Entity In Last 3 Yrs:":'Auditor.pdf',
        "Certificate For Security Star Rating:":'Star_rating.pdf',
        "Proof Of Training Certificate Of Manpower Supplied:":'Train_man.pdf',
        "Write-Up On Recruitment, Training And Safety Policy Note:":'WRITE_UP.pdf',
        "Proof Of Training Infrastructure Or Documents Substantiating Tie-Up:":'Train_inf.pdf',
        "EPF Challans, ESI Challans Or Bank Statements Indicating The Credited EPF Or Service Provider Had ESI/EPF Or Wages:":"CHALLAN.pdf",
        "MSME":"MSME.pdf"}





        #check_box='body > div.container > div:nth-child(5) > div.col-md-2.sidefilter > div.cat-dropdown.catClass > span > div > ul > li:nth-child({#}) > a > label > input[type=checkbox]'    
        #FOR NEW PAGE
        tech_flag=False
        pr_flag=False
        up_flag=False
        bid_no,l='',[] #l for storing requirements
        #NEW PAGE KEYS
        #status_xpath='//*[@id="bidCard"]/div[#]/div[1]/p[2]/span'
        #bubble_stat_key='//*[@id="bidCard"]/div[#]/div[3]/div[2]/div[1]/ul/li[4]'                                                            #PARTICIPATION
        #part_but_key='//*[@id="bidCard"]/div[#]/div[3]/div[2]/div[2]/div/a/input'
        
        #OLD PAGE KEYS
        #status_xpath='//*[@id="pagi_content"]/div[#]/div[1]/p[4]/span'
        #bubble_stat_key='//*[@id="pagi_content"]/div[#]/div[6]/ul/li[4]'
        #part_but_key="//*[@id='pagi_content']/div[#]/div[7]/a/input" #PARTICIPATION  BUTTON KEY
        #rec=1
        #cl=5
        for i in range(100):
            
            tech_flag,pr_flag,up_flag=False,False,False
            browser.implicitly_wait(10)
            url=browser.current_url
            waiter.until(EC.url_changes(url))
            if "https://bidplus.gem.gov.in/bidding/sellerbid/participate" in browser.current_url:
                ele('//*[@id="accordion"]/div/div[1]/h4/a').click()
                if "y" in input("Address available?").lower():
                    Technical(inplace=False)
                    Upload() 
            elif "https://bidplus.gem.gov.in/bidding/sellerbid/finalize" in browser.current_url:
                Price(inplace=False)
                Upload()
            elif "https://bidplus.gem.gov.in/bidding/sellerbid/biddoc" in browser.current_url:
                Upload()
            else:
                pass
            if browser.title=="GeM | Verfy & Sign":
                ele('/html/body/header/section[2]/section/div[2]/div/div/div[2]/div/ul/li[4]/a').click() #CLICK ON BIDS OPTIONS
                time.sleep(0.5)
                ele('/html/body/header/section[2]/section/div[2]/div/div/div[2]/div/ul/li[4]/ul/li[1]/a').click() #CLICK ON 
                                                                                    #BID LISTS BUTTON 
            if up_flag:
                waiter.until(EC.url_contains("https://bidplus.gem.gov.in/seller-bids"))
                ele('//*[@id="old_bid_dash"]').click()
                ele('/html/body/div[2]/div[1]/div[1]/div/div[2]/a[1]/button').click()
                ele("//*[@id='exTab2']/div[1]/div[1]/div/div[1]/div/ul/li[2]/a").click()
                
            
        
        
        """NEW PAGE CODE

        ele("//*[@id='service']").click() #SELECTING SERVICE BIDS
        ele("/html/body/div[2]/div[5]/div[1]/div[5]/span/div/button").click() #SELECTING CATEGORIES
        ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[2]/a/label/input').click()#SELECT ALL CATS
        ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[2]/a/label/input').click()#SELECT ALL
                                                                #THOSE ALREADY SELECTED
        ele('/html/body/div[2]/div[5]/div[1]/div[5]/span/div/ul/li[30]/a/label/input').click()
        ele("/html/body/div[2]/div[5]/div[1]/div[5]/span/div/button").click()
        ele('//*[@id="highValue"]').click() #CHECK MARK THAT HIGH-VALUE BID SECTION AGAIN
                
        if(page>1):
            waiter.until(EC.presence_of_element_located((By.XPATH,f'//*[@id="light-pagination"]/a[1]'))).click()
        for i in range(3,page+1):
            waiter.until(EC.presence_of_element_located((By.XPATH,f'//*[@id="light-pagination"]/a[{i}]'))).click()
        """
    except KeyboardInterrupt as e:
        tender_doc.to_excel("TENDER-GEM1.xlsx")
        print("ENDING SESSION")
    
        print("TENDERS FILLED THIS SESSION :",tender_doc["BID NO"].count()-init_tender_count)
    



















