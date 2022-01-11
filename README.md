# Modelling French Grammar with Context Free Grammar (CFG)

### Some advantages of modelling French grammar with a CFG
The rules defined in the context-free grammar allow possible sentences as combinations of
unrelated individual words and groups of words. Since context-free grammar allows a wider
range of rules than regular French grammar, we have the freedom of producing a much wider
range of sentence structures. We can also capture many of the defining features of natural
human language, such as their potential for infinitely recursive structures. Overall, our context
free grammar is most useful in describing the nested chain structure of sentences which cannot
be explicitly defined in regular French grammar.

### Some disadvantages of modelling French grammar with a CFG
There are several disadvantages such as a lack of specific guidelines for lexical and syntactic
analysis. It is quite difficult to incorporate enough lexical rules such that each of the syntactic
categories are expressed in a grammatically correct manner; instead, it tends to over-generate
and under-generate. Notations in the CFG can become very complex, with extensive amounts
of rules and non-terminal subcategories that need to be handled. There are several words in the
French vocabulary that are spelt differently but mean the same thing, as a result this can lead to
the CFG rejecting completely valid sentences due to the alternative spelling not being covered
in the rules.

### Some aspects of French grammar that my CFG does not handle
Several aspects of French grammar are not handled by my CFG: sentences are not allowed to
start with a noun that does not have an article. For example ‘chat mange le poisson’ will be
rejected by my CFG. The CFG is too permissible in the sense that it uses proper nouns in
sentences where the subject does not agree with the predicate. For example ‘Montréal mange
le poisson’ is a valid sentence according to the CFG. It also does not handle sentences that
contain negations in direct object pronouns. For example ‘il le ne regarde pas’ is rejected by the
CFG.

### Overgeneration cases:
*‘Montréal mange le poisson’*
This sentence is grammatically incorrect.

### Undergeneration cases:
*‘il la ne regarde pas’*
This is a grammatically correct sentence that is missed.

## Accepted sentences:

*‘les Bleus regardent la télévision’*
### Parse tree:
(S
(NP (DT_pl les) (PN_pl Bleus))
(VP (V_ils regardent) (NP (DT_fm la) (N_fm télévision))))

*‘les chats mangent le beau poisson’*
### Parse tree:
(S
(NP (DT_pl les) (N_pl chats))
(VP
(V_ils mangent)
(NP (B (DT_ml le) (A_pre beau)) (N_ml poisson))))
‘il la regarde’
### Parse tree:
(S (B (PR_je il) (DT_fm la)) (V_je regarde))

*‘nous ne regardons pas la télévision’*
### Parse tree:
(S
(NP nous)
(VP
(L (PP_nous (NE ne) (V_nous regardons)) (NG pas))
(NP (DT_fm la) (N_fm télévision))))


## Rejected sentences

*‘les heureux chats mangent le poisson’*
Since the adjective ‘heureux is suppose to follow the noun ‘chats’

*‘la poisson mangent les chats’*
Since the article ‘la’’ does not agree with the grammatical gender of the noun ‘poisson’

*‘il regarde la télévisions’*
Since the determiner ‘la’ does not agree with the plural of the noun ‘télévisions’

*‘Je mange les’*
Since the determiner is after the noun
