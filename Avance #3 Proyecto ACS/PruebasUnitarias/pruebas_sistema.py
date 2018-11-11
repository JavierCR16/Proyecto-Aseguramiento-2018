'''
Created on Nov 11, 2018

@author: Javier
'''
import unittest

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class SimpleTestCase(unittest.TestCase):
    
    def test_prueba1(self):
        driver= webdriver.Chrome("../Driver Chrome/chromedriver.exe")# es para ver cual va a usar
        #https://sites.google.com/a/chromium.org/chromedriver/downloads

        driver.get("http://127.0.0.1:5000/") # es la pagina web que se va a probar
        driver.find_element_by_name("directorioArchivos").send_keys('C:/Users/Javier/Desktop/Aseguramiento de la Calidad del Software/Material Dropbox/proyectos/datasets/Batch')# hay varios metodos para buscar/ si es un input entonces se le manda .send_keys("y el texto")
        time.sleep(3)
        driver.set_page_load_timeout(1000)

        driver.find_element_by_name("Segmentar").send_keys(Keys.ENTER)# si es que es un boton/ se usa click, pero si por X o Y razon el boton queda tapado por algo entonces es mejor usar Keys
        self.prueba2_sistema(driver)
        
        time.sleep(10)
        driver.quit()
        
    def prueba2_sistema(self,driver):
        time.sleep(5)
        driver.find_element_by_name("Resultados").send_keys(Keys.ENTER)
        driver.set_page_load_timeout(1000)
        
        time.sleep(5)
        driver.find_element_by_name("CSV").send_keys(Keys.ENTER)
        driver.set_page_load_timeout(1000)
        
        time.sleep(5)
        driver.find_element_by_name("DICE").send_keys(Keys.ENTER)
        driver.set_page_load_timeout(1000)
        
        