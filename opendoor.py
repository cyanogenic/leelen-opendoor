from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import pickle

########## 配置 ##########
workspace = os.path.abspath(os.path.dirname(__file__))
cookies_path = workspace + '/cookies.pkl'
# 服务器信息
server_ip = '192.168.1.168'
username = '13012345678'
password = 'cqMYG14dss'
# XPATH
##########################

def esafe_login():
    # 登录并保存Cookie
    # TODO Try Catch
    browser.get("http://" + server_ip + "/esafe/login")
    username_input = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    username_input.clear()
    username_input.send_keys(username)
    browser.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    browser.find_element(By.XPATH, '//button[@class="el-button login-in el-button--primary el-button--medium"]').click()
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="dashboard-container"]')))
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
    browser.get("http://" + server_ip + "/esafe/deviceManage/deviceList")

# 启动无头浏览器
drive_options = webdriver.ChromeOptions()
drive_options.add_argument('--headless')
drive_options.add_argument('--lang=zh-CN')
browser = webdriver.Chrome(options=drive_options)
browser.set_window_size(1920, 1080)

# 判断Cookies文件是否存在
if os.path.exists("cookies.pkl"):
    print("存在Cookies文件,加载中...")
    # 加载Cookies
    browser.execute_cdp_cmd('Network.enable', {})
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.execute_cdp_cmd('Network.setCookie', cookie)
    browser.execute_cdp_cmd('Network.disable', {})
    browser.get("http://" + server_ip + "/esafe/deviceManage/deviceList")
    # 判断Cookies是否过期
    # TODO 修改判断策略
    try:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-main"]/div/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]')))
    except Exception as e:
        print("Cookies过期,登录中...")
        esafe_login()
else:
    print("未发现Cookies文件,登录中...")
    esafe_login()

print("登陆成功,拉取设备列表中...")
WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="el-table__row"]')))
browser.get_screenshot_as_file(workspace + '/screenshots/1.png')
# TODO XPATH设为全局变量
WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-main"]/div/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]'))).screenshot(workspace + '/screenshots/2.png')
opendoor_button = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-main"]/div/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[11]/div/i[1]')))
opendoor_button.screenshot(workspace + '/screenshots/3.png')
print("拉取完成,开门中...")
ActionChains(browser).move_to_element(opendoor_button).click().perform()
# TODO try catch
WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="el-message-box__wrapper"]')))
browser.get_screenshot_as_file(workspace + '/screenshots/4.png')

browser.quit()
