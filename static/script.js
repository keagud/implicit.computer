const setQuote = () => (async () => {
  const quoteElement = document.querySelector(".dynamic-quote");

  if (isNakedCSS()) {

    let nakedLink = document.createElement('a');
    nakedLink.innerText = "happy CSS naked day!"
    nakedLink.href = "https://css-naked-day.github.io/";

    quoteElement.appendChild(nakedLink);
    return;

  }


  await fetch("/quotes.json")
    .then(r => r.json())
    .then(j => j["quotes"])
    .then(arr => {
      let index = Math.floor(Math.random() * (arr.length));
      quoteElement.textContent = `"${arr[index]}"`;
    })
})();



function removeCSS() {
  let styleLinks = document.querySelectorAll('link[rel="stylesheet"]');

  let styleBlocks = document.querySelectorAll('style');

  for (const e of [...styleLinks, ...styleBlocks]) {
    e.parentNode.removeChild(e);
  }
}


function isNakedCSS() {
  let today = new Date();


  console.log(today.getUTCMonth());
  console.log(today.getUTCDate());
  //getUTCMonth is zero-indexed, so 3 is April
  return (today.getUTCMonth() === 3 && Math.abs(today.getUTCDate() - 9 ) <= 1);



}


function main() {
  setQuote();
  if (isNakedCSS()) { 
    console.log("It's april 9");

    removeCSS(); }
}

main();
