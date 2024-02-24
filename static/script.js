(async () => {
  const quoteElement = document.querySelector(".dynamic-quote");
  await fetch("/quotes.json")
    .then(r => r.json())
    .then(j => j["quotes"])
    .then(arr => {
      let index = Math.floor(Math.random() * (arr.length));
      quoteElement.textContent = `"${arr[index]}"`;
    })
})();

