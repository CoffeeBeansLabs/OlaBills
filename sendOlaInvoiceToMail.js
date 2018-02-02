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
var novCrn = [1303446230,1302212742,1300496867,1299297864,1297454032,1291203888,1289154999,12879777952,1286479839,754994891,754993599,753941017,752412891,751690311,750858263,1277137733,1275540720,1273898496,1273709484,747909119,1271572455,1270900122,1270735149,746257715,1268142712,1265767960,1262424922]

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
