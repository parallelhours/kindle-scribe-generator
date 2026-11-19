# templates/crossword/conjugator.py
"""
Spanish verb conjugator.
conjugate(infinitive, tense, subject) -> str

Tenses: present | preterite | imperfect | future | conditional | subjunctive | imperative
Subjects (non-imperative): yo | tú | él | nosotros | vosotros | ellos
Subjects (imperative):     tú | usted | nosotros | vosotros | ustedes
"""

_S = ["yo", "tú", "él", "nosotros", "vosotros", "ellos"]
_I = ["tú", "usted", "nosotros", "vosotros", "ustedes"]

def _t(forms): return dict(zip(_S, forms))
def _i(forms): return dict(zip(_I, forms))


# ── Regular conjugation rules ─────────────────────────────────────────────────

def _stem(infinitive):
    return infinitive[:-2], infinitive[-2:]


_REGULAR = {
    "ar": {
        "present":     _t(["o",  "as",  "a",  "amos",  "áis",  "an"]),
        "preterite":   _t(["é",  "aste","ó",  "amos",  "asteis","aron"]),
        "imperfect":   _t(["aba","abas","aba","ábamos","abais","aban"]),
        "future":      _t(["é",  "ás",  "á",  "emos",  "éis",  "án"]),
        "conditional": _t(["ía", "ías", "ía", "íamos", "íais", "ían"]),
        "subjunctive": _t(["e",  "es",  "e",  "emos",  "éis",  "en"]),
        "imperative":  _i(["a",  "e",   "emos","ad",   "en"]),
    },
    "er": {
        "present":     _t(["o",  "es",  "e",  "emos",  "éis",  "en"]),
        "preterite":   _t(["í",  "iste","ió", "imos",  "isteis","ieron"]),
        "imperfect":   _t(["ía", "ías", "ía", "íamos", "íais", "ían"]),
        "future":      _t(["é",  "ás",  "á",  "emos",  "éis",  "án"]),
        "conditional": _t(["ía", "ías", "ía", "íamos", "íais", "ían"]),
        "subjunctive": _t(["a",  "as",  "a",  "amos",  "áis",  "an"]),
        "imperative":  _i(["e",  "a",   "amos","ed",   "an"]),
    },
    "ir": {
        "present":     _t(["o",  "es",  "e",  "imos",  "ís",   "en"]),
        "preterite":   _t(["í",  "iste","ió", "imos",  "isteis","ieron"]),
        "imperfect":   _t(["ía", "ías", "ía", "íamos", "íais", "ían"]),
        "future":      _t(["é",  "ás",  "á",  "emos",  "éis",  "án"]),
        "conditional": _t(["ía", "ías", "ía", "íamos", "íais", "ían"]),
        "subjunctive": _t(["a",  "as",  "a",  "amos",  "áis",  "an"]),
        "imperative":  _i(["e",  "a",   "amos","id",   "an"]),
    },
}

_FUTURE_CONDITIONAL_TENSES = {"future", "conditional"}


# Stem-changing verbs: "ie" (e→ie), "ue" (o→ue), "i" (e→i, -ir only).
# -ir verbs also take the weak change (e→i, o→u) in the 3rd-person preterite,
# nosotros/vosotros subjunctive and the nosotros command.
STEM_CHANGES = {
    # e → ie
    "pensar": "ie", "cerrar": "ie", "comenzar": "ie", "empezar": "ie",
    "entender": "ie", "perder": "ie", "mentir": "ie", "preferir": "ie",
    "sentir": "ie", "despertar": "ie", "divertir": "ie", "recomendar": "ie",
    "nevar": "ie",
    # o → ue
    "volver": "ue", "devolver": "ue", "resolver": "ue", "encontrar": "ue",
    "recordar": "ue", "mostrar": "ue", "almorzar": "ue", "costar": "ue",
    "dormir": "ue", "morir": "ue", "volar": "ue", "tostar": "ue",
    "acostar": "ue", "llover": "ue", "probar": "ue", "soñar": "ue",
    # e → i
    "pedir": "i", "servir": "i", "repetir": "i", "corregir": "i",
    "seguir": "i", "despedir": "i", "vestir": "i", "elegir": "i",
}

_BOOT = {
    "present":     {"yo", "tú", "él", "ellos"},
    "subjunctive": {"yo", "tú", "él", "ellos"},
    "imperative":  {"tú", "usted", "ustedes"},
}
_WEAK_IR = {
    "preterite":   {"él", "ellos"},
    "subjunctive": {"nosotros", "vosotros"},
    "imperative":  {"nosotros"},
}
_STRONG_CHANGE = {"ie": ("e", "ie"), "ue": ("o", "ue"), "i": ("e", "i")}
_WEAK_CHANGE   = {"ie": ("e", "i"),  "ue": ("o", "u"),  "i": ("e", "i")}
_VOWELS = "aeiouáéíóú"
_UNACCENT = str.maketrans("áéíóú", "aeiou")


