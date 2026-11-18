# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Vocabulary topics (Vocab section): noun gender and pronouns.

TOPICS is a list of topic dicts, rendered in order, each followed by a practice page:
    {"id": str, "title": str, "pages": [[block, ...], ...]}
Block vocabulary: see templates/spanish/layout.py. User-added words live in
additions.MY_WORDS and are printed on word pages after these topics.
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


def _table(header, rows, widths=None, gray_rows=()):
    return {"type": "table", "header": header, "rows": rows, "widths": widths,
            "gray_rows": list(gray_rows)}


def _spaced(topic):
    """Insert a small gap after each table: 4 pt before text, 3 pt before a heading."""
    pages = []
    for blocks in topic["pages"]:
        out = []
        for i, b in enumerate(blocks):
            out.append(b)
            nxt = blocks[i + 1] if i + 1 < len(blocks) else None
            if b["type"] in ("table", "compare") and nxt and nxt["type"] != "spacer":
                out.append(_sp(3 if nxt["type"] == "heading" else 4))
        pages.append(out)
    return {**topic, "pages": pages}


# --------------------------------------------------------------------------
# 1. Masculine / feminine
# --------------------------------------------------------------------------
# (ending, usually, examples, exceptions)
_ENDINGS = [
    ("-o", "masculine", "el libro, el carro, el vaso",
     "la mano, la foto, la moto, la radio"),
    ("-a", "feminine", "la casa, la mesa, la playa",
     "el día, el mapa, el sofá, el planeta; most -ma words (below)"),
    ("-ción, -sión", "feminine", "la canción, la estación, la televisión", "none"),
    ("-dad, -tad, -tud", "feminine", "la ciudad, la libertad, la actitud", "none"),
    ("-umbre", "feminine", "la costumbre, la cumbre", "none"),
    ("-d (others)", "usually feminine", "la pared, la red, la salud", "el césped"),
    ("-aje", "masculine", "el viaje, el mensaje, el paisaje", "none"),
    ("-ma (Greek origin)", "masculine", "el problema, el tema, el idioma, el clima",
     "not Greek, so feminine: la cama, la forma, la crema"),
    ("-or", "masculine", "el color, el dolor, el amor", "la flor, la labor"),
    ("-l, -r, -n", "usually masculine", "el papel, el hotel, el lugar, el pan, el jardín",
     "la sal, la piel, la miel, la razón, la imagen; most -ión words are feminine "
     "(la opinión, la región), but el avión, el camión"),
    ("-j", "masculine", "el reloj", "few nouns end in -j"),
    ("-z", "mixed: learn each one", "el lápiz, el arroz, el pez",
     "feminine: la luz, la voz, la nariz, la paz, la vez"),
    ("-e", "either: learn each one", "el café, el parque, el nombre",
     "feminine: la noche, la calle, la clase, la gente"),
    ("-ista", "both (people)", "el / la turista, el / la artista", "none"),
    ("-ante, -ente", "both (people)", "el / la estudiante, el / la cantante",
     "some have an -a form: la presidenta, la clienta"),
]

