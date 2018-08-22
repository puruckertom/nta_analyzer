from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import os
import time
import urllib


def batch_search(masses=None,formulas=None,directory='',by_formula=True,ppm=10):
    chrome_profile = webdriver.ChromeOptions()
    profile = {"download.default_directory": directory,
           "download.prompt_for_download": False,
           "download.directory_upgrade": True,
           "safebrowsing.enabled": True}
    chrome_profile.add_experimental_option("prefs", profile)
    
    external_url = "https://comptox.epa.gov/dashboard/dsstoxdb/batch_search"
    internal_url = "http://comptox.zn.epa.gov/dashboard/dsstoxdb/batch_search"
#Helpful command line switches
# http://peter.sh/experiments/chromium-command-line-switches/

    chrome_profile.add_argument("--disable-extensions")
    driver = webdriver.Chrome(executable_path=os.getcwd()+"\chromedriver.exe",
                               chrome_options=chrome_profile)
    driver.set_window_position(0,0)
    driver.maximize_window()

    if urllib.urlopen(external_url).getcode() == 200:
        value = 'value'
        driver.get(external_url)
    else:
        driver.get(internal_url)
        value = 'true-value'        
    if by_formula:
        driver.find_element_by_xpath('//*[@'+value+'="exact_formula"]').click()

        inputElement = driver.find_element_by_id("batch-search-chemicals")
        list_formulas = "\n".join(formulas)
        print list_formulas
        inputElement.send_keys(list_formulas)
    else:
        driver.find_element_by_xpath('//*[@'+value+'="ms_ready_monoisotopic_mass"]').click()
        driver.find_element_by_xpath('//*[@id="batch-search-mass-error-select"]/option[@value="'+str(ppm)+'"]').click() 
        inputElement = driver.find_element_by_id("batch-search-chemicals")
        list_masses = "\n".join(masses)
        print list_masses
        inputElement.send_keys(list_masses)
    #driver.find_element_by_id("display-batch-chemicals-btn").click()

    #Select to download the data
    driver.find_element_by_xpath('//*[@id="batch-search-panel-download"]').click()

    # select to dowload in specific format
    driver.find_element_by_xpath('//*[@id="batch-search-filetype"]/option[@value="tsv"]').click()

    #driver.find_element_by_id('select-all-properties').click()
    #dtxsid=driver.find_element_by_xpath('//*[@value="ATSDRLST"]')
    #driver.execute_script("return arguments[0].scrollIntoView();", dtxsid)
    #driver.execute_script("window.scrollBy(0, 500)")
    #CASRN
    driver.find_element_by_xpath('//*[@value="casrn" and @class="batch-search-input-checkbox"]').click()
    #time.sleep(4)

    #INChlKey
    driver.find_element_by_xpath('//*[@value="inchi_key"]').click()

    #IUPAC Name
    driver.find_element_by_xpath('//*[@value="acd_iupac_name"]').click()


    #Molecular Formula
    driver.find_element_by_xpath('//*[@value="mol_formula"]').click()

    #Average Mass
    #driver.find_element_by_xpath('//*[@value="compounds.mol_weight as average_mass"]').click()

    # Monoisotopic Mass
    driver.find_element_by_xpath('//*[@value="monoisotopic_mass"]').click()

    # OPERA Model Predictions
    #driver.find_element_by_xpath('//*[@value="opera_predictions"]').click()

    # TEST Model Predictions
    #driver.find_element_by_xpath('//*[@id="columns_" and @value="test_predictions"]').click()


    # Data Sources
    driver.find_element_by_xpath('//*[@value="data_sources"]').click()

    # Assay Hit Count
    driver.find_element_by_xpath('//*[@value="assays"]').click()


    # EXpoCast
    driver.find_element_by_xpath('//*[@value="expocast"]').click()

    submit = driver.find_element_by_xpath('//*[@id="batch-search-download-chemicals"]')
    time.sleep(2)
    if submit.is_enabled():
    	print "enabled"
    	submit.send_keys(Keys.ENTER);
    return True


#formulas=['C10H14N2O4','C10H5Cl2NO2']
#directory=os.getcwd()
#batch_search(formulas,directory)