def _replace_last(stem, old, new):
    i = stem.rfind(old)
    return stem if i < 0 else stem[:i] + new + stem[i + 1:]


def _apply_stem_change(stem, kind, ending, tense, subject):
    if subject in _BOOT.get(tense, ()):
        return _replace_last(stem, *_STRONG_CHANGE[kind])
    if ending == "ir" and subject in _WEAK_IR.get(tense, ()):
        return _replace_last(stem, *_WEAK_CHANGE[kind])
    return stem


_EER_PRETERITE = {"ió": "yó", "ieron": "yeron", "iste": "íste",
                  "imos": "ímos", "isteis": "ísteis"}


def _orthography(stem, ending, tense, suffix):
    """Spelling changes that keep the consonant sound (or add y)."""
    first = suffix[0].translate(_UNACCENT)
    if ending == "ar":
        if first == "e":
            if stem.endswith("c"):
                stem = stem[:-1] + "qu"      # tocar → toqué
            elif stem.endswith("g"):
                stem = stem + "u"            # llegar → llegué
            elif stem.endswith("z"):
                stem = stem[:-1] + "c"       # organizar → organicé
        return stem, suffix
    if first in "ao":
        if ending == "ir" and stem.endswith("gu"):
            stem = stem[:-1]                 # seguir → sigo
        elif stem.endswith("g"):
            stem = stem[:-1] + "j"           # recoger → recojo
        elif len(stem) > 1 and stem.endswith("c") and stem[-2] in _VOWELS:
            stem = stem[:-1] + "zc"          # conocer → conozco
    if ending == "ir" and stem.endswith("u") and not stem.endswith(("gu", "qu")):
        if suffix == "ió":                   # huir → huyó
            suffix = "yó"
        elif suffix.startswith("ie"):        # huir → huyeron
            suffix = "y" + suffix[1:]
        elif first != "i":                   # huir → huyo, huya
            stem = stem + "y"
    if ending == "er" and stem[-1:] in ("a", "e", "o") and tense == "preterite":
        suffix = _EER_PRETERITE.get(suffix, suffix)   # creer → creyó, creíste
    return stem, suffix


def _conjugate_regular(infinitive, tense, subject):
    stem, ending = _stem(infinitive)
    suffix = _REGULAR[ending][tense][subject]
    if tense in _FUTURE_CONDITIONAL_TENSES:
        return infinitive + suffix
    kind = STEM_CHANGES.get(infinitive)
    if kind:
        stem = _apply_stem_change(stem, kind, ending, tense, subject)
    stem, suffix = _orthography(stem, ending, tense, suffix)
    return stem + suffix


def is_irregular(infinitive: str) -> bool:
    """Irregular or stem-changing (spelling-only changes count as regular)."""
    return infinitive in IRREGULAR_VERBS or infinitive in STEM_CHANGES


# ── Irregular verbs ───────────────────────────────────────────────────────────

