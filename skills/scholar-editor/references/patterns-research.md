# Research-Grounded Patterns -- P25 through P38
#
# scholar-editor v2.0.0
# License: MIT
# Author: Nick Hidalgo
#
# Sources:
#   Desaire et al. (2023) Cell Reports Physical Science -- >99% accuracy classifier
#   GPTZero / Tian (2023) Princeton -- perplexity and burstiness methodology
#   Hans et al. (2024) ICML -- Binoculars zero-shot detection
#   Georgiou et al. (2024) MDPI -- linguistic feature analysis
#   Liang et al. (2023) Stanford/Patterns -- GPT detector bias
#   Kendro, Maloney & Jarvis (2025) eScholarship -- lexical diversity
#   Shaib et al. (2024) -- syntactic template repetition
#   Tercon (2025) arXiv:2510.05136 -- linguistic survey
#   VERMILLION framework (ResearchLeap, 2025)
#   Originality.ai LinkedIn study (2025)
#   Willo resume detection study (2025)
#   Goedecke (2024) -- em dash frequency analysis
#   Multiple domain-specific sources cited inline
#
# These 14 patterns address structural, statistical, and stylometric signals
# that detectors actually measure. Load alongside patterns-24.md.
# Apply in Pass 2 of both CLEAN and VOICE modes.

---

## STRUCTURAL PATTERNS (statistical signals)

---

### P25 -- Sentence-Length Uniformity (Low Burstiness)
**Severity:** CRITICAL
**Detection basis:** GPTZero burstiness metric (Tian, Princeton, 2023);
Desaire et al. (2023) sentence-length diversity as core classifier feature;
Munoz-Ortiz et al. (2024) -- humans show "more scattered sentence length distributions."

**Signal:** AI sentences cluster in a narrow 15-25 word band with low
standard deviation. Human writing produces dramatically wider variance --
fragments, rhetorical questions, and 50+-word constructions sit alongside
short punchy statements.

**How to detect (manual):** Count the words in each sentence. If the shortest
and longest are within 10 words of each other for a full paragraph, that is
a burstiness failure.

**Before:**
> The company launched its new product line in the fourth quarter. The launch
> included three new SKUs targeted at enterprise customers. The reception from
> early adopters was positive across all metrics.

**After:**
> The company launched three new enterprise SKUs in Q4. Early reception was
> strong. Not everyone was convinced -- one early adopter called the pricing
> "aggressive" -- but the volume numbers held.

**Fix rules:**
- Every paragraph must contain at least one sentence under 8 words.
- Every paragraph must contain at least one sentence over 30 words.
- Use fragments deliberately. Use one-sentence paragraphs.
- Vary the opening construction: not every sentence starts with subject-verb.

---

### P26 -- Equivocal Language Deficit (Transition Imbalance)
**Severity:** HIGH
**Detection basis:** Desaire et al. (2023) -- "but", "however", "although"
significantly more frequent in human academic writing; one of the highest-weight
features in their >99% accuracy XGBoost model.

**Signal:** AI overuses additive transitions (Furthermore, Additionally, Moreover,
Moreover, That being said, In addition) at 3-5x the human rate. AI underuses
contrastive transitions (but, however, although, yet, still, even so, that said).
The ratio of additive-to-contrastive transitions is a reliable detection signal.

**Additive overuse list:** Furthermore, Moreover, Additionally, In addition,
As well as, On top of that, Not only that, That being said, Moving on,
Building on this, Let's now turn to, Now let's consider

**Contrastive underuse list:** but, however, although, yet, still, even so,
that said, despite this, in contrast, on the other hand, regardless, nonetheless

**Before:**
> The new process reduces waste. Furthermore, it cuts processing time by 30%.
> Additionally, employee satisfaction has improved. Moreover, costs are down.

**After:**
> The new process reduces waste and cuts processing time by 30%. Costs are down.
> Employee satisfaction has improved too, although it's too early to say whether
> that's causal or just coincidence.

**Fix rules:**
- For every two "Furthermore/Additionally/Moreover" occurrences, add at least
  one contrastive connector.
- Drop formal transitions entirely where possible -- let semantic flow do the work.
- Use casual alternatives: "But," "And," "Plus," "Here's the thing."

---

### P27 -- Impersonal Epistemic Hedging
**Severity:** HIGH
**Detection basis:** VERMILLION framework Signal I (ResearchLeap, 2025);
multiple sources confirm 3-5x overuse rate. Liang et al. (Stanford, 2023)
note that formulaic hedging is a core feature of AI text.

