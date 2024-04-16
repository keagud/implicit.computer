+++
title = "Hie to the Hinterlands"
date = 2024-03-22
[taxonomies]
tags = ["thinkin", "100DaysToOffload"]
+++


*#100DaysToOffload day 7/100*

The Web is getting worse. I'm not going to enumerate examples of how the big digital platforms have gotten slower/more bloated/more invasive/generally less functional in the last 5-ish years, but I'm sure you can think of some. 

Much has been made of the concept of [enshittification](https://en.wikipedia.org/wiki/Enshittification), which, again, I will assume you're already familiar with. As this process becomes more blatant and the rent-seeking is laid bare, we've seen migrations away from the large FAANG platforms to alternative online spaces, most notably the Fediverse and personal blogs (such as, ahem, this one). There's no term I'm aware of that encompasses this shadow version of the Web; "small web" gets used sometimes, but that's not quite what I'm talking about. It's one part, certainly, but I also want to include the Fediverse, and stuff using the Gemini protocol, and E2E encrypted messaging like Signal that's not part of "the Web" in quite the same way. I'm going to refer to this whole set as the *hinterlands* for reasons I hope will become clear later. 
 
 The hinterlands is tremendously diverse, but I propose some common traits by which to recognize if an online space qualifies:
 
 
### Growth (by whatever metric) is not considered the end goal, or an unalloyed good
When I started using the Fediverse I was kind of surprised by how even posts from popular accounts or public figures didn't get a lot of likes and shares. On Mastodon a toot has gone viral if it hits a triple digit share count. On Twitter, that's *peanuts*. A lot of the difference can be chalked up to the smaller number of users, but there's also a general cultural norm of indifference to or rejection of optimizing for bigger numbers that I find more salient.


### Accurate metrics are hard(er) or impossible to gauge.
Web metrics are a hard problem. Getting accurate metrics on the section of the Web outside the central platforms is functionally impossible, for partly technical and partly cultural reasons. On the technical side, protocols like RSS and ActivityPub simply do not have the capacity for any but the coarsest telemetry[^1]. Perhaps the admins of my Mastodon instance can determine my general location from my login IP, but that information is unavailable to the network as a whole because the ActivityPub protocol does not define how it could be shared. 

Culturally, hinterlanders are prone to pre-emptively covering their tracks. They use VPNs and uBlock and LibreWolf,  maybe even dedicated anti-tracker hardware like a [Pi-Hole](https://pi-hole.net/). As as a made-up example: I might see in my server log that 95% of visitors to this site are using Chrome on Windows, but I have zero faith in that number's accuracy because fudging User-Agent headers is easy and widespread[^2]. 


### Monetization is difficult or impossible by design and culture
How do you make a million dollars as a hinterlands influencer? You don't. Largely this follows from the above point: that which cannot be quantified cannot be sold. 

### You need to be somewhat "in the know" to find things
It's extremely unlikely that you are reading this because The Algorithm thought it would maximize your click-through rate. Probably you saw the link posted on Mastodon, or you know me in real life. If an algorithm did bring you here, it's likely one of the more transparent ones like Hacker News's ranking system[^3]. In other words, you probably didn't arrive here directly from the centralized Web; you came from somewhere else in the hinterlands. In the more extreme cases, hinterland zones might be invitation only and require an existing member to vouch for you.

### Division of (technical) labor is less stark. 
This site does not have a dedicated sysadmin or backend engineer or frontend design person; there's just me, a Docker image and some cron hacks, and this is not an especially unusual setup. That's not to say you can't post anything outside of a major platform without a CS degree, but it's generally less plug-and-play than, say, Medium. 

## Digital Barbarism

As I've migrated more and more into non-centralized Web spaces and those common traits have become more clear, I've been haunted by something familiar about the whole ecosystem. Only recently did it click into place: the Web is like the [Southeast Asian Massif](https://en.wikipedia.org/wiki/Southeast_Asian_Massif).

Or rather, it reminds me of James C. Scott's excellent book on the geopolitics of Southeast Asia, [The Art of Not Being Governed](https://en.wikipedia.org/wiki/The_Art_of_Not_Being_Governed), in which that region is called out as one especially resilient example of a *shatter zone* (or less technically, a *hinterland*). These are places in the hills (or just generally in rugged landscapes, but historically the association is with hills) where the city-states, nestled in agrarian valleys, can't reach you (or tax you or enslave you). Shatter zones are where the barbarians live.

"Barbarian" feels almost like a slur, or at least a negative value judgement, but that feeling alone speaks volumes. Barbarianism itself is pretty great; it's just been the target of a smear campaign going back to the literal dawn of civilization. The written historical record would lead you to believe all the cool stuff was happening in the Valley states, but that shouldn't be surprising- written language is a Valley technology!  

A barbarian is just defined as someone who's evaluated the contract offered by civilization and said nah, I'm good.  In fact, Scott argues that despite the Valley people constantly proclaiming the Hill folk to be a different and inferior people altogether, generally there's no significant genetic differences between the two groups and the ethnic angle is constructed *post hoc*. For most of human history, if you didn't like being a state subject, you could *literally just opt out and leave*.


That's not to imply it was easy to *stay* ungoverned. It takes effort and know-how... like an Art, if you will. Scott argues that the "primitive" traits historically associated with "barbarian" peoples - illiteracy, nomadism, non-hierarchy, to name a few - are evolved cultural defenses against civilizing projects[^4]: 

    Broadly speaking, whenever a society or part of a society elects to evade incorporation or appropriation, it moves toward simpler, smaller, and more dispersed social units—toward what we have earlier termed the elementary forms of social organization. The most appropriation-resistant social structures—though they also impede collective action of any kind—are acephalous ("headless") small aggregates of households. Such forms of social organization, along with appropriation-resistant forms of agriculture and residence, are invariably coded "barbarian," "primitive," and "backward" by the lowland padi "civilizations." It is no coincidence that this metric of more or less civilized agriculture and social organization should so perfectly map onto their suitability for appropriation and subordination, respectively 


To resist the yoke of civilization, you need to be agile. You need to be hard to measure, because if you can be measured you can be subjugated. You need to be at least a little out of the way and hard to reach. Crucially, you need to be able to [pack up and go somewhere else at any time](https://en.wikipedia.org/wiki/Self-hosting_(web_services)).

Barbarians aren't unproductive in the sense that they don't make things, but they're *economically* unproductive by design. They produce, but they do not produce [commodities](https://www.metafilter.com/95152/Userdriven-discontent#3256046). Surplus stuff just makes it harder to keep moving, after all.

Barbarian culture is simultaneously non-hierarchical and insular. Division of labor is less extreme than in the Valley, and often women enjoy comparable social status to men. But that doesn't make them friendly; you can't just waltz into camp and expect to be welcomed with open arms. Barbarians don't want to be [embraced](https://en.wikipedia.org/wiki/Embrace,_extend,_and_extinguish), because they know the first wave of conquest often puts on a smiling face.

Scott focuses on one specific region but clarifies that this pattern of convergent evolution happens all over the world. Barbarism isn't a single culture, it's a toolkit for maximizing autonomy that re-emerges when conditions are right. 

First, a central authority entices people to move in and put down roots. At the time this seems like a good deal, since it makes resources like markets a lot more accessible and allows access to new kinds of goods. Maybe the authority even redistributes resources (like farmland) to new settlers as an incentive. But this isn't sustainable, and sooner or later the settlers feel the burden of taxation, conscription, and in the most extreme (but pretty common historically) case, enslavement as the powers that be must squeeze them ever-harder to keep the wheels of government turning. So the common folk hang up their citizen caps, put on barbarian furs, and move out to the hinterlands.

Is it just me, or does that sound familiar?


## What Does This Actually Mean?
Well, I dunno. In any case, it's an interesting pattern to observe. 

One obvious difference between the digital hinterlands and the real one is the stakes involved. I've been speaking about digital "spaces" since that's the dominant metaphor, and while it's not like the online world is totally unimportant, it's inarguably far *less* important than the literal, physical world in which your human body lives. We talk about "migrating" off Twitter, but you can do that without leaving your chair.  Google will monetize the hell out of your data, but they will not literally enslave you [^5]. 

At the same time, it sure feels like they're the same *class* of thing, and the difference is one of degree rather than kind.  [It's like poetry, it rhymes](https://www.youtube.com/watch?v=yFqFLo_bYq0).




---
[^1]: I suppose I could look at nginx's logs to see who accessed the Atom feed and from where, but that's not especially helpful. I have no way of knowing which links were clicked, which pages within the feed were read the most and least, how long readers lingered on a given section before moving on, or any of the rest of the meat and potatoes of Web analytics.


[^2]: I know this because I use Firefox or LibreWolf on Linux, and *my User-Agent still says Chrome on Windows* because some sites will just give up if your request says you're using something else.


[^3]: Does Hacker News count though? Eeeh, I think it's kind of ambiguous. On an ordinal scale it's definately closer to Lemmy than Facebook in terms of these traits.

[^4]: Idk how to cite this properly since I got it from an ebook without obvious page numbering. It's from chapter 7, anyway.


[^5]: If you're reading this in like, 2044, it's possible that sentence aged *very poorly.*
