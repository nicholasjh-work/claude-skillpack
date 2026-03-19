# Pattern Reference -- 24 AI Writing Patterns
#
# scholar-editor v1.0.0
# License: MIT
# Source: Wikipedia:Signs_of_AI_writing (WikiProject AI Cleanup)
#         https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
# Academic grounding: MIT Technology Review (2022) statistical token analysis,
#                     ArXiv 1906.04043 Gehrmann et al. GLTR lexical proxies
#
# Key insight: LLMs use statistical algorithms to guess what should come next.
# The result tends toward the most statistically likely result that applies to
# the widest variety of cases -- which is why AI text feels generic.

---

## CONTENT PATTERNS

---

### P1 -- Undue Emphasis on Significance, Legacy, and Broader Trends
**Severity:** MED
**Trigger words:** stands as, serves as, is a testament to, is a reminder that,
vital/significant/crucial/pivotal/key role/moment, underscores/highlights its
importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting,
contributing to the, setting the stage for, marking/shaping the, represents/marks
a shift, key turning point, evolving landscape, focal point, indelible mark,
deeply rooted

**Problem:** LLMs puff up importance by adding statements about how arbitrary
details represent or contribute to a broader topic.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989,
> marking a pivotal moment in the evolution of regional statistics in Spain.
> This initiative was part of a broader movement across Spain to decentralize
> administrative functions.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and
> publish regional statistics independently from Spain's national statistics office.

---

### P2 -- Undue Emphasis on Notability and Media Coverage
**Severity:** LOW
**Trigger words:** independent coverage, local/regional/national media outlets,
written by a leading expert, active social media presence

**Problem:** LLMs hit readers with claims of notability without specific context.

**Before:**
> Her views have been cited in The New York Times, BBC, and Financial Times.
> She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus
> on outcomes rather than methods.

---

### P3 -- Superficial Analyses with -ing Endings
**Severity:** MED
**Trigger words:** highlighting..., underscoring..., emphasizing..., ensuring...,
reflecting/symbolizing..., contributing to..., cultivating/fostering...,
encompassing..., showcasing...

**Problem:** AI tacks present participle phrases onto sentences to add fake depth.

**Before:**
> The temple's color palette resonates with the region's natural beauty,
> symbolizing Texas bluebonnets and the Gulf of Mexico, reflecting the
> community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold. The architect said these referenced
> local bluebonnets and the Gulf coast.

---

### P4 -- Promotional and Advertisement-like Language
**Severity:** MED
**Trigger words:** boasts a, vibrant, rich (figurative), profound, enhancing its,
showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of,
groundbreaking (figurative), renowned, breathtaking, must-visit, stunning,
state-of-the-art, world-class, cutting-edge, innovative, dynamic, game-changing

**Problem:** LLMs default to tourist-brochure and press-release tone.

**Before:**
> Nestled within the breathtaking region of Gonder, Alamata Raya Kobo stands as
> a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its
> weekly market and 18th-century church.

---

### P5 -- Vague Attributions and Weasel Words
**Severity:** LOW
**Trigger words:** industry reports, observers have cited, experts argue,
some critics argue, several sources/publications (when few cited),
research suggests, studies show, it is widely believed

**Problem:** AI attributes opinions to vague authorities without specific sources.

**Before:**
> Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019
> survey by the Chinese Academy of Sciences.

---

### P6 -- Formulaic Challenges and Future Prospects Sections
**Severity:** LOW
**Trigger words:** Despite its... faces several challenges..., Despite these
challenges, Challenges and Legacy, Future Outlook, going forward,
continues to thrive, bright future ahead

**Problem:** LLMs insert a formulaic "Challenges" section as structural padding.

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban
> areas. Despite these challenges, with its strategic location, Korattur
> continues to thrive as an integral part of Chennai's growth.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The
> municipal corporation began a stormwater drainage project in 2022.

---

## LANGUAGE AND GRAMMAR PATTERNS

---