IRREGULAR_VERBS = {
    "ser": {
        "present":     _t(["soy",   "eres",    "es",    "somos",    "sois",      "son"]),
        "preterite":   _t(["fui",   "fuiste",  "fue",   "fuimos",   "fuisteis",  "fueron"]),
        "imperfect":   _t(["era",   "eras",    "era",   "éramos",   "erais",     "eran"]),
        "subjunctive": _t(["sea",   "seas",    "sea",   "seamos",   "seáis",     "sean"]),
        "imperative":  _i(["sé",    "sea",     "seamos","sed",      "sean"]),
    },
    "estar": {
        "present":     _t(["estoy",   "estás",    "está",    "estamos",    "estáis",     "están"]),
        "preterite":   _t(["estuve",  "estuviste","estuvo",  "estuvimos",  "estuvisteis","estuvieron"]),
        "subjunctive": _t(["esté",    "estés",    "esté",    "estemos",    "estéis",     "estén"]),
        "imperative":  _i(["está",    "esté",     "estemos", "estad",      "estén"]),
    },
    "ir": {
        "present":     _t(["voy",  "vas",   "va",    "vamos",    "vais",    "van"]),
        "preterite":   _t(["fui",  "fuiste","fue",   "fuimos",   "fuisteis","fueron"]),
        "imperfect":   _t(["iba",  "ibas",  "iba",   "íbamos",   "ibais",   "iban"]),
        "subjunctive": _t(["vaya", "vayas", "vaya",  "vayamos",  "vayáis",  "vayan"]),
        "imperative":  _i(["ve",   "vaya",  "vayamos","id",      "vayan"]),
    },
    "hacer": {
        "present":     _t(["hago",  "haces",   "hace",   "hacemos",  "hacéis",   "hacen"]),
        "preterite":   _t(["hice",  "hiciste", "hizo",   "hicimos",  "hicisteis","hicieron"]),
        "future":      _t(["haré",  "harás",   "hará",   "haremos",  "haréis",   "harán"]),
        "conditional": _t(["haría", "harías",  "haría",  "haríamos", "haríais",  "harían"]),
        "subjunctive": _t(["haga",  "hagas",   "haga",   "hagamos",  "hagáis",   "hagan"]),
        "imperative":  _i(["haz",   "haga",    "hagamos","haced",    "hagan"]),
    },
    "tener": {
        "present":     _t(["tengo",   "tienes",   "tiene",   "tenemos",   "tenéis",    "tienen"]),
        "preterite":   _t(["tuve",    "tuviste",  "tuvo",    "tuvimos",   "tuvisteis", "tuvieron"]),
        "future":      _t(["tendré",  "tendrás",  "tendrá",  "tendremos", "tendréis",  "tendrán"]),
        "conditional": _t(["tendría", "tendrías", "tendría", "tendríamos","tendríais", "tendrían"]),
        "subjunctive": _t(["tenga",   "tengas",   "tenga",   "tengamos",  "tengáis",   "tengan"]),
        "imperative":  _i(["ten",     "tenga",    "tengamos","tened",     "tengan"]),
    },
    "querer": {
        "present":     _t(["quiero",   "quieres",  "quiere",  "queremos",  "queréis",   "quieren"]),
        "preterite":   _t(["quise",    "quisiste", "quiso",   "quisimos",  "quisisteis","quisieron"]),
        "future":      _t(["querré",   "querrás",  "querrá",  "querremos", "querréis",  "querrán"]),
        "conditional": _t(["querría",  "querrías", "querría", "querríamos","querríais", "querrían"]),
        "subjunctive": _t(["quiera",   "quieras",  "quiera",  "queramos",  "queráis",   "quieran"]),
        "imperative":  _i(["quiere",   "quiera",   "queramos","quered",    "quieran"]),
    },
    "poder": {
        "present":     _t(["puedo",   "puedes",  "puede",  "podemos",  "podéis",   "pueden"]),
        "preterite":   _t(["pude",    "pudiste", "pudo",   "pudimos",  "pudisteis","pudieron"]),
        "future":      _t(["podré",   "podrás",  "podrá",  "podremos", "podréis",  "podrán"]),
        "conditional": _t(["podría",  "podrías", "podría", "podríamos","podríais", "podrían"]),
        "subjunctive": _t(["pueda",   "puedas",  "pueda",  "podamos",  "podáis",   "puedan"]),
        "imperative":  _i(["puede",   "pueda",   "podamos","poded",     "puedan"]),
    },
    "decir": {
        "present":     _t(["digo",  "dices",   "dice",   "decimos",  "decís",    "dicen"]),
        "preterite":   _t(["dije",  "dijiste", "dijo",   "dijimos",  "dijisteis","dijeron"]),
        "future":      _t(["diré",  "dirás",   "dirá",   "diremos",  "diréis",   "dirán"]),
        "conditional": _t(["diría", "dirías",  "diría",  "diríamos", "diríais",  "dirían"]),
        "subjunctive": _t(["diga",  "digas",   "diga",   "digamos",  "digáis",   "digan"]),
        "imperative":  _i(["di",    "diga",    "digamos","decid",    "digan"]),
    },
    "venir": {
        "present":     _t(["vengo",   "vienes",   "viene",   "venimos",   "venís",     "vienen"]),
        "preterite":   _t(["vine",    "viniste",  "vino",    "vinimos",   "vinisteis", "vinieron"]),
        "future":      _t(["vendré",  "vendrás",  "vendrá",  "vendremos", "vendréis",  "vendrán"]),
        "conditional": _t(["vendría", "vendrías", "vendría", "vendríamos","vendríais", "vendrían"]),
        "subjunctive": _t(["venga",   "vengas",   "venga",   "vengamos",  "vengáis",   "vengan"]),
        "imperative":  _i(["ven",     "venga",    "vengamos","venid",     "vengan"]),
    },
    "oír": {
        "present":     _t(["oigo",  "oyes",   "oye",   "oímos",   "oís",     "oyen"]),
        "preterite":   _t(["oí",    "oíste",  "oyó",   "oímos",   "oísteis", "oyeron"]),
        "imperfect":   _t(["oía",   "oías",   "oía",   "oíamos",  "oíais",   "oían"]),
        "future":      _t(["oiré",  "oirás",  "oirá",  "oiremos", "oiréis",  "oirán"]),
        "conditional": _t(["oiría", "oirías", "oiría", "oiríamos","oiríais", "oirían"]),
        "subjunctive": _t(["oiga",  "oigas",  "oiga",  "oigamos", "oigáis",  "oigan"]),
        "imperative":  _i(["oye",   "oiga",   "oigamos","oíd",    "oigan"]),
    },
    "dar": {
        "present":     _t(["doy",  "das",   "da",    "damos",   "dais",    "dan"]),
        "preterite":   _t(["di",   "diste", "dio",   "dimos",   "disteis", "dieron"]),
        "subjunctive": _t(["dé",   "des",   "dé",    "demos",   "deis",    "den"]),
        "imperative":  _i(["da",   "dé",    "demos", "dad",     "den"]),
    },
    "ver": {
        "present":    _t(["veo",  "ves",  "ve",  "vemos",  "veis",   "ven"]),
        "preterite":  _t(["vi",   "viste","vio",  "vimos",  "visteis","vieron"]),
        "imperfect":  _t(["veía", "veías","veía", "veíamos","veíais", "veían"]),
        "subjunctive":_t(["vea",  "veas", "vea",  "veamos", "veáis",  "vean"]),
        "imperative": _i(["ve",   "vea",  "veamos","ved",   "vean"]),
    },
    "saber": {
        "present":     _t(["sé",     "sabes",   "sabe",   "sabemos",  "sabéis",   "saben"]),
        "preterite":   _t(["supe",   "supiste", "supo",   "supimos",  "supisteis","supieron"]),
        "future":      _t(["sabré",  "sabrás",  "sabrá",  "sabremos", "sabréis",  "sabrán"]),
        "conditional": _t(["sabría", "sabrías", "sabría", "sabríamos","sabríais", "sabrían"]),
        "subjunctive": _t(["sepa",   "sepas",   "sepa",   "sepamos",  "sepáis",   "sepan"]),
        "imperative":  _i(["sabe",   "sepa",    "sepamos","sabed",    "sepan"]),
    },
    "conocer": {
        "present":     _t(["conozco",  "conoces", "conoce",  "conocemos", "conocéis",  "conocen"]),
        "subjunctive": _t(["conozca",  "conozcas","conozca", "conozcamos","conozcáis", "conozcan"]),
        "imperative":  _i(["conoce",   "conozca", "conozcamos","conoced","conozcan"]),
    },
    "traer": {
        "present":     _t(["traigo",  "traes",   "trae",   "traemos",  "traéis",   "traen"]),
        "preterite":   _t(["traje",   "trajiste","trajo",  "trajimos", "trajisteis","trajeron"]),
        "subjunctive": _t(["traiga",  "traigas", "traiga", "traigamos","traigáis",  "traigan"]),
        "imperative":  _i(["trae",    "traiga",  "traigamos","traed",  "traigan"]),
    },
    "poner": {
        "present":     _t(["pongo",   "pones",   "pone",   "ponemos",  "ponéis",   "ponen"]),
        "preterite":   _t(["puse",    "pusiste", "puso",   "pusimos",  "pusisteis","pusieron"]),
        "future":      _t(["pondré",  "pondrás", "pondrá", "pondremos","pondréis",  "pondrán"]),
        "conditional": _t(["pondría", "pondrías","pondría","pondríamos","pondríais","pondrían"]),
        "subjunctive": _t(["ponga",   "pongas",  "ponga",  "pongamos", "pongáis",  "pongan"]),
        "imperative":  _i(["pon",     "ponga",   "pongamos","poned",   "pongan"]),
    },
    "salir": {
        "present":     _t(["salgo",   "sales",   "sale",   "salimos",  "salís",    "salen"]),
        "future":      _t(["saldré",  "saldrás", "saldrá", "saldremos","saldréis",  "saldrán"]),
        "conditional": _t(["saldría", "saldrías","saldría","saldríamos","saldríais","saldrían"]),
        "subjunctive": _t(["salga",   "salgas",  "salga",  "salgamos", "salgáis",  "salgan"]),
        "imperative":  _i(["sal",     "salga",   "salgamos","salid",   "salgan"]),
    },
    "volver": {
        "present":     _t(["vuelvo",  "vuelves", "vuelve",  "volvemos", "volvéis",  "vuelven"]),
        "subjunctive": _t(["vuelva",  "vuelvas", "vuelva",  "volvamos", "volváis",  "vuelvan"]),
        "imperative":  _i(["vuelve",  "vuelva",  "volvamos","volved",   "vuelvan"]),
    },
    "devolver": {
        "present":     _t(["devuelvo", "devuelves","devuelve","devolvemos","devolvéis","devuelven"]),
        "subjunctive": _t(["devuelva", "devuelvas","devuelva","devolvamos","devolváis","devuelvan"]),
        "imperative":  _i(["devuelve", "devuelva", "devolvamos","devolved","devuelvan"]),
    },
    "encontrar": {
        "present":     _t(["encuentro","encuentras","encuentra","encontramos","encontráis","encuentran"]),
        "subjunctive": _t(["encuentre","encuentres","encuentre","encontremos","encontréis","encuentren"]),
        "imperative":  _i(["encuentra","encuentre","encontremos","encontrad","encuentren"]),
    },
    "recordar": {
        "present":     _t(["recuerdo", "recuerdas","recuerda","recordamos","recordáis","recuerdan"]),
        "subjunctive": _t(["recuerde", "recuerdes","recuerde","recordemos","recordéis","recuerden"]),
        "imperative":  _i(["recuerda", "recuerde", "recordemos","recordad","recuerden"]),
    },
    "mostrar": {
        "present":     _t(["muestro",  "muestras", "muestra",  "mostramos","mostráis", "muestran"]),
        "subjunctive": _t(["muestre",  "muestres", "muestre",  "mostremos","mostréis", "muestren"]),
        "imperative":  _i(["muestra",  "muestre",  "mostremos","mostrad",  "muestren"]),
    },
    "almorzar": {
        "present":     _t(["almuerzo", "almuerzas","almuerza","almorzamos","almorzáis","almuerzan"]),
        "preterite":   _t(["almorcé",  "almorzaste","almorzó","almorzamos","almorzasteis","almorzaron"]),
        "subjunctive": _t(["almuerce", "almuerces","almuerce","almorcemos","almorcéis","almuercen"]),
        "imperative":  _i(["almuerza", "almuerce", "almorcemos","almorzad","almuercen"]),
    },
    "costar": {
        "present":     _t(["cuesto",  "cuestas",  "cuesta",   "costamos","costáis",  "cuestan"]),
        "subjunctive": _t(["cueste",  "cuestes",  "cueste",   "costemos","costéis",  "cuesten"]),
        "imperative":  _i(["cuesta",  "cueste",   "costemos", "costad",  "cuesten"]),
    },
    "dormir": {
        "present":     _t(["duermo",  "duermes",  "duerme",  "dormimos", "dormís",    "duermen"]),
        "preterite":   _t(["dormí",   "dormiste", "durmió",  "dormimos", "dormisteis","durmieron"]),
        "subjunctive": _t(["duerma",  "duermas",  "duerma",  "durmamos", "durmáis",   "duerman"]),
        "imperative":  _i(["duerme",  "duerma",   "durmamos","dormid",   "duerman"]),
    },
    "morir": {
        "present":     _t(["muero",   "mueres",   "muere",   "morimos",  "morís",     "mueren"]),
        "preterite":   _t(["morí",    "moriste",  "murió",   "morimos",  "moristeis", "murieron"]),
        "subjunctive": _t(["muera",   "mueras",   "muera",   "muramos",  "muráis",    "mueran"]),
        "imperative":  _i(["muere",   "muera",    "muramos", "morid",    "mueran"]),
    },
    "pedir": {
        "present":     _t(["pido",    "pides",    "pide",    "pedimos",  "pedís",     "piden"]),
        "preterite":   _t(["pedí",    "pediste",  "pidió",   "pedimos",  "pedisteis", "pidieron"]),
        "subjunctive": _t(["pida",    "pidas",    "pida",    "pidamos",  "pidáis",    "pidan"]),
        "imperative":  _i(["pide",    "pida",     "pidamos", "pedid",    "pidan"]),
    },
    "servir": {
        "present":     _t(["sirvo",   "sirves",   "sirve",   "servimos", "servís",    "sirven"]),
        "preterite":   _t(["serví",   "serviste", "sirvió",  "servimos", "servisteis","sirvieron"]),
        "subjunctive": _t(["sirva",   "sirvas",   "sirva",   "sirvamos", "sirváis",   "sirvan"]),
        "imperative":  _i(["sirve",   "sirva",    "sirvamos","servid",   "sirvan"]),
    },
    "repetir": {
        "present":     _t(["repito",  "repites",  "repite",  "repetimos","repetís",   "repiten"]),
        "preterite":   _t(["repetí",  "repetiste","repitió", "repetimos","repetisteis","repitieron"]),
        "subjunctive": _t(["repita",  "repitas",  "repita",  "repitamos","repitáis",  "repitan"]),
        "imperative":  _i(["repite",  "repita",   "repitamos","repetid", "repitan"]),
    },
    "pensar": {
        "present":     _t(["pienso",  "piensas",  "piensa",  "pensamos", "pensáis",   "piensan"]),
        "subjunctive": _t(["piense",  "pienses",  "piense",  "pensemos", "penséis",   "piensen"]),
        "imperative":  _i(["piensa",  "piense",   "pensemos","pensad",   "piensen"]),
    },
    "cerrar": {
        "present":     _t(["cierro",  "cierras",  "cierra",  "cerramos", "cerráis",   "cierran"]),
        "subjunctive": _t(["cierre",  "cierres",  "cierre",  "cerremos", "cerréis",   "cierren"]),
        "imperative":  _i(["cierra",  "cierre",   "cerremos","cerrad",   "cierren"]),
    },
    "comenzar": {
        "present":     _t(["comienzo","comienzas","comienza","comenzamos","comenzáis","comienzan"]),
        "preterite":   _t(["comencé", "comenzaste","comenzó","comenzamos","comenzasteis","comenzaron"]),
        "subjunctive": _t(["comience","comiences","comience","comencemos","comencéis","comiencen"]),
        "imperative":  _i(["comienza","comience","comencemos","comenzad","comiencen"]),
    },
    "empezar": {
        "present":     _t(["empiezo", "empiezas", "empieza", "empezamos","empezáis",  "empiezan"]),
        "preterite":   _t(["empecé",  "empezaste","empezó",  "empezamos","empezasteis","empezaron"]),
        "subjunctive": _t(["empiece", "empieces", "empiece", "empecemos","empecéis",  "empiecen"]),
        "imperative":  _i(["empieza", "empiece",  "empecemos","empezad", "empiecen"]),
    },
    "entender": {
        "present":     _t(["entiendo","entiendes","entiende","entendemos","entendéis","entienden"]),
        "subjunctive": _t(["entienda","entiendas","entienda","entendamos","entendáis","entiendan"]),
        "imperative":  _i(["entiende","entienda","entendamos","entended","entiendan"]),
    },
    "perder": {
        "present":     _t(["pierdo",  "pierdes",  "pierde",  "perdemos", "perdéis",   "pierden"]),
        "subjunctive": _t(["pierda",  "pierdas",  "pierda",  "perdamos", "perdáis",   "pierdan"]),
        "imperative":  _i(["pierde",  "pierda",   "perdamos","perded",   "pierdan"]),
    },
    "mentir": {
        "present":     _t(["miento",  "mientes",  "miente",  "mentimos", "mentís",    "mienten"]),
        "preterite":   _t(["mentí",   "mentiste", "mintió",  "mentimos", "mentisteis","mintieron"]),
        "subjunctive": _t(["mienta",  "mientas",  "mienta",  "mintamos", "mintáis",   "mientan"]),
        "imperative":  _i(["miente",  "mienta",   "mintamos","mentid",   "mientan"]),
    },
    "preferir": {
        "present":     _t(["prefiero","prefieres","prefiere","preferimos","preferís", "prefieren"]),
        "preterite":   _t(["preferí", "preferiste","prefirió","preferimos","preferisteis","prefirieron"]),
        "subjunctive": _t(["prefiera","prefieras","prefiera","prefiramos","prefiráis","prefieran"]),
        "imperative":  _i(["prefiere","prefiera","prefiramos","preferid","prefieran"]),
    },
    "jugar": {
        "present":     _t(["juego",   "juegas",   "juega",   "jugamos",  "jugáis",    "juegan"]),
        "preterite":   _t(["jugué",   "jugaste",  "jugó",    "jugamos",  "jugasteis", "jugaron"]),
        "subjunctive": _t(["juegue",  "juegues",  "juegue",  "juguemos", "juguéis",   "jueguen"]),
        "imperative":  _i(["juega",   "juegue",   "juguemos","jugad",    "jueguen"]),
    },
    "conducir": {
        "present":     _t(["conduzco","conduces","conduce","conducimos","conducís","conducen"]),
        "preterite":   _t(["conduje","condujiste","condujo","condujimos","condujisteis","condujeron"]),
        "subjunctive": _t(["conduzca","conduzcas","conduzca","conduzcamos","conduzcáis","conduzcan"]),
        "imperative":  _i(["conduce","conduzca","conduzcamos","conducid","conduzcan"]),
    },
    "producir": {
        "present":     _t(["produzco","produces","produce","producimos","producís","producen"]),
        "preterite":   _t(["produje","produjiste","produjo","produjimos","produjisteis","produjeron"]),
        "subjunctive": _t(["produzca","produzcas","produzca","produzcamos","produzcáis","produzcan"]),
        "imperative":  _i(["produce","produzca","produzcamos","producid","produzcan"]),
    },
    "reducir": {
        "present":     _t(["reduzco","reduces","reduce","reducimos","reducís","reducen"]),
        "preterite":   _t(["reduje","redujiste","redujo","redujimos","redujisteis","redujeron"]),
        "subjunctive": _t(["reduzca","reduzcas","reduzca","reduzcamos","reduzcáis","reduzcan"]),
        "imperative":  _i(["reduce","reduzca","reduzcamos","reducid","reduzcan"]),
    },
    "traducir": {
        "present":     _t(["traduzco","traduces","traduce","traducimos","traducís","traducen"]),
        "preterite":   _t(["traduje","tradujiste","tradujo","tradujimos","tradujisteis","tradujeron"]),
        "subjunctive": _t(["traduzca","traduzcas","traduzca","traduzcamos","traduzcáis","traduzcan"]),
        "imperative":  _i(["traduce","traduzca","traduzcamos","traducid","traduzcan"]),
    },
    "escoger": {
        "present":     _t(["escojo",  "escoges",  "escoge",  "escogemos","escogéis",  "escogen"]),
        "subjunctive": _t(["escoja",  "escojas",  "escoja",  "escojamos","escojáis",  "escojan"]),
        "imperative":  _i(["escoge",  "escoja",   "escojamos","escoged", "escojan"]),
    },
    "proteger": {
        "present":     _t(["protejo", "proteges", "protege", "protegemos","protegéis","protegen"]),
        "subjunctive": _t(["proteja", "protejas", "proteja", "protejamos","protejáis","protejan"]),
        "imperative":  _i(["protege", "proteja",  "protejamos","proteged","protejan"]),
    },
    "corregir": {
        "present":     _t(["corrijo", "corriges", "corrige", "corregimos","corregís", "corrigen"]),
        "preterite":   _t(["corregí","corregiste","corrigió","corregimos","corregisteis","corrigieron"]),
        "subjunctive": _t(["corrija", "corrijas", "corrija", "corrijamos","corrijáis","corrijan"]),
        "imperative":  _i(["corrige", "corrija",  "corrijamos","corregid","corrijan"]),
    },
    "ofrecer": {
        "present":     _t(["ofrezco", "ofreces",  "ofrece",  "ofrecemos","ofrecéis",  "ofrecen"]),
        "subjunctive": _t(["ofrezca", "ofrezcas", "ofrezca", "ofrezcamos","ofrezcáis","ofrezcan"]),
        "imperative":  _i(["ofrece",  "ofrezca",  "ofrezcamos","ofreced","ofrezcan"]),
    },
    "parecer": {
        "present":     _t(["parezco", "pareces",  "parece",  "parecemos","parecéis",  "parecen"]),
        "subjunctive": _t(["parezca", "parezcas", "parezca", "parezcamos","parezcáis","parezcan"]),
        "imperative":  _i(["parece",  "parezca",  "parezcamos","pareced","parezcan"]),
    },
    # haber has no real imperative; conjugate() falls back for that tense.
    "haber": {
        "present":     _t(["he",      "has",      "ha",      "hemos",     "habéis",    "han"]),
        "preterite":   _t(["hube",    "hubiste",  "hubo",    "hubimos",   "hubisteis", "hubieron"]),
        "future":      _t(["habré",   "habrás",   "habrá",   "habremos",  "habréis",   "habrán"]),
        "conditional": _t(["habría",  "habrías",  "habría",  "habríamos", "habríais",  "habrían"]),
        "subjunctive": _t(["haya",    "hayas",    "haya",    "hayamos",   "hayáis",    "hayan"]),
    },
    "resolver": {
        "present":     _t(["resuelvo","resuelves","resuelve","resolvemos","resolvéis","resuelven"]),
        "subjunctive": _t(["resuelva","resuelvas","resuelva","resolvamos","resolváis","resuelvan"]),
        "imperative":  _i(["resuelve","resuelva","resolvamos","resolved","resuelvan"]),
    },
    "leer": {
        "preterite":   _t(["leí",     "leíste",   "leyó",    "leímos",    "leísteis",  "leyeron"]),
    },
    "seguir": {
        "present":     _t(["sigo",    "sigues",   "sigue",   "seguimos",  "seguís",    "siguen"]),
        "preterite":   _t(["seguí",   "seguiste", "siguió",  "seguimos",  "seguisteis","siguieron"]),
        "subjunctive": _t(["siga",    "sigas",    "siga",    "sigamos",   "sigáis",    "sigan"]),
        "imperative":  _i(["sigue",   "siga",     "sigamos", "seguid",    "sigan"]),
    },
    "incluir": {
        "present":     _t(["incluyo", "incluyes", "incluye", "incluimos", "incluís",   "incluyen"]),
        "preterite":   _t(["incluí",  "incluiste","incluyó", "incluimos", "incluisteis","incluyeron"]),
        "subjunctive": _t(["incluya", "incluyas", "incluya", "incluyamos","incluyáis", "incluyan"]),
        "imperative":  _i(["incluye", "incluya",  "incluyamos","incluid", "incluyan"]),
    },
    "sentir": {
        "present":     _t(["siento",  "sientes",  "siente",  "sentimos",  "sentís",    "sienten"]),
        "preterite":   _t(["sentí",   "sentiste", "sintió",  "sentimos",  "sentisteis","sintieron"]),
        "subjunctive": _t(["sienta",  "sientas",  "sienta",  "sintamos",  "sintáis",   "sientan"]),
        "imperative":  _i(["siente",  "sienta",   "sintamos","sentid",    "sientan"]),
    },
    "buscar": {
        "preterite":   _t(["busqué",  "buscaste", "buscó",   "buscamos",  "buscasteis","buscaron"]),
        "subjunctive": _t(["busque",  "busques",  "busque",  "busquemos", "busquéis",  "busquen"]),
        "imperative":  _i(["busca",   "busque",   "busquemos","buscad",   "busquen"]),
    },
    "caber": {
        "present":     _t(["quepo",   "cabes",    "cabe",    "cabemos",   "cabéis",    "caben"]),
        "preterite":   _t(["cupe",    "cupiste",  "cupo",    "cupimos",   "cupisteis", "cupieron"]),
        "future":      _t(["cabré",   "cabrás",   "cabrá",   "cabremos",  "cabréis",   "cabrán"]),
        "conditional": _t(["cabría",  "cabrías",  "cabría",  "cabríamos", "cabríais",  "cabrían"]),
        "subjunctive": _t(["quepa",   "quepas",   "quepa",   "quepamos",  "quepáis",   "quepan"]),
        "imperative":  _i(["cabe",    "quepa",    "quepamos","cabed",     "quepan"]),
    },
    "andar": {
        "preterite":   _t(["anduve",  "anduviste","anduvo",  "anduvimos", "anduvisteis","anduvieron"]),
    },
    # caer: preterite (cayó, caíste) comes from the -aer spelling rule.
    "caer": {
        "present":     _t(["caigo",   "caes",     "cae",     "caemos",    "caéis",     "caen"]),
        "subjunctive": _t(["caiga",   "caigas",   "caiga",   "caigamos",  "caigáis",   "caigan"]),
        "imperative":  _i(["cae",     "caiga",    "caigamos","caed",      "caigan"]),
    },
    "esquiar": {
        "present":     _t(["esquío",  "esquías",  "esquía",  "esquiamos", "esquiáis",  "esquían"]),
        "subjunctive": _t(["esquíe",  "esquíes",  "esquíe",  "esquiemos", "esquiéis",  "esquíen"]),
        "imperative":  _i(["esquía",  "esquíe",   "esquiemos","esquiad",  "esquíen"]),
    },
    # oír ends in -ír, so every tense is listed.
    "oír": {
        "present":     _t(["oigo",    "oyes",     "oye",     "oímos",     "oís",       "oyen"]),
        "preterite":   _t(["oí",      "oíste",    "oyó",     "oímos",     "oísteis",   "oyeron"]),
        "imperfect":   _t(["oía",     "oías",     "oía",     "oíamos",    "oíais",     "oían"]),
        "future":      _t(["oiré",    "oirás",    "oirá",    "oiremos",   "oiréis",    "oirán"]),
        "conditional": _t(["oiría",   "oirías",   "oiría",   "oiríamos",  "oiríais",   "oirían"]),
        "subjunctive": _t(["oiga",    "oigas",    "oiga",    "oigamos",   "oigáis",    "oigan"]),
        "imperative":  _i(["oye",     "oiga",     "oigamos", "oíd",       "oigan"]),
    },
    "llegar": {
        "preterite":   _t(["llegué",  "llegaste", "llegó",   "llegamos",  "llegasteis","llegaron"]),
        "subjunctive": _t(["llegue",  "llegues",  "llegue",  "lleguemos", "lleguéis",  "lleguen"]),
        "imperative":  _i(["llega",   "llegue",   "lleguemos","llegad",   "lleguen"]),
    },
}


