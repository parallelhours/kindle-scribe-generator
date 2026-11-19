"""
Sentence frames for verb clues — the textbook drill format:

    Ayer yo ___ (comprar) pan.

The time marker cues the tense (the same cues as the Cuaderno's "Which tense
do I use?" chart), the infinitive in parentheses names the verb, and a short
complement makes it a real sentence. Latin American Spanish: no vosotros.

conjugation_clue(verb, tense, subject) -> str | None
    None means "don't use this form" (no sensible sentence exists for it).
"""

# Tense marker frames. {s} is the subject slot.
TENSE_FRAME = {
    "present":     "Todos los días {s} ___",
    "preterite":   "Ayer {s} ___",
    "imperfect":   "Antes {s} siempre ___",
    "future":      "Mañana {s} ___",
    "conditional": "Con más tiempo, {s} ___",
    "subjunctive": "Ojalá que {s} ___",
}
# Clitic subjects (me gusta…): the present needs no marker, and in the
# imperfect "siempre" must come before the pronoun.
_CLITIC_FRAME = {"present": "{s} ___", "imperfect": "Antes siempre {s} ___"}

SUBJECT_WORD = {"yo": "yo", "tú": "tú", "él": "él", "nosotros": "nosotros", "ellos": "ellos"}

# Commands: tú / usted / ustedes are cued by who is addressed; nosotros by "let's".
IMPERATIVE_FRAME = {
    "tú":       ("Ana", "tú"),
    "usted":    ("señor", "usted"),
    "ustedes":  ("chicos", "ustedes"),
    "nosotros": (None, "let's"),
}

# Complement after "(infinitive)". Must read naturally with every person and
# tense, so no adjectives (they would need gender/number agreement).
COMPLEMENT = {
    "abrir": "la ventana", "acabar": "de comer", "acampar": "en la playa",
    "afirmar": "lo mismo", "almorzar": "temprano", "andar": "en bicicleta",
    "animar": "al equipo", "aprender": "algo nuevo", "avanzar": "rápido",
    "ayudar": "a Pedro", "bailar": "salsa", "bajar": "las escaleras",
    "barrer": "el piso", "beber": "agua", "bucear": "en el Caribe",
    "buscar": "las llaves", "caber": "en el carro", "cambiar": "de opinión",
    "caminar": "al parque", "cantar": "una canción", "cenar": "tarde",
    "cerrar": "la puerta", "charlar": "con amigos", "chatear": "en línea",
    "cocinar": "arroz", "comentar": "la noticia", "comenzar": "la clase",
    "comer": "fruta", "comprar": "pan", "comprender": "la pregunta",
    "conducir": "al trabajo", "conocer": "la ciudad", "conquistar": "el mundo",
    "considerar": "la oferta", "construir": "una casa", "contratar": "a un abogado",
    "contribuir": "con dinero", "corregir": "el examen", "correr": "en el parque",
    "crear": "un plan", "creer": "la historia", "criticar": "la película",
    "cubrir": "la comida", "dar": "un regalo", "deber": "estudiar más",
    "decidir": "rápido", "decir": "la verdad", "dedicar": "tiempo a la familia",
    "depositar": "el cheque", "desayunar": "huevos", "descargar": "la aplicación",
    "descubrir": "un secreto", "despedir": "al empleado", "destruir": "el puente",
    "devolver": "el libro", "dormir": "ocho horas", "empezar": "el trabajo",
    "emplear": "a dos personas", "encontrar": "un buen restaurante",
    "enseñar": "español", "entender": "la pregunta", "entrar": "a la casa",
    "entrenar": "para el maratón", "entrevistar": "al candidato",
    "escoger": "un color", "escribir": "una carta", "escuchar": "música",
    "esperar": "el autobús", "esquiar": "en las montañas", "estar": "en casa",
    "estudiar": "español", "expandir": "el negocio", "explicar": "la lección",
    "explorar": "la ciudad", "expresar": "una opinión", "formar": "un equipo",
    "ganar": "el partido", "hablar": "con Pedro", "hacer": "la tarea",
    "huir": "del peligro", "incluir": "a todos", "incorporar": "ideas nuevas",
    "indicar": "el camino", "influir": "en la decisión", "ir": "al mercado",
    "jugar": "al fútbol", "leer": "el periódico", "levantar": "la mano",
    "limpiar": "la cocina", "llamar": "a Pedro", "llegar": "temprano",
    "llevar": "una chaqueta", "manejar": "al trabajo", "mejorar": "la pronunciación",
    "mencionar": "el problema", "mentir": "un poco", "mirar": "la televisión",
    "montar": "a caballo", "mostrar": "las fotos", "nadar": "en el mar",
    "necesitar": "ayuda", "ofrecer": "ayuda", "oír": "un ruido",
    "ordenar": "una pizza", "organizar": "la fiesta", "pasar": "la tarde en casa",
    "pasear": "por el parque", "pedir": "la cuenta", "pensar": "en el viaje",
    "perder": "las llaves", "permitir": "visitas", "planchar": "la camisa",
    "poder": "venir", "poner": "la mesa", "preferir": "el té",
    "preparar": "la cena", "producir": "café", "pronunciar": "la palabra",
    "proteger": "a los niños", "querer": "ir a la playa", "recibir": "un regalo",
    "recoger": "a los niños", "recordar": "el número", "reducir": "los gastos",
    "repasar": "el vocabulario", "repetir": "la pregunta", "resolver": "el problema",
    "responder": "el correo", "retirar": "dinero", "romper": "el vaso",
    "saber": "la respuesta", "salir": "con amigos", "saludar": "a la profesora",
    "seguir": "las instrucciones", "sentir": "frío",
    "servir": "la sopa", "subir": "las escaleras", "tener": "cuidado",
    "terminar": "la tarea", "tocar": "la guitarra", "tomar": "café",
    "tostar": "el pan", "trabajar": "en casa", "traducir": "el texto",
    "traer": "el postre", "vender": "el carro", "venir": "a la fiesta",
    "ver": "una película", "viajar": "a México", "visitar": "el museo",
    "vivir": "una aventura", "volar": "a Cartagena", "volver": "a casa",
}