### P7 -- Overused AI Vocabulary Words
**Severity:** HIGH (when density > 3 per paragraph), MED (isolated use)
**Word list (expanded from research -- Desaire et al. 2023, GPTNone 2025):**
additionally, align with, crucial, delve, emphasizing, enduring, enhance,
fostering, garner, highlight (verb), interplay, intricate/intricacies,
key (adjective), landscape (abstract noun), leverage, navigate, orchestrate,
pivotal, robust, seamlessly, showcase, spearhead, tapestry (abstract noun),
testament, transformative, underscore (verb), valuable, vibrant, synergy,
holistic, proactive, thought leader, best-in-class, value-add, ecosystem,
impactful, innovative, dynamic, cutting-edge, game-changing, revolutionize,
championed, cultivated, comprehensive, demonstrating, showcasing, measurable,
meticulous, proven ability, proven record,
utilize (use "use"), facilitate (use "help"), results-driven, detail-oriented,
self-starter, passionate about, I am excited to, I am thrilled to,
delighted to announce, paradigm shift, mission-critical, synergize,
actionable insights, move the needle, circle back, bandwidth (non-technical),
dive deep, unpack, at the end of the day, going forward

**Problem:** These words appear far more frequently in post-2023 text and
cluster together in a recognizable pattern.

**Before:**
> Additionally, an enduring testament to Italian colonial influence is the
> widespread adoption of pasta in the local culinary landscape, showcasing
> how these dishes have integrated into the traditional diet.

**After:**
> Pasta dishes, introduced during Italian colonization, remain common,
> especially in the south.

---

### P8 -- Avoidance of "is"/"are" (Copula Avoidance)
**Severity:** MED
**Trigger words:** serves as, stands as, marks, represents [a], boasts,
features, offers [a], functions as, acts as

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Gallery 825 serves as LAAA's exhibition space. The gallery features four
> separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space. The gallery has four rooms totaling
> 3,000 square feet.

---

### P9 -- Negative Parallelisms
**Severity:** MED
**Trigger phrases:** Not only...but..., It's not just about..., it's...,
It's not merely..., it's..., This isn't just..., More than just...

**Problem:** These constructions are overused to artificially elevate importance.

**Before:**
> It's not just about the beat riding under the vocals; it's part of the
> aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

---

### P10 -- Rule of Three Overuse
**Severity:** MED
**Pattern:** Any list of exactly three items used for rhetorical effect rather
than completeness.

**Problem:** LLMs force ideas into threes to appear thorough.

**Before:**
> The event features keynote sessions, panel discussions, and networking
> opportunities. Attendees can expect innovation, inspiration, and industry
> insights.

**After:**
> The event includes talks, panels, and informal networking between sessions.

**Note:** A list of three is fine when there genuinely are three distinct things.
Flag only when the three items feel padded or when two would suffice.

---

### P11 -- Elegant Variation (Synonym Cycling)
**Severity:** LOW
**Pattern:** The same entity referred to by a different synonym in each sentence
to avoid repetition.

**Problem:** AI repetition-penalty causes excessive synonym substitution that
reads as artificial.

**Before:**
> The protagonist faces many challenges. The main character must overcome
> obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.

---

### P12 -- False Ranges
**Severity:** LOW
**Pattern:** "from X to Y" where X and Y are not on a meaningful scale or
spectrum.

**Problem:** LLMs use range constructions to simulate comprehensiveness.

**Before:**
> Our journey has taken us from the singularity of the Big Bang to the grand
> cosmic web, from the birth and death of stars to the enigmatic dance of
> dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about
> dark matter.

---

## STYLE PATTERNS

---

### P13 -- Punctuation Pattern Failures
**Severity:** HIGH (em dash density > 2 per paragraph), MED (contraction avoidance,
semicolon/colon deficit), LOW (isolated em dash, curly quotes, ellipsis char)
**Detection basis:** Desaire et al. (2023) -- punctuation is one of four major
feature categories in their >99% accuracy classifier; Goedecke (2024) em dash
frequency analysis; VERMILLION framework.

**Em dash overuse:** LLMs use em dashes at historically elevated rates.
Replace with comma, period, colon, or parentheses. Flag > 2 per paragraph.