**Signal:** AI hedges with impersonal formulaic phrases at high frequency.
Humans hedge with first-person epistemic phrases that signal actual uncertainty
rather than trained politeness patterns.

**Impersonal AI hedges (flag these):**
It's important to note that, It's worth noting that, It should be noted that,
It's worth mentioning that, It is crucial to understand that, Generally speaking,
In many cases, It is widely accepted that, As a general rule, Broadly speaking,
It would be remiss not to mention, One might argue that, It could be argued that

**Human epistemic equivalents (use these instead):**
I think, I suspect, I'm not sure but, From what I've seen, In my experience,
As far as I can tell, My read is, I'd guess, That said, Honestly,
Worth flagging, One thing I'm not sure about, This is where it gets murky

**Before:**
> It's important to note that the data may not be fully representative.
> It should be noted that further research is needed in this area.

**After:**
> The data is thin -- I wouldn't draw hard conclusions from it. This area
> needs more research before anyone should feel confident either way.

**Fix rules:**
- Replace impersonal hedges with first-person equivalents where context allows.
- In formal/technical writing where first-person is inappropriate, delete the
  hedge entirely and lead with the substantive claim plus an explicit qualifier.
- One hedge per paragraph maximum. Delete the rest.

---

### P28 -- Lexical Dispersion (Even Word Distribution)
**Severity:** MED
**Detection basis:** Kendro, Maloney & Jarvis (2025) eScholarship -- SVM
classifiers achieve >97% accuracy using lexical diversity metrics alone;
dispersion identified as the discriminating dimension.

**Signal:** AI distributes repeated words evenly across a document. Humans
naturally cluster related terms -- mentioning a concept several times in one
paragraph then dropping it. AI's even distribution reads as mechanically
consistent rather than contextually driven.

**Also: Hyper-diversity paradox.** Contrary to intuition, LLMs show *higher*
overall lexical diversity than humans (more unique words per document). This
means adding rare synonyms to "sound more human" actually makes text *more*
detectable. The fix is natural clustering, not forced diversity.

**Before (even distribution -- AI tell):**
> [Paragraph 1]: The system optimizes performance...
> [Paragraph 3]: Performance metrics indicate...
> [Paragraph 5]: To optimize performance further...
> [Paragraph 7]: System performance has improved...

**After (natural clustering -- human pattern):**
> [Paragraph 1-2]: ...performance...optimize...performance...metrics...
> [Paragraphs 3-7]: No further use -- topic has moved on.

**Fix rules:**
- Allow key terms to cluster in the relevant section.
- Do not substitute synonyms just to avoid repetition -- let the word repeat.
- Do not spread a concept thin across an entire document.
- Hapax legomena (words used exactly once) should appear naturally, not be
  forced. Human text has 40-60% hapax density; AI is lower.

---

### P29 -- Register Uniformity
**Severity:** MED
**Detection basis:** Georgiou et al. (MDPI, 2024) using Biber's
multidimensional framework -- AI aligns consistently with informational/
academic register regardless of context; humans show register variation.

**Signal:** AI maintains the same tone throughout a document. A formal opening
stays formal throughout; a casual opening stays casual. Human writing shifts
between registers -- formal analysis to casual aside to technical explanation
to personal observation.

**Additional tells from Munoz-Ortiz et al. (2024):**
- AI displays a **positivity bias**: emphasizes joy while humans express
  stronger negative emotions including frustration and criticism.
- AI produces "more formal, structured, positive, and motivational" content
  across all domains regardless of context.

**Before (uniform formal register):**
> The implementation of the new framework resulted in measurable efficiency
> gains. The organizational response to these changes was largely positive.
> The subsequent adoption rate exceeded initial projections significantly.

**After (register shifted):**
> The new framework worked. Efficiency improved by the numbers.
> People were mostly fine with it -- a few grumbled about the rollout,
> which is pretty normal -- and adoption came in above what we expected.

**Fix rules:**
- Identify the dominant register and introduce at least one deliberate shift.
- Allow negative emotions proportionately: frustration, doubt, criticism,
  ambivalence. These are not unprofessional; they are human.
- Vary vocabulary register within a passage: one technical term, one casual
  synonym, one specific proper noun.

---

## LINGUISTIC PATTERNS (grammar and syntax)

---

### P30 -- Syntactic Template Repetition
**Severity:** MED
**Detection basis:** Shaib et al. (2024) -- 76% of syntactic templates in AI
text appear in pre-training data vs 35% in human text; CR-POS metric identified
as "the metric that identifies the most differences between human and model-
generated text."

