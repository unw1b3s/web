const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs');
(async()=>{
const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const page=await browser.newPage({viewport:{width:1280,height:900}});
const checks=[]; const errors=[]; page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8080');
await page.screenshot({path:'evidence/home-desktop.png',fullPage:true});
await page.goto('http://127.0.0.1:8080/?page=register');
await page.locator('button[type=submit],button').last().click();
checks.push({test:'Клиент показывает ошибку пустой формы',passed:!!await page.locator('.client-error').textContent()});
await page.screenshot({path:'evidence/register-validation.png',fullPage:true});
await page.goto('http://127.0.0.1:8080/?page=login');
await page.locator('[name=login]').fill('student');await page.locator('[name=password]').fill('Student123');await page.locator('button').last().click();
await page.screenshot({path:'evidence/account.png',fullPage:true});
await page.goto('http://127.0.0.1:8080/?page=applications');
while(await page.getByRole('button',{name:'Удалить заявку',exact:true}).count()) await page.getByRole('button',{name:'Удалить заявку',exact:true}).first().click();
await page.goto('http://127.0.0.1:8080/?page=apply');
await page.locator('[name=event]').selectOption({index:1}); await page.locator('[name=payment]').selectOption('invoice');await page.locator('[name=room]').selectOption('small');await page.locator('button').last().click();
checks.push({test:'Заявка из браузера',passed:(await page.locator('main').textContent()).includes('Изменения сохранены')});
await page.screenshot({path:'evidence/applications.png',fullPage:true});
for(const route of ['events','account','applications','apply']){
await page.setViewportSize({width:390,height:844});await page.goto('http://127.0.0.1:8080/?page='+route);
checks.push({test:'390×844 '+route,passed:await page.evaluate(()=>document.documentElement.scrollWidth<=390)});
await page.screenshot({path:'evidence/mobile-'+route+'.png',fullPage:true});
}
await page.getByRole('button',{name:'Выйти',exact:true}).click();
for(const route of ['register','login']){
await page.goto('http://127.0.0.1:8080/?page='+route);checks.push({test:'390×844 '+route,passed:await page.evaluate(()=>document.documentElement.scrollWidth<=390)});await page.screenshot({path:'evidence/mobile-'+route+'.png',fullPage:true});
}
await page.goto('http://127.0.0.1:8080/?page=login');await page.locator('[name=login]').fill('admin');await page.locator('[name=password]').fill('Admin12345');await page.locator('button').last().click();
await page.goto('http://127.0.0.1:8080/?page=admin');checks.push({test:'390×844 admin',passed:await page.evaluate(()=>document.documentElement.scrollWidth<=390)});await page.screenshot({path:'evidence/mobile-admin.png',fullPage:true});
await page.setViewportSize({width:1280,height:900}); await page.screenshot({path:'evidence/admin.png',fullPage:true});
await page.locator('[name=status]').first().selectOption('3');await page.getByRole('button',{name:'Показать',exact:true}).click();await page.screenshot({path:'evidence/admin-filter.png',fullPage:true});
await page.emulateMedia({reducedMotion:'reduce'});checks.push({test:'Отключение анимаций',passed:await page.locator('main').evaluate(el=>getComputedStyle(el).animationName)==='none'});
checks.push({test:'Нет ошибок JavaScript',passed:errors.length===0});
fs.writeFileSync('evidence/browser.json',JSON.stringify({browser:await browser.version(),checks,errors},null,2));
console.log(JSON.stringify(checks,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