**Semicolon and colon deficit:** Human academic writers use more semicolons
and colons than AI. These mark nuanced logical relationships. AI avoids them.
Add them where two independent but related clauses connect.

**Contraction avoidance:** AI writes "do not" instead of "don't," "cannot"
instead of "can't" in informal contexts. This creates artificial formality.
Use contractions where a human writer of the target register would.

**Capital letters per period (Desaire et al., 2023):** Human text contains
2x more capital letters per period than AI text -- reflecting more proper
nouns, acronyms, and domain terminology. Increasing named references naturally
fixes this.

**Ellipsis character:** AI often uses the single Unicode ellipsis character
rather than three separate periods. Flag and replace.

**Before:**
> The term is primarily promoted by Dutch institutions--not by the people
> themselves. You do not say "Netherlands, Europe" as an address--yet this
> mislabeling continues--even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people
> themselves. You don't say "Netherlands, Europe" as an address; yet this
> mislabeling persists in official documents.

---

### P14 -- Overuse of Boldface
**Severity:** LOW
**Pattern:** More than 3 bolded phrases per paragraph, or bolding that
emphasizes non-critical terms.

**Problem:** AI chatbots emphasize phrases in boldface mechanically.

**Before:**
> It blends **OKRs**, **KPIs**, and visual strategy tools such as the
> **Business Model Canvas** and **Balanced Scorecard**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model
> Canvas and Balanced Scorecard.

---

### P15 -- Inline-Header Vertical Lists
**Severity:** LOW
**Pattern:** Bullet list where each item starts with a bolded word or phrase
followed by a colon and explanation.

**Problem:** AI outputs this structure reflexively instead of writing prose.

**Before:**
> - **User Experience:** The interface has been significantly improved.
> - **Performance:** Algorithms have been optimized for speed.
> - **Security:** End-to-end encryption has been added.

**After:**
> The update improves the interface, speeds up load times, and adds
> end-to-end encryption.

---

### P16 -- Title Case in Headings
**Severity:** LOW
**Pattern:** All main words capitalized in a section heading.

**Problem:** AI chatbots capitalize headings in Title Case by default.

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships

---

### P17 -- Emojis Used as Structural Decoration
**Severity:** LOW
**Pattern:** Emojis at the start of bullet points or headings when not
contextually appropriate.

**Before:**
> - Rocket Launch Phase: Product launches Q3
> - Key Insight: Users prefer simplicity
> - Next Steps: Schedule follow-up

**After:**
> The product launches in Q3. User research showed a preference for simplicity.
> Next step: schedule a follow-up.

---

### P18 -- Curly Quotation Marks
**Severity:** LOW
**Pattern:** Unicode "smart quotes" in text that should use straight ASCII quotes.

**Note:** Flag only when the surrounding text uses mixed quote styles, or when
the source was clearly plain-text and curly quotes are an AI artifact.

---

## COMMUNICATION PATTERNS

---

### P19 -- Collaborative Communication Artifacts
**Severity:** HIGH
**Trigger phrases:** I hope this helps, Of course!, Certainly!, You're absolutely
right!, Would you like me to..., Let me know if..., Here is a..., Here's a...,
Happy to help, Great question!, Feel free to ask, As requested, I'd be happy to

**Problem:** Chatbot correspondence phrases get pasted into content as-is.

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me
> know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages
> led to widespread unrest.

---

### P20 -- Knowledge-Cutoff Disclaimers
**Severity:** LOW
**Trigger phrases:** as of my last update, as of [date], up to my last training,
while specific details are limited, based on available information,
I don't have access to real-time

**Problem:** AI disclaimers about incomplete knowledge left in published text.

**Before:**
> While specific details about the company's founding are not extensively
> documented in readily available sources, it appears to have been established
> sometime in the 1990s.

**After:**
> The company was founded in 1994, according to its registration documents.

---

### P21 -- Sycophantic/Servile Tone
**Severity:** HIGH
**Trigger phrases:** Great question!, You're absolutely right!, That's an
excellent point!, Absolutely!, Of course!, Certainly!, I'd be delighted to

**Problem:** Overly positive, people-pleasing language signals chatbot output.

