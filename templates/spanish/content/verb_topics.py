# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Verb reference topics for the Verbs section.

VERB_TOPICS is a list of topic dicts, rendered in order:
    {"id": str, "title": str, "pages": [[block, ...], ...], "practice": bool (optional)}
Block vocabulary: see templates/spanish/layout.py. Conjugated forms are pulled from
VERBS (verbs_data.py) wherever VERBS holds them, so the cross-checked data stays the
single source of truth. To add topics, append to VERB_TOPICS (Tasks 8 and 9 extend it).
"""
from templates.spanish.content.verbs_data import VERBS

_PERSONS = ["yo", "tú", "él/ella/Ud.", "nosotros", "vosotros", "ellos/Uds."]
_VOS = 4  # 0-based data row of vosotros (printed gray)
_MODELS = ("hablar", "comer", "vivir")
_MODEL_HEADER = ["", "-ar (hablar)", "-er (comer)", "-ir (vivir)"]


def _f(verb, tense, i):
    """One form from VERBS: i is the person index (0 = yo ... 5 = ellos)."""
    return VERBS[verb][tense][i]


def _marked(form, stem):
    """Bold the ending: habl + hablé gives habl**é**."""
    if not form.startswith(stem):
        raise ValueError(f"{form!r} does not start with stem {stem!r}")
    return f"{stem}**{form[len(stem):]}**"


def _endings_table(tense, header=_MODEL_HEADER, verbs=_MODELS, stems=None):
    """Person-by-class chart with the ending of each form in bold; vosotros row gray."""
    stems = stems or [v[:-2] for v in verbs]
    rows = [[p] + [_marked(_f(v, tense, i), s) for v, s in zip(verbs, stems)]
            for i, p in enumerate(_PERSONS)]
    n = len(verbs)
    return {"type": "table", "header": header, "rows": rows,
            "widths": [0.22] + [0.78 / n] * n, "gray_rows": [_VOS]}


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


# --------------------------------------------------------------------------
# 4. Present
# --------------------------------------------------------------------------
_PRESENT = {
    "id": "present",
    "title": "Present tense",
    "pages": [
        [
            _h("When to use it"),
            _b("Habits and routines: **Trabajo** desde casa. ~I work from home.~",
               "Facts and things that are true now: El agua **hierve** a 100 grados. "
               "~Water boils at 100 degrees.~",
               "What is happening now, where English often uses -ing: ¿Qué **haces**? "
               "~What are you doing?~",
               "Near future, with a time word: **Salgo** mañana. ~I'm leaving tomorrow.~"),
            _h("How to form it"),
            _t("Drop **-ar**, **-er** or **-ir** from the infinitive and add the ending for the "
               "person. -er and -ir verbs share every ending except nosotros and vosotros."),
            _endings_table("present"),
            _sp(),
            _ex("Mi hermana habla inglés y francés.", "My sister speaks English and French."),
            _h("Present for the near future"),
            _t("With a time word (mañana, esta noche, el sábado), the present can talk about "
               "plans, just like English \"I'm leaving tomorrow.\" It sounds casual and certain."),
            _ex("Te llamo esta noche.", "I'll call you tonight."),
        ],
        [
            _h("Stem-changing verbs (\"boot\" verbs)"),
            _t("The stem vowel changes in every form **except nosotros and vosotros**. The "
               "endings stay regular. Four types:"),
            {"type": "conj", "verbs": ["pensar", "volver", "pedir", "jugar"],
             "tenses": ["present"]},
            _t("**pensar**: e to ie. **volver**: o to ue. **pedir**: e to i (-ir verbs only). "
               "**jugar**: u to ue (the only one). More common stem-changers:"),
            {"type": "table", "header": ["e to ie", "o to ue", "e to i"],
             "rows": [
                 ["querer ~to want~", "poder ~can, to be able~", "servir ~to serve~"],
                 ["empezar ~to begin~", "dormir ~to sleep~", "repetir ~to repeat~"],
                 ["entender ~to understand~", "encontrar ~to find~", "seguir ~to follow~"],
                 ["preferir ~to prefer~", "costar ~to cost~", "decir ~to say~ (digo)"],
                 ["cerrar ~to close~", "recordar ~to remember~", "vestirse ~to get dressed~"],
                 ["tener ~to have~ (tengo)", "almorzar ~to have lunch~", "medir ~to measure~"],
             ],
             "widths": None, "gray_rows": []},
            _sp(),
            _ex("¿Quieres café o prefieres jugo?", "Do you want coffee, or would you rather "
                "have juice?"),
        ],
        [
            _h("Irregular yo forms"),
            _t("Only the **yo** form is irregular; the other persons follow the normal pattern "
               "(some also stem-change: tengo, **tienes**; digo, **dices**; **oír** adds a y: oyes, oye, oyen)."),
            {"type": "table", "header": ["Type", "Infinitive", "yo", "English"],
             "rows": [
                 ["-go", "tener", _f("tener", "present", 0), "~I have~ (tienes, tiene...)"],
                 ["-go", "hacer", _f("hacer", "present", 0), "~I do, I make~"],
                 ["-go", "salir", _f("salir", "present", 0), "~I leave, I go out~"],
                 ["-go", "poner", _f("poner", "present", 0), "~I put~"],
                 ["-go", "decir", _f("decir", "present", 0), "~I say, I tell~ (dices, dice...)"],
                 ["-go", "venir", _f("venir", "present", 0), "~I come~ (vienes, viene...)"],
                 ["-go", "traer", _f("traer", "present", 0), "~I bring~"],
                 ["-go", "oír", _f("oír", "present", 0), "~I hear~ (oyes, oye, oímos, oyen)"],
                 ["-zco", "conocer", _f("conocer", "present", 0),
                  "~I know (a person or place)~"],
                 ["-zco", "conducir", _f("conducir", "present", 0), "~I drive~"],
                 ["-zco", "producir", "produzco", "~I produce~"],
                 ["-jo", "escoger", _f("escoger", "present", 0), "~I choose~"],
                 ["other", "seguir", _f("seguir", "present", 0),
                  "~I follow, I keep on~ (sigues, sigue...)"],
             ],
             "widths": [0.11, 0.19, 0.17, 0.53], "gray_rows": []},
            _t("Why: in **escojo** the g becomes j before -o to keep the sound. **seguir** "
               "stem-changes e to i and drops the u before -o (sigo, sigues)."),
            _sp(),
            _ex("Hago ejercicio y después salgo con mis amigos.",
                "I work out, and then I go out with my friends."),
        ],
        [
            _h("Fully irregular verbs"),
            _t("Memorize **ser**, **estar** and **ir** whole. **ser** and **estar** both mean \"to be\"; **ir** = to go."),
            {"type": "conj", "verbs": ["ser", "estar", "ir"], "tenses": ["present"]},
            _sp(2),
            {"type": "conj", "verbs": ["haber", "dar", "saber", "ver"], "tenses": ["present"]},
            _t("**haber** is a helper verb (he comido ~I have eaten~). On its own, use **hay** "
               "~there is, there are~: Hay un banco cerca. ~There's a bank nearby.~"),
            _t("Only the yo form is odd in **dar** (doy), **saber** (sé) and **ver** (veo)."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 5. Present progressive
# --------------------------------------------------------------------------
_PROG_EN = ["~I am speaking~", "~you are speaking~", "~he/she is, you are speaking~",
            "~we are speaking~", "~you all are speaking (Spain)~",
            "~they are, you all are speaking~"]

_IRREG_GERUNDS = [
    ("dormir", "~sleeping~", "-ir stem change: o to u"),
    ("pedir", "~asking for, ordering~", "-ir stem change: e to i"),
    ("decir", "~saying, telling~", "e to i"),
    ("sentir", "~feeling~", "e to i"),
    ("venir", "~coming~", "e to i"),
    ("leer", "~reading~", "vowel + -iendo: i becomes y"),
    ("oír", "~hearing~", "i becomes y"),
    ("traer", "~bringing~", "i becomes y"),
    ("ir", "~going~", "fully irregular"),
]

_PROGRESSIVE = {
    "id": "progressive",
    "title": "Present progressive",
    "pages": [
        [
            _h("When to use it"),
            _t("For an action **in progress right now**, at this moment: English \"I am ...-ing.\" "
               "For habits and general facts, use the simple present. Unlike English, Spanish "
               "does not use it for plans: \"I'm leaving tomorrow\" is **Salgo mañana**."),
            _h("How to form it"),
            _t("**estar** (present) + the **-ndo form**. Drop -ar and add **-ando**; drop -er or "
               "-ir and add **-iendo**. The -ndo form never changes for person or gender."),
            {"type": "table", "header": ["", "estar + -ndo", "English"],
             "rows": [[p, f"{_f('estar', 'present', i)} habl**ando**", _PROG_EN[i]]
                      for i, p in enumerate(_PERSONS)],
             "widths": [0.22, 0.34, 0.44], "gray_rows": [_VOS]},
            _sp(2),
            {"type": "table", "header": ["", "-ar", "-er", "-ir"],
             "rows": [["ending", "**-ando**", "**-iendo**", "**-iendo**"],
                      ["example", "trabaj**ando** ~working~", "com**iendo** ~eating~",
                       "escrib**iendo** ~writing~"]],
             "widths": [0.22, 0.26, 0.26, 0.26], "gray_rows": []},
            _sp(),
            _ex("Los hombres están leyendo el periódico.", "The men are reading the newspaper."),
            _ex("¿Qué estás haciendo? —Estoy cocinando.", "What are you doing? —I'm cooking."),
            _ex("Está lloviendo mucho; mejor nos quedamos en casa.",
                "It's raining hard; we'd better stay home."),
        ],
        [
            _h("Irregular -ndo forms"),
            {"type": "table", "header": ["Infinitive", "-ndo form", "English", "Why"],
             "rows": [[v, VERBS[v]["gerund"], en, why] for v, en, why in _IRREG_GERUNDS],
             "widths": [0.19, 0.21, 0.27, 0.33], "gray_rows": []},
            _t("Rule of thumb: -ir verbs that stem-change in the present also change in the "
               "-ndo form (e to i, o to u). When the stem ends in a vowel (le-er, o-ír, "
               "tra-er), -iendo becomes **-yendo**."),
            _h("Where pronouns go"),
            _t("Object and reflexive pronouns go **before estar** or are **attached to the -ndo "
               "form**. Both mean the same. When you attach, add an accent to keep the stress."),
            {"type": "compare", "left": "Before estar", "right": "Attached to -ndo",
             "rows": [
                 ["**Lo** estoy leyendo.", "Estoy leyéndo**lo**."],
                 ["**Me** estoy duchando.", "Estoy duchándo**me**."],
                 ["**Se lo** estoy explicando.", "Estoy explicándo**selo**."],
             ]},
            _t("~I'm reading it. / I'm taking a shower. / I'm explaining it to him.~"),
        ],
    ],
}

# --------------------------------------------------------------------------
# 6. ir a + infinitive
# --------------------------------------------------------------------------
_IR_A_EN = ["~I'm going to eat~", "~you're going to eat~", "~he/she is, you are going to eat~",
            "~we're going to eat~", "~you all are going to eat (Spain)~",
            "~they are, you all are going to eat~"]

_IR_A = {
    "id": "ir-a",
    "title": "Future with ir a",
    "pages": [
        [
            _h("When to use it"),
            _t("For plans and things that are about to happen: English \"going to.\" In everyday "
               "Latin American Spanish this is the most common way to talk about the future, "
               "more common than the future tense (comeré)."),
            _h("How to form it"),
            _t("**ir** (present) + **a** + **infinitive**. Only ir changes; the infinitive stays "
               "the same."),
            {"type": "table", "header": ["", "ir + a + infinitive", "English"],
             "rows": [[p, f"**{_f('ir', 'present', i)} a** comer", _IR_A_EN[i]]
                      for i, p in enumerate(_PERSONS)],
             "widths": [0.22, 0.34, 0.44], "gray_rows": [_VOS]},
            _h("Good to know"),
            _b("**Vamos a** + infinitive also means \"let's\": ¡Vamos a comer! ~Let's eat!~",
               "Pronouns go before ir or attach to the infinitive: **Lo** voy a comprar = "
               "Voy a comprar**lo**. ~I'm going to buy it.~",
               "It works with ir itself: **Voy a ir** al banco. ~I'm going to go to the bank.~",
               "In the past, **iba a** + infinitive = \"was going to\": Iba a llamarte, pero "
               "se me olvidó. ~I was going to call you, but I forgot.~",
               "Time words: mañana, esta noche, el próximo año, la semana que viene, pronto, "
               "más tarde."),
            _sp(),
            _ex("Vamos a nadar esta tarde.", "We're going to swim this afternoon."),
            _ex("¿Qué vas a hacer este fin de semana?",
                "What are you going to do this weekend?"),
            _ex("Va a llover; lleva un paraguas.", "It's going to rain; take an umbrella."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 7. acabar de + infinitive
# --------------------------------------------------------------------------
_ACABAR = ["acabo", "acabas", "acaba", "acabamos", "acabáis", "acaban"]
_ACABAR_EN = ["~I just arrived~", "~you just arrived~", "~he/she, you just arrived~",
              "~we just arrived~", "~you all just arrived (Spain)~",
              "~they, you all just arrived~"]

_ACABAR_DE = {
    "id": "acabar-de",
    "title": "Just did: acabar de",
    "pages": [
        [
            _h("When to use it"),
            _t("For something that **just happened**, a moment ago: English \"just\" or "
               "\"have just.\" Spanish uses the present of acabar even though English uses a "
               "past form."),
            _h("How to form it"),
            _t("**acabar** (present, regular -ar) + **de** + **infinitive**."),
            {"type": "table", "header": ["", "acabar + de + infinitive", "English"],
             "rows": [[p, f"**{_ACABAR[i]} de** llegar", _ACABAR_EN[i]]
                      for i, p in enumerate(_PERSONS)],
             "widths": [0.22, 0.34, 0.44], "gray_rows": [_VOS]},
            _h("Good to know"),
            _b("Past of it: **acababa de** + infinitive = \"had just\": Acababa de salir "
               "cuando me llamaste. ~I had just left when you called me.~",
               "Pronouns go before acabar or attach to the infinitive: **Lo** acabo de ver = "
               "Acabo de ver**lo**. ~I just saw him.~",
               "Without de + infinitive, acabar means \"to finish\": Acabé el libro. "
               "~I finished the book.~"),
            _sp(),
            _ex("Acaban de llegar al restaurante.", "They just arrived at the restaurant."),
            _ex("Acabo de hablar con mi mamá.", "I just talked to my mom."),
            _ex("¿Acabas de despertarte?", "Did you just wake up?"),
        ],
    ],
}

# --------------------------------------------------------------------------
# 8. Preterite
# --------------------------------------------------------------------------
_STRONG_HEADER = ["", "u-stem: tener", "i-stem: venir", "j-stem: decir"]

_STRONG = [
    # (group, infinitive, yo, él, ellos, English for yo)
    ("u", "estar", None, None, None, "~I was~"),
    ("u", "tener", None, None, None, "~I had; I got~"),
    ("u", "poder", None, None, None, "~I managed to~ (no pude ~I failed to~)"),
    ("u", "poner", None, None, None, "~I put~"),
    ("u", "saber", None, None, None, "~I found out~"),
    ("u", "caber", "cupe", "cupo", "cupieron", "~I fit~"),
    ("u", "andar", "anduve", "anduvo", "anduvieron", "~I walked~"),
    # existential haber: only hubo, even with plurals (never "hubieron muchas personas")
    ("u", "haber", "—", "hubo", "—", "hubo = ~there was, there were~ (never \"hubieron\")"),
    ("i", "querer", None, None, None, "~I tried~ (no quise ~I refused~)"),
    ("i", "venir", None, None, None, "~I came~"),
    ("i", "hacer", None, None, None, "~I did, I made~ (z in hizo)"),
    ("j", "decir", None, None, None, "~I said, I told~"),
    ("j", "traer", None, None, None, "~I brought~"),
    ("j", "conducir", None, None, None, "~I drove~"),
]


def _strong_row(group, verb, yo, el, ellos, en):
    if yo is None:
        yo, el, ellos = (_f(verb, "preterite", i) for i in (0, 2, 5))
    return [group, verb, yo, el, ellos, en]


_PRETERITE = {
    "id": "preterite",
    "title": "Preterite",
    "pages": [
        [
            _h("When to use it"),
            _b("A **completed action** at a specific time or in a closed period: ayer, anoche, "
               "el lunes, en 2019, hace dos años.",
               "A **sequence of events**: this happened, then that.",
               "Actions **earlier today**. In Latin America the preterite is normal here: "
               "Hoy **comí** arroz. ~Today I ate rice.~",
               "Something that lasted a set time or happened a set number of times: "
               "**Viví** en Bogotá tres años. ~I lived in Bogotá for three years.~"),
            _t("Trigger words: ayer, anoche, anteayer, la semana pasada, el año pasado, hace + "
               "time, una vez, de repente, esta mañana."),
            _h("How to form it"),
            _t("Drop -ar, -er or -ir and add the ending. -er and -ir share one set. Note the "
               "accents on yo and él."),
            _endings_table("preterite"),
            _b("**nosotros** of -ar and -ir verbs looks like the present (hablamos, vivimos); "
               "context tells you which.",
               "-ar and -er stem-changers do **not** change in the preterite: pensé, volví, "
               "entendí."),
            _sp(2),
            _ex("Ayer fui al supermercado y compré fruta.",
                "Yesterday I went to the supermarket and bought fruit."),
            _ex("Hoy desayuné temprano.", "I had breakfast early today."),
        ],
        [
            _h("Spelling changes in the yo form"),
            _t("Verbs ending in **-car, -gar, -zar** change spelling in the **yo** form only, to "
               "keep the sound. The rest is regular."),
            {"type": "table", "header": ["Ending", "Change", "Examples (yo)"],
             "rows": [
                 ["-car", "c becomes **qu**",
                  f"buscar: {_f('buscar', 'preterite', 0)} ~I looked for~; tocar: toqué "
                  "~I touched, I played (music)~; sacar: saqué ~I took out~"],
                 ["-gar", "g becomes **gu**",
                  f"llegar: {_f('llegar', 'preterite', 0)} ~I arrived~; pagar: pagué "
                  f"~I paid~; jugar: {_f('jugar', 'preterite', 0)} ~I played~"],
                 ["-zar", "z becomes **c**",
                  f"empezar: {_f('empezar', 'preterite', 0)} ~I began~; almorzar: almorcé "
                  "~I had lunch~"],
             ],
             "widths": [0.12, 0.2, 0.68], "gray_rows": []},
            _h("-ir stem-changers: él and ellos only"),
            _t("-ir verbs that stem-change in the present change in the preterite too, but "
               "**only in él/ella/Ud. and ellos/Uds.**: e becomes i, o becomes u."),
            {"type": "conj", "verbs": ["dormir", "pedir", "sentir"], "tenses": ["preterite"]},
            _h("i becomes y: leer, oír, -uir verbs"),
            _t("When the stem ends in a vowel, the i of -ió and -ieron becomes **y**. leer, creer "
               "and oír also take accents (leíste, leímos); -uir verbs do not (incluiste)."),
            {"type": "table", "header": ["Infinitive", "él/ella", "ellos/ellas", "English (él)"],
             "rows": [
                 ["leer", _f("leer", "preterite", 2), _f("leer", "preterite", 5), "~he read~"],
                 ["creer", "creyó", "creyeron", "~he believed~"],
                 ["oír", _f("oír", "preterite", 2), _f("oír", "preterite", 5), "~he heard~"],
                 ["incluir", _f("incluir", "preterite", 2), _f("incluir", "preterite", 5),
                  "~he included~"],
                 ["construir", "construyó", "construyeron", "~he built~"],
             ],
             "widths": [0.22, 0.22, 0.26, 0.30], "gray_rows": []},
        ],
        [
            _h("Strong-stem irregulars"),
            _t("These take a new stem and special endings with **no accents**: -e, -iste, -o, "
               "-imos, -isteis, -ieron. j-stems drop the i: **-eron** (dijeron, trajeron)."),
            _endings_table("preterite", header=_STRONG_HEADER,
                           verbs=("tener", "venir", "decir"), stems=("tuv", "vin", "dij")),
            _sp(2),
            {"type": "table", "header": ["", "Infinitive", "yo", "él/ella", "ellos", "English (yo)"],
             "rows": [_strong_row(*r) for r in _STRONG],
             "widths": [0.05, 0.15, 0.15, 0.15, 0.18, 0.32], "gray_rows": []},
            _t("Meaning shifts: in the preterite, **supe** = ~I found out~, **pude** = "
               "~I managed to~, **quise** = ~I tried~, and **conocí** = ~I met~."),
            _t("**hay / hubo / había** never go plural: **Hubo** muchos problemas. "
               "~There were a lot of problems.~"),
        ],
        [
            _h("ser, ir, dar, ver"),
            _t("**ser** and **ir** share the same preterite; context tells you which. "
               "**dar** takes -er/-ir endings. dar and ver have **no accents** (di, dio, vi, vio)."),
            {"type": "conj", "verbs": ["ser", "ir", "dar", "ver"], "tenses": ["preterite"]},
            _sp(),
            _ex("¿Qué hiciste el fin de semana? —Fui a la playa con unos amigos.",
                "What did you do over the weekend? —I went to the beach with some friends."),
            _ex("Fui programador durante veinte años.", "I was a programmer for twenty years."),
            _t("With jobs, Spanish leaves out un/una: **Fui programador**, not \"fui un "
               "programador.\" Add un/una only with a description: Fui **un buen** programador."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 9. Imperfect
# --------------------------------------------------------------------------
_IMP_REGULAR = ["tener", "estar", "hacer", "haber", "poner", "oír", "dar"]

_IMPERFECT = {
    "id": "imperfect",
    "title": "Imperfect",
    "pages": [
        [
            _h("When to use it"),
            _b("**Habits** and repeated actions in the past (English \"used to,\" \"would\"): "
               "De niño, **jugaba** fútbol todos los días. ~As a kid, I played soccer every day.~",
               "**Background and description**: time, weather, age, feelings, what things were "
               "like: **Eran** las ocho. **Hacía** frío. **Tenía** diez años. ~It was eight "
               "o'clock. It was cold. I was ten.~",
               "An action **in progress** in the past (English \"was ...-ing\"), often "
               "interrupted by a preterite: **Leía** cuando sonó el teléfono. ~I was reading "
               "when the phone rang.~",
               "Polite requests: **Quería** un café, por favor. ~I'd like a coffee, please.~"),
            _t("Trigger words: siempre, todos los días, cada semana, a menudo, normalmente, "
               "antes, mientras, de niño, cuando era joven."),
            _h("How to form it"),
            _t("Drop -ar, -er or -ir and add the ending. -er and -ir are identical. No stem "
               "changes and no spelling changes."),
            _endings_table("imperfect"),
            _t("yo and él/ella have the same form; add the subject if it isn't clear."),
            _sp(2),
            _ex("Era ingeniero cuando trabajaba en Oracle.",
                "I was an engineer when I worked at Oracle."),
            _ex("Cuando era niño, vivíamos cerca del mar.",
                "When I was a kid, we lived near the sea."),
        ],
        [
            _h("Only three irregulars: ser, ir, ver"),
            {"type": "conj", "verbs": ["ser", "ir", "ver"], "tenses": ["imperfect"]},
            _t("**ver** just keeps its e: ve- + -ía (veía)."),
            _h("Irregular elsewhere, regular here"),
            _t("Verbs that are irregular in the present or preterite follow the normal pattern "
               "in the imperfect:"),
            {"type": "table", "header": ["Infinitive", "yo / él", "nosotros", "English (yo)"],
             "rows": [[v, _f(v, "imperfect", 0), _f(v, "imperfect", 3), en]
                      for v, en in zip(_IMP_REGULAR, [
                          "~I had, I used to have~", "~I was~", "~I did, I used to do~",
                          "había = ~there was, there were~", "~I put, I used to put~",
                          "~I heard, I used to hear~", "~I gave, I used to give~"])],
             "widths": [0.2, 0.2, 0.22, 0.38], "gray_rows": []},
            _sp(),
            _ex("Mi abuela siempre nos hacía arepas los domingos.",
                "My grandmother always made us arepas on Sundays."),
            _ex("Hacía mucho calor y todos estaban cansados.",
                "It was very hot, and everyone was tired."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 10. Preterite vs. imperfect
# --------------------------------------------------------------------------
_CMP_PRET_IMP = {
    "id": "cmp-pret-imp",
    "title": "Preterite vs. imperfect",
    "pages": [
        [
            _t("Both are past tenses. The **preterite** tells **what happened**: completed "
               "events, the story line. The **imperfect** describes **what was going on**: the "
               "background, habits and descriptions."),
            {"type": "compare", "left": "Preterite: what happened",
             "right": "Imperfect: what was going on",
             "rows": [
                 ["Completed action at a specific time", "Habit or repeated action (\"used to\")"],
                 ["Sequence of events: this, then that", "Background: time, weather, age, place"],
                 ["The action that interrupts", "The action in progress that gets interrupted"],
                 ["Start or end of something (empezó, terminó)",
                  "Description: what people and things were like"],
                 ["A set number of times or a closed period (tres años)",
                  "Ongoing state, no clear start or end"],
             ]},
            _sp(2),
            {"type": "compare", "left": "Preterite trigger words", "right": "Imperfect trigger words",
             "rows": [
                 ["ayer, anoche, el lunes pasado", "siempre, todos los días, cada semana"],
                 ["una vez, dos veces, de repente", "a menudo, normalmente, a veces"],
                 ["hace dos años, en 2020", "de niño, cuando era joven, antes"],
                 ["hoy, esta mañana (Latin America)", "mientras"],
             ]},
            _t("Trigger words are hints, not rules. Ask yourself: am I telling what happened, "
               "or setting the scene?"),
            {"type": "timeline", "events": [
                {"pos": 0.05, "label": "**estaba** en casa ~(ongoing)~", "mark": "past"},
                {"pos": 0.5, "label": "**llegaste** ~(event)~", "mark": "point"},
                {"pos": 1.0, "label": "ahora", "mark": "now"},
            ], "caption": "**Estaba** en casa (imperfect) is the background that was going on; "
                          "**llegaste** (preterite) is the event that happened in the middle of it."},
            _ex("Estaba en casa cuando llegaste.", "I was at home when you arrived."),
            _ex("Mientras cocinaba, sonó el teléfono.", "While I was cooking, the phone rang."),
        ],
        [
            _h("Same verb, two tenses"),
            {"type": "compare", "left": "Preterite", "right": "Imperfect",
             "rows": [
                 ["Ayer **comí** en ese restaurante. ~Yesterday I ate at that restaurant.~",
                  "Siempre **comía** en ese restaurante. ~I always used to eat at that "
                  "restaurant.~"],
                 ["**Fue** un día largo. ~It was a long day.~ (the whole day, now over)",
                  "**Era** un día bonito. ~It was a beautiful day.~ (setting the scene)"],
                 ["**Conocí** a María en 2019. ~I met María in 2019.~",
                  "Ya **conocía** a María. ~I already knew María.~"],
                 ["**Supe** la verdad. ~I found out the truth.~",
                  "**Sabía** la verdad. ~I knew the truth.~"],
                 ["**Tuve** que trabajar. ~I had to work (and I did).~",
                  "**Tenía** que trabajar. ~I had to work (I was supposed to).~"],
             ]},
            _sp(),
            _ex("Eran las once y llovía cuando salimos del cine.",
                "It was eleven o'clock and raining when we left the movie theater."),
            _ex("De niños íbamos a la playa todos los veranos, pero un verano fuimos a las "
                "montañas.",
                "As kids we went to the beach every summer, but one summer we went to the "
                "mountains."),
            _sp(),
            {"type": "xref", "text": "All the forms: **Preterite**", "dest": "t-preterite"},
            {"type": "xref", "text": "All the forms: **Imperfect**", "dest": "t-imperfect"},
        ],
    ],
}

# --------------------------------------------------------------------------
# 11. Future
# --------------------------------------------------------------------------
_INF_STEMS = _MODELS  # future and conditional endings go on the whole infinitive

_FUT_IRREG = [
    # (group, infinitive, stem, English for yo); yo form pulled from VERBS
    ("drop e", "poder", "podr-", "~I will be able to~"),
    ("drop e", "saber", "sabr-", "~I will know~"),
    ("drop e", "querer", "querr-", "~I will want~"),
    ("drop e", "haber", "habr-", "~I will have~ (helper); **habrá** = ~there will be~"),
    ("drop e", "caber", "cabr-", "~I will fit~"),
    ("vowel to d", "tener", "tendr-", "~I will have~"),
    ("vowel to d", "salir", "saldr-", "~I will leave, I will go out~"),
    ("vowel to d", "venir", "vendr-", "~I will come~"),
    ("vowel to d", "poner", "pondr-", "~I will put~"),
    ("short", "hacer", "har-", "~I will do, I will make~"),
    ("short", "decir", "dir-", "~I will say, I will tell~"),
]


def _stem_form(verb, tense, typed):
    """yo form from VERBS, or the typed form for verbs VERBS lacks (caber)."""
    return _f(verb, tense, 0) if verb in VERBS else typed


_FUTURE = {
    "id": "future",
    "title": "Future tense",
    "pages": [
        [
            _h("When to use it"),
            _b("What **will** happen: El concierto **será** en el estadio. ~The concert will "
               "be at the stadium.~",
               "Promises and predictions: Te **llamaré** mañana. ~I'll call you tomorrow.~",
               "Guessing about **now** (\"probably,\" \"I wonder\"): ¿Dónde **estará** Ana? "
               "~I wonder where Ana is.~ **Estará** en el trabajo. ~She's probably at work.~"),
            _t("In everyday Latin American speech, **ir a** + infinitive (voy a llamar) is more "
               "common for plans. The future tense sounds a little more formal or more certain, "
               "and it is the normal way to guess."),
            _h("How to form it"),
            _t("Keep the **whole infinitive** and add the ending. All three classes use the "
               "same endings, and every form except nosotros has an accent."),
            _endings_table("future", stems=_INF_STEMS),
            _sp(),
            _ex("Mañana hablaré con mi jefe.", "Tomorrow I'll talk to my boss."),
            _ex("¿Qué hora será? —Serán las tres.",
                "I wonder what time it is. —It's probably three."),
        ],
        [
            _h("Irregular stems"),
            _t("These verbs change the stem, but the endings stay the same: **-é, -ás, -á, "
               "-emos, -éis, -án**. The same stems are used for the conditional."),
            {"type": "table", "header": ["Change", "Infinitive", "Stem", "yo", "English (yo)"],
             "rows": [[g, v, stem, _stem_form(v, "future", "cabré"), en]
                      for g, v, stem, en in _FUT_IRREG],
             "widths": [0.17, 0.15, 0.12, 0.14, 0.42], "gray_rows": []},
            _t("Verbs built on these keep the change: mantener (**mantendré**), "
               "suponer (**supondré**)."),
            _t("**habrá** ~there will be~ is always singular, like hay: **Habrá** muchas "
               "personas. ~There will be a lot of people.~"),
            _sp(),
            _ex("El próximo año tendremos más tiempo para viajar.",
                "Next year we'll have more time to travel."),
            _ex("Te prometo que llegaré a tiempo.", "I promise I'll be on time."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 12. Conditional
# --------------------------------------------------------------------------
_COND_IRREG = ["tener", "poder", "hacer", "decir", "salir", "venir", "poner", "saber",
               "querer", "haber"]
_COND_EN = ["~I would have~", "~I could, I would be able to~", "~I would do, I would make~",
            "~I would say, I would tell~", "~I would leave~", "~I would come~",
            "~I would put~", "~I would know~", "~I would want~",
            "~I would have~ (helper); **habría** = ~there would be~"]

_CONDITIONAL = {
    "id": "conditional",
    "title": "Conditional",
    "pages": [
        [
            _h("When to use it"),
            _b("English **\"would\"**: Yo no **diría** eso. ~I wouldn't say that.~ With an "
               "if-clause: Si tuviera dinero, **compraría** un carro. ~If I had money, I would "
               "buy a car.~",
               "**Politeness**: **Me gustaría** un café. ~I'd like a coffee.~ ¿**Podrías** "
               "ayudarme? ~Could you help me?~ ¿**Podría** traerme la cuenta? ~Could you (Ud.) "
               "bring me the check?~",
               "**Advice** with deber: **Deberías** descansar. ~You should rest.~",
               "The future seen from the past: Dijo que **llamaría**. ~He said he would call.~"),
            _h("How to form it"),
            _t("Like the future: keep the **whole infinitive** and add **-ía** endings. The "
               "irregular verbs use the same stems as the future (tendr-, podr-, har-...)."),
            _endings_table("conditional", stems=_INF_STEMS),
            _t("Don't mix it up with the imperfect: com**ía** ~I was eating, I used to eat~, "
               "comer**ía** ~I would eat~."),
            _sp(2),
            _ex("Me gustaría reservar una mesa para dos, por favor.",
                "I'd like to reserve a table for two, please."),
        ],
        [
            _h("Irregular stems (same as the future)"),
            {"type": "table", "header": ["Infinitive", "yo", "English (yo)"],
             "rows": [[v, _f(v, "conditional", 0), en] for v, en in zip(_COND_IRREG, _COND_EN)],
             "widths": [0.2, 0.2, 0.6], "gray_rows": []},
            _h("Sounding polite"),
            {"type": "compare", "left": "Direct", "right": "Polite (conditional)",
             "rows": [
                 ["Quiero un café. ~I want a coffee.~",
                  "**Me gustaría** un café. ~I'd like a coffee.~"],
                 ["¿Puedes ayudarme? ~Can you help me?~",
                  "¿**Podrías** ayudarme? ~Could you help me?~"],
                 ["Debes llamar a tu mamá. ~You must call your mom.~",
                  "**Deberías** llamar a tu mamá. ~You should call your mom.~"],
             ]},
            _t("**deber** in the present sounds strong (\"must\"); **debería** is friendly advice "
               "(\"should\")."),
            _t("When English \"would\" means \"used to,\" use the imperfect: De niño, **jugaba** "
               "en la calle. ~As a kid, I would play in the street.~"),
            _sp(),
            _ex("¿Podría decirme dónde está la estación?",
                "Could you tell me where the station is?"),
            _ex("Deberías llevar una chaqueta; hace frío.",
                "You should take a jacket; it's cold."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 13. Present perfect
# --------------------------------------------------------------------------
_PP_EN = ["~I have spoken~", "~you have spoken~", "~he/she has, you have spoken~",
          "~we have spoken~", "~you all have spoken (Spain)~",
          "~they have, you all have spoken~"]

_IRREG_PART = [
    ("hacer", "~done, made~"), ("decir", "~said, told~"), ("ver", "~seen~"),
    ("escribir", "~written~"), ("poner", "~put~"), ("volver", "~returned, come back~"),
    ("abrir", "~opened~"), ("romper", "~broken~"), ("morir", "~died~"),
    ("cubrir", "~covered~"), ("descubrir", "~discovered~"), ("resolver", "~solved~"),
]


def _part_rows():
    """Irregular participles from VERBS, two per row to save space."""
    cells = [[v, f"**{VERBS[v]['participle']}**", en] for v, en in _IRREG_PART]
    half = (len(cells) + 1) // 2
    return [cells[i] + cells[i + half] for i in range(half)]


_PRES_PERFECT = {
    "id": "pres-perfect",
    "title": "Present perfect",
    "pages": [
        [
            _h("When to use it"),
            _b("**Experiences** up to now, often with nunca, alguna vez, ya, todavía no, "
               "dos veces: **He estado** en Colombia dos veces. ~I've been to Colombia twice.~ "
               "**Nunca he probado** el mole. ~I've never tried mole.~",
               "**A period that is still open** (este año, esta semana, últimamente): Este año "
               "**hemos viajado** mucho. ~We've traveled a lot this year.~"),
            _t("**Latin America:** for an action that is finished, even one from earlier today, "
               "use the **preterite**: Hoy **comí** temprano. ~I ate early today.~ "
               "¿Ya **comiste**? ~Have you eaten yet?~ \"Hoy he comido\" sounds like Spain."),
            _h("How to form it"),
            _t("**haber** (present) + **past participle**. haber means \"have\" only as this "
               "helper; for \"to have\" (own), use tener."),
            {"type": "table", "header": ["", "haber + participle", "English"],
             "rows": [[p, f"**{_f('haber', 'present', i)}** hablado", _PP_EN[i]]
                      for i, p in enumerate(_PERSONS)],
             "widths": [0.22, 0.34, 0.44], "gray_rows": [_VOS]},
            _sp(2),
            {"type": "table", "header": ["", "-ar", "-er", "-ir"],
             "rows": [["participle", "**-ado**", "**-ido**", "**-ido**"],
                      ["example", f"habl**ado** ~spoken~", f"com**ido** ~eaten~",
                       f"viv**ido** ~lived~"]],
             "widths": [0.22, 0.26, 0.26, 0.26], "gray_rows": []},
            _t("When the stem ends in a, e or o, the i takes an accent: "
               f"**{VERBS['leer']['participle']}**, **{VERBS['oír']['participle']}**, "
               f"**{VERBS['traer']['participle']}**, **creído**."),
            _sp(),
            _ex("¿Has estado en México? —Sí, he ido tres veces.",
                "Have you been to Mexico? —Yes, I've been three times."),
        ],
        [
            _h("Irregular participles"),
            {"type": "table",
             "header": ["Infinitive", "Participle", "English"] * 2,
             "rows": _part_rows(),
             "widths": [0.15, 0.15, 0.2] * 2, "gray_rows": []},
            _t("Verbs built on these follow them: devolver (devuelto), describir (descrito)."),
            _h("Rules"),
            _b("**haber + participle never split.** Pronouns and **no** go before haber: "
               "**Se lo** he dicho. ~I've told him.~ **No lo** he visto. ~I haven't seen it.~",
               "**The participle never changes** for gender or number: Las **he comprado**. "
               "~I've bought them.~ María **ha llegado**. ~María has arrived.~",
               "**hay** becomes **ha habido** ~there has been, there have been~, always "
               "singular: **Ha habido** muchos problemas."),
            _sp(),
            _ex("Hemos practicado mucho esta semana.", "We've practiced a lot this week."),
            _ex("Todavía no he terminado el libro.", "I haven't finished the book yet."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 14. Past perfect
# --------------------------------------------------------------------------
_PLUP_EN = ["~I had eaten~", "~you had eaten~", "~he/she, you had eaten~",
            "~we had eaten~", "~you all had eaten (Spain)~", "~they, you all had eaten~"]

_PAST_PERFECT = {
    "id": "past-perfect",
    "title": "Past perfect",
    "pages": [
        [
            _h("When to use it"),
            _t("For an action that happened **before another past event**: English \"had "
               "done.\" Common with ya ~already~, todavía no ~not yet~, nunca ~never~, "
               "antes ~before~ and cuando ~when~."),
            _h("How to form it"),
            _t("**haber** (imperfect) + **past participle**. The participles are the same as in "
               "the present perfect (hablado, comido, hecho, dicho...)."),
            {"type": "table", "header": ["", "haber + participle", "English"],
             "rows": [[p, f"**{_f('haber', 'imperfect', i)}** comido", _PLUP_EN[i]]
                      for i, p in enumerate(_PERSONS)],
             "widths": [0.22, 0.34, 0.44], "gray_rows": [_VOS]},
            _h("Good to know"),
            _b("Same rules as the present perfect: pronouns and no go **before haber** (ya **se "
               "lo** había dicho), the two words never split, and the participle never changes.",
               "**había** on its own means ~there was, there were~ and is always singular: "
               "**Había** muchas personas, never \"habían muchas personas.\"",
               "\"Had just\" is **acababa de** + infinitive: Acababa de llegar. ~I had just "
               "arrived.~"),
            _sp(),
            _ex("Había comido antes de salir.", "I had eaten before I left."),
            _ex("Ya habían llegado cuando llamé.", "They had already arrived when I called."),
            _ex("Cuando llegamos al cine, la película ya había empezado.",
                "When we got to the movie theater, the movie had already started."),
            _ex("Nunca había visto el mar antes de ese viaje.",
                "I had never seen the ocean before that trip."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 15. Present perfect vs. past perfect
# --------------------------------------------------------------------------
_CMP_PERFECTS = {
    "id": "cmp-perfects",
    "title": "Present perfect vs. past perfect",
    "pages": [
        [
            _t("Both are **haber + participle**. The difference is the reference point: the "
               "present perfect looks back from **now**; the past perfect looks back from "
               "**a moment in the past**."),
            {"type": "compare", "left": "Present perfect: up to now",
             "right": "Past perfect: before another past event",
             "rows": [
                 ["haber in the present: **he, has, ha, hemos, han** + participle",
                  "haber in the imperfect: **había, habías, había, habíamos, habían** + "
                  "participle"],
                 ["English: have/has done", "English: had done"],
                 ["Experiences so far; a period still open (este año)",
                  "An action finished before something else in the past"],
                 ["Clues: nunca, alguna vez, ya, todavía no, este año",
                  "Clues: ya... cuando, antes de, todavía no... cuando"],
             ]},
            _h("Present perfect: the period reaches now"),
            {"type": "timeline", "events": [
                {"pos": 0.15, "label": "2019: Cartagena", "mark": "point"},
                {"pos": 0.55, "label": "2024: Medellín", "mark": "point"},
                {"pos": 1.0, "label": "ahora", "mark": "now"},
            ], "caption": "**He estado** en Colombia dos veces. ~I've been to Colombia twice.~ "
                          "Both trips are counted in a period that is still open, up to **now**."},
            _h("Past perfect: one past event before another"),
            {"type": "timeline", "events": [
                {"pos": 0.2, "label": "1. **habían llegado**", "mark": "point"},
                {"pos": 0.6, "label": "2. **llamé**", "mark": "point"},
                {"pos": 1.0, "label": "ahora", "mark": "now"},
            ], "caption": "Ya **habían llegado** cuando **llamé**. ~They had already arrived when "
                          "I called.~ First they arrived, then I called; both are in the past."},
            _ex("Este mes hemos ido al cine tres veces.",
                "We've gone to the movies three times this month."),
            _ex("Cuando llegué a la fiesta, Ana ya se había ido.",
                "When I got to the party, Ana had already left."),
        ],
        [
            _h("Same verb, two perfects"),
            {"type": "compare", "left": "Present perfect", "right": "Past perfect",
             "rows": [
                 ["Nunca **he visto** nieve. ~I've never seen snow.~",
                  "Nunca **había visto** nieve antes de ese viaje. ~I had never seen snow "
                  "before that trip.~"],
                 ["**He leído** ese libro dos veces. ~I've read that book twice.~",
                  "**Había leído** el libro antes de ver la película. ~I had read the book "
                  "before I saw the movie.~"],
                 ["Todavía no **ha llegado**. ~He hasn't arrived yet.~",
                  "Todavía no **había llegado** cuando salimos. ~He hadn't arrived yet when "
                  "we left.~"],
                 ["**Se lo he dicho** muchas veces. ~I've told him many times.~",
                  "Ya **se lo había dicho**. ~I had already told him.~"],
             ]},
            _h("Rules for both"),
            _b("Pronouns and **no** go **before haber**: **se lo** he dicho, **no lo** había "
               "visto. Never between haber and the participle.",
               "The participle never changes: Las **he comprado**. Las **había comprado**. "
               "~I've bought them. I had bought them.~"),
            _h("Latin America: present perfect or preterite?"),
            {"type": "compare", "left": "Present perfect", "right": "Preterite",
             "rows": [
                 ["Experiences up to now: **He estado** en Colombia dos veces. ~I've been to "
                  "Colombia twice.~",
                  "Finished actions, even earlier today: Hoy **comí** arroz. ~Today I ate "
                  "rice.~"],
                 ["Never, so far: Nunca **he probado** el mole. ~I've never tried mole.~",
                  "Esta mañana **fui** al banco. ~This morning I went to the bank.~"],
                 ["Still open: Esta semana **he trabajado** mucho. ~I've worked a lot this "
                  "week.~",
                  "¿Ya **comiste**? ~Have you eaten yet?~ (normal in Latin America)"],
             ]},
            _sp(),
            {"type": "xref", "text": "All the forms: **Present perfect**", "dest": "t-pres-perfect"},
            {"type": "xref", "text": "All the forms: **Past perfect**", "dest": "t-past-perfect"},
        ],
    ],
}

# --------------------------------------------------------------------------
# 16. Present subjunctive
# --------------------------------------------------------------------------
_SUBJ_STEPS = ["hablar", "comer", "vivir", "tener", "hacer", "conocer", "decir"]
_SUBJ_STEPS_EN = ["~(that) I speak~", "~(that) I eat~", "~(that) I live~", "~(that) I have~",
                  "~(that) I do, make~", "~(that) I know~", "~(that) I say~"]

_SPELLING_SUBJ = [
    ("-car", "c becomes **qu**", "buscar", "~look for~"),
    ("-gar", "g becomes **gu**", "llegar", "~arrive~"),
    ("-zar", "z becomes **c**", "empezar", "~begin~ (also e to ie)"),
    ("-ger", "g becomes **j**", "escoger", "~choose~"),
    ("-guir", "gu becomes **g**", "seguir", "~follow~ (also e to i)"),
]

_PRES_SUBJ = {
    "id": "pres-subj",
    "title": "Present subjunctive",
    "pages": [
        [
            _h("What it is"),
            _t("The subjunctive is a **mood**, not a time. It usually appears after **que** when "
               "the first part of the sentence expresses a wish, a feeling, a doubt or a "
               "recommendation: Quiero que **vengas**. ~I want you to come.~"),
            _h("How to form it"),
            _t("1. Take the **yo** form of the present. 2. Drop the **-o**. 3. Add the "
               "\"opposite\" endings: -ar verbs take **e** endings; -er and -ir verbs take "
               "**a** endings. Irregular yo forms carry over (tengo, tenga)."),
            {"type": "table", "header": ["Infinitive", "yo present", "subjunctive (yo)",
                                         "English"],
             "rows": [[v, _f(v, "present", 0), f"**{_f(v, 'pres_subj', 0)}**", en]
                      for v, en in zip(_SUBJ_STEPS, _SUBJ_STEPS_EN)],
             "widths": [0.2, 0.2, 0.25, 0.35], "gray_rows": []},
            _sp(2),
            _endings_table("pres_subj"),
            _t("yo and él/ella have the same form."),
            _sp(2),
            _ex("Quiero que hables con ella.", "I want you to talk to her."),
            _sp(),
            {"type": "xref", "text": "The triggers: **When to use the subjunctive**",
             "dest": "t-subj-when"},
        ],
        [
            _h("Six irregulars"),
            _t("Their yo form does not end in a plain -o (doy, estoy, voy, he, sé, soy), so learn them "
               "whole. **dé** has an accent to tell it apart from de ~of~."),
            {"type": "conj", "verbs": ["dar", "estar", "ir"], "tenses": ["pres_subj"]},
            _sp(2),
            {"type": "conj", "verbs": ["haber", "saber", "ser"], "tenses": ["pres_subj"]},
            _t("As \"there is, there are,\" **haya** stays singular: Ojalá **haya** buenas "
               "noticias. ~I hope there's good news.~"),
            _sp(),
            _ex("Es importante que estés aquí a las ocho.",
                "It's important for you to be here at eight."),
            _ex("Ojalá que sea verdad.", "I hope it's true."),
        ],
        [
            _h("Spelling changes"),
            _t("To keep the sound of the consonant, the spelling changes in **every** person."),
            {"type": "table", "header": ["Ending", "Change", "Infinitive", "subj. (yo)",
                                         "English"],
             "rows": [[e, ch, v, f"**{_f(v, 'pres_subj', 0)}**", en]
                      for e, ch, v, en in _SPELLING_SUBJ],
             "widths": [0.12, 0.22, 0.18, 0.18, 0.30], "gray_rows": []},
            _h("Stem-changing verbs"),
            _t("-ar and -er verbs change like the present: all forms except nosotros and "
               "vosotros. -ir verbs also change **nosotros and vosotros**: e becomes i, "
               "o becomes u (durmamos, sintamos). pedir-type verbs keep the i everywhere: "
               f"{_f('pedir', 'pres_subj', 0)}, {_f('pedir', 'pres_subj', 3)}."),
            {"type": "conj", "verbs": ["pensar", "volver", "dormir", "sentir"],
             "tenses": ["pres_subj"]},
            _sp(),
            _ex("Espero que te sientas mejor.", "I hope you feel better."),
            _ex("Es mejor que lleguemos temprano.", "It's better if we get there early."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 17. Past subjunctive
# --------------------------------------------------------------------------
_PAST_SUBJ_STEPS = ["hablar", "comer", "tener", "ir", "decir", "poder", "hacer", "leer",
                    "dormir", "pedir"]
_PAST_SUBJ_EN = ["~(that) I spoke~", "~(that) I ate~", "~(that) I had~",
                 "~(that) I went~ (ser: ~(that) I were~)", "~(that) I said~", "~(that) I could~",
                 "~(that) I did, made~", "~(that) I read~", "~(that) I slept~",
                 "~(that) I asked for~"]

_PAST_SUBJ = {
    "id": "past-subj",
    "title": "Past subjunctive",
    "pages": [
        [
            _h("When to use it"),
            _b("The same triggers as the present subjunctive, when the main verb is in the "
               "**past** or the **conditional**: Quiero que **vengas**. ~I want you to come.~ "
               "Quería que **vinieras**. ~I wanted you to come.~",
               "**If** something were true (si-clauses): Si **tuviera** tiempo, viajaría. "
               "~If I had time, I would travel.~",
               "Wishes that are unlikely or impossible: Ojalá **pudiera** ir. ~I wish I could "
               "go.~",
               "Extra-polite requests: **Quisiera** un café. ~I'd like a coffee.~"),
            _h("How to form it"),
            _t("1. Take the **ellos** form of the preterite. 2. Drop **-ron**. 3. Add **-ra, "
               "-ras, -ra, -ramos, -rais, -ran**. Regular -ar verbs end in **-ara**, -er/-ir verbs "
               "in **-iera**, and every preterite irregular carries over (tuvieron, tuviera). "
               "nosotros takes an accent: habl**áramos**, com**iéramos**."),
            _endings_table("past_subj"),
        ],
        [
            _h("From the preterite"),
            {"type": "table", "header": ["Infinitive", "ellos preterite", "past subj. (yo)",
                                         "English"],
             "rows": [[v, _f(v, "preterite", 5), f"**{_f(v, 'past_subj', 0)}**", en]
                      for v, en in zip(_PAST_SUBJ_STEPS, _PAST_SUBJ_EN)],
             "widths": [0.18, 0.24, 0.24, 0.34], "gray_rows": []},
            _t("You will also see **-se** forms (hablase, tuviese), mostly in Spain and in "
               "writing. They mean the same; you only need to recognize them."),
            _t("As \"there were,\" **hubiera** stays singular, like hay: Si **hubiera** más "
               "tiempo... ~If there were more time...~"),
            _sp(),
            _ex("Me pidió que lo llamara.", "He asked me to call him."),
            _ex("Si yo fuera tú, hablaría con ella.", "If I were you, I'd talk to her."),
            _ex("Era importante que todos llegaran a tiempo.",
                "It was important for everyone to arrive on time."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 18. When to use the subjunctive
# --------------------------------------------------------------------------
_SUBJ_WHEN = {
    "id": "subj-when",
    "title": "When to use the subjunctive",
    "pages": [
        [
            _t("The subjunctive goes in the part after **que** when the first part is **not a "
               "plain statement of fact**: a wish, a feeling, a judgment, a doubt. Usually there "
               "are **two different subjects**; with one subject, use the infinitive: Quiero "
               "**ir**. ~I want to go.~ Quiero que **vayas**. ~I want you to go.~"),
            {"type": "table", "header": ["Trigger", "Expressions", "Example"],
             "rows": [
                 ["Wishes", "querer que, esperar que, preferir que, pedir que",
                  "Quiero que **vengas**. ~I want you to come.~"],
                 ["Advice", "recomendar que, sugerir que, aconsejar que",
                  "Te recomiendo que **pruebes** el ajiaco. ~I recommend you try the "
                  "ajiaco.~"],
                 ["Emotion", "me alegra que, me gusta que, siento que ~I'm sorry that~, tener miedo de que",
                  "Me alegra que **estés** aquí. ~I'm glad you're here.~"],
                 ["Impersonal", "es importante que, es necesario que, es mejor que, es posible "
                  "que", "Es mejor que **salgamos** temprano. ~It's better if we leave early.~"],
                 ["Doubt, denial", "dudar que, no creer que, no es verdad que",
                  "Dudo que **llueva**. ~I doubt it will rain.~"],
                 ["Ojalá", "ojalá, ojalá que ~I hope, I wish~",
                  "Ojalá **haga** buen tiempo. ~I hope the weather is nice.~"],
                 ["Linking words", "para que, antes de que, sin que, a menos que",
                  "Llámame antes de que **salgas**. ~Call me before you leave.~"],
             ],
             "widths": [0.17, 0.35, 0.48], "gray_rows": []},
            _t("Certainty takes the **indicative**: es verdad que, es obvio que, creo que, "
               "estoy seguro de que: Creo que **viene**. ~I think he's coming.~"),
            _ex("Mis papás quieren que estudie más.", "My parents want me to study more."),
            _ex("Te lo explico para que lo entiendas.",
                "I'll explain it to you so that you understand it."),
        ],
        [
            _h("aunque and cuando: fact or not yet?"),
            {"type": "compare", "left": "Indicative: a fact", "right": "Subjunctive: uncertain or not yet",
             "rows": [
                 ["Aunque **llueve**, vamos a salir. ~Even though it's raining, we're going "
                  "out.~",
                  "Aunque **llueva**, vamos a salir. ~Even if it rains, we're going out.~"],
                 ["Cuando **llego** a casa, ceno. ~When I get home, I have dinner.~ (habit)",
                  "Cuando **llegues** a casa, llámame. ~When you get home, call me.~ (future)"],
             ]},
            _h("si-clauses: real or imagined?"),
            {"type": "compare", "left": "Real or likely", "right": "Unreal or unlikely",
             "rows": [
                 ["si + **present**, then present, future or command",
                  "si + **past subjunctive**, then **conditional**"],
                 ["Si **tengo** tiempo, **viajo**. ~If I have time, I travel.~",
                  "Si **tuviera** tiempo, **viajaría**. ~If I had time, I would travel.~"],
                 ["Si **llueve**, nos **quedaremos** en casa. ~If it rains, we'll stay home.~",
                  "Si **fuera** rico, **compraría** una finca. ~If I were rich, I would buy a "
                  "farm.~"],
             ]},
            _t("After si (if), never use the present subjunctive (Si **tengo**, not \"si tenga\") or "
               "the conditional (Si **tuviera**, not \"si tendría\"). The halves can swap "
               "places: Viajaría si tuviera tiempo."),
            _sp(),
            _ex("Ojalá que no llueva mañana.", "I hope it doesn't rain tomorrow."),
            _ex("Si tuviera más dinero, compraría un carro nuevo.",
                "If I had more money, I would buy a new car."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 19. Indicative vs. subjunctive
# --------------------------------------------------------------------------
_CMP_IND_SUBJ = {
    "id": "cmp-ind-subj",
    "title": "Indicative vs. subjunctive",
    "pages": [
        [
            _t("The **indicative** states facts and what you believe is true. The "
               "**subjunctive** is for what you want, doubt, feel about, or what is not real "
               "yet. Same sentence frame, different mood:"),
            {"type": "compare", "left": "Indicative", "right": "Subjunctive",
             "rows": [
                 ["Creo que **viene**. ~I think he's coming.~",
                  "No creo que **venga**. ~I don't think he's coming.~"],
                 ["Sé que **está** en casa. ~I know she's at home.~",
                  "Dudo que **esté** en casa. ~I doubt she's at home.~"],
                 ["Es verdad que **habla** inglés. ~It's true that he speaks English.~",
                  "Es posible que **hable** inglés. ~It's possible that he speaks English.~"],
                 ["Tengo un amigo que **habla** japonés. ~I have a friend who speaks "
                  "Japanese.~",
                  "Busco a alguien que **hable** japonés. ~I'm looking for someone who speaks "
                  "Japanese.~"],
                 ["Cuando **llego** a casa, ceno. ~When I get home, I have dinner.~",
                  "Cuando **llegue** a casa, te llamo. ~When I get home, I'll call you.~"],
                 ["Aunque **está** cansado, trabaja. ~Even though he's tired, he works.~",
                  "Aunque **esté** cansado, va a trabajar. ~Even if he's tired, he's going to "
                  "work.~"],
                 ["Si **tengo** tiempo, te ayudo. ~If I have time, I'll help you.~",
                  "Si **tuviera** tiempo, te ayudaría. ~If I had time, I would help you.~"],
             ]},
            _t("Quick test: am I saying it is true? Use the indicative. Am I wishing, "
               "doubting, reacting, or talking about something not yet real? Use the "
               "subjunctive. **creer que** and **pensar que** take the indicative; **no creer "
               "que** and **no pensar que** take the subjunctive."),
            _ex("Creo que mañana va a hacer sol, pero no creo que haga calor.",
                "I think it'll be sunny tomorrow, but I don't think it'll be hot."),
            _ex("Sé que tienes razón, pero dudo que ella lo acepte.",
                "I know you're right, but I doubt she'll accept it."),
            _sp(),
            {"type": "xref", "text": "All the forms: **Present subjunctive**", "dest": "t-pres-subj"},
            {"type": "xref", "text": "The triggers: **When to use the subjunctive**",
             "dest": "t-subj-when"},
        ],
    ],
}

# --------------------------------------------------------------------------
# 20. Commands
# --------------------------------------------------------------------------
# Formal commands = present subjunctive (Ud. = él form, Uds. = ellos form), pulled from VERBS.
_UD_YO_RULE = [
    ("hablar", "~speak~"), ("comer", "~eat~"), ("escribir", "~write~"),
    ("tener", "~have~"), ("hacer", "~do, make~"), ("salir", "~leave, go out~"),
    ("decir", "~say, tell~"), ("oír", "~listen, hear~"), ("traer", "~bring~"),
    ("conducir", "~drive~"), ("volver", "~come back~"), ("pedir", "~ask for, order~"),
]
_UD_SPELLING = [("buscar", "~look for~"), ("llegar", "~arrive~"), ("empezar", "~begin~")]
_UD_IRREG = [("ser", "~be~"), ("ir", "~go~"), ("dar", "~give~"), ("estar", "~be~"),
             ("saber", "~know~")]

# The 8 irregular tú commands (not stored in VERBS; tests check them against the conjugator).
TU_IRREGULAR = [
    ("decir", "di", "~say, tell~"), ("hacer", "haz", "~do, make~"), ("ir", "ve", "~go~"),
    ("poner", "pon", "~put~"), ("salir", "sal", "~leave, go out~"), ("ser", "sé", "~be~"),
    ("tener", "ten", "~have~"), ("venir", "ven", "~come~"),
]
_TU_REGULAR = [("hablar", "~speak~"), ("comer", "~eat~"), ("escribir", "~write~"),
               ("pensar", "~think~"), ("volver", "~come back~"), ("pedir", "~ask for, order~"),
               ("dormir", "~sleep~")]


def _ud_row(v, en):
    yo = _f(v, "present", 0)
    return [v, yo, _f(v, "pres_subj", 2), _f(v, "pres_subj", 5), en]


_COMMANDS = {
    "id": "commands",
    "title": "Commands",
    "pages": [
        [
            _h("When to use them"),
            _t("To tell someone to do something: instructions, directions, requests, advice. "
               "Add **por favor** to soften them. Choose the form by who you are talking to:"),
            _b("**tú**: a friend, family member, child, or someone your age in a casual setting.",
               "**usted (Ud.)**: a stranger, an older person, a waiter, a driver, at work. In "
               "much of Colombia, usted is common even between friends and family.",
               "**ustedes (Uds.)**: more than one person, formal or not. In Latin America "
               "ustedes is the only plural; vosotros commands (hablad, comed) are used only "
               "in Spain."),
            _h("Formal commands: Ud. and Uds."),
            _t("1. Start with the **yo** form of the present. 2. Drop the **-o**. 3. Add the "
               "**opposite** ending: -ar verbs take **-e / -en**; -er and -ir verbs take "
               "**-a / -an**. The negative just adds **no**: **No hable.** These are the "
               "Ud./Uds. forms of the present subjunctive."),
            {"type": "table", "header": ["Infinitive", "yo", "Ud.", "Uds.", "English"],
             "rows": [_ud_row(v, en) for v, en in _UD_YO_RULE],
             "widths": [0.2, 0.17, 0.17, 0.18, 0.28], "gray_rows": []},
            _t("The yo form carries its irregularity along: **tengo** gives **tenga**, "
               "**oigo** gives **oiga**, **vuelvo** gives **vuelva**."),
        ],
        [
            _h("Formal commands: spelling changes and irregulars"),
            _t("To keep the sound of the consonant, **-car** becomes **-que**, **-gar** becomes "
               "**-gue**, and **-zar** becomes **-ce**:"),
            {"type": "table", "header": ["Infinitive", "Ud.", "Uds.", "English"],
             "rows": [[v, _f(v, "pres_subj", 2), _f(v, "pres_subj", 5), en]
                      for v, en in _UD_SPELLING],
             "widths": [0.25, 0.22, 0.23, 0.30], "gray_rows": []},
            _t("Five verbs whose yo form does not end in a plain -o are irregular; learn them "
               "whole:"),
            {"type": "table", "header": ["Infinitive", "yo", "Ud.", "Uds.", "English"],
             "rows": [_ud_row(v, en) for v, en in _UD_IRREG],
             "widths": [0.2, 0.17, 0.17, 0.18, 0.28], "gray_rows": []},
            _t("**dé** has an accent so it isn't confused with the word **de** ~of, from~. "
               "**¡Oiga!** is also a way to get someone's attention, like \"Excuse me!\", but it can sound abrupt; **disculpe** is more polite."),
            _h("Polite requests"),
            _t("With service staff, a question often sounds friendlier than a command: "
               "**¿Me trae** la cuenta, por favor? ~Could you bring me the check?~ In Colombia "
               "you will hear **¿Me regala** un café? ~Can I have a coffee?~ (you still pay)."),
            _ex("Siga derecho dos cuadras y voltee a la izquierda.",
                "Go straight two blocks and turn left."),
            _ex("Por favor, no hablen durante la película.",
                "Please don't talk during the movie."),
        ],
        [
            _h("Informal commands: tú"),
            _t("**Affirmative** = the **él** form of the present: **habla**, **come**, "
               "**escribe**. Stem changes stay. **Negative** = **no** + the **tú** form of the "
               "present subjunctive: the Ud. command + **s** (dé gives "
               "**des**, without the accent)."),
            {"type": "table", "header": ["Infinitive", "tú: do it", "tú: don't", "English"],
             "rows": [[v, _f(v, "present", 2), "no " + _f(v, "pres_subj", 1), en]
                      for v, en in _TU_REGULAR],
             "widths": [0.22, 0.22, 0.26, 0.30], "gray_rows": []},
            _h("The 8 irregular tú commands"),
            _t("Only the affirmative is irregular. The negative follows the normal rule: **no** + tú "
               "subjunctive."),
            {"type": "table", "header": ["Infinitive", "tú: do it", "tú: don't", "English"],
             "rows": [[v, f"**{tu}**", "no " + _f(v, "pres_subj", 1), en]
                      for v, tu, en in TU_IRREGULAR],
             "widths": [0.22, 0.22, 0.26, 0.30], "gray_rows": []},
            _t("Four of them just drop the ending: **sal**, **ven**, **ten**, **pon**. **ve** "
               "(go) looks like a form of ver, and **sé** (be) like \"I know\"; context makes it "
               "clear."),
        ],
        [
            _h("Where the pronouns go"),
            _b("**Affirmative**: attach the pronouns to the end, written as one word: "
               "**dime** ~tell me~, **siéntese** ~sit down (Ud.)~, **levántate** ~get up~.",
               "**Negative**: put them **before** the verb, after no: **no me digas**, **no se "
               "siente**, **no te levantes**.",
               "**Order**: indirect (to whom) before direct (what): da + me + lo = **dámelo** "
               "~give it to me~; **no me lo des** ~don't give it to me~.",
               "**le / les** + lo, la becomes **se**: **dáselo** ~give it to him/her~; **no se "
               "lo digas** ~don't tell him/her~."),
            _h("The accent mark"),
            _t("Adding pronouns makes the word longer, so write an accent to keep the stress "
               "where it was: **da** + me + lo = **dámelo**; **traiga** + me = **tráigame**; "
               "**levanta** + te = **levántate**. A one-syllable command plus one pronoun "
               "needs none: **dime**, **hazlo**, **ponlo**."),
            {"type": "table", "header": ["Command", "+ pronouns", "Negative", "English"],
             "rows": [
                 ["da", "**dámelo**", "no me lo des", "~give it to me~"],
                 ["di", "**dime**", "no me digas", "~tell me~"],
                 ["haz", "**hazlo**", "no lo hagas", "~do it~"],
                 ["levanta", "**levántate**", "no te levantes", "~get up~"],
                 ["traiga (Ud.)", "**tráigamelo**", "no me lo traiga", "~bring it to me~"],
             ],
             "widths": [0.2, 0.24, 0.27, 0.29], "gray_rows": []},
            _t("\"Let's ...\": the everyday way is **vamos a** + infinitive: **¡Vamos a "
               "comer!** ~Let's eat!~"),
            _ex("Pásame la sal, por favor.", "Pass me the salt, please."),
            _ex("Tráigame la cuenta, por favor.", "Bring me the check, please."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 21. Reflexive verbs
# --------------------------------------------------------------------------
_REFL_PRON = ["me", "te", "se", "nos", "os", "se"]
_REFL_EN = ["~I get up~", "~you get up~", "~he/she gets, you get up~", "~we get up~",
            "~you all get up (Spain)~", "~they get, you all get up~"]

_REFLEXIVE = {
    "id": "reflexive",
    "title": "Reflexive verbs",
    "pages": [
        [
            _h("When to use them"),
            _t("A reflexive verb has **-se** on the infinitive (**levantarse**). The action "
               "comes back to the subject: **Me levanto** ~I get up~ (literally \"I raise "
               "myself\"). Daily routines are full of them. English often uses \"get\" or "
               "nothing at all."),
            _h("How to form it"),
            _t("Conjugate the verb as usual and put the matching pronoun **before** it. Without "
               "the pronoun, the meaning changes: **Levanto** la mano. ~I raise my hand.~"),
            {"type": "table", "header": ["", "levantarse", "English"],
             "rows": [[p, f"**{_REFL_PRON[i]}** {_f('levantar', 'present', i)}", _REFL_EN[i]]
                      for i, p in enumerate(_PERSONS)],
             "widths": [0.22, 0.34, 0.44], "gray_rows": [_VOS]},
            _t("With an infinitive or -ndo form, the pronoun can go before the conjugated verb "
               "or on the end: **Me voy a duchar** = **Voy a ducharme**; **Me estoy vistiendo** "
               "= **Estoy vistiéndome** (add the accent). With affirmative commands it goes on "
               "the end: **¡Levántate!**"),
            _t("Use **el, la, los, las** (not mi, tu) with body parts and clothes: **Me lavo "
               "las manos.** ~I wash my hands.~ **Ponte la chaqueta.** ~Put on your jacket.~"),
            _ex("Me levanto a las seis y me ducho.", "I get up at six and take a shower."),
            _ex("¿Cómo te llamas? —Me llamo Ana.", "What's your name? —My name is Ana."),
        ],
        [
            _h("Common reflexive verbs"),
            {"type": "table", "header": ["Infinitive", "yo", "English", "Note"],
             "rows": [
                 ["despertarse", "me despierto", "~to wake up~", "e to ie"],
                 ["levantarse", "me levanto", "~to get up~", ""],
                 ["ducharse", "me ducho", "~to take a shower~", ""],
                 ["vestirse", "me visto", "~to get dressed~", "e to i"],
                 ["acostarse", "me acuesto", "~to go to bed~", "o to ue"],
                 ["llamarse", "me llamo", "~to be called, named~", ""],
                 ["sentirse", "me siento", "~to feel~ (bien, mal...)", "e to ie"],
                 ["sentarse", "me siento", "~to sit down~", "e to ie"],
                 ["irse", "me voy", "~to leave, to go away~", "like ir"],
                 ["quedarse", "me quedo", "~to stay~", ""],
                 ["preocuparse", "me preocupo", "~to worry~", ""],
             ],
             "widths": [0.22, 0.24, 0.36, 0.18], "gray_rows": []},
            _t("**me siento** means both \"I feel\" (sentirse) and \"I sit down\" (sentarse); "
               "context tells them apart: Me siento bien. ~I feel fine.~"),
            _h("Same verb, different meaning"),
            {"type": "compare", "left": "Without se", "right": "With se",
             "rows": [
                 ["**ir** ~to go~: Voy al banco. ~I'm going to the bank.~",
                  "**irse** ~to leave~: Me voy. ~I'm leaving.~"],
                 ["**dormir** ~to sleep~: Duermo ocho horas. ~I sleep eight hours.~",
                  "**dormirse** ~to fall asleep~: Me dormí. ~I fell asleep.~"],
                 ["**llamar** ~to call~: Llamo a mi mamá. ~I call my mom.~",
                  "**llamarse** ~to be named~: Se llama Luis. ~His name is Luis.~"],
                 ["**quedar** ~to be located~: ¿Dónde queda el banco? ~Where is the bank?~",
                  "**quedarse** ~to stay~: Me quedo en casa. ~I'm staying home.~"],
                 ["**poner** ~to put~: Pongo la mesa. ~I set the table.~",
                  "**ponerse** ~to put on; to become~: Me pongo nervioso. ~I get nervous.~"],
             ]},
            _ex("Me dormí viendo la película.", "I fell asleep watching the movie."),
            _ex("Ya me voy; nos vemos mañana.", "I'm leaving now; see you tomorrow."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 22. Gustar-type verbs
# --------------------------------------------------------------------------
_GUSTA, _GUSTAN = _f("gustar", "present", 2), _f("gustar", "present", 5)

_GUSTAR = {
    "id": "gustar",
    "title": "Gustar-type verbs",
    "pages": [
        [
            _h("How gustar works"),
            _t("**gustar** means \"to be pleasing.\" The thing you like is the **subject**, so "
               "the verb agrees with **it**, not with you. The person who likes it is shown by a "
               "pronoun in front: **Me gusta el café.** ~I like coffee~ (literally \"Coffee "
               "pleases me\")."),
            {"type": "table", "header": ["", "One thing or an infinitive", "Plural things"],
             "rows": [
                 ["**me**", f"me **{_GUSTA}** el café ~I like coffee~",
                  f"me **{_GUSTAN}** los perros ~I like dogs~"],
                 ["**te**", f"te {_GUSTA} bailar ~you like to dance~",
                  f"te {_GUSTAN} las películas ~you like movies~"],
                 ["**le**", f"le {_GUSTA} la playa ~he/she likes, you like the beach~",
                  f"le {_GUSTAN} los tacos ~he/she likes, you like tacos~"],
                 ["**nos**", f"nos {_GUSTA} viajar ~we like to travel~",
                  f"nos {_GUSTAN} las montañas ~we like the mountains~"],
                 ["**os**", f"os {_GUSTA} la música ~you all like music (Spain)~",
                  f"os {_GUSTAN} los libros ~you all like books (Spain)~"],
                 ["**les**", f"les {_GUSTA} el fútbol ~they, you all like soccer~",
                  f"les {_GUSTAN} los gatos ~they, you all like cats~"],
             ],
             "widths": [0.1, 0.45, 0.45], "gray_rows": [_VOS]},
            _b("Use **a** + person to say who, or for emphasis: **A Juan le gusta** el café. "
               "~Juan likes coffee.~ **A mí me gusta, ¿y a ti?** ~I like it, and you?~",
               "Negative: **no** goes first: **No me gustan** las cebollas. ~I don't like "
               "onions.~",
               "Past, for one experience: **Me gustó** la película. ~I liked the movie.~ "
               "Polite wish: **Me gustaría** un café. ~I'd like a coffee.~",
               "**Me gustas** means \"I like you\" romantically. For a person who is nice, say "
               "**Me cae bien.** ~I like him/her.~"),
            _ex("¿Te gusta la comida colombiana? —Sí, me encanta.",
                "Do you like Colombian food? —Yes, I love it."),
        ],
        [
            _h("Verbs that work like gustar"),
            {"type": "table", "header": ["Verb", "English", "Example"],
             "rows": [
                 ["encantar", "~to love (things), to delight~",
                  "Me encanta esta ciudad. ~I love this city.~"],
                 ["interesar", "~to interest~",
                  "Me interesa la historia. ~I'm interested in history.~"],
                 ["molestar", "~to bother~",
                  "Me molesta el ruido. ~The noise bothers me.~"],
                 ["doler (o to ue)", "~to hurt~",
                  "Me duele la cabeza. ~My head hurts.~ Me duelen los pies. ~My feet hurt.~"],
                 ["importar", "~to matter, to care about~",
                  "No me importa. ~I don't care.~ ¿Le importa si abro la ventana? ~Do you mind "
                  "if I open the window?~"],
                 ["faltar", "~to be missing, to lack~",
                  "Me falta un tenedor. ~I'm missing a fork.~"],
                 ["quedar", "~to have left; to fit, to suit~",
                  "Me quedan diez dólares. ~I have ten dollars left.~ Esa camisa te queda "
                  "bien. ~That shirt looks good on you.~"],
             ],
             "widths": [0.18, 0.27, 0.55], "gray_rows": []},
            _t("**encantar** is already strong, so it doesn't need mucho: **Me encanta.** ~I love "
               "it.~ With **doler**, use **la, los** for the body part, "
               "not mi: **Me duele la espalda.** ~My back hurts.~"),
            _ex("Me duelen los pies después de caminar todo el día.",
                "My feet hurt after walking all day."),
            _ex("A mis hijos no les gusta levantarse temprano.",
                "My kids don't like getting up early."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 23. Helper verbs: should, have to, can
# --------------------------------------------------------------------------
_HELPERS = {
    "id": "helpers",
    "title": "Helper verbs: should, have to, can",
    "pages": [
        [
            _h("Helper + infinitive"),
            _t("Conjugate the helper and put the second verb in the **infinitive**: **Tengo que "
               "trabajar.** ~I have to work.~ Of these, only **tener que** and **hay que** "
               "need **que**."),
            {"type": "table", "header": ["Helper", "English", "How strong it sounds", "Example"],
             "rows": [
                 ["**tener que**", "~to have to~", "strong; the everyday \"I have to\"",
                  "Tengo que trabajar mañana. ~I have to work tomorrow.~"],
                 ["**deber**", "~must, should~", "strong; duty or a rule",
                  "Debes usar el cinturón de seguridad. ~You must wear your seat belt.~"],
                 ["**hay que**", "~one has to, you have to~", "general rule, no person; "
                  "always hay",
                  "Hay que pagar en efectivo. ~You have to pay in cash.~"],
                 ["**necesitar**", "~to need (to)~", "medium; a real need",
                  "Necesito descansar. ~I need to rest.~"],
                 ["**debería**", "~should, ought to~", "soft; friendly advice",
                  "Debería dormir más. ~I should sleep more.~"],
                 ["**poder**", "~can, to be able to, may~", "ability or permission",
                  "¿Puedo pagar con tarjeta? ~Can I pay by card?~"],
                 ["**querer**", "~to want (to)~", "a wish, not a duty",
                  "Quiero aprender a bailar salsa. ~I want to learn to dance salsa.~"],
             ],
             "widths": [0.17, 0.2, 0.25, 0.38], "gray_rows": []},
            _t("**tener que** and **deber** are both strong; **necesitar** is a real need; **debería** is "
               "soft, friendly advice. **hay que** is the impersonal \"you have to,\" with no specific "
               "person. **debería** is the conditional of deber, the polite \"should.\""),
            _ex("No tienes que venir, pero me gustaría verte.",
                "You don't have to come, but I'd like to see you."),
        ],
        [
            _h("\"I should\" and \"I have to\": the forms"),
            {"type": "conj", "verbs": ["deber"], "tenses": ["present", "conditional"]},
            _sp(2),
            {"type": "conj", "verbs": ["tener", "poder"], "tenses": ["present"]},
            _h("Watch out"),
            _b("**no tener que** = \"don't have to\"; **no deber** = \"must not\": **No "
               "tienes que** pagar. ~You don't have to pay.~ **No debes** fumar aquí. ~You must "
               "not smoke here.~",
               "In the past: **tuve que** ~I had to (and did)~, **tenía que** ~I had to, I was "
               "supposed to~. **Debería haber** + participle = \"I should have\": "
               "**Debería haber estudiado más.** ~I should have studied more.~",
               "A softer \"I want\": **quisiera** ~I would like~: **Quisiera** una mesa para "
               "dos. ~I'd like a table for two.~"),
            _ex("Hay que llegar temprano; el vuelo sale a las siete.",
                "You have to get there early; the flight leaves at seven."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 24. Weather
# --------------------------------------------------------------------------
_RAIN_ROWS = [
    ("present", lambda v: _f(v, "present", 2), "~it rains, it's raining~"),
    ("progressive", lambda v: f"{_f('estar', 'present', 2)} {VERBS[v]['gerund']}",
     "~it's raining (right now)~"),
    ("ir a", lambda v: f"{_f('ir', 'present', 2)} a {v}", "~it's going to rain~"),
    ("preterite", lambda v: _f(v, "preterite", 2), "~it rained~"),
    ("imperfect", lambda v: _f(v, "imperfect", 2), "~it was raining, it used to rain~"),
    ("future", lambda v: _f(v, "future", 2), "~it will rain~"),
    ("conditional", lambda v: _f(v, "conditional", 2), "~it would rain~"),
    ("pres. perfect", lambda v: f"{_f('haber', 'present', 2)} {VERBS[v]['participle']}",
     "~it has rained~"),
    ("pres. subjunctive", lambda v: f"(que) {_f(v, 'pres_subj', 2)}", "~(that) it rains~"),
]

_WEATHER = {
    "id": "weather",
    "title": "Weather",
    "pages": [
        [
            _h("To rain, to snow"),
            _t("**llover** ~to rain~ (o to ue) and **nevar** ~to snow~ (e to ie) have only "
               "one form per tense, the **él** form, with no subject: **Llueve.** ~It's "
               "raining.~ Spanish has no word for \"it\" here. The nouns: **la lluvia** "
               "~the rain~, **la nieve** ~the snow~."),
            {"type": "table", "header": ["Tense", "llover", "nevar", "English (llover)"],
             "rows": [[name, f"**{fn('llover')}**", f"**{fn('nevar')}**", en]
                      for name, fn, en in _RAIN_ROWS],
             "widths": [0.24, 0.2, 0.2, 0.36], "gray_rows": []},
            _t("Ojalá no **llueva** mañana. ~I hope it doesn't rain tomorrow.~"),
            _ex("Ayer llovió toda la tarde.", "It rained all afternoon yesterday."),
            _ex("Lleva un paraguas; va a llover.", "Take an umbrella; it's going to rain."),
        ],
        [
            _h("hace, está, hay"),
            _t("Ask: **¿Qué tiempo hace?** or **¿Cómo está el clima?** ~What's the weather "
               "like?~"),
            {"type": "table", "header": ["Spanish", "English", "Spanish", "English"],
             "rows": [
                 ["**hace** frío", "~it's cold~", "**hace** calor", "~it's hot~"],
                 ["**hace** sol", "~it's sunny~", "**hace** viento", "~it's windy~"],
                 ["**hace** fresco", "~it's cool~", "**hace** buen tiempo",
                  "~the weather is nice~"],
                 ["**está** nublado", "~it's cloudy~", "**hace** mal tiempo",
                  "~the weather is bad~"],
                 ["**está** despejado", "~it's clear~", "**está** lloviendo",
                  "~it's raining~"],
                 ["**hay** niebla", "~it's foggy~", "**está** nevando", "~it's snowing~"],
                 ["**hay** neblina", "~it's misty, foggy~", "**hay** tormenta",
                  "~there's a storm~"],
             ],
             "widths": [0.24, 0.26, 0.24, 0.26], "gray_rows": []},
            _b("**hace** + noun takes **mucho**, not muy: **Hace mucho frío.** ~It's very "
               "cold.~",
               "People feel with **tener**: **Tengo frío.** ~I'm cold.~ The weather uses "
               "**hacer**: **Hace frío.** ~It's cold (out).~",
               "In the past, describe with the imperfect: **Hacía** sol. ~It was sunny.~ Sum up "
               "a whole period with the preterite: Ayer **hizo** mucho calor. ~It was very hot "
               "yesterday.~",
               "In Latin America, **el clima** is often used for the day's weather, too."),
            _ex("En Bogotá hace frío por la mañana.", "In Bogotá it's cold in the morning."),
            _ex("Cuando era niño, nevaba mucho en mi ciudad.",
                "When I was a kid, it used to snow a lot in my city."),
        ],
    ],
}

# --------------------------------------------------------------------------
# 1. Which tense do I use? (navigation: no practice page)
# --------------------------------------------------------------------------
def _a(label, tense, tid):
    return {"label": label, "tense": tense, "dest": f"t-{tid}"}


_WHICH_TENSE = {
    "id": "which-tense",
    "title": "Which tense do I use?",
    "practice": False,
    "pages": [
        [
            _t("Find the question that fits what you want to say, then tap the tense to go to "
               "its page."),
            {"type": "chart", "nodes": [
                {"q": "Is it about now, or always true?", "answers": [
                    _a("A habit, a routine or a fact", "Present tense", "present"),
                    _a("Happening right now, at this moment", "Present progressive",
                       "progressive"),
                ]},
                {"q": "Is it about the future?", "answers": [
                    _a("A plan: what you are going to do", "Future with ir a", "ir-a"),
                    _a("A prediction or a promise: \"will\" (ir a works too)", "Future tense", "future"),
                    _a("A fixed plan with a time word (mañana)", "Present tense", "present"),
                ]},
                {"q": "Is it about the past?", "answers": [
                    _a("It happened a moment ago: \"I just ...\"", "Just did: acabar de",
                       "acabar-de"),
                    _a("A finished event: ayer, dos veces, en 2020", "Preterite",
                       "preterite"),
                    _a("Background, a description, a habit, or \"was ...-ing\"",
                       "Imperfect", "imperfect"),
                    _a("Not sure which of those two?", "Preterite vs. imperfect",
                       "cmp-pret-imp"),
                    _a("An experience, or still true now: \"I have ...\"", "Present perfect",
                       "pres-perfect"),
                    _a("Before another past event: \"I had ...\"", "Past perfect",
                       "past-perfect"),
                    _a("\"Have done\" or \"had done\"?", "Present perfect vs. past perfect",
                       "cmp-perfects"),
                ]},
                {"q": "Is it imaginary, polite, or advice?", "answers": [
                    _a("\"would\", \"could\", \"should\"", "Conditional", "conditional"),
                    _a("An unreal \"if\": if I had, if I were", "Past subjunctive",
                       "past-subj"),
                ]},
                {"q": "Does it follow que after a wish, a doubt, an emotion or advice?",
                 "answers": [
                    _a("The first verb is present, future or a command", "Present subjunctive",
                       "pres-subj"),
                    _a("The first verb is past or conditional", "Past subjunctive",
                       "past-subj"),
                    _a("Not sure the subjunctive is needed?", "When to use the subjunctive",
                       "subj-when"),
                    _a("The same sentence both ways", "Indicative vs. subjunctive",
                       "cmp-ind-subj"),
                 ]},
                {"q": "Are you telling someone to do something?", "answers": [
                    _a("Instructions, requests, directions", "Commands", "commands"),
                ]},
                {"q": "Something else?", "answers": [
                    _a("Doing it to yourself: me levanto", "Reflexive verbs", "reflexive"),
                    _a("Liking and hurting: me gusta, me duele", "Gustar-type verbs", "gustar"),
                    _a("\"should\", \"have to\", \"can\"", "Helper verbs", "helpers"),
                    _a("Rain, snow, hot or cold", "Weather", "weather"),
                    _a("All irregular forms in one place", "Master irregular verbs",
                       "master-irregulars"),
                    _a("Every tense side by side", "Tense overview", "tense-overview"),
                ]},
            ]},
        ],
    ],
}

# --------------------------------------------------------------------------
# 2. Master irregular verb table (navigation/reference: no practice page)
# --------------------------------------------------------------------------
MASTER_TENSES = ["present", "preterite", "imperfect", "future", "conditional", "pres_subj"]
_MASTER_PAGES = [
    ["ser", "estar", "ir", "tener"],
    ["hacer", "decir", "venir", "poder"],
    ["querer", "saber", "poner", "salir"],
    ["dar", "ver", "oír", "traer"],
    ["haber"],
]


def _master_verb(v):
    return [{"type": "conj", "verbs": [v], "tenses": MASTER_TENSES},
            _t(f"**{v}**: participle **{VERBS[v]['participle']}**, -ndo form "
               f"**{VERBS[v]['gerund']}**")]


def _master_page(verbs):
    out = []
    for v in verbs:
        out += _master_verb(v)
    return out


_MASTER = {
    "id": "master-irregulars",
    "title": "Master irregular verbs",
    "practice": False,
    "pages": [_master_page(p) for p in _MASTER_PAGES[:-1]] + [
        _master_page(_MASTER_PAGES[-1]) + [
            _t("This table shows **haber** as the helper verb of the perfect tenses: **he** "
               "hablado ~I have spoken~, **había** hablado ~I had spoken~. Its preterite "
               "(hube...) is rare as a helper."),
            _t("**Existential haber (there is/are) is always singular: hay, hubo, había, "
               "habrá, habría, haya.** Hay dos bancos. ~There are two banks.~ Había muchas "
               "personas (not habían). ~There were a lot of people.~"),
            _sp(),
            {"type": "xref", "text": "How to use them: **Present perfect**",
             "dest": "t-pres-perfect"},
            {"type": "xref", "text": "**Past perfect**", "dest": "t-past-perfect"},
        ],
    ],
}

# --------------------------------------------------------------------------
# 3. Tense overview (navigation/reference: no practice page)
# --------------------------------------------------------------------------
def _ov(build, en, name):
    return [name] + [build(v) for v in _MODELS] + [en]


def _haber_plus(tense):
    return lambda v: f"{_f('haber', tense, 0)} {VERBS[v]['participle']}"


_OVERVIEW_ROWS = [
    _ov(lambda v: _f(v, "present", 0), "~I speak~", "Present"),
    _ov(lambda v: f"{_f('estar', 'present', 0)} {VERBS[v]['gerund']}", "~I am speaking~",
        "Present progressive"),
    _ov(lambda v: f"{_f('ir', 'present', 0)} a {v}", "~I'm going to speak~", "ir a + infinitive"),
    _ov(lambda v: f"acabo de {v}", "~I just spoke~", "acabar de + infinitive"),
    _ov(lambda v: _f(v, "preterite", 0), "~I spoke~", "Preterite"),
    _ov(lambda v: _f(v, "imperfect", 0), "~I used to speak, I was speaking~", "Imperfect"),
    _ov(lambda v: _f(v, "future", 0), "~I will speak~", "Future"),
    _ov(lambda v: _f(v, "conditional", 0), "~I would speak~", "Conditional"),
    _ov(_haber_plus("present"), "~I have spoken~", "Present perfect"),
    _ov(_haber_plus("imperfect"), "~I had spoken~", "Past perfect"),
    _ov(lambda v: f"que {_f(v, 'pres_subj', 0)}", "~that I speak~", "Present subjunctive"),
    _ov(lambda v: f"que {_f(v, 'past_subj', 0)}", "~that I spoke~", "Past subjunctive"),
    _ov(lambda v: f"{_f(v, 'present', 2)} / {_f(v, 'pres_subj', 2)}",
        "~speak!~", "Command (tú / Ud.)"),
]

_OVERVIEW = {
    "id": "tense-overview",
    "title": "Tense overview",
    "practice": False,
    "pages": [
        [
            _t("One regular verb of each class in the **yo** form (commands: tú / Ud.). The "
               "English is for hablar; comer ~to eat~ and vivir ~to live~ work the same way."),
            {"type": "table", "header": ["Tense", "hablar", "comer", "vivir", "English (hablar)"],
             "rows": _OVERVIEW_ROWS,
             "widths": [0.24, 0.17, 0.17, 0.17, 0.25], "gray_rows": []},
            _t("**que** is not part of the verb, but the subjunctive usually follows it."),
            _sp(),
            {"type": "xref", "text": "Choosing a tense: **Which tense do I use?**",
             "dest": "t-which-tense"},
            {"type": "xref", "text": "All the irregular forms: **Master irregular verbs**",
             "dest": "t-master-irregulars"},
        ],
    ],
}

_PADDED = {"table", "conj", "compare", "timeline"}


def _spaced(topic, gap=4):
    """Insert a small spacer after each table-like block unless one already follows."""
    pages = []
    for blocks in topic["pages"]:
        out = []
        for i, b in enumerate(blocks):
            out.append(b)
            nxt = blocks[i + 1] if i + 1 < len(blocks) else None
            if b["type"] in _PADDED and nxt is not None and nxt["type"] != "spacer":
                out.append(_sp(gap))
        pages.append(out)
    return {**topic, "pages": pages}


# Topic order = print order. Append new topics here.
_TOPICS = [
    _WHICH_TENSE,
    _MASTER,
    _OVERVIEW,
    _PRESENT,
    _PROGRESSIVE,
    _IR_A,
    _ACABAR_DE,
    _PRETERITE,
    _IMPERFECT,
    _CMP_PRET_IMP,
    _FUTURE,
    _CONDITIONAL,
    _PRES_PERFECT,
    _PAST_PERFECT,
    _CMP_PERFECTS,
    _PRES_SUBJ,
    _PAST_SUBJ,
    _SUBJ_WHEN,
    _CMP_IND_SUBJ,
    _COMMANDS,
    _REFLEXIVE,
    _GUSTAR,
    _HELPERS,
    _WEATHER,
]

VERB_TOPICS = [_spaced(t) for t in _TOPICS]
