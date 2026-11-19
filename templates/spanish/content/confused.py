# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Commonly confused words (Phrases & Grammar, Part C).

TOPICS: topic dicts (see grammar.py), each followed by a practice page.
CONFUSED_XREFS: lines on the section contents page that link to the comparison
topics in the Verbs section. In a notebook without Verbs they print as plain text.
"""
from templates.spanish.content.grammar import _b, _cmp, _ex, _h, _sp, _spaced, _t, _table

# --------------------------------------------------------------------------
_SER_ESTAR = {
    "id": "ser-estar",
    "title": "Ser vs. estar",
    "pages": [
        [
            _h("ser: what something is / estar: how or where it is"),
            _cmp("ser", "estar", [
                ["Identity, job: **Soy** profesora. ~I'm a teacher.~",
                 "Location of people and things: **Estoy** en la oficina. ~I'm at the "
                 "office.~"],
                ["Origin, nationality: **Es** de Colombia. ~He's from Colombia.~",
                 "Feelings, physical states: **Está** cansado. ~He's tired.~"],
                ["Description, personality: La casa **es** grande. Ana **es** simpática. "
                 "~The house is big. Ana is nice.~",
                 "Condition, result of a change: La tienda **está** cerrada. ~The store is "
                 "closed.~"],
                ["Time, dates: **Son** las tres. Hoy **es** lunes. ~It's three o'clock. "
                 "Today is Monday.~",
                 "Actions in progress (-ndo): **Estoy** trabajando. ~I'm working.~"],
                ["Material, owner: **Es** de madera. **Es** mío. ~It's made of wood. It's "
                 "mine.~",
                 "How something tastes, looks or seems now: La sopa **está** rica. ~The soup "
                 "is delicious.~"],
                ["Where an **event** takes place: La fiesta **es** en mi casa. ~The party is "
                 "at my house.~",
                 "Set phrases: **estar** de acuerdo ~to agree~, de vacaciones ~on vacation~, "
                 "de pie ~standing~"],
            ]),
            _sp(),
            _h("Quick test"),
            _b("Is it about **what** something is, or what it's **like** in general? Use "
               "**ser**.",
               "Is it about **how** it is right now, or **where** it is? Use **estar**.",
               "Two traps: events take **ser** for their location (El concierto **es** en el "
               "estadio), and death takes **estar** (**Está** muerto)."),
            _t("\"Permanent vs. temporary\" is only a rough guide: you say **es** joven ~he's "
               "young~ (it will change) and **está** muerto ~he's dead~ (it won't)."),
            _sp(2),
            _ex("Mi papá es médico, pero hoy está de vacaciones.",
                "My dad is a doctor, but today he's on vacation."),
            _ex("El concierto es en el estadio, que está cerca de mi casa.",
                "The concert is at the stadium, which is near my house."),
        ],
        [
            _h("Adjectives that change meaning"),
            _table(["Adjective", "with ser", "with estar"], [
                ["aburrido", "**es** aburrido ~is boring~", "**está** aburrido ~is bored~"],
                ["listo", "**es** listo ~is clever, smart~", "**está** listo ~is ready~"],
                ["rico", "**es** rico ~is rich; (food in general) is tasty~",
                 "**está** rico ~(this food, now) tastes delicious~"],
                ["malo", "**es** malo ~is bad (a bad person or thing)~",
                 "**está** malo ~is sick (informal); has gone bad~"],
                ["verde", "**es** verde ~is green (color)~",
                 "**está** verde ~is unripe; is inexperienced~"],
                ["seguro", "**es** seguro ~is safe~", "**está** seguro ~is sure~"],
                ["vivo", "**es** vivo ~is sharp, quick-witted; in Colombia often 'sly, a smart operator'~", "**está** vivo ~is alive~"],
                ["callado", "**es** callado ~is a quiet person~",
                 "**está** callado ~is being quiet~"],
                ["nervioso", "**es** nervioso ~is a nervous person~",
                 "**está** nervioso ~is nervous (right now)~"],
            ], [0.18, 0.41, 0.41]),
            _sp(),
            _t("With food, **estar** describes this dish right now: La sopa **está** rica. "
               "**ser** gives a general opinion: Las arepas **son** ricas."),
            _t("Careful with people: **es** bueno ~is a good person~; **está** bueno is slang "
               "for ~is attractive~ (with food it just means ~tastes good~)."),
            _sp(2),
            _ex("La película es aburrida y yo estoy aburrido.",
                "The movie is boring, and I'm bored."),
            _ex("¿Ya estás lista? Vamos a llegar tarde.",
                "Are you ready yet? We're going to be late."),
        ],
    ],
}

# --------------------------------------------------------------------------
_POR_PARA = {
    "id": "por-para",
    "title": "Por vs. para",
    "pages": [
        [
            _h("The big picture"),
            _t("Rough guide: **para** points ahead, to a goal, a person who receives "
               "something, a destination or a deadline. **por** points back to a cause, or "
               "describes a route, an exchange, a means or a length of time."),
            _cmp("para", "por", [
                ["Purpose (in order to) + infinitive: Estudio **para** aprender. ~I study (in "
                 "order) to learn.~",
                 "Cause, reason: Lo hice **por** ti. ~I did it because of you (for your "
                 "sake).~"],
                ["Who receives it: Este regalo es **para** ti. ~This gift is for you.~",
                 "Exchange, price: Pagué 50.000 pesos **por** la camisa. ~I paid 50,000 pesos "
                 "for the shirt.~"],
                ["Destination: Salgo **para** Cali mañana. ~I'm leaving for Cali tomorrow.~",
                 "Through, along, around: Caminamos **por** el parque. ~We walked through "
                 "the park.~"],
                ["Deadline: La tarea es **para** el viernes. ~The homework is due Friday.~",
                 "Length of time: Viví allí **por** dos años. ~I lived there for two years.~ "
                 "(often left out: Viví allí dos años.)"],
                ["Opinion: **Para** mí, es fácil. ~For me (in my opinion), it's easy.~",
                 "Means: Hablamos **por** teléfono. ~We talked on the phone.~"],
                ["Employer: Trabajo **para** una empresa. ~I work for a company.~",
                 "In place of: Hoy trabajo **por** mi compañero. ~Today I'm working for (in "
                 "place of) my coworker.~"],
                ["Compared with what's expected: **Para** ser extranjero, habla muy bien. "
                 "~For a foreigner, he speaks very well.~",
                 "Per, rate: dos veces **por** semana ~twice a week~; 80 kilómetros **por** "
                 "hora ~80 kilometers per hour~"],
            ]),
            _sp(),
            _t("Thank you for is always **gracias por**, because the thing you're thankful "
               "for is the cause: Gracias **por** la ayuda. ~Thanks for the help.~"),
            _sp(2),
            _ex("Salgo para Medellín el lunes por la mañana.",
                "I'm leaving for Medellín on Monday morning."),
            _ex("Gracias por todo; esto es para ti.", "Thanks for everything; this is for you."),
        ],
        [
            _h("Same English \"for\", different meaning"),
            _cmp("para", "por", [
                ["Lo compré **para** mi mamá. ~I bought it for my mom (to give her).~",
                 "Lo compré **por** mi mamá. ~I bought it on my mom's behalf (or because of "
                 "her).~"],
                ["Trabajo **para** ganar dinero. ~I work to earn money (goal).~",
                 "Trabajo **por** necesidad. ~I work out of necessity (cause).~"],
                ["Vamos **para** el centro. ~We're heading downtown (destination).~",
                 "Pasamos **por** el centro. ~We went through downtown (route).~"],
            ]),
            _sp(),
            _h("Fixed expressions"),
            _table(["with por", "", "with para", ""], [
                ["por favor", "~please~", "para siempre", "~forever~"],
                ["por eso", "~that's why~", "¿para qué?", "~what for?~"],
                ["por fin", "~finally~", "para nada", "~not at all~"],
                ["por supuesto", "~of course~", "para llevar", "~to go (food)~"],
                ["por ejemplo", "~for example~", "para entonces", "~by then~"],
                ["por lo menos", "~at least~", "", ""],
                ["por si acaso", "~just in case~", "", ""],
                ["¿por qué?", "~why?~", "", ""],
            ], [0.22, 0.28, 0.22, 0.28]),
            _sp(),
            _t("**¿Por qué?** asks for the cause (why?); **¿para qué?** asks for the purpose "
               "(what for?). The answer to ¿por qué? is **porque** (one word, no accent)."),
            _ex("¿Para qué sirve esto? —Para abrir botellas.",
                "What's this for? —For opening bottles."),
            _ex("Llévate un paraguas por si acaso.", "Take an umbrella just in case."),
        ],
    ],
}

# --------------------------------------------------------------------------
_SABER_CONOCER = {
    "id": "saber-conocer",
    "title": "Saber vs. conocer",
    "pages": [[
        _h("Two verbs for to know"),
        _cmp("saber: facts, information, skills", "conocer: people, places, familiarity", [
            ["Facts: **Sé** su número. ~I know her number.~",
             "People: **Conozco** a tu hermano. ~I know your brother.~"],
            ["+ infinitive = know how to: **Sé** nadar. ~I know how to swim.~",
             "Places: **Conozco** Cartagena. ~I know Cartagena (I've been there).~"],
            ["+ que, si, or a question word: No **sé** dónde está. ~I don't know where it "
             "is.~",
             "Things you've come across: **Conozco** esta canción. ~I know this song.~"],
        ]),
        _sp(),
        _b("Both have an irregular yo form: **sé**, sabes, sabe ... / **conozco**, conoces, "
           "conoce ...",
           "Know how to is just **saber** + infinitive; you don't need cómo: **Sé** manejar. "
           "~I know how to drive.~",
           "**conocer** a person takes the personal **a**: Conozco **a** Luis."),
        _h("In the preterite, the meaning shifts"),
        _t("**supe** = I found out; **conocí** = I met (for the first time). The imperfect "
           "keeps the normal meaning: **sabía** = I knew; **conocía** = I knew (was "
           "acquainted with)."),
        _sp(2),
        _ex("¿Sabes si hay una farmacia cerca?", "Do you know if there's a pharmacy nearby?"),
        _ex("No conozco bien la ciudad.", "I don't know the city well."),
        _ex("Supe la noticia ayer.", "I found out the news yesterday."),
        _ex("Conocí a mi esposa en Bogotá.", "I met my wife in Bogotá."),
    ]],
}

# --------------------------------------------------------------------------
_PEDIR_PREGUNTAR = {
    "id": "pedir-preguntar",
    "title": "Pedir vs. preguntar",
    "pages": [[
        _h("Two verbs for to ask"),
        _cmp("pedir: ask for, request, order", "preguntar: ask a question", [
            ["Ask for something: **Pedí** la cuenta. ~I asked for the check.~",
             "Ask for information: **Pregunté** la hora. ~I asked what time it was.~"],
            ["Order food: Voy a **pedir** una limonada. ~I'm going to order a lemonade.~",
             "+ si or a question word: Le **pregunté** si venía. ~I asked him if he was "
             "coming.~"],
            ["Ask someone to do something: **pedir que** + subjunctive: Le **pedí** que me "
             "ayudara. ~I asked him to help me.~",
             "Ask about someone: **preguntar por**: Mi mamá **preguntó por** ti. ~My mom "
             "asked about you.~"],
        ]),
        _sp(),
        _b("**pedir** already includes for: **pedir** ayuda = ~to ask for help~ (not pedir "
           "por ayuda).",
           "**pedir** changes e to i: pido, pides, pide, pedimos, piden; preterite **pidió**, "
           "**pidieron**.",
           "To ask a question is also **hacer una pregunta**: ¿Puedo hacerte una pregunta? "
           "~Can I ask you a question?~"),
        _sp(2),
        _ex("¿Puedo pedirte un favor?", "Can I ask you a favor?"),
        _ex("Le pregunté dónde vivía.", "I asked her where she lived."),
        _ex("Te pido que llegues temprano.", "I'm asking you to arrive early."),
    ]],
}

# --------------------------------------------------------------------------
_LLEVAR_TRAER = {
    "id": "llevar-traer",
    "title": "Llevar vs. traer",
    "pages": [[
        _h("Think of where the speaker is"),
        _t("**traer** = to bring, toward here (where the speaker is). **llevar** = to take, "
           "away from here, to somewhere else."),
        _cmp("traer: bring (here)", "llevar: take (there)", [
            ["¿Me **traes** un vaso de agua? ~Can you bring me a glass of water?~",
             "**Llevo** a los niños al colegio. ~I take the kids to school.~"],
            ["**Trae** tu guitarra a la fiesta. ~Bring your guitar to the party.~ (the party "
             "is at my place)",
             "Voy a **llevar** vino a la fiesta. ~I'm going to take wine to the party.~ (the "
             "party is somewhere else)"],
        ]),
        _sp(),
        _t("Careful: English often says bring where Spanish says **llevar**. ~I'll bring "
           "dessert to your house~ = **Llevo** el postre a tu casa."),
        _h("Other common uses of llevar"),
        _b("Give someone a ride: ¿Me **llevas** al aeropuerto? ~Can you take me to the "
           "airport?~",
           "Wear: **Lleva** una camisa azul. ~He's wearing a blue shirt.~",
           "Time spent: **Llevo** dos años aquí. ~I've been here for two years.~",
           "Food to go: Es **para llevar**. ~It's to go.~"),
        _t("**traer** is irregular: **traigo** (I bring), **traje** (I brought)."),
        _sp(2),
        _ex("Mañana te traigo el libro.", "I'll bring you the book tomorrow."),
        _ex("Siempre llevo agua cuando voy a caminar.", "I always take water when I go walking."),
    ]],
}

# --------------------------------------------------------------------------
_TOCAR_JUGAR = {
    "id": "tocar-jugar",
    "title": "Tocar vs. jugar",
    "pages": [[
        _h("Two verbs for to play"),
        _cmp("tocar: instruments, music; touch", "jugar: games, sports; children playing", [
            ["Play an instrument: **Toco** la guitarra. ~I play the guitar.~",
             "Play a sport: **Juego** fútbol. ~I play soccer.~"],
            ["Play music (live): La banda **toca** salsa los sábados. ~The band plays salsa "
             "on Saturdays.~",
             "Play a game: **Jugamos** cartas. ~We play cards.~"],
            ["Touch: No **toques** eso. ~Don't touch that.~",
             "Children playing: Los niños **juegan** en el parque. ~The kids are playing in "
             "the park.~"],
        ]),
        _sp(),
        _b("Sports: Latin America mostly says **jugar fútbol**; Spain says **jugar al "
           "fútbol**. Both are correct.",
           "**jugar** changes u to ue: juego, juegas, juega, jugamos, juegan.",
           "To play a recording, use **poner**: Pon esa canción. ~Play that song.~"),
        _h("tocar: whose turn it is"),
        _t("**Me toca** (te toca, le toca ...) = it's my turn. In Colombia and much of Latin "
           "America it also means I have to, as a duty that falls to you: **Me toca** "
           "trabajar el sábado. ~I have to work on Saturday.~"),
        _sp(2),
        _ex("Mi hija toca el piano muy bien.", "My daughter plays the piano very well."),
        _ex("¿Jugamos un partido de tenis el sábado?",
            "Shall we play a game of tennis on Saturday?"),
        _ex("Ahora te toca a ti.", "Now it's your turn."),
    ]],
}

# --------------------------------------------------------------------------
_HAY_ESTA = {
    "id": "hay-esta",
    "title": "Hay vs. está / están",
    "pages": [[
        _h("Does it exist, or where is it?"),
        _cmp("hay: there is, there are", "está / están: is, are (located)", [
            ["Says that something **exists**. Used with un, una, a number, mucho, algún, "
             "or no article: **Hay** un banco cerca. ~There's a bank nearby.~",
             "Says **where** a specific thing is. Used with el, la, mi, este, or a name: "
             "El banco **está** en la esquina. ~The bank is on the corner.~"],
            ["**Hay** dos farmacias en esta calle. ~There are two pharmacies on this street.~",
             "Las farmacias **están** cerca del parque. ~The pharmacies are near the park.~"],
            ["¿**Hay** baño aquí? ~Is there a bathroom here?~",
             "¿Dónde **está** el baño? ~Where's the bathroom?~"],
        ]),
        _sp(),
        _h("hay has no plural"),
        _t("**hay** is the same for one or many: hay un libro, hay tres libros. The same goes "
           "for every tense of this haber: **había** muchas personas, **hubo** dos accidentes, "
           "**va a haber** problemas. (Habían muchas personas is often heard, but it is "
           "considered incorrect.)"),
        _t("**estar** agrees with its subject: el libro **está**, los libros **están**."),
        _t("Also: **hay que** + infinitive = one has to, you have to: **Hay que** pagar en "
           "efectivo. ~You have to pay in cash.~"),
        _sp(2),
        _ex("¿Hay un cajero automático por aquí?", "Is there an ATM around here?"),
        _ex("Mis llaves están en la mesa.", "My keys are on the table."),
        _ex("Había mucha gente en el concierto.", "There were a lot of people at the concert."),
    ]],
}

# --------------------------------------------------------------------------
_PERO_SINO = {
    "id": "pero-sino",
    "title": "Pero vs. sino",
    "pages": [[
        _h("Two words for but"),
        _cmp("pero: but (adds a contrast)", "sino: but rather, instead (corrects)", [
            ["Both parts are true: Es caro, **pero** es bueno. ~It's expensive, but it's "
             "good.~",
             "After a negative, replaces what was denied: No es caro, **sino** barato. "
             "~It isn't expensive, but (rather) cheap.~"],
            ["After a negative, if nothing is replaced: No es caro, **pero** no me gusta. "
             "~It isn't expensive, but I don't like it.~",
             "Before a conjugated verb, use **sino que**: No lo compré, **sino que** lo hice "
             "yo. ~I didn't buy it; I made it myself.~"],
        ]),
        _sp(),
        _b("Test: if the first part has **no** and you could say but rather or but instead, "
           "use **sino**. Otherwise use **pero**.",
           "**no solo ... sino también** = not only ... but also."),
        _sp(2),
        _ex("Quiero ir, pero no puedo.", "I want to go, but I can't."),
        _ex("No vivo en Bogotá, sino en Medellín.", "I don't live in Bogotá but in Medellín."),
        _ex("No solo canta, sino que también baila.", "She not only sings but also dances."),
    ]],
}

TOPICS = [_spaced(t) for t in (_SER_ESTAR, _POR_PARA, _SABER_CONOCER, _PEDIR_PREGUNTAR, _LLEVAR_TRAER,
          _TOCAR_JUGAR, _HAY_ESTA, _PERO_SINO)]

CONFUSED_XREFS = [
    {"text": "See also: Preterite vs. imperfect (Verbs)", "dest": "t-cmp-pret-imp"},
    {"text": "See also: Present perfect vs. past perfect (Verbs)", "dest": "t-cmp-perfects"},
    {"text": "See also: Indicative vs. subjunctive (Verbs)", "dest": "t-cmp-ind-subj"},
]