**Signal:** AI reuses the same grammatical constructions repeatedly within a
document. Common templates: Subject + Verb + Object + Result, "By [verb-ing]
X, Y achieves Z", "[Adj] [Noun] [Verb] [Obj], [participle phrase]."
This creates the "textbook structure" feeling -- every bullet or paragraph
follows the same syntactic mold.

**Resume-specific (Willo, 2025):** All bullets following identical
Verb + Object + Result structure is a strong AI signal.

**Before (template repetition):**
> - Managed the project team, resulting in on-time delivery.
> - Developed the new framework, resulting in 30% efficiency gains.
> - Led the integration effort, resulting in seamless adoption.

**After (varied structure):**
> - Ran the project team -- we shipped on time.
> - Built the new framework; efficiency went up 30%.
> - The integration was messy but it landed. Adoption came in above forecast.

**Fix rules:**
- No two consecutive bullets or sentences should use the same syntactic template.
- Alternate: SVO, inverted, fragment, embedded clause, question, passive where
  appropriate.
- Break the "[Verb]-ing X, Y achieves Z" template -- this is extremely common
  in AI text.

---

### P31 -- Formulaic Professional Openers and Closers
**Severity:** HIGH (email/professional domain), MED (other domains)
**Detection basis:** Multiple sources estimate 95% AI probability for
"I hope this email finds you well" as an opener (Kassorla, 2025; Gmelius, 2025).
Originality.ai LinkedIn study (2025): 54% of long LinkedIn posts AI-generated;
AI posts are 107% longer with 45% less engagement.

**Opener signal list (flag these):**
I hope this email finds you well, I hope this message finds you well,
I am reaching out to, I wanted to circle back, I am writing to inquire,
I am following up on, Trust this finds you well, I hope you are doing well,
I wanted to touch base, Per my last email, As per our conversation,
I am excited to share, I am pleased to inform you

**Closer signal list (flag these):**
Please do not hesitate to contact me, Feel free to reach out,
Do not hesitate to reach out, I look forward to hearing from you,
Thank you for your time and consideration, Best regards (when mechanical),
Please let me know if you have any questions, I am available to discuss further,
Warm regards (when not appropriate to the relationship)

**Before:**
> I hope this email finds you well. I am reaching out to inquire about the
> possibility of scheduling a meeting. Please do not hesitate to contact me
> if you have any questions. Best regards.

**After:**
> Are you free Thursday for 30 minutes? I want to go over the Q3 numbers
> before the board call. Let me know what works.

**Fix rules:**
- Delete email openers entirely. Start with the reason for writing.
- Replace mechanical closers with a specific next action or genuine sign-off.
- Match formality to the actual relationship, not a default professional register.
- Calibrate email length -- human professional emails are shorter than AI emails.

---

### P32 -- Prompt Echo and Bookending
**Severity:** MED
**Detection basis:** GPTNone (2025), Pangram Labs (2026), Steere/Inside Higher
Ed (2024) -- AI "bookends" content by restating the prompt in the introduction
and again near the end; this is rare in human writing.

**Signal:** AI introduces a piece by restating what it was asked to write about,
then closes by restating what it covered. Creates a "sandwiched" structure:
announce/deliver/recap. Human writing starts in media res or with a specific
hook and ends with synthesis or a new question rather than summary.

**Before:**
> In this essay, I will explore the causes of the French Revolution.
> [body content]
> In conclusion, we have seen that the French Revolution was caused by financial
> crisis, food shortages, and social inequality.

**After:**
> France in 1789 was technically bankrupt and chronically hungry.
> [body content]
> The financial collapse and the bread shortage did not cause the Revolution
> alone -- they created the conditions where any spark could catch.

**Fix rules:**
- Delete "In this essay/article/post, I will..." entirely.
- Delete "In conclusion/In summary/To summarize" plus any restatement.
- Replace conclusions with synthesis, implication, or a new question.
- Start with a specific detail, observation, or claim -- not an announcement.

---

### P33 -- Predictable Paragraph Structure (Topic Sentence First)
**Severity:** LOW
**Detection basis:** GPTNone (2025) -- AI follows "textbook structure, literally
the five-paragraph essay format taught in middle school"; every paragraph opens
with a topic sentence that previews exactly what follows.

**Signal:** Every paragraph begins with a topic sentence that states what the
paragraph will say. This is correct middle-school writing but signals AI in
professional and creative contexts. Human writers vary opening structures:
evidence-first, question-first, contradiction-first, detail-first.

