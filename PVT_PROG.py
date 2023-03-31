import pandas as pd
import time
import traceback
from path import Path
from datetime import date

from PROGRAM import waiter,login,browser,ele,alert,Technical,Price
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

verify_bids={"BID NO":[]}
def Upload_PVT():
    print("WAITING IN UPLOAD")
    waiter.until(EC.url_contains('https://bidplus.gem.gov.in/bidding/sellerbid/biddoc'))
    if "https://bidplus.gem.gov.in/bidding/sellerbid/biddoc" in browser.current_url:
        print("Inside upload section")
        global up_flag,exp_dict,exp_file,pr_exp,l
        up_flag=True
        ele('//*[@id="accordion"]/div/div[1]/h4/a').click()
        requirement=browser.find_element(By.ID,"collapseBuyer")
        time.sleep(1)
        l=requirement.text.replace("\n",":").split(":")
        #'//*[@id="docfile"]/div[2]/div[1]/label'
        but_keys='/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[{}]/div[2]/div[1]'
        #label_key="/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[{}]/div[1]/label"
        label_key='//*[@id="docfile"]/div[{}]/div[1]/label'
        p1='/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[{}]/div[2]/div[1]/p[1]'
        p2='/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[{}]/div[2]/div[1]/p[2]'
        browser.implicitly_wait(2)
        #'/html/body/div[2]/div/div/div[4]/div[2]/div/form/div[CHANGINGGGGGG]/div[2]/div[1]/input'  
        try:
            browser.find_element(By.CSS_SELECTOR,"input[type='radio'][value='emdopt_yes']").click()
            Select(browser.find_element(By.ID,'emd_category')).select_by_visible_text("Start-up")
            browser.find_element(By.CSS_SELECTOR,"input#fuemdcer").send_keys(get_file(file_dict["STARTUP"]))
        except Exception as e:
            print("NO EMD EXEMPTION REQUIRED ERROR ")
        size=ele('/html/body/div[2]/div/div/div[4]/div[2]/div/form').get_attribute("length")
        for i in range(1,int(size)):
            browser.implicitly_wait(10)
            file_size=10
            num_pages=102
            try: 
                key=label_key.format(i)
                label=browser.find_element(By.XPATH,key).text
                #browser.implicitly_wait(5)
                """try:
                    file_size=ele(p1.format(i)).text[15:17]
                    num_pages=ele(p2.format(i)).text[18:21]    
                except:
                    pass"""
                browser.find_element(By.XPATH,but_keys.format(i)+"/input").send_keys(get_file(file_dict[label],file_size,num_pages))

            except Exception as e:
                pass
    Verify_PVT(True)            

def Verify_PVT(up_flag=False):
    if up_flag:
        browser.implicitly_wait(10)
        waiter.until(EC.title_contains("GeM | Verfy & Sign"))
        global tender_doc_pvt,update_dict
        time.sleep(0.75)
        ele('/html/body/div[2]/div/div/div[1]/div/div[1]/h4/a/i').click()
        
        bid_no=l[1].strip()
        if not(bid_no.strip() in tender_doc_pvt["BID NO"].values):
            update_dict["QTY"]=l[-1][-3:-1].replace("(","")
            update_dict["BID NO"]=bid_no
            update_dict["DURATION"]=l[l.index("Contract Duration")+1].strip()
            update_dict["ORGANIZATION"]=l[l.index("Department")+1] if len(l[l.index("Department")+1].strip())>3 else l[l.index("Organisation")+1].strip()
            update_dict["STATE"]=input("ENTER THE STATE PLEASE")
            print("TENDER DETAILS:")
            print(update_dict)
            tender_doc_pvt=tender_doc_pvt.append(update_dict,ignore_index=True)
            tender_doc_pvt.to_excel("TENDER_PVT.xlsx")
            verify_bids["BID NO"].append(bid_no)
            pd.DataFrame(verify_bids).to_excel("VERIFY_BIDS.xlsx")
            ele('/html/body/header/section[2]/section/div[2]/div/div/div[2]/div/ul/li[4]/a').click() #CLICK ON BIDS OPTIONS
            time.sleep(0.5)
            ele('/html/body/header/section[2]/section/div[2]/div/div/div[2]/div/ul/li[4]/ul/li[1]/a').click() #CLICK ON 
                                                                                    #BID LISTS BUTTON 
            #ele('//*[@id="verify_undertaking"]').click()
            #browser.find_element(By.XPATH,'//*[@id="bid_submit"]').click()
            #waiter.until(EC.new_window_is_opened(browser.window_handles))
            #browser.switch_to.window(browser.window_handles[-1])


def get_file(file,size=10,num_pages=101):
    file=path+f"/{file}"
    if size==2:
        print("THE SIZE FOR THE FILE:",file.name," Is ",size)
        return get_100_pages(path+"\\"+(file.stem+"2.pdf"))
    return file.abspath()