_GENDER = {
    "id": "gender",
    "title": "Masculine and feminine nouns",
    "pages": [
        [
            _h("Every noun has a gender"),
            _t("Every Spanish noun is **masculine** or **feminine**, even for things. The "
               "gender decides the article and the ending of adjectives: **el** carro "
               "nuev**o**, **la** casa nuev**a**. Learn each new noun **with its article**."),
            _table(["", "masculine", "feminine"], [
                ["the (one)", "el", "la"],
                ["the (more than one)", "los", "las"],
                ["a / some", "un / unos", "una / unas"],
            ], [0.36, 0.32, 0.32]),
            _h("The ending is a good clue"),
            _table(["Ending", "Gender", "Examples", "Main exceptions"],
                   [[f"**{e}**", g, ex, exc] for e, g, ex, exc in _ENDINGS],
                   [0.17, 0.17, 0.32, 0.34]),
            _t("\"Usually\" means just that: the rules cover most nouns, not all. When in "
               "doubt, look up the article."),
        ],
        [
            _h("Common exceptions to memorize"),
            _b("**el día**, **el mapa**, **el sofá**, **el planeta** end in -a but are "
               "masculine. So are most -ma words from Greek: **el problema**, **el sistema**, "
               "**el programa**, **el idioma**.",
               "**la mano** ends in -o but is feminine: **la mano derecha**.",
               "**la foto** and **la moto** are short for la fotografía and la motocicleta, so "
               "they stay feminine.",
               "**la radio** is the broadcast (escuchar la radio). In much of Latin America the "
               "radio set itself is often **el radio**."),
            _h("el agua: a feminine noun with el"),
            _t("Feminine nouns that begin with a **stressed a-** or **ha-** take **el** and "
               "**un** in the singular, only to avoid the sound \"la a-\". The noun is still "
               "**feminine**: adjectives stay feminine, and the plural goes back to **las**."),
            _table(["Singular", "Plural", "English"], [
                ["el agua fría", "las aguas", "~the cold water / the waters~"],
                ["el águila", "las águilas", "~the eagle(s)~"],
                ["el aula", "las aulas", "~the classroom(s)~"],
                ["el hambre", "-", "~hunger~"],
            ], [0.38, 0.24, 0.38]),
            _b("Only **el / un** change. Other words stay feminine: **esta** agua, **mucha** "
               "hambre (Tengo mucha hambre. ~I'm very hungry.~), **toda** el agua.",
               "Only when the stress falls on that first a-: **la** amiga, **la** abuela, "
               "**la** hamaca (stress not on the first a)."),
            _h("People"),
            _b("Change **-o** to **-a**, or add **-a** to a consonant: el amigo / la amiga; "
               "el profesor / la profesora.",
               "Same word, different article: **el / la** estudiante, **el / la** turista.",
               "Different words: el hombre / la mujer, el papá / la mamá."),
            _ex("El problema es que no tengo tiempo.", "The problem is that I don't have time."),
            _ex("Me duele la mano derecha.", "My right hand hurts."),
            _ex("El agua del río está muy fría.", "The river water is very cold."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 2. Pronouns
# --------------------------------------------------------------------------
# subject, reflexive, direct object, indirect object, after a preposition
_PRONOUNS = [
    ("yo", "me", "me", "me", "mí (conmigo)"),
    ("tú", "te", "te", "te", "ti (contigo)"),
    ("él", "se", "lo", "le", "él"),
    ("ella", "se", "la", "le", "ella"),
    ("usted", "se", "lo / la", "le", "usted"),
    ("nosotros, -as", "nos", "nos", "nos", "nosotros, -as"),
    ("vosotros, -as", "os", "os", "os", "vosotros, -as"),
    ("ellos", "se", "los", "les", "ellos"),
    ("ellas", "se", "las", "les", "ellas"),
    ("ustedes", "se", "los / las", "les", "ustedes"),
]
_PRON_VOS = 6

# owner, before the noun, after the noun / alone, English
_POSSESSIVES = [
    ("yo", "mi, mis", "mío, mía, míos, mías", "~my / mine~"),
    ("tú", "tu, tus", "tuyo, tuya, tuyos, tuyas", "~your / yours~"),
    ("él, ella, Ud.", "su, sus", "suyo, suya, suyos, suyas", "~his, her, your / his, hers, "
     "yours~"),
    ("nosotros", "nuestro, -a, -os, -as", "nuestro, -a, -os, -as", "~our / ours~"),
    ("vosotros", "vuestro, -a, -os, -as", "vuestro, -a, -os, -as", "~your / yours (Spain)~"),
    ("ellos, Uds.", "su, sus", "suyo, suya, suyos, suyas", "~their, your / theirs, yours~"),
]
_POSS_VOS = 4

_PRONOUNS_TOPIC = {
    "id": "pronouns",
    "title": "Pronouns",
    "pages": [
        [
            _h("The pronoun chart"),
            _t("Each column answers a different question. **Subject**: who does it? "
               "**Reflexive**: the subject does it to itself (me levanto). **Direct object**: what or "
               "whom? **Indirect object**: to or for whom? **After a preposition**: para mí, "
               "con ella."),
            _table(["Subject", "Reflexive", "Direct", "Indirect", "After a prep."],
                   [list(r) for r in _PRONOUNS], [0.22, 0.16, 0.17, 0.16, 0.29],
                   gray_rows=[_PRON_VOS]),
            _b("**vosotros** and **os** are used only in Spain. In Latin America **ustedes** is "
               "the plural \"you\" for everyone, friends included, so it takes the third-person "
               "forms: **se**, **los / las**, **les**. **Les** traigo el menú. ~I'll bring you "
               "(all) the menu.~",
               "**lo / la** and **le** also mean \"you\" for **usted**: ¿**Lo** llevo al "
               "aeropuerto, señor? ~Shall I take you to the airport, sir?~",
               "After a preposition, only **yo** and **tú** change: para **mí**, para **ti**. "
               "With **con** they become **conmigo** and **contigo**. (After entre and según, "
               "use yo and tú: entre tú y yo.)",
               "**mí** ~me~ has an accent; **mi** ~my~ does not. **ti** never has one.",
               "The reflexive se also has forms after a preposition, **sí** and **consigo**: "
               "Lo lleva **consigo**. ~He takes it with him.~"),
            _h("Direct object: what or whom"),
            _t("The direct object receives the action. The pronoun replaces it so you don't "
               "repeat the noun: Compré **las frutas**. = **Las** compré. **lo, la, los, las** "
               "match the noun in gender and number."),
            _table(["Spanish", "English"], [
                ["**Lo** vi ayer.", "~I saw him (or it) yesterday.~"],
                ["**Las** compré en el mercado.", "~I bought them at the market.~"],
                ["¡Míra**lo**!", "~Look at it! / Look at him!~"],
            ], [0.5, 0.5]),
        ],
        [
            _h("Indirect object: to or for whom"),
            _t("**me, te, le, nos, os, les** tell you who receives the thing or the benefit. "
               "Spanish usually keeps **le / les** even when the person is named: **Le** doy "
               "un libro **a mi hermano**. Add **a** + person to make clear who le is: le "
               "escribí **a ella**."),
            _table(["Spanish", "English"], [
                ["**Le** doy un libro.", "~I'm giving him (her, you) a book.~"],
                ["**Me** dijeron la verdad.", "~They told me the truth.~"],
                ["**Les** escribí una carta.", "~I wrote them a letter.~"],
            ], [0.5, 0.5]),
            _h("Two pronouns together"),
            _b("**Order**: indirect before direct (person before thing), both before a "
               "conjugated verb: **Me lo** dio. ~He gave it to me.~",
               "**le / les + lo, la, los, las: le / les becomes se.** Never \"le lo\": Le di "
               "el libro a Ana. = **Se lo** di.",
               "**se** can mean to him, to her, to you, to them. Add **a él, a ella, a usted, "
               "a ellos** if it isn't clear: Se lo di **a ella**."),
            _table(["Spanish", "English"], [
                ["**Se lo** di.", "~I gave it to him (her, them).~"],
                ["**Me la** trajeron.", "~They brought it to me.~"],
                ["¡Dá**selo**!", "~Give it to him!~"],
                ["¡Mánda**noslo**!", "~Send it to us!~"],
            ], [0.5, 0.5]),
            _h("Where the pronoun goes"),
            _table(["With ...", "Pronoun goes", "Example"], [
                ["a conjugated verb", "before it, as a separate word",
                 "**Lo** compro. No **lo** compro."],
                ["an infinitive", "attached to the end", "Quiero comprar**lo**."],
                ["an -ndo form", "attached to the end", "Estoy comprándo**lo**."],
                ["an affirmative command", "attached to the end", "¡Cómpra**lo**!"],
                ["a negative command", "before the verb, after no", "¡No **lo** compres!"],
                ["two verbs (ir a, querer, estar + -ndo ...)",
                 "either before the first verb or attached to the second",
                 "**Lo** voy a hacer. = Voy a hacer**lo**."],
            ], [0.3, 0.33, 0.37]),
        ],
        [
            _h("The accent mark"),
            _t("Attaching pronouns makes the word longer. Write an accent to keep the stress "
               "where it was: diciendo + lo = **diciéndolo**; da + me + lo = **dámelo**; "
               "dar + me + lo = **dármelo**. One pronoun on an infinitive needs no accent: "
               "comprarlo, hacerlo."),
            _ex("Lo estoy haciendo. = Estoy haciéndolo.", "I'm doing it."),
            {"type": "xref", "text": "More on pronouns with commands: **Commands**",
             "dest": "t-commands"},
            _h("Possessives: my, mine"),
            _table(["Owner", "Before the noun", "After the noun / alone", "English"],
                   [list(r) for r in _POSSESSIVES], [0.2, 0.25, 0.3, 0.25],
                   gray_rows=[_POSS_VOS]),
            _b("Possessives agree with the **thing owned**, not the owner: **mis** libros, "
               "**nuestra** casa, **su** carro (their car).",
               "The short forms go **before** the noun. The long forms go **after** the noun "
               "or after ser: un amigo **mío** ~a friend of mine~; Es **mío**. ~It's mine.~",
               "With el, la, los, las, the long form replaces the noun: Tu carro es rojo; "
               "**el mío** es azul.",
               "**su** can mean his, her, your, or their. To be clear, use **de** + person: "
               "la casa **de ella**.",
               "**tu** ~your~ has no accent; **tú** ~you~ does."),
            _ex("¿Este celular es tuyo? —No, el mío es negro.",
                "Is this cell phone yours? —No, mine is black."),
        ],
    ],
}

TOPICS = [_spaced(_GENDER), _spaced(_PRONOUNS_TOPIC)]
