import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url="https://www.treksandtrails.org/tours/kaas-plateau-thoseghar-waterfall-tour-from-pune"
def scrape(link):
      req = requests.get(link)
      soup = BeautifulSoup(req.content, "html.parser")

      child_soup = soup.find("div", id="overview").find("div",class_="content ckeditor-content")

      for child in child_soup.findChildren():
            if(child.name=="h3" or child.name=="h2"):
                  print("\n",child.text)      
            elif(child.name=="p"):
                  print(child.text)
            elif(child.name=="ul"):
                  for i in child.findChildren("li"):
                        print(i.text)

      print("\nInclusions:")
      inclusions= soup.find("div", class_="inclusions").find("div", class_="ckeditor-content").ul.findChildren("li")
      for i in inclusions:
            print(i.text)

      print("\nExclusions:")
      exclusions = soup.find("div", class_="exclusions").find("div", class_="ckeditor-content").ul.findChildren("li")
      for i in exclusions:
            print(i.text)

      child_soup2=soup.find("div", id="highlights")
      print(child_soup2.find("div",class_="title h2").text)
      counter=1
      for child in child_soup2.find("div", class_="content ckeditor-content").findChildren():
            if(child.name=="h3" or child.name=="h2"):
                  print("\n",child.text)
                  counter=1
            elif(child.name=="ul"):
                  for i in child.findChildren("li"):
                        print(str(counter) + "- " + i.text)
                        counter+=1

      child_soup3 = soup.find("div", id="itinerary").find("div",class_="content").find("div",class_="content ckeditor-content")
      print("\nFAQs")
      for child in child_soup3.findChildren():
            if(child.name=="p" or child.name=="h3"):
                  if(child.name=="h3"):
                        print("\n")
                  print(child.text)
            elif(child.name=="ul"):
                  for i in child.findChildren("li"):
                        print("-> ",i.text)
      print("\n")   

      image_urls = []

      driver = webdriver.Chrome()
      driver.get(link)
      button = driver.find_element(By.ID,"gallery-btn")
      button.click()
      WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"lg")))
      page_source = driver.page_source
      driver.quit()

      driver_soup = BeautifulSoup(page_source,features="html.parser")

      images=driver_soup.find("div",class_="lg-thumb-outer lg-grab").find("div",class_="lg-thumb lg-group").findChildren()
      for image in images:
            photo=image.find("img")
            if photo:
                  photo=photo.get("src")
                  image_urls.append(photo)

      for image_url in image_urls:
            print(image_url)

scrape(url)