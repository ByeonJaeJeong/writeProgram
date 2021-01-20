from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os
from pystray import MenuItem as item
import pystray
from PIL import Image

def write():
    #글로벌 브라우저 크롬실행
    global browser
    global chrome
    #게시글 아이디 리스트
    idList=[]
    #로그인페이지
    loginURL='http://www.tcafe2a.com/'
    
    browser=webdriver.Chrome(chrome)     

    browser.get(loginURL)
    browser.implicitly_wait(3)

    #id password 값 입력
    id='qsz78547'
    pw='k8866k'
    count=True
    #tcafe 아이디 입력
    elem_login= browser.find_element_by_name('mb_id')
    elem_login.send_keys(id)


    #tcafe 비밀번호 입력
    elem_login =browser.find_element_by_name('mb_password')
    elem_login.clear()
    elem_login.send_keys(pw)

    #tcafe 로그인 버튼 클릭
    loginButtonXpath='//*[@id="ol_before"]/form/fieldset/div[1]/span[2]/button'
    browser.find_element_by_xpath(loginButtonXpath).click()

    #포인트 톡 으로 이동
    pointTalkURL='http://www.tcafe2a.com/bbs/board.php?bo_table=ptok'
    browser.get(pointTalkURL)
    #테이블 공지 제외한 아이디 찾기
    tbodyXpath='//*[@id="fboardlist"]/div[1]/table/tbody'
    table=browser.find_element_by_class_name('div-table')
    tbody=table.find_element_by_tag_name("tbody")
    for tr in tbody.find_elements_by_tag_name("tr"):
        notice=tr.get_attribute('class')
        if(notice=='active'):
            continue
        id=tr.get_attribute('id')
        idList.append(id)
    #게시글 진입
    boardURL='http://www.tcafe2a.com/bbs/board.php?bo_table=ptok&wr_id='
    for boardID in idList:
        browser.get(boardURL+boardID)
        #댓글 확인
        section=browser.find_element_by_xpath('//*[@id="bo_vc"]')
        for media in section.find_elements_by_class_name('media'):
            count=True;
            media_heading=media.find_element_by_class_name('media-heading')
            a_tag=media_heading.find_element_by_tag_name('a')
            span=a_tag.find_element_by_tag_name('span')
            if('까군'==span.text):
                count=False
                break;
            else:
                continue;
        #카운트가 1이 아니면 글작성
        if(count):
            textarea=browser.find_element_by_xpath('//*[@id="wr_content"]')
            textarea.send_keys('ㅍㅈㅍㅈ')
            submit=browser.find_element_by_xpath('//*[@id="btn_submit"]').click()
            time.sleep(2)



def quit_window(icon, item):
    icon.visible=False
    icon.stop()
def show_window(icon, item):
    global showtext
    global browser
    if(item.text=='실행'):
        showtext='중지'
        write()
    else:
        showtext='실행'
        #웹창 닫기 
        browser.close()
   # icon.update_menu()
def setup(icon):
    icon.visible=True
    while (icon.visible):
       # menu = (item('Quit', quit_window), item(showtext, show_window))
        #icon.menu=menu
        
        time.sleep(1)
        
if __name__ == "__main__":
    #현재 폴더 경로 찾기
    chrome=os.getcwd()+'/chromedriver.exe'
    
    
    showtext='실행'
    #트레이 만들기
    image = Image.open("image.ico")
    menu = (item('Quit', quit_window), item(showtext, show_window))
    icon = pystray.Icon("name", image, "Tcafe", menu)
    icon.run()
   

    #헤드리스
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    
    
    #브라우저 전역으로 선언
    browser=''     
        
    



    