**Before:**
> Social media has significantly impacted modern communication. It has enabled
> instant global connectivity. People can now share information in real time.
> Businesses use these platforms for marketing.

**After:**
> A protest that would have taken weeks to organize in 2005 can now be
> coordinated in hours. That speed has changed what political movements
> look like -- not always for the better.

**Fix rules:**
- Vary paragraph openings: start some with evidence, some with questions,
  some with contradictions, some with a specific observation.
- Allow some paragraphs to begin mid-thought, assuming context from the prior.
- Keep some paragraphs short -- one or two sentences. Not every idea needs
  a full paragraph.

---

### P34 -- Positivity Bias and Negative Sentiment Avoidance
**Severity:** MED
**Detection basis:** Munoz-Ortiz et al. (2024) -- AI emphasizes joy and positive
emotions while humans express stronger negative emotions; AI produces "more
positive and motivational" content across all domains.

**Signal:** AI systematically avoids negative emotions, criticism, doubt, and
frustration. It defaults to "impressive results," "positive reception," and
"exciting progress" even when the situation calls for acknowledging problems.
Humans express proportionate negativity: frustration, ambivalence, criticism,
genuine uncertainty.

**Positivity inflation list (flag these):**
I am thrilled to, I am excited about, I am delighted to, impressive results,
outstanding performance, remarkable achievement, exceptional progress,
significant improvements, positive reception, enthusiastic response,
we are proud to announce, I am pleased to share

**Before:**
> The project delivered impressive results. Team performance was outstanding
> throughout the implementation. I am thrilled to report that we exceeded our
> targets significantly.

**After:**
> We hit our targets -- came in 12% above forecast. The rollout was messier
> than planned (the data migration took two extra weeks), but the end result
> held. The team pushed hard.

**Fix rules:**
- Replace enthusiasm inflation with specific numbers.
- Acknowledge what went wrong or what is uncertain.
- Express genuine opinions, including negative ones.
- Use "good" instead of "exceptional." Use "worked" instead of "delivered
  outstanding results."
- Match emotional register to actual outcomes: do not call ordinary success
  extraordinary.

---

## DOMAIN-SPECIFIC PATTERNS

---

### P35 -- Nominalization Overuse
**Severity:** MED
**Detection basis:** Tercon (2025) arXiv:2510.05136 survey; Andre et al. (2023);
Herbold et al. (2023) -- AI achieves formality through "nominal density and
lexicalization rather than passive voice"; LLMs "place much emphasis on nominal
phrases."

**Signal:** AI converts actions into abstract nouns, creating noun-heavy
constructions that reduce clarity and increase word count. This is the opposite
of Strunk and White -- AI violates "use active verbs" systematically.

**Common nominalizations to defuse:**
the optimization of -> optimizing
the implementation of -> implementing
the facilitation of -> facilitating
the achievement of -> achieving
the establishment of -> establishing
the utilization of -> using
the development of -> developing
the enhancement of -> improving
the identification of -> identifying
the consideration of -> considering
the creation of a solution -> solving
the delivery of results -> delivering results
the provision of support -> supporting

**Before:**
> The implementation of the new system resulted in the enhancement of
> operational efficiency through the optimization of processing workflows.

**After:**
> Implementing the new system improved operational efficiency by streamlining
> how we process workflows.

**Fix rules:**
- Scan for "the [verb-tion/ment/ance] of" constructions and convert to verb form.
- Prefer active verbs over noun phrases wherever possible.
- Flag abstract noun clusters: more than two nominalizations per sentence.

---

### P36 -- Noun Density Excess and Pronoun Deficit
**Severity:** MED
**Detection basis:** Georgiou et al. (MDPI, 2024) LASSO analysis -- "AI text
uses significantly more nouns and coordinating conjunctions while human text
uses more adjectives, adpositions, auxiliaries, and pronouns." AI achieves
formality through nominal density.

**Signal:** AI uses long noun phrases where humans would use pronouns or shorter
constructions. AI avoids "I," "we," "they," "it" in contexts where humans would
naturally use them. Creates dense, impersonal prose.

**Before:**
> The development team implemented the solution. The team's implementation
> resulted in the resolution of the underlying technical issues that had
> previously prevented the system from functioning correctly.

**After:**
> The dev team implemented it. That fixed the underlying issue -- the system
> had been broken for two weeks and now it isn't.

**Fix rules:**
- Replace noun phrases with pronouns after first introduction.
- Use "I" and "we" where first-person is natural.
- Reduce average noun phrase length by cutting pre-modifiers.
- Increase auxiliary verbs: "would," "could," "might," "should."

---