# Verbs whose subject is a thing (or a clitic like "me" for gustar-type verbs):
# subject → (words in the subject slot, complement). Only these persons are used.
THIRD_PERSON = {
    "gustar":    {"él": ("me", "el café"),        "ellos": ("me", "los perros")},
    "encantar":  {"él": ("me", "la playa"),       "ellos": ("me", "los tacos")},
    "interesar": {"él": ("me", "la historia"),    "ellos": ("me", "los idiomas")},
    "molestar":  {"él": ("me", "el ruido"),       "ellos": ("me", "los mosquitos")},
    "costar":    {"él": ("el libro", "diez dólares"),  "ellos": ("los libros", "diez dólares")},
    "funcionar": {"él": ("el carro", "bien"),          "ellos": ("los carros", "bien")},
    "resultar":  {"él": ("el examen", "fácil"),        "ellos": ("los exámenes", "fáciles")},
    "caer":      {"él": ("la lluvia", "fuerte"),       "ellos": ("las hojas", "del árbol")},
    "llover":    {"él": ("", "mucho")},
    "nevar":     {"él": ("", "en las montañas")},
}
_CLITIC = {"gustar", "encantar", "interesar", "molestar"}

# Tenses with no natural sentence for a verb.
SKIP_TENSES = {
    "encantar": {"conditional"}, "interesar": {"conditional"},
    "molestar": {"conditional"},
    "costar": {"conditional"}, "funcionar": {"conditional"},
    "resultar": {"conditional"}, "caer": {"conditional"},
    "llover": {"conditional"}, "nevar": {"conditional"},
    # "Con más tiempo, yo perdería las llaves" makes no sense.
    "perder": {"conditional"}, "romper": {"conditional"}, "sentir": {"conditional"},
    "caber": {"conditional"}, "necesitar": {"conditional"}, "creer": {"conditional"},
    "mentir": {"conditional"},
}

