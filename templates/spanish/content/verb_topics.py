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
               "(some also stem-change: tengo, **tienes**; digo, **dices**)."),
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
            _t("Memorize these whole. **ser** and **estar** both mean \"to be\"; **ir** = to go."),
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
    ("u", "haber", None, None, None, "él: hubo ~there was, there were~"),
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
            _ex("Estaba en la casa cuando llegaste.", "I was at home when you arrived."),
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
    _PRESENT,
    _PROGRESSIVE,
    _IR_A,
    _ACABAR_DE,
    _PRETERITE,
    _IMPERFECT,
    _CMP_PRET_IMP,
]

VERB_TOPICS = [_spaced(t) for t in _TOPICS]