### P37 -- Power Verb Clustering (Resume/Career Domain)
**Severity:** HIGH (resume domain), LOW (other domains)
**Detection basis:** Willo (2025) resume detection study; UseResume.ai (2025);
Jobscan 2026 -- replacing 5-7 formulaic buzzwords reduces AI detection by 81%.

**Signal:** AI clusters impressive-sounding action verbs across consecutive
bullets. "Spearheaded," "orchestrated," "leveraged," and "championed" appearing
in adjacent bullets with mismatched seniority level signals AI authorship.
Round achievement metrics (50%, 30%, 100%) across multiple bullets signal
fabrication.

**Power verb cluster list (flag when 3+ appear in adjacent bullets):**
Spearheaded, Orchestrated, Championed, Pioneered, Revolutionized,
Transformed, Drove, Leveraged, Cultivated, Established best practices,
Fostered a culture of, Delivered exceptional results, Exceeded targets by

**Metric fabrication signals:**
- Round numbers (50%, 30%, 100%) across 3+ bullets without attribution
- Scale language inconsistent with seniority (entry-level candidate claiming
  "enterprise-wide transformation")
- Passive achievement framing ("resulted in X%" without specifying what was done)

**Before:**
> - Spearheaded enterprise-wide digital transformation, increasing efficiency 50%
> - Orchestrated cross-functional teams to deliver cutting-edge solutions
> - Championed adoption of innovative frameworks, driving 30% cost reduction

**After:**
> - Built the internal reporting dashboard used daily by 40+ analysts; cut
>   manual reconciliation time from 3 hours to 20 minutes
> - Ran a 4-person cross-functional team that shipped the billing integration
>   4 weeks ahead of schedule
> - Replaced two vendor tools with one internal system, saving $47K/year

**Fix rules:**
- Replace power verbs with simple past-tense action verbs: built, ran, wrote,
  cut, shipped, hired, redesigned, closed, moved.
- Use specific project names, team sizes, tools, and timeframes.
- Replace round metrics with specific numbers where possible.
- Match language sophistication to actual experience level.

---

### P38 -- Experiential Specificity Absence
**Severity:** HIGH
**Detection basis:** Cross-domain synthesis of all studies reviewed.
The single most reliable human signal across all four domains (professional,
creative, resume, academic) is experiential specificity -- details that
only a person with lived experience could provide.

**Signal:** AI substitutes generic references for specific ones:
"Many studies" instead of naming one. "Researchers" instead of naming who.
"In recent years" instead of giving a year. "A significant improvement"
instead of the actual number. Sensory detail, named places, actual dates,
real people, and domain-specific observations that require genuine experience
are systematically absent from AI-generated text.

**Generic substitution list (flag these when specifics are available):**
Many studies show, Research suggests, Experts agree, Industry observers note,
In recent years, Over the past decade, Studies have found, It has been shown,
Various sources indicate, A significant improvement, Considerable progress,
Multiple stakeholders, Several team members, Various challenges, Numerous factors

**Before:**
> Research suggests that remote work has significantly impacted employee
> satisfaction. Many companies have seen improvements in various metrics.
> Industry observers note this trend continues to evolve.

**After:**
> A 2023 Stanford study found that hybrid workers reported 13% higher
> satisfaction scores than fully remote workers -- a finding that surprised
> most of the researchers involved. At Atlassian, for instance, async-first
> policies cut meeting time by 40% without the satisfaction drop most
> teams expected.

**Fix rules:**
- Replace every generic attribution with a specific source: name, year,
  institution, study, or first-hand account.
- Add at least one concrete sensory or observational detail per major section.
- Replace "significant/considerable/various/multiple" with the actual number
  or named item.
- Use `<add specific>` placeholder when specifics are not available rather
  than inventing them.
- In creative writing: name the place, date the memory, describe the object.
  Generic setting is a creative AI tell.

---

## Updated Severity Quick Reference (P25-P38)

| Severity | New Patterns | Action |
|---|---|---|
| CRITICAL | P25 (burstiness) | Fix before anything else in both modes |
| HIGH | P26 (transition imbalance), P27 (impersonal hedging), P31 (formulaic openers), P37 (power verbs, resume), P38 (no specificity) | Mandatory fix in both modes |
| MED | P28 (even dispersion), P29 (register uniformity), P30 (syntactic templates), P32 (prompt echo), P34 (positivity bias), P35 (nominalization), P36 (noun density) | Fix in both modes |
| LOW | P33 (predictable paragraph structure) | Fix when pattern is dense; acceptable in short text |
