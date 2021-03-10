// A library for getting all ola bills mail
require('chromedriver');

var webdriver = require('selenium-webdriver'),
    By = webdriver.By,
    until = webdriver.until;

var driver = new webdriver.Builder()
    .forBrowser('chrome')
    .build();

var mobile = process.env.MOBILE_NUMBER;
var mail = process.env.EMAIL;

//All crn number for a particular month
var novCrn = []

var sendInvoiceMail = function(crn){
	driver.get('https://www.olacabs.com/invoice');
	driver.findElement(By.xpath('//*[@id="container"]/div[2]/form/table/tbody/tr[1]/td[2]/input')).sendKeys(crn);
	driver.findElement(By.xpath('//*[@id="container"]/div[2]/form/table/tbody/tr[2]/td[2]/input')).sendKeys(mobile);
	driver.findElement(By.xpath('//*[@id="container"]/div[2]/form/table/tbody/tr[3]/td[2]/input')).sendKeys(mail);
	driver.findElement(By.xpath('//*[@id="container"]/div[2]/form/table/tbody/tr[4]/td[2]/input')).click();
	setTimeout(function(){}, 2000);
	return "submit crn"+crn;
}


novCrn.map(sendInvoiceMail);
driver.quit();
