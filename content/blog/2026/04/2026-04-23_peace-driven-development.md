+++
title = "Peace-Driven Development"
slug = "peace-driven-development"
date = 2026-04-23
aliases = [ "blog/peace-driven-development",]

[taxonomies]
tags = [ "webdev", "meta",]
+++


This site first participated in the fine tradition of [CSS Naked Day](https://css-naked-day.org/) in [2024](https://implicit.computer/blog/2024/04/css-naked-2024/), and it *should* have done so again automatically in 2025 if the script I wrote worked (I didn't think to check at the time). That CSS-less version was functional, but wonky and not especially nice to read. At the time I was using a heavily tweaked version of the [no style, please!](https://www.getzola.org/themes/zola-no-style-please/) theme and leaning a lot on CSS to make my additions cohere with the base theme; minus that CSS band-aid there were a lot of random `<div>`s and `<span>`s peppered everywhere. I never did any accessibility testing on that version of the site but I imagine it was not great in that regard either.

In the summer of 2025 I finally committed to re-writing my [Zola](https://www.getzola.org/) templates from scratch: no base theme, no dependencies, just rawdoggin the HTML. I'm by no stretch a professional web designer but I think the end result looked pretty OK for an amateur effort - it had light and dark modes, responsive menus for mobile screens, the other basic bells and whistles people expect nowadays. I also took the chance to replace all those odd block elements with proper [semantic HTML](https://developer.mozilla.org/en-US/curriculum/core/semantic-html/). That theme remained for about 6 months until April 9, 2026 rolled around, when I remembered to check out the live CSS-less site and found that, to my shock and some amount of horror, it looked *way better* that way. It was like being the idiot disciple slapped into enlightenment in the last line of a [kōan](https://en.wikipedia.org/wiki/Koan).


Probably my impression is shaped by the years of needing to interact with multi-megabyte React web apps that show you multiple seconds of ugly [skeleton text](https://www.nngroup.com/articles/skeleton-screens/) before you're permitted to see the 10 KB of text you actually came to read, but I find myself conditioned now to see an unstyled page of HTML as something profoundly *peaceful.* Zen, almost. You get the thing you came for, quickly, and nothing else. It's an honest signal that the author has faith in their content to stand on its own merits. So, I removed nearly all of the handcrafted styles in favor of letting the [W3C](https://www.w3.org/) take the wheel. There's still some CSS, mostly to keep the top nav menu from bunching up and to keep the main text centered and readable. But it's much less, only around 100 lines in total, and every line has a clear purpose. My friend Wyatt takes this approach even further with his [mostly plaintext blog](https://wyattscarpenter.github.io/blog/), something I respect the hell out of in principle, but I do think hypertext is cool and based and I'm not willing to give that up just yet.


I will accept that this aesthetic reaction could be unique to me, and that for most people the modern web app design philosophy provides a preferable experience. That's quite possible. If you feel that way, I invite to you bring back the "normal" Web experience on this site by closing your eyes for 1-5 seconds after clicking a link, to simulate load times slower than instantaneous, and to subject whatever device you're using to a hairdryer until it's toasty warm and throttling hard. You should also email your name, date of birth, citizenship status and sexual orientation to [info@palantir.com](mailto:info@palantir.com) to simulate the cookie tracking I don't use. 

(snark aside - the *actual* intended reading experience for Implicit Computer has always been RSS, which you can configure in your client however you like)
