---json
{
    "title": "ActivityPub Part 2: GoToSocial Considered Neato",
    "date": "2024-06-23",
    "tags": [
        "100DaysToOffload",
        "Protocolapalooza",
        "tech",
        "ActivityPub",
        "gotosocial"
    ],
    "permalink": "/blog/activitypub-2.html",
    "layout": "post.html"
}
---


Here's the lesson I've learned since my last post: making a simple ActivityPub server that implements the minimum subset of the spec is not difficult. But to have the server be *actually usable and viable for federation*... well I don't think that's too difficult either, but it's more effort than I'm willing to expend on something that's only 25% of the overall project goal. 

Once you need to post messages to the inboxes of other servers, you need to keep track of which servers should be notified, and the keys needed to sign the messages, so naturally a database comes to mind. And at that point it's easier to just keep the actual post content in the database as well, so you need to make a mechanism to keep the database state in sync with the static site content, plus a bunch of SQL queries to fetch and organize the required data for each ActivityPub object, and eventually, while you're elbow-deep in yak fur, you remember that you still need to get going on the other three planned protocol integrations.

So I snapped out of my haze and turned to [GoToSocial](https://gotosocial.org/), a minimalist ActivityPub server designed for tiny or single-user instances that, most helpfully, also implements the Mastodon client API. That means I can offload the fiddly stuff to the GoToSocial process and just write some pretty standard REST API calls to interact with it as needed.


Before I get into the specific code, I need to talk about the overall deployment strategy I'm trying to stick to for this project. Everything is running on a Digital Ocean VPS (Debian) at the lowest tier (512 MB RAM, 1 CPU, 10GB disk) - partially this is because I like the challenge of programming with low resource availability, and partially it's because I'm not made of money. I have a systemd timer that runs this python script every minute:


```python
#!/bin/env python3

from pathlib import Path
import datetime as dt
import subprocess
import sys

LOCAL_PATH=Path("/var/site/")
REPO_URL = "https://github.com/keagud/implicit.computer.git"
LOCAL_PATH.mkdir(parents=True, exist_ok=True)

def update_last_changed():
    with open(LOCAL_PATH.joinpath("updated"), 'w') as fp:
        fp.write(dt.datetime.now().isoformat())

def main():
    head_file =  LOCAL_PATH.joinpath(".git/refs/heads/master")
    if head_file.exists():
        old_head = open(head_file, "r").read().strip()
        res = subprocess.run("git reset HEAD --hard && git pull", shell=True, cwd=LOCAL_PATH)
        res.check_returncode()

        new_head = open(head_file, "r").read().strip()
        if new_head == old_head:
            subprocess.run('logger -t "check-updates" "No changes to remote"', shell=True)
            sys.exit(0)
    else:
        subprocess.run(f"git clone {REPO_URL} {LOCAL_PATH.as_posix()}", shell=True).check_returncode()

        subprocess.run(f"git submodule update --init", shell=True, cwd=LOCAL_PATH).check_returncode()

    update_last_changed()


if __name__ == "__main__":
    main()
```


The gist is, it checks for changes to the remote and, if there are any, pulls them and pokes `/var/site/updated`.  Then I have another systemd service that watches for changes to that file[^1] and runs all the scripts in `/opt/site/on_change/` - for example, the script `/opt/site/on_change/build_web.sh` looks like this:

```bash
#!/bin/bash

zola --root /var/site build \
	--output-dir /var/www/implicit.computer/html \
	--force

```

Nginx is then configured to serve static files from that directory, etc etc. I like this flow, because it means the git repo where I keep my posts is the single source of truth and I can trivially tack on extra build tasks by adding a new script to that directory. 

Getting back to ActivityPub, though, there's a problem with this setup. A static site builder is kind of like a pure function  (in the functional programming sense) in that it deterministically maps an input (markdown files and configuration) into an output (the built site) without any kind of internal state. For the Web that's fine; some pages will be re-rendered unnecessarily on each build, but that's invisible from the perspective of the client. 


ActivityPub differs in that each posted status has a unique ID assigned by the server -GoToSocial in this case, which is out of my direct control - that's used for deduplication. A naive ActivityPub integration script that just sends a POST to GoToSocial for every content file on every build will result in a lot of duplicate entries that nonetheless have different IDs,  and hence spam for everyone that's federating with my instance. 

To avoid that, each post is sent with a spoiler text field generated from the slug and the posted date, acting as an ersatz primary key. When a rebuild is triggered, first all the previously sent posts are fetched and it's determined if any of the slugs for the posts in the local repo directory are unaccounted for in the spoiler text fields from the server. If not, there's nothing to do, so the program exits, otherwise it submits the new post content.  One downside here is that if I edit a post later for typos or clarification, there's no automated way to update the version GoToSocial has as well, and I instead need to manually update.


Overall this seems to work pretty well! The spoiler text workaround even doubles as a "see more" function to avoid showing huge walls of text unprompted. You can check it out by looking up `@blog@activity.implicit.computer` in the ActivityPub client of your choice (no included web view unfortunately - that's the cost of minimalism)

I do want to return to my from-scratch ActivityPub server eventually, but GoToSocial already has a lot of the properties I would want to emphasize - it's a single binary, it uses sqlite and it's very light on resource usage - so I'm not in a rush. Setting it up was also quite straightforward thanks to their excellent [documentation.](https://docs.gotosocial.org/en/latest/) 


The minimal client I wrote in Rust to handle API interactions is [here](https://codeberg.org/keagud/protocols) if you're curious. I'll also be using that repo going forward for any other code I write for this project. Speaking of, next time I'll be looking into [nostr](https://nostr.com/), and I hope to actually write the server myself for that. 



---
[^1]: That's kind of a hacky way to do it, I know, but I couldn't find an established "real" way to do this kind of thing with systemd.



