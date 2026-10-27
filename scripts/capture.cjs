const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs');const path=require('path');
(async()=>{
const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const page=await browser.newPage({viewport:{width:1280,height:900}});const map=JSON.parse(fs.readFileSync('evidence/practice-map.json'));
const sources={3:'applications.png',4:'register-validation.png',9:'admin-filter.png',10:'home-desktop.png',11:'review.png',13:'mobile-applications.png',14:'account.png',17:'workshop-desktop.png',18:'workshop-mobile.png'};
const results=[];
for(const [n,dir] of Object.entries(map)){
 await page.setViewportSize({width:1280,height:900});
 await page.goto('file://'+path.resolve(dir,'result.html'));
 await page.screenshot({path:path.join(dir,'report-screen.png'),fullPage:true,animations:"disabled"});
 if(sources[n]) fs.copyFileSync('evidence/'+sources[n],path.join(dir,'screenshot.png'));
 else if(n==='8') {await page.setViewportSize({width:390,height:844});await page.goto('file://'+path.resolve(dir,'mobile-register.html'));await page.screenshot({path:path.join(dir,'screenshot.png'),fullPage:true,animations:"disabled"});}
 else if(n==='7'){await page.goto('file://'+path.resolve(dir,'moodboard.html'));await page.screenshot({path:path.join(dir,'screenshot.png'),fullPage:true,animations:"disabled"});}
 else fs.copyFileSync(path.join(dir,'report-screen.png'),path.join(dir,'screenshot.png'));
 results.push({practice:Number(n),screenshot:path.join(dir,'screenshot.png'),report:path.join(dir,'report-screen.png'),source:sources[n]?'Снимок работающего приложения':'Снимок результата в браузере'});
}
for(const n of ['7','8']){
 for(const file of fs.readdirSync(map[n]).filter(f=>f.startsWith(n==='7'?'mockup-':'mobile-')&&f.endsWith('.html'))){
 await page.setViewportSize(n==='7'?{width:1280,height:900}:{width:390,height:844});await page.goto('file://'+path.resolve(map[n],file));await page.screenshot({path:path.join(map[n],file.replace('.html','.png')),fullPage:true,animations:"disabled"});
 results.push({practice:Number(n),file,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
 }
}
fs.writeFileSync('evidence/screenshots.json',JSON.stringify(results,null,2));console.log('Captured',results.length);
await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
