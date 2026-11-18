# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Grammar rules (Phrases & Grammar, Part B).

TOPICS is a list of topic dicts, rendered in order, each followed by a practice page:
    {"id": str, "title": str, "pages": [[block, ...], ...]}
Block vocabulary: see templates/spanish/layout.py.
"""


def _h(text):
    return {"type": "heading", "text": text}


def _t(text):
    return {"type": "text", "text": text}


def _b(*items):
    return {"type": "bullets", "items": list(items)}


def _ex(es, en):
    return {"type": "example", "es": es, "en": en}


def _sp(h=4):
    return {"type": "spacer", "h": h}


def _table(header, rows, widths=None):
    return {"type": "table", "header": header, "rows": rows, "widths": widths, "gray_rows": []}


def _cmp(left, right, rows):
    return {"type": "compare", "left": left, "right": right, "rows": rows}


def _spaced(topic):
    """Insert a small gap after each table/compare box that runs straight into text."""
    pages = []
    for blocks in topic["pages"]:
        out = []
        for i, b in enumerate(blocks):
            out.append(b)
            nxt = blocks[i + 1] if i + 1 < len(blocks) else None
            if b["type"] in ("table", "compare") and nxt and nxt["type"] not in (
                    "spacer", "heading"):
                out.append(_sp(4))
        pages.append(out)
    return {**topic, "pages": pages}


# --------------------------------------------------------------------------
_HACE = {
    "id": "hace",
    "title": "How long: hace + time",
    "pages": [[
        _h("Four patterns with hace"),
        _t("For something that started in the past and **is still going on**, Spanish uses "
           "the **present** tense, where English uses \"have been ...-ing\"."),
        _table(["Pattern", "Example", "Meaning"], [
            ["**hace** + time + **que** + present",
             "**Hace** dos horas **que** las muchachas **juegan**.",
             "~The girls have been playing for two hours.~ (still playing)"],
            ["present + **desde hace** + time",
             "Las muchachas **juegan desde hace** dos horas.",
             "~Same meaning, different order.~"],
            ["preterite + **hace** + time",
             "**Llegué hace** tres días.",
             "~I arrived three days ago.~ (finished)"],
            ["**hacía** + time + **que** + imperfect",
             "**Hacía** un año **que vivía** allí.",
             "~I had been living there for a year.~ (up to a past moment)"],
        ], [0.33, 0.37, 0.30]),
        _sp(),
        _h("Asking how long"),
        _ex("¿Cuánto tiempo hace que estudias español? —Hace seis meses.",
            "How long have you been studying Spanish? —For six months."),
        _h("Ago"),
        _t("With a finished action (preterite), **hace** + time means **ago**. It can go "
           "first or last: Llegué **hace** tres días = **Hace** tres días llegué."),
        _ex("Comí hace una hora.", "I ate an hour ago."),
        _h("Had been"),
        _t("Put the whole pattern in the past: **hacía** + time + **que** + imperfect = "
           "\"had been ...-ing\" when something else happened."),
        _ex("Hacía media hora que esperábamos cuando por fin llegó el bus.",
            "We had been waiting for half an hour when the bus finally came."),
        _h("Good to know"),
        _b("**hace** never becomes plural: hace un día, hace dos años (not hacen).",
           "**desde** + a starting point: desde enero, desde 2020. **desde hace** + a length "
           "of time: desde hace tres meses.",
           "Also very common: **llevar** + time + -ndo: **Llevo** dos años **viviendo** aquí. "
           "~I've been living here for two years.~"),
    ]],
}

# --------------------------------------------------------------------------
_COMPARATIVES = {
    "id": "comparatives",
    "title": "Comparatives: more / less than",
    "pages": [[
        _h("más / menos ... que"),
        _t("To compare two things, put **más** (more) or **menos** (less) before the word "
           "and **que** (than) after it."),
        _table(["Pattern", "Example"], [
            ["más / menos + **adjective** + que",
             "Bogotá es **más grande que** Cali. ~Bogotá is bigger than Cali.~"],
            ["más / menos + **adverb** + que",
             "Ella habla **más rápido que** yo. ~She speaks faster than I do.~"],
            ["más / menos + **noun** + que",
             "Tengo **menos tiempo que** tú. ~I have less time than you.~"],
            ["**verb** + más / menos + que",
             "Mi hermano **come más que** yo. ~My brother eats more than I do.~"],
            ["más / menos **de** + number",
             "Hay **más de** cien personas. ~There are more than a hundred people.~"],
        ], [0.36, 0.64]),
        _b("After **que**, use **yo** and **tú**, not mí and ti: más alto que **yo**.",
           "Before a number, use **de**, not que: más **de** diez. (But **no ... más que** "
           "means only: No tengo más que diez mil pesos. ~I only have ten thousand pesos.~)"),
        _h("Irregular: mejor, peor, mayor, menor"),
        _table(["Word", "Comparative", "Example"], [
            ["bueno, bien ~good, well~", "**mejor** ~better~",
             "Este café es **mejor que** el otro. ~This coffee is better than the other one.~"],
            ["malo, mal ~bad, badly~", "**peor** ~worse~",
             "Hoy me siento **peor que** ayer. ~Today I feel worse than yesterday.~"],
            ["viejo ~old~ (age)", "**mayor** ~older~",
             "Mi hermana es **mayor que** yo. ~My sister is older than me.~"],
            ["joven ~young~", "**menor** ~younger~",
             "Soy **menor que** mi primo. ~I'm younger than my cousin.~"],
        ], [0.24, 0.20, 0.56]),
        _b("Plural: **mejores, peores, mayores, menores**. They don't change for gender.",
           "For quality and skill, say **mejor** and **peor**, not más bueno or más malo.",
           "Meaning older / younger, **mayor** and **menor** are for people. For things, say "
           "**más viejo** / **más nuevo**. (With things, mayor / menor mean bigger / smaller: "
           "el mayor problema.)"),
        _sp(2),
        _ex("Mi mamá cocina mejor que nadie.", "My mom cooks better than anyone."),
        _ex("Mi carro es más viejo que el tuyo.", "My car is older than yours."),
    ]],
}

# --------------------------------------------------------------------------
_EQUALITY = {
    "id": "equality",
    "title": "Equality: tan / tanto ... como",
    "pages": [[
        _h("as ... as"),
        _table(["Pattern", "Example"], [
            ["**tan** + adjective + **como**",
             "Mi casa es **tan grande como** la tuya. ~My house is as big as yours.~"],
            ["**tan** + adverb + **como**",
             "No corro **tan rápido como** tú. ~I don't run as fast as you.~"],
            ["**tanto / tanta / tantos / tantas** + noun + **como**",
             "Tengo **tantos libros como** tú. ~I have as many books as you.~"],
            ["verb + **tanto como**",
             "Trabajo **tanto como** mi jefe. ~I work as much as my boss.~"],
        ], [0.40, 0.60]),
        _sp(),
        _h("tan never changes; tanto agrees with its noun"),
        _t("**tan** goes before adjectives and adverbs and has only one form. **tanto** goes "
           "before a noun and matches it in gender and number. After a verb it is always "
           "**tanto**."),
        _table(["tanto + masc. sing.", "tanta + fem. sing.", "tantos + masc. pl.",
                "tantas + fem. pl."], [
            ["tanto trabajo", "tanta gente", "tantos amigos", "tantas horas"],
            ["~so much work~", "~so many people~", "~so many friends~", "~so many hours~"],
        ]),
        _t("Note: **gente** is a singular word in Spanish, so it takes **tanta**."),
        _h("Without como: so, so much"),
        _t("On their own, **tan** = so and **tanto** = so much / so many: ¡Estoy **tan** "
           "cansado! ~I'm so tired!~ ¡Comí **tanto**! ~I ate so much!~"),
        _sp(2),
        _ex("Ana es tan alta como su papá.", "Ana is as tall as her dad."),
        _ex("No hay tanta gente como ayer.", "There aren't as many people as yesterday."),
        _ex("Ahora no viajo tanto como antes.", "I don't travel as much as I used to."),
    ]],
}

# --------------------------------------------------------------------------
_SUPERLATIVES = {
    "id": "superlatives",
    "title": "Superlatives: the most, the least",
    "pages": [[
        _h("el / la / los / las + más / menos + adjective + de"),
        _t("Put the article first, then the noun (if any), then **más** or **menos** and the "
           "adjective. The group comes after **de**, where English says in or of: el más alto "
           "**de** la clase ~the tallest in the class~."),
        _table(["Pattern", "Example"], [
            ["el / la + noun + **más** + adj. + de",
             "Es **la** ciudad **más bonita de** Colombia. ~It's the prettiest city in "
             "Colombia.~"],
            ["los / las + noun + **menos** + adj. + de",
             "Son **los** cursos **menos caros de** la universidad. ~They're the least "
             "expensive courses at the university.~"],
            ["el / la + **más** + adj. (no noun)",
             "Manuel es **el más** aficionado a los conciertos. ~Manuel is the biggest "
             "concert fan.~"],
            ["el **mejor** / el **peor** + noun",
             "Es **el mejor** restaurante **del** barrio. ~It's the best restaurant in the "
             "neighborhood.~"],
            ["el **mayor** / el **menor**",
             "Soy **el menor de** tres hermanos. ~I'm the youngest of three siblings.~"],
        ], [0.38, 0.62]),
        _b("With mejor, peor, mayor and menor, don't add más: **el mejor**, not el más bueno.",
           "**mejor** and **peor** usually go before the noun: la **mejor** película ~the best "
           "movie~."),
        _h("-ísimo: very, extremely"),
        _t("To say very or extremely (no comparison), drop the final vowel and add **-ísimo** "
           "(-ísima, -ísimos, -ísimas): rico: **riquísimo**, fácil: **facilísimo**, mucho: "
           "**muchísimo**, cansado: **cansadísimo**."),
        _t("Spelling keeps the sound: c becomes **qu** (rico: riquísimo), g becomes **gu** "
           "(largo: larguísimo), z becomes **c** (feliz: felicísimo)."),
        _sp(2),
        _ex("Esta sopa está riquísima.", "This soup is really delicious."),
        _ex("Es el más alto de su familia.", "He's the tallest in his family."),
        _ex("El examen fue facilísimo.", "The exam was super easy."),
    ]],
}

# --------------------------------------------------------------------------
_NEGATIVES = {
    "id": "negatives",
    "title": "Negatives: nunca, nadie, nada",
    "pages": [[
        _h("Negative words and their opposites"),
        _table(["Negative", "English", "Positive opposite"], [
            ["**nada**", "~nothing, (not) anything~", "algo ~something~"],
            ["**nadie**", "~nobody, (not) anybody~", "alguien ~somebody~"],
            ["**nunca**, jamás", "~never, (not) ever~", "siempre ~always~, alguna vez ~ever~"],
            ["**ninguno, ninguna** (ningún)", "~no, none, (not) any~",
             "alguno, alguna (algún) ~some, any~"],
            ["**tampoco**", "~(not) either, neither~", "también ~also, too~"],
            ["**ni ... ni**", "~neither ... nor~", "o ... o ~either ... or~"],
        ], [0.32, 0.32, 0.36]),
        _sp(),
        _h("The double negative is correct"),
        _t("If the negative word comes **after** the verb, put **no** before the verb. In "
           "Spanish this is normal, not a mistake. If the negative word comes **first**, "
           "leave out no."),
        _cmp("After the verb: no + verb + negative word",
             "Before the verb: no extra no", [
                 ["**No** veo **nada**. ~I don't see anything.~",
                  "**Nada** me sorprende. ~Nothing surprises me.~"],
                 ["**No** viene **nunca**. ~He never comes.~",
                  "**Nunca** viene. ~He never comes.~"],
                 ["**No** conozco a **nadie**. ~I don't know anybody.~",
                  "**Nadie** me conoce. ~Nobody knows me.~"],
             ]),
        _sp(),
        _b("**ninguno** becomes **ningún** before a masculine singular noun: No tengo "
           "**ningún** problema. ~I don't have any problem.~",
           "It is almost always singular, even where English uses a plural: No tengo "
           "**ninguna** pregunta. ~I don't have any questions.~",
           "You can stack negatives: **Nunca** le digo **nada** a **nadie**. ~I never tell "
           "anybody anything.~"),
        _sp(2),
        _ex("No hay nadie en la oficina.", "There's nobody in the office."),
        _ex("Nunca he estado en México.", "I've never been to Mexico."),
        _ex("No quiero nada, gracias.", "I don't want anything, thanks."),
    ]],
}

# --------------------------------------------------------------------------
_PERSONAL_A = {
    "id": "personal-a",
    "title": "Personal a",
    "pages": [[
        _h("a before a person who receives the action"),
        _t("When the direct object (the one the action is done to) is a **specific person**, "
           "put **a** in front of it. It isn't translated. Things don't take it."),
        _cmp("Person: a", "Thing: no a", [
            ["Veo **a** María. ~I see María.~", "Veo la casa. ~I see the house.~"],
            ["Busco **a** mi hermano. ~I'm looking for my brother.~",
             "Busco mis llaves. ~I'm looking for my keys.~"],
            ["Conozco **a** tu jefe. ~I know your boss.~",
             "Conozco Bogotá. ~I know Bogotá.~"],
            ["Llamé **a** mi mamá. ~I called my mom.~", "Llamé un taxi. ~I called a taxi.~"],
        ]),
        _sp(),
        _h("Also use it with"),
        _b("**alguien, nadie, quién**: ¿Viste **a** alguien? No vi **a** nadie. ~Did you see "
           "anyone? I didn't see anyone.~ ¿**A** quién llamaste? ~Who did you call?~",
           "Pets you think of as family: Llevo **a** mi perro al parque. ~I take my dog to "
           "the park.~",
           "**a** + **el** contracts to **al**: Visité **al** médico. ~I went to the doctor.~"),
        _h("Usually no a"),
        _b("After **tener**: Tengo dos hermanos. ~I have two brothers.~",
           "After **hay**: Hay muchos turistas. ~There are a lot of tourists.~",
           "When the person isn't anyone specific: Busco **un** profesor de guitarra. ~I'm "
           "looking for a guitar teacher (any one).~ Compare: Busco **al** profesor de "
           "guitarra. ~I'm looking for the guitar teacher.~"),
        _sp(2),
        _ex("¿Conoces a mi novia?", "Do you know my girlfriend?"),
        _ex("Ayer vi a Carlos en el centro comercial.", "Yesterday I saw Carlos at the mall."),
    ]],
}

# --------------------------------------------------------------------------
_QUE_CUAL = {
    "id": "que-cual",
    "title": "¿Qué? vs. ¿Cuál?",
    "pages": [[
        _h("Both can mean what or which"),
        _t("The choice depends on what comes next and on whether you are choosing from a "
           "group."),
        _table(["Use", "When", "Example"], [
            ["**¿Qué** + noun?", "what or which + a noun",
             "¿**Qué** color te gusta? ~What color do you like?~"],
            ["**¿Qué** + verb?", "what, in general",
             "¿**Qué** quieres? ~What do you want?~"],
            ["**¿Qué es ...?**", "asking for a definition or explanation",
             "¿**Qué es** una arepa? ~What is an arepa?~"],
            ["**¿Cuál es ...? ¿Cuáles son ...?**",
             "asking for a specific piece of information: name, number, address",
             "¿**Cuál es** tu número? ~What's your number?~"],
            ["**¿Cuál(es)?** **¿Cuál de ...?**", "choosing from a group",
             "¿**Cuál** prefieres? ~Which one do you prefer?~"],
        ], [0.27, 0.33, 0.40]),
        _sp(),
        _t("Right before a noun, use **qué**: ¿**Qué** libro? You will also hear ¿Cuál libro? "
           "in parts of Latin America, but ¿qué libro? is always correct."),
        _h("The tricky one: what is ...?"),
        _cmp("¿Qué es ...? = explain it to me", "¿Cuál es ...? = which one, tell me the answer", [
            ["¿**Qué es** el ajiaco? ~What is ajiaco?~ (a description)",
             "¿**Cuál es** tu comida favorita? ~What's your favorite food?~"],
            ["¿**Qué es** un correo electrónico? ~What is an email?~",
             "¿**Cuál es** tu correo? ~What's your email address?~"],
        ]),
        _sp(),
        _ex("¿Cuál es tu dirección?", "What's your address?"),
        _ex("¿Qué hora es?", "What time is it?"),
        _ex("¿Cuáles de estos zapatos te gustan más?", "Which of these shoes do you like best?"),
    ]],
}

TOPICS = [_spaced(t) for t in (_HACE, _COMPARATIVES, _EQUALITY, _SUPERLATIVES, _NEGATIVES,
                                _PERSONAL_A, _QUE_CUAL)]
