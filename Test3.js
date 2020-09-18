//Puppeteer
const puppeteer = require("puppeteer");
const _ = require("lodash");

//General variables
const headlessFlag = true;

//main function
(async function main() {
  try {
    console.log("Started");
    const browser = await puppeteer.launch({ headless: headlessFlag });
    const page = await browser.newPage();
    page.setUserAgent(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    );

    await page.goto(
      "https://imagingupload.concursolutions.com/file/p0001055xim2/7FC1C0838EEF2D19B03F2A9E2B52F543CDCD050336DA1B262F2F0CBB728073A99B22BFB1F9718E577AF3A223A0636CA66853161DDA38FD1D2BA6E96136F6C8CCH1BFBA923443E222081608D3C90809491?id=52A05C7905824F098B63&e=p0001055xim2&t=AN&s=Expense-EMT"
    );
    console.log("URL loaded");
  } catch (e) {
    console.log("our error", e);
  }
})();
