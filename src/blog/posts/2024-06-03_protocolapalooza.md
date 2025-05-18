---json
{
    "title": "Announcing Protocolapalooza!",
    "date": "2024-06-03",
    "tags": [
        "100DaysToOffload",
        "Protocolapalooza",
        "tech"
    ],
    "permalink": "/blog/protocol-month.html",
    "layout": "post.html"
}
---

It's a new day, a new month, and a new era for the implicit dot computer weblog. 

I've been posting somewhat less frequently than I'd like (or than I need to keep my pace for [#100DaysToOffload](/tags/100daystooffload)) while I've prepared for the Network+ and Security+ exams. But now that I'm on the other side of that and beginning to ramp up the job search into overdrive, I need some kind of larger project to distract myself from continually refreshing my email inbox.

Therefore, I hereby decree the month of June 2024 (plus possibly part of July as needed) to be PROTOCOLAPALOOZA!


As I've [previously discussed](/blog/hinterlands), there's a whole shadow-Web of decentralized, non-commercial, quality stuff for those who know where to look. A lot of it is trusty old HTML over HTTP that's just tucked away in a quieter corner of the Web, but there's also some more daring projects that take a radically different approach. We're currently in the midst of a Cambrian explosion of alternative visions for what the Internet might be, and this month I want to dive into the primordial soup and highlight some of my favorite weird isopods. 

The specific "indie" protocols I want to examine are:

- ActivityPub (https://en.wikipedia.org/wiki/ActivityPub)
- Nostr (https://en.wikipedia.org/wiki/Nostr)
- Gopher (https://en.wikipedia.org/wiki/Gopher_(protocol))
- Gemini (https://en.wikipedia.org/wiki/Gemini_(protocol))


Of those, only Gopher and Gemini are "true" layer 7 protocols; messages in both ActivityPub and Nostr are functionally just JSON transmitted over HTTP/HTTPS. But I'm including them anyway because I think there's a family resemblance between the members of this set, even with such a clear split down the middle. Plus, if I do a series on the indie internet I kind of *have* to include ActivityPub, otherwise it would feel incomplete. 


The best way to learn is doing, so what better way to examine the Fediverse, Gopherspace, Geminispace and ... the Nostrsphere? ... than to integrate this very site with each of them? For each exploration, my goal will be to make this site's content available over the protocol, ideally by implementing it myself from scratch (I reserve the right to fall back to a library if needed, though). 

By "availability" over a protocol I mean the text content of this site (such as this post) should be accessible to an appropriate client in the "normal" way it would fetch content. That's going to vary - for example, Gopher is a pretty straightforward client-server setup, but ActivityPub clients add an additional layer of indirection by communicating with a "home" server that then "federates" with other servers (like email, kind of).  I would consider the "normal" method of fetching content for ActivityPub to be that server-server interaction rather than the client-server one, so that's what I'll be implementing. Non-text content is off the table entirely for my own sanity.


Next time, I'll start digging into ActivityPub. If this sounds like your jam, consider subscribing to the [atom feed](/atom.xml) to get my posts delivered hot and fresh right from the text editor. If not, that's also fine, I've been told there are other websites you can visit.