# ── Public API ────────────────────────────────────────────────────────────────

TENSES = ["present", "preterite", "imperfect", "future", "conditional", "subjunctive", "imperative"]
SUBJECTS = {
    "present":     ["yo", "tú", "él", "nosotros", "vosotros", "ellos"],
    "preterite":   ["yo", "tú", "él", "nosotros", "vosotros", "ellos"],
    "imperfect":   ["yo", "tú", "él", "nosotros", "vosotros", "ellos"],
    "future":      ["yo", "tú", "él", "nosotros", "vosotros", "ellos"],
    "conditional": ["yo", "tú", "él", "nosotros", "vosotros", "ellos"],
    "subjunctive": ["yo", "tú", "él", "nosotros", "vosotros", "ellos"],
    "imperative":  ["tú", "usted", "nosotros", "vosotros", "ustedes"],
}


def conjugate(infinitive: str, tense: str, subject: str) -> str:
    """Return the conjugated form of infinitive for the given tense and subject."""
    if tense not in TENSES:
        raise ValueError(f"Unknown tense {tense!r}. Expected one of {TENSES}")
    if subject not in SUBJECTS[tense]:
        raise ValueError(f"Unknown subject {subject!r} for tense {tense!r}. Expected one of {SUBJECTS[tense]}")
    irreg = IRREGULAR_VERBS.get(infinitive, {})
    if tense in irreg:
        return irreg[tense][subject]
    return _conjugate_regular(infinitive, tense, subject)


def get_all_conjugations(infinitive: str) -> dict:
    """Return all conjugations for infinitive as {tense: {subject: form}}."""
    return {
        tense: {subj: conjugate(infinitive, tense, subj) for subj in SUBJECTS[tense]}
        for tense in TENSES
    }
