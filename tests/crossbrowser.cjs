const pw=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs');
(async()=>{
 const results=[];
 for(const engine of ['chromium','firefox']){
 const browser=await pw[engine].launch(engine==='chromium'?{headless:true,executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}:{headless:true});
 console.log('Started',engine); const context=await browser.newContext(); const page=await context.newPage();page.setDefaultTimeout(15000);page.setDefaultNavigationTimeout(15000);
 for(const base of ['http://127.0.0.1:8080','http://127.0.0.1:8081']){
 console.log(engine,base);await context.clearCookies();
 for(const size of [{width:1280,height:900},{width:390,height:844}]){
 await page.setViewportSize(size);
 for(const route of ['events','register','login']){
 const response=await page.goto(base+'/?page='+route);results.push({engine,version:browser.version(),base,route,width:size.width,status:response.status(),noOverflow:await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)});
 }
 }
 await page.locator('[name=login]').fill('student');await page.locator('[name=password]').fill('Student123');await page.locator('button').last().click();
 for(const route of ['account','apply','applications']){
 await page.goto(base+'/?page='+route);results.push({engine,base,route,width:390,noOverflow:await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)});
 }
 if(base.endsWith('8081') && engine==='chromium'){await page.goto(base);await page.screenshot({path:'evidence/workshop-mobile.png',fullPage:true});await page.setViewportSize({width:1280,height:900});await page.screenshot({path:'evidence/workshop-desktop.png',fullPage:true});}
 await page.getByRole('button',{name:'Выйти',exact:true}).click();
 await page.goto(base+'/?page=login');await page.locator('[name=login]').fill('admin');await page.locator('[name=password]').fill('Admin12345');await page.locator('button').last().click();await page.setViewportSize({width:390,height:844});await page.goto(base+'/?page=admin');results.push({engine,base,route:'admin',width:390,noOverflow:await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)});
 }
 fs.writeFileSync('evidence/crossbrowser.json',JSON.stringify(results,null,2));await browser.close();
 }
 fs.writeFileSync('evidence/crossbrowser.json',JSON.stringify(results,null,2));console.log(`${results.length} проверок; ошибок переполнения: ${results.filter(x=>!x.noOverflow).length}`);
})().catch(e=>{console.error(e);process.exit(1)});
