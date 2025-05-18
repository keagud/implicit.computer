---json
{
    "title": "ActivityPub Part 1: Static Files Are All You Need* (*to have a visible profile)",
    "date": "2024-06-10",
    "tags": [
        "100DaysToOffload",
        "Protocolapalooza",
        "tech",
        "ActivityPub"
    ],
    "permalink": "/blog/activitypub-1.html",
    "layout": "post.html"
}
---

After a few posts worth of preamble, it's finally time to get our hands dirty with ActivityPub! I started out by reading through the specification for [ActivityPub itself](https://www.w3.org/TR/activitypub/), which defines the inter-server and client-server interactions, and skimming the specification for [ActivityStreams](https://www.w3.org/TR/activitystreams-core/), which defines the schemas (schemata?) used for messages in those interactions. I do recommend you read at least the ActivityPub spec if you're interested - for a technical specification, it's actually very readable - but you shouldn't need to in order to follow this post. I also recommend [this blog post](https://blog.joinmastodon.org/2018/06/how-to-implement-a-basic-activitypub-server/) from Mastodon creator Eugen Rochko, where he walks through a basic toy implementation in Ruby.


First, a high-level primer on what's going on when you view an ActivityPub profile from a different server. When `@alice@foo.example` looks up the profile of `@bob@bar.example`, here's what happens:[^1] first, the server at `foo.example` sends a GET request to `bar.example/.well-known/webfinger?resource=acct:bob@bar.example`. If Bob is actually a user there, it sends a JSON response containing a link to Bob's [Actor Object](https://www.w3.org/TR/activitystreams-vocabulary/#actor-types), let's say `bar.example/users/bob`; this URI is what uniquely and canonically identifies Bob to the outside world. `foo.example` can then dereference the URI to get the Actor object, which can include a whole bunch of stuff depending on the implementing application. In the case of Mastodon, it might include references to a screen name that differs from the username, a list of followers or followed accounts, a summary to put in the account bio, and more. The bare minimum required by the specification, though, is just endpoints for an inbox to receive POSTs from other servers, and an outbox from which other servers can GET posted content.


Luckily, we don't actually care about getting messages from other servers (at least at this point), so the inbox endpoint can just point at nothing for the time being. In fact, let's put aside the task of POSTing at other inboxes as well and just set our sights on a publicly visible profile page; how much can we accomplish by just setting up a directory of static files and serving it with nginx?


First off, we need to handle requests to `/.well-known/webfinger?resource=acct:username@domain.com`, but since this is a server with exactly one user, we don't have to care about parsing the query parameters and can just put this in `/.well-known/webfinger.json`: 

```json
{
    "links": [
        {
            "href" : "https://activity.implicit.computer/users/blog.json",
            "rel" : "self",
            "type": "application/activity+json"
        }
    ],
    "subject" : "acct:blog@activity.implicit.computer"

}

```

(N.B. The `type : application/activity+json` is crucial to the whole operation. My first attempt had a minor typo in that line that caused Mastodon to silently ignore the link and claim the user didn't exist)

Right now this will ignore the query part of the incoming url entirely and always serve this same response; for the final version, though, I'll configure an nginx rule to 404 if the query doesn't match the `@blog@activity.implicit.computer` account. Once the requesting server gets this response, they'll query `/users/blog.json`, which again can just be a static file:


```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1"
  ],
  "id": "https://activity.implicit.computer/users/blog.json",
  "inbox": "https://activity.implicit.computer/inbox/",
  "name": "blog",
  "outbox": "https://activity.implicit.computer/outbox/outbox",
  "publicKey": {
    "id": "https://activity.implicit.computer/users/blog.pem",
    "owner": "https://activity.implicit.computer/users/blog.json",
    "publicKeyPem": "-----BEGIN RSA PUBLIC KEY-----\ndQw4w9WgXcQ...\n----END RSA PUBLIC KEY-----"
  },
  "type": "Service"
}

```

`type : Service` is to identify this actor as a bot; a human account would have a `Person` type. Everything else in the object should be fairly straightforward except the `publicKey` - we don't actually need that now, while we're just serving files to be requested by other servers, but Mastodon requires POSTs to be cryptographically signed, and I figured it would be easier to include that now than later.

One other thing worth stating explicitly is that the `id` must be a self-reference to the object itself. In other words, we need to make sure the `id` field for the Actor object always matches a URI where that same Actor object can be retrieved. 

As mentioned, the inbox endpoint doesn't need to do anything right now, but the [outbox](https://www.w3.org/TR/activitypub/#outbox) does. I believe you *can* just have a big old document with all the user's posts, but good manners dictates we add some paging to avoid an accidental DoS.[^2] 

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "first": "https://activity.implicit.computer/outbox/page0",
  "id": "https://activity.implicit.computer/outbox/outbox",
  "last": "https://activity.implicit.computer/outbox/page1",
  "totalItems": 25,
  "type": "OrderedCollection"
}
```

This includes links to the first and last pages (there's only 2 right now, but it can grow as I add more posts). Dereferencing the first page gives a list of all the IDs for my hot posts, in reverse chronological order, and a link to the next page in the series.


```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://activity.implicit.computer/outbox/page0",
  "next": "https://activity.implicit.computer/outbox/page1",
  "orderedItems": [
    "https://activity.implicit.computer/content/mastodon-server",
    "https://activity.implicit.computer/content/protocol-month",
    "https://activity.implicit.computer/content/vegetarian",
    ...
    ],
  "partOf": "https://activity.implicit.computer/outbox/outbox",
  "type": "OrderedCollectionPage"
}
```

The actual content for each post is served at `/content/<post-slug>.json`. For reasons that will become clear shortly, though, I cannot test that these files are formatted correctly yet, so I'll hold off on sharing the specifics for now. Putting it all together, we get this directory structure:

```
/var/activity
    /.well-known
        /webfinger.json
    /outbox
        /outbox.json
        /page0.json
        /page1.json
        ...
    /content
        /2-film-reviews.json
        /anglicization.json
        ...
    /users
        /blog.json

```


I wrote a Rust program to convert the raw markdown posts to JSON under the correct schema, and to write everything to a directory in the right configuration. It's not especially interesting IMO, but I'll still link the full source once the implementation is complete. Now we just point nginx at `/var/activity` and navigate to `@blog@activity.implicit.computer` in the Mastodon web interface, and voila! A visible profile!

There's a few immediately apparent issues, though. Most significantly, all my beautiful posts are gone! It turns out making the posts available to GET from an endpoint is only half the story; you also need to POST the activity to the inboxes of all following users. 

If you've used Mastodon, maybe you've had the experience of scrolling through someone's post history on a different instance, when you hit a message saying older posts could not be retrieved and you need visit the originating server to see them. The reason you can see the later messages is that someone on your instance followed that user, resulting in your instance receiving POST updates that could be then shown to you, but anything from before that happens is invisible.[^3] So while the content for this site is *technically* available over ActivityPub now, it won't be shown to anyone until we add a mechanism to post to the inboxes of other servers.

I think that's enough for now, though. Thanks for reading, and I hope you'll join me again next time as I leave the comfort of nginx and write some HTTP calls myself.

---
[^1]: Ignoring the cases where `foo.example` already has a cached response, or where its administrators have explicitly blocked `bar.example`,  etc etc.

[^2]: In practice putting everything in one object would probably not bring down the client requesting it, but I still think it'd be kind of rude.

[^3]: More on the rules for inter-server visibility [here](https://fedi.tips/which-posts-and-accounts-can-i-see-from-my-server/)
