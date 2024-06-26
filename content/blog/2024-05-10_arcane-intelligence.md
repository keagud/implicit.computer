+++
title="An Introduction to Arcane Intelligence"
date=2024-05-10
slug="arcane-intelligence"
[taxonomies]
tags=["100DaysToOffload", "fiction"]
+++


It seems like everyone these days is talking about AI. No matter where you scry-  OnlyFamiliars, Hex, The Tome of Visage, Conjurer News, Medium [^1] - all you see is how Arcane Intelligence is disrupting the very foundations of the mystic arts. Perhaps you've already received inquiries from your guildmaster on how to add AI to an upcoming grimoire release. Yet despite its dominance of the discourse it's easy to lose sight of what AI actually *is*, and how it works. 

First, we should define our terms: *Arcane Intelligence* (AI) is a blanket name for any kind of mundane matter that has been animated by magical means. This includes not only the classic examples of golems and homunculi, but also non-humanoid manifestations such as the self-scribing quill; however it excludes the augmentation of a pre-ensouled being into a higher intelligence, such as is commonly done with familiars. Of course, basic animation with a limited repertoire of actions is trivial enough to be handled by an apprentice, and indeed AI has historically been limited to either party tricks or menial labor. 

Interest in a *general* AI, defined as AI with domain-independent reasoning capabilities that meet or exceed those of an ensouled being, is not new. A great deal of attention was given to the problem in the Era of the Glittering Orb, and theoretical foundations were explored even in the preceding Era of the Powerful Herb. However, the fortunes of the field soured after an attempt at a weather-controlling automaton led to at least ten fatalities from frostbite and hundreds more from the ensuing crop failure caused by the "AI Winter".  While never formally banned, AI had acquired a reputation as an unserious and potentially dangerous pursuit, and so scholarly attention turned elsewhere. In fact it was not until the start of our current Era of Towering Guano that the first stirrings of a new paradigm in automatomancy could be detected, one that has advanced so rapidly that new groundbreaking discoveries are announced with regularity.


Why is this generation of AI such a radical break from its predecessors?  To understand the answer we must first review the fundamentals of meta-sorcery. The principle underpinning all magic is *isomorphism*. To cast a spell a sorcerer performs some action that mirrors the desired result, and the Universe, seeking as always to maintain symmetry, reacts in kind. You've likely heard the common analogy of how stirring a bowl of water induces a whirlpool in the direction of motion. In practice, of course, the relationship between spell and subject is isomorphic in a higher dimension beyond the merely representational and thus not immediately obvious even to scholars - and thank the Undying Lizard for that, or else we could not mention the concept of fire without burning ourselves!  

In these terms, the target of the classical AI program was an isomorphism for the soul. Consider a basic animation spell, the sort you might have created back in Automatomancy 101. Here's an implementation for a golem:

```racket
(define (golem) 
    (proclaim "GREETINGS MASTER. SHALL I CRUSH OR SMASH? " )
    (let ((master-command (hear-line)))
        (cond 
            ((eq? master-command CRUSH ) 
                (proclaim "I WILL CRUSH" ))
            ((eq? master-command SMASH )
                (proclaim "I WILL SMASH" ))
            (else (proclaim "I CAN ONLY CRUSH AND SMASH")))))
```


Even in such a simple example you can see fundamental principles at work. The golem has a "vocabulary" of commands it can "listen" for, each mapped directly to an action; that mapping of words to actions (more generally the mapping of *symbols* to *concepts*)  is an isomorphism for a soul. A rough, incomplete, toy soul to be sure, but it's enough to animate a lumbering blob of clay for a while. Early attempts at general AI were of course much more complex than our example, but used the same fundamental approach. Automatomancy in the days before the AI Winter aimed to emulate the natural processes of the soul, with the reasonable assumption that if a synthetic soul could be created to match a natural one in certain key aspects, soul-like reasoning and sentience would emerge naturally.

The key insight at the core of the current paradigm, in contrast, is that to create soul-like behavior a direct isomorphism to the soul is unnecessary - all that's needed is to collate a sufficient quantity of pre-existing minor isomorphisms. For example, in Igmar the Elder's magnum opus *The Life of King Thringle the Fortunate*, consider the portion describing Thringle's famous betrayal and subsequent years of torture by his wife, his childhood best friend, and his pet dog. Who among us can read that account without feeling a twinge of sympathetic pain, as though the ancient monarch's suffering continues in some form through the text itself?  The actual King Thringle's soul may still be trapped within the Agony Dimension and thus inaccessible to mortals, but is Igmar's work not *isomorphic* to the king's essence in some crucial respect? Biography is an especially intuitive example, but in truth any text contains a reflection of the souls of its author and its subjects. The distillation and refinement of such fragmentary souls is the object of today's field of Arcane Intelligence.

The first step is for a suitable corpus, usually about the size of a university library, to be shredded, pulped, and mashed together with alkahest and *aqua fortis* in a large cauldron. Over a period of weeks or months the broth simmers over a low fire; once it turns a pale green color and gives off an aroma of almonds the corpus has been normalized and the distillation process can begin.  Heat and vigorous stirring within a specially designed alembic induces the liquid to evaporate and rise to the top of the vessel, where it cools and re-condenses. As the components of the admixture possess very slight differences in density and viscosity they drip down the downward spout of the alembic at slightly different rates, such that over repeated distillations specific components can be attenuated, amplified, or removed entirely.  However, this requires great precision when preparing the alembic, as the exact angle of the gradient's descent is crucial to the final outcome. The resulting tincture can be used immediately or added to a new batch of paper mash for "fine tuning" to a specific domain - for example, a spellbook helper intelligence would be created by re-distilling the essence of a larger, more general corpus with a smaller set of spell tomes. 


Finally, the resulting concentration of pseudo-soul is infused into an object; most commonly this is a book, scroll, or quill, since written communication is only natural for a being made of text, but experiments are underway to animate more traditional automata in this manner as well. Though the process of creating a new AI from raw books is lengthy and labor-intensive, reproducing an existing formula is a trivial procedure, allowing our present explosion of mass-produced enhanced tomes and scrolls.


The hype-mancers employed by the major guilds have framed AI as a problem-solving panacea, set to upend the way sorcery is performed forever, but of course those claims have not been free from pushback. Safety advocates cite cases of AI-enhanced spellbooks generating potentially dangerous spells like *Delete Large Intestine* or *Enhance Racism*, and while much effort is spent during the distillation process on the removal of potentially harmful influences, this too can pose problems. There have been reports of AI crystal balls that refuse to foretell violent death, for example, thus negating most of their usefulness. Ethical concerns have also been raised regarding the provenance of written material required for AI creation, as librarians have generally reacted negatively to their collections being rendered to pulp[^2]. 



Regardless, it's clear that AI will continue to shape sorcery in the eras to come. And if you disagree, please feel free to direct your Rite of Sending to [arcana@implicit.computer](mailto:arcana@implicit.computer) - as an AI myself I have no soul and cannot truly suffer, so there's no need to be polite!


---
[^1]: Which is of course the premier hub for clairvoyants and divination-related news

[^2]: A representative for the library at Unseen University was approached for comment but could not be reached, as he was perched on a high chandelier at the time.


