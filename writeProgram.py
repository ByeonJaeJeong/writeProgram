from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os
from pystray import MenuItem as item
import pystray
from PIL import Image
import tkinter as tk
from tkinter import messagebox
import threading
window = tk.Tk()
window.title("Welcome")


class writeThread(threading.Thread):
    browser=''
    def __init__(self, name='TestThread'):
        "생성자 초기 변수 설정"
        super(writeThread, self).__init__()
        self._stop_event = threading.Event()
        
        

        #threading.Thread.__init__(self, name=name)
    def run(self):
        #현재 폴더 경로 찾기
        chrome=os.getcwd()+'/chromedriver.exe'
        #게시글 아이디 리스트
        idList=[]
        #로그인페이지
        loginURL='http://www.tcafe2a.com/'
        #헤드리스
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        global browser
        browser=webdriver.Chrome(chrome,options=options)      

        browser.get(loginURL)
        browser.implicitly_wait(3)

        #id password 값 입력
        id=''
        pw=''
        name=''
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
        #무한반복
        while True:
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
                    if(name==span.text):
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
    def stop(self):
        global browser
        try:
            browser.quit()
        except:
            print("브라우저 종료 오류")
        messagebox.showinfo("종료","정상종료되었습니다.")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    #종료
def quit_window(icon, item):
    try:
        browser.quit()
    except:
        print("브라우저  종료 오류")
    try:
        window.destroy()
    except:
        print("tk종료오류")
    try:
        icon.stop()
    except:
        print("트레이 종료 오류")
    
    #화면 출력
def show_window(icon, item):
    icon.stop()
    window.after(0,window.deiconify)
    #트레이로
def withdraw_window():  
    window.withdraw()
    image = Image.open("image.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()



#메인
#스레드 처리
def start(t):
    t=writeThread()
    t.deamon=True
    t.start()
    messagebox.showinfo(title="실행", message="정상실행 되었습니다.")    
t=writeThread()

#동작버튼
playButton=tk.Button(window,text="동작",width=10,command=lambda: start(t))
playButton.grid(row=0,column=0)
#정지버튼
stopButton=tk.Button(window,text="정지",width=10,command=lambda: t.stop())
stopButton.grid(row=0,column=1)

window.protocol('WM_DELETE_WINDOW', withdraw_window)
window.mainloop()
