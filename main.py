import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *

# 防止打印一些无用的日志
# test 2021 11 14 10:26
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
driver = webdriver.Chrome(options=option)

# 等待用户登录并定位到课程页面
driver.get("https://www.mvazqh.org.cn/")
wait = WebDriverWait(driver, 120, 2)
try:
    alert = wait.until(presence_of_element_located((By.CSS_SELECTOR, '[data-status="1"]')), print("请登录并切换到课程页面！"))
except:
    print('你没有登录并切换到课程页面，刷课失败，请重新运行程序。')
    driver.close()
    sys.exit() # 退出程序

# 现已成功到达课程页面
driver.find_element(By.CSS_SELECTOR, '[data-status="0"]').click() # 切换到未完成
# driver.find_element(By.CLASS_NAME, 'layui-input').send_keys('1')
# driver.find_element(By.CLASS_NAME, 'layui-laypage-btn').click() # 切换到第一页
# print('已自动切换到未完成课程的第一页。')

time.sleep(5)

while True:
    # 打开页面上所有课程详情
    try:
        for knowns in driver.find_elements(By.CLASS_NAME, 'known'):
            knowns.click()
    except:
        print('展开详情失败！')
        pass
    
    time.sleep(5)
    
    courses = driver.find_elements(By.CLASS_NAME, 'course-learning-progress')
    print(len(courses))
    if (len(courses) == 0): # 页面已没有课程
        break
    
    num = 0
    while True:
        learned_progress = float(courses[num].find_element(
            By.CLASS_NAME, 'learned-section-num').text[:-1])
        if learned_progress < 100:
            break
        num += 1
        
    course_detail = courses[num] # 选择第num门课学习
    progress = course_detail.find_element(By.CLASS_NAME, 'learned-section-num').text # 学习进度
    if float(progress[:-1]) >= 100: # 已经学完了，跳过
        continue
    course_detail.find_element(By.CLASS_NAME, 'required-course-play').click() # 点击学习
    driver.switch_to.window(driver.window_handles[1])
    
    try:
        driver.implicitly_wait(5)
        title = driver.find_element(By.CLASS_NAME, 'first_title').get_attribute('innerText')
        # timelabel = driver.find_element(By.CLASS_NAME, 'currentTimeLabel').get_attribute('innerText')
        print('开始学习课程《{}》。'.format(title))
        print('当前进度：', end='', flush=True)
    except:
        print('开始学习下一门课程。')
        pass
    
    # 将隐藏的进度条改为可见
    driver.execute_script("document.getElementById(\"showInfo\").style.display='block';")
    info = driver.find_element(By.ID, 'showInfo') # 获取进度条元素
        
    milestone = 0
    percent = 0
    while percent < 100: # 学习进度不到100%
        if percent // 10 * 10 > milestone: # 每当进度为整十，输出提示
            milestone = percent // 10 * 10
            print(str(milestone) + '% ', end='', flush=True)
        time.sleep(10)
        
        # 将隐藏的进度条改为可见
        driver.execute_script("document.getElementById(\"showInfo\").style.display='block';")
        try:
            percent = int(re.findall('\d+', info.text)[0])
        except:
            time.sleep(2)
            percent = int(re.findall('\d+', info.text)[0])
        
    print('100%')
    print('课程已学习完毕。\n')
    time.sleep(2)
    
    # 关闭当前标签页并回到第一个标签页（默认课程总览页面在第一个标签页）
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    time.sleep(2)

print('已经学完了所有课程。恭喜！')