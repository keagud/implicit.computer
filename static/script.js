const setQuote = () => (async () => {
  const quoteElements = document.querySelectorAll(".dynamic-quote");


  await fetch("/quotes.json")
    .then(r => r.json())
    .then(j => j["quotes"])
    .then(arr => {

      for (let e of quoteElements) {
      let index = Math.floor(Math.random() * (arr.length));
      e.textContent = `"${arr[index]}"`;

      }
    })
})();



setQuote();