#2588719

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


if __name__=="__main__":
    tender_doc_pvt=pd.read_excel("TENDER_PVT.xlsx").filter(regex='^(?!Unnamed)')
    init_tender_count=tender_doc_pvt["BID NO"].count()
    try:
        path=Path("E:\\ANACONDA\\Scripts\\PVT_DOCS")  #PVT LTD DOCS PATH
        update_dict={"DATE":str(date.today()),"BID NO":'',"ORGANIZATION":'',"STATE":'',"QTY":'',
                    "DURATION":'',"STATUS":'',"KIND":''}



        login(user_id="saindia11",password="Ssharma@2010")

        ele("//*[@id='exTab2']/div[1]/div[1]/div/div[1]/div/ul/li[2]/a").click() #SERVICE BIDS

        ele("//*[@id='category_selection']").click() #VIEW CATEGORIES

        buts_pvt=[ele("//*[@id='catList']/p[1]/label/input"),ele('//*[@id="catList"]/p[2]/label/input'),
        ele('//*[@id="catList"]/p[3]/label/input'),ele('//*[@id="catList"]/p[4]/label/input'),ele('//*[@id="catList"]/p[5]/label/input'),
        ele('//*[@id="catList"]/p[8]/label/input'),ele('//*[@id="catList"]/p[9]/label/input'),ele('//*[@id="catList"]/p[10]/label/input'),
        ]

        time.sleep(1)#FOR ALL-PVT,RESOURCES,GEM TO PREVENT 'ELEMENTNOTINTERACTABLE' EXCEPTION
        for i in buts_pvt:
            i.click()
        ele("/html/body/div[3]/div/div/form/div[3]/button[1]").click() #CLICK ON SEARCH BUTTON AFTER SELECTING CATEGORIES

        try:
            ele('//*[@id="skip_main_content"]/div/div/div[5]/a').click()
        except:
            print("PROBABLY ALL CONTENTS ARE DISPLAYED NO ISSUE IN PAGE NUMBERS")

        file_dict={
        "EPF Challans, ESI Challans Or Bank Statements Indicating The Credited EPF Or Service Provider Had ESI/EPF Or Wages:":"CHALLAN.pdf",
        "Statutory Auditor Certificate:":'Statutory.pdf',
        "Bidder Turnover:":'Bidder.pdf',
        "OEM Authorization Certificate:":'OEM.pdf',
        "OEM Annual Turnover:":'Bidder.pdf',
        "Copy Of Labour Licence/PF/EPF/ESI Registration Letter/Certificate:":'Labour.pdf',
        "Copy Of Certificate For Incorporation/Registration Of Bidding Entity Under Appropriate Act/Authority In India:":'Incorporation.pdf',
        "Auditor Certificate For Profit Making Entity In Last 3 Yrs:":'Auditor.pdf',
        "Registration Document For DGR Registration And Other Licenses:":'',
        "Certificate For Security Star Rating:":'Star_rating.pdf',
        "Proof Of Training Certificate Of Manpower Supplied:":'Train_man.pdf',
        "Write-Up On Recruitment, Training And Safety Policy Note:":'WRITE_UP.pdf',
        "Proof Of Training Infrastructure Or Documents Substantiating Tie-Up:":'Train_inf.pdf',
        "MSME":"MSME.pdf",
        "STARTUP":"STARTUP.pdf",}
        tech_flag=False
        pr_flag=False
        up_flag=False
        l=[]

        rec=1
        cl=5
        for i in range(100):
            tech_flag,pr_flag,up_flag=False,False,False
            browser.implicitly_wait(10)
            url=browser.current_url
            waiter.until(EC.url_changes(url))
            if "https://bidplus.gem.gov.in/bidding/sellerbid/participate" in browser.current_url:
                ele('//*[@id="accordion"]/div/div[1]/h4/a').click()
                if "y" in input("Address available?").lower():
                    Technical(inplace=False)
                    Upload_PVT() 
            elif "https://bidplus.gem.gov.in/bidding/sellerbid/finalize" in browser.current_url:
                Price(inplace=False)
                Upload_PVT()
            elif "https://bidplus.gem.gov.in/bidding/sellerbid/biddoc" in browser.current_url:
                Upload_PVT()
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
                ele("//*[@id='exTab2']/div[1]/div[1]/div/div[1]/div/ul/li[2]/a").click()#SERVICE BIDS
    except KeyboardInterrupt:
        #Note that in order for keyboard interrupt to wor, you need to be in this segment if the code
        #if the control is in one of the methods above, keyboard interrupt might not end up here.
        print("ENDING SESSION")
        print("TENDERS FILLED THIS SESSION: ",tender_doc_pvt["BID NO"].count()-init_tender_count)                
                
            
            
        

        output_file="TENDER_PVT.xlsx"
        tender_doc_pvt.to_excel(output_file)



