**Before:**
> Great question! You're absolutely right that this is complex. That's an
> excellent point about the economic factors.

**After:**
> The economic factors are relevant here.

---

## FILLER AND HEDGING PATTERNS

---

### P22 -- Filler Phrases
**Severity:** MED (in professional writing), LOW (in casual writing)

**Replace these exactly:**
- "In order to achieve this goal" -> "To achieve this"
- "Due to the fact that" -> "Because"
- "At this point in time" -> "Now"
- "In the event that" -> "If"
- "Has the ability to" -> "Can"
- "It is important to note that" -> (delete, lead with the fact)
- "It is worth noting that" -> (delete)
- "It goes without saying that" -> (delete)
- "As previously mentioned" -> (delete or refer specifically)
- "In today's fast-paced environment" -> (delete)
- "In the modern era" -> (delete or be specific)
- "At the end of the day" -> (delete)
- "Moving forward" -> "Next" or be specific
- "Going forward" -> same
- "In terms of" -> rewrite the sentence
- "With regard to" -> "On" or rewrite
- "Generally speaking" -> (delete or be specific)
- "In many cases" -> (delete or give a specific case)
- "It could be argued that" -> state the argument directly
- "One might suggest that" -> (delete the frame, make the claim)
- "Broadly speaking" -> (delete)
- "For all intents and purposes" -> (delete)
- "To a certain extent" -> specify the extent or cut
- "It is fair to say that" -> (delete, just say it)
- "In light of the above" -> (delete, connect ideas directly)
- "As we can see" -> (delete, trust the reader)
- "Needless to say" -> (delete -- if needless, don't say it)

---

### P23 -- Excessive Hedging and Confidence Moderation
**Severity:** LOW (stacking), MED (systematic confidence leveling)
**Detection basis:** ResearchGate (2025) paraphrasing study -- AI applies
systematic "confidence moderation": strong claims get softened ("undoubtedly"
-> "clearly"), uncertain claims get hedged further. Result: uniform medium
confidence throughout, regardless of actual evidence.

**Pattern 1 -- Stacked qualifiers:**
Two or more qualifiers in a single claim drain it of any content.

**Before:**
> It could potentially possibly be argued that the policy might have some
> effect on outcomes.

**After:**
> The policy may affect outcomes.

**Pattern 2 -- Uniform confidence leveling:**
Every claim carries the same level of certainty, whether discussing
well-established facts or speculative ideas. Human writers are more confident
on established claims and more tentative on uncertain ones.

**Before:**
> This approach may potentially improve outcomes. The method could possibly
> reduce costs. Results might be significant.

**After:**
> This approach improves outcomes -- the evidence on that is solid.
> Cost reduction is plausible but we don't have numbers yet.
> The results could be significant or trivial; we won't know until Q2.

**Note:** One qualifier is correct and necessary on uncertain claims. Flag when:
- Two or more qualifiers appear in one sentence
- Every sentence in a paragraph carries the same hedging intensity
- Hedge language appears on claims that are actually well-established

---

### P24 -- Generic Positive Conclusions
**Severity:** HIGH
**Trigger phrases:** The future looks bright, exciting times lie ahead,
this journey toward excellence, the possibilities are endless, in conclusion,
to summarize, as we look to the future, together we can, only time will tell,
this is just the beginning, the best is yet to come

**Problem:** AI closes with generic uplift that adds no information.

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they
> continue their journey toward excellence.

**After:**
> The company plans to open two more locations next year.

---

## Severity Quick Reference (P1-P24)

| Severity | Patterns | Action |
|---|---|---|
| HIGH | P7 (dense), P13 (dense), P19, P21, P24 | Block in CLEAN mode; mandatory fix in VOICE mode |
| MED | P1, P3, P4, P8, P9, P10, P13 (punctuation), P22, P23 (systematic) | Fix in both modes |
| LOW | P2, P5, P6, P11, P12, P14, P15, P16, P17, P18, P20, P23 (stacking) | Fix when they cluster; ignore isolated instances in short text |

See `references/patterns-research.md` for P25-P38 (research-grounded structural,
stylometric, and domain-specific patterns). Load alongside this file in Pass 2.