# Whole-sentence overrides: {verb: {tense: template or {subject: template}}}.
# A verb listed here uses ONLY the tenses given.
SPECIAL = {
    # ser + an adjective needs agreement, so most tenses use thing subjects.
    "ser": {
        "present":     "{s} ___ (ser) de Colombia.",
        "preterite":   {"él": "Ayer la fiesta ___ (ser) divertida.",
                        "ellos": "Ayer las clases ___ (ser) aburridas."},
        "imperfect":   {"él": "Antes la casa ___ (ser) azul.",
                        "ellos": "Antes las casas ___ (ser) azules."},
        "future":      {"él": "Mañana ___ (ser) lunes."},
        "subjunctive": {"él": "Ojalá que el examen ___ (ser) fácil.",
                        "ellos": "Ojalá que los exámenes ___ (ser) fáciles."},
        "imperative":  {"tú": "¡___ (ser) paciente, Ana! (tú)",
                        "usted": "¡___ (ser) paciente, señor! (usted)",
                        "ustedes": "¡___ (ser) pacientes, chicos! (ustedes)",
                        "nosotros": "¡___ (ser) pacientes! (let's)"},
    },
    # haber as the helper verb: present perfect vs. past perfect, as in the Cuaderno.
    "haber": {
        "present":     "Hoy {s} ya ___ (haber) comido.",
        "imperfect":   "Cuando llegaste, {s} ya ___ (haber) comido.",
        "future":      "A las tres, {s} ya ___ (haber) comido.",
        "subjunctive": "Ojalá que {s} ya ___ (haber) comido.",
    },
    "parecer": {
        "present":   {"él": "Me ___ (parecer) una buena idea.",
                      "ellos": "Me ___ (parecer) unas buenas ideas."},
        "preterite": {"él": "Ayer la película me ___ (parecer) larga.",
                      "ellos": "Ayer las clases me ___ (parecer) largas."},
    },
    "ocurrir": {
        "present":   {"él": "Esto ___ (ocurrir) a menudo.",
                      "ellos": "Estas cosas ___ (ocurrir) a menudo."},
        "preterite": {"él": "Ayer ___ (ocurrir) un accidente.",
                      "ellos": "Ayer ___ (ocurrir) dos accidentes."},
    },
    "existir": {
        "present":   {"él": "Ese problema todavía ___ (existir).",
                      "ellos": "Esos problemas todavía ___ (existir)."},
        "imperfect": {"él": "Antes ese problema no ___ (existir).",
                      "ellos": "Antes esos problemas no ___ (existir)."},
    },
    "morir": {
        "preterite": {"él": "Mi abuelo ___ (morir) en 1990.",
                      "ellos": "Mis abuelos ___ (morir) en 1990."},
    },
}
# gustar's conditional is the classic polite request.
_GUSTAR_CONDITIONAL = {"él": "Me ___ (gustar) un café, por favor.",
                       "ellos": "Me ___ (gustar) dos cafés, por favor."}

# Stative verbs: "Todos los días yo sé…" sounds wrong, so the present has no marker.
PRESENT_NO_MARKER = {"saber", "conocer", "entender", "comprender", "caber", "recordar", "creer"}

# Verbs with no natural command form.
NO_COMMAND = {
    "poder", "caber", "deber", "haber", "querer", "saber", "estar", "necesitar",
    "perder", "mentir", "sentir", "morir", "parecer", "ocurrir", "existir",
} | set(THIRD_PERSON)


def _tidy(text: str) -> str:
    text = " ".join(text.split())
    return text.replace(" ,", ",").replace(" .", ".").replace(" !", "!")


def _end(text: str) -> str:
    text = _tidy(text)
    return text if text[-1] in ".!?" else text + "."


def conjugation_clue(verb: str, tense: str, subject: str):
    """Return the clue sentence for verb/tense/subject, or None to skip the form."""
    if subject == "vosotros":
        return None

    if verb in SPECIAL:
        tpl = SPECIAL[verb].get(tense)
        if tpl is None:
            return None
        if isinstance(tpl, dict):
            return tpl.get(subject)
        clue = _tidy(tpl.format(s=SUBJECT_WORD.get(subject, subject)))
        return clue[0].upper() + clue[1:]

    if tense == "imperative":
        if verb in NO_COMMAND or subject not in IMPERATIVE_FRAME:
            return None
        who, tag = IMPERATIVE_FRAME[subject]
        comp = COMPLEMENT.get(verb, "")
        body = f"¡___ ({verb}) {comp}"
        body = _tidy(body + (f", {who}!" if who else "!"))
        return f"{body} ({tag})"

    if tense in SKIP_TENSES.get(verb, ()):
        return None

    if verb in THIRD_PERSON:
        slot = THIRD_PERSON[verb].get(subject)
        if slot is None:
            return None
        if verb == "gustar" and tense == "conditional":
            return _GUSTAR_CONDITIONAL[subject]
        subj, comp = slot
        frame = TENSE_FRAME[tense]
        if verb in _CLITIC:
            frame = _CLITIC_FRAME.get(tense, frame)
        elif subj and tense == "present":
            frame = "{s} ___"   # "El libro cuesta…" needs no time marker
        clue = _end(f"{frame.format(s=subj)} ({verb}) {comp}")
        return clue[0].upper() + clue[1:]

    frame = TENSE_FRAME[tense]
    if tense == "present" and verb in PRESENT_NO_MARKER:
        frame = "{s} ___"
    comp = COMPLEMENT.get(verb, "")
    clue = _end(f"{frame.format(s=SUBJECT_WORD[subject])} ({verb}) {comp}")
    return clue[0].upper() + clue[1:]
