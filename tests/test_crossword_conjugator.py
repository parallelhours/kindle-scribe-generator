# tests/test_crossword_conjugator.py
from templates.crossword.conjugator import conjugate, get_all_conjugations

# --- Regular -ar ---
def test_regular_ar_present():
    assert conjugate("hablar", "present", "yo") == "hablo"
    assert conjugate("hablar", "present", "tú") == "hablas"
    assert conjugate("hablar", "present", "él") == "habla"
    assert conjugate("hablar", "present", "nosotros") == "hablamos"
    assert conjugate("hablar", "present", "vosotros") == "habláis"
    assert conjugate("hablar", "present", "ellos") == "hablan"

def test_regular_ar_preterite():
    assert conjugate("hablar", "preterite", "yo") == "hablé"
    assert conjugate("hablar", "preterite", "tú") == "hablaste"
    assert conjugate("hablar", "preterite", "él") == "habló"
    assert conjugate("hablar", "preterite", "nosotros") == "hablamos"
    assert conjugate("hablar", "preterite", "vosotros") == "hablasteis"
    assert conjugate("hablar", "preterite", "ellos") == "hablaron"

def test_regular_ar_imperfect():
    assert conjugate("hablar", "imperfect", "yo") == "hablaba"
    assert conjugate("hablar", "imperfect", "nosotros") == "hablábamos"

def test_regular_ar_future():
    assert conjugate("hablar", "future", "yo") == "hablaré"
    assert conjugate("hablar", "future", "ellos") == "hablarán"

def test_regular_ar_conditional():
    assert conjugate("hablar", "conditional", "yo") == "hablaría"

def test_regular_ar_subjunctive():
    assert conjugate("hablar", "subjunctive", "yo") == "hable"
    assert conjugate("hablar", "subjunctive", "nosotros") == "hablemos"

def test_regular_ar_imperative():
    assert conjugate("hablar", "imperative", "tú") == "habla"
    assert conjugate("hablar", "imperative", "usted") == "hable"
    assert conjugate("hablar", "imperative", "vosotros") == "hablad"

# --- Regular -er ---
def test_regular_er_present():
    assert conjugate("comer", "present", "yo") == "como"
    assert conjugate("comer", "present", "tú") == "comes"
    assert conjugate("comer", "present", "nosotros") == "comemos"
    assert conjugate("comer", "present", "vosotros") == "coméis"

def test_regular_er_preterite():
    assert conjugate("comer", "preterite", "yo") == "comí"
    assert conjugate("comer", "preterite", "él") == "comió"
    assert conjugate("comer", "preterite", "nosotros") == "comimos"

def test_regular_er_imperfect():
    assert conjugate("comer", "imperfect", "yo") == "comía"
    assert conjugate("comer", "imperfect", "nosotros") == "comíamos"

def test_regular_er_subjunctive():
    assert conjugate("comer", "subjunctive", "yo") == "coma"
    assert conjugate("comer", "subjunctive", "nosotros") == "comamos"

def test_regular_er_imperative():
    assert conjugate("comer", "imperative", "tú") == "come"
    assert conjugate("comer", "imperative", "vosotros") == "comed"

# --- Regular -ir ---
def test_regular_ir_present():
    assert conjugate("vivir", "present", "yo") == "vivo"
    assert conjugate("vivir", "present", "vosotros") == "vivís"

def test_regular_ir_preterite():
    assert conjugate("vivir", "preterite", "yo") == "viví"
    assert conjugate("vivir", "preterite", "él") == "vivió"

def test_regular_ir_imperfect():
    assert conjugate("vivir", "imperfect", "yo") == "vivía"
    assert conjugate("vivir", "imperfect", "nosotros") == "vivíamos"

def test_regular_ir_subjunctive():
    assert conjugate("vivir", "subjunctive", "yo") == "viva"

def test_regular_ir_imperative():
    assert conjugate("vivir", "imperative", "tú") == "vive"
    assert conjugate("vivir", "imperative", "vosotros") == "vivid"

# --- Key irregular verbs ---
def test_ser_present():
    assert conjugate("ser", "present", "yo") == "soy"
    assert conjugate("ser", "present", "tú") == "eres"
    assert conjugate("ser", "present", "nosotros") == "somos"

def test_ser_preterite():
    assert conjugate("ser", "preterite", "yo") == "fui"
    assert conjugate("ser", "preterite", "él") == "fue"

def test_ser_imperfect():
    assert conjugate("ser", "imperfect", "yo") == "era"
    assert conjugate("ser", "imperfect", "nosotros") == "éramos"

def test_estar_present():
    assert conjugate("estar", "present", "yo") == "estoy"
    assert conjugate("estar", "present", "tú") == "estás"

def test_ir_present():
    assert conjugate("ir", "present", "yo") == "voy"
    assert conjugate("ir", "present", "nosotros") == "vamos"

def test_ir_preterite():
    assert conjugate("ir", "preterite", "yo") == "fui"

def test_ir_imperfect():
    assert conjugate("ir", "imperfect", "yo") == "iba"
    assert conjugate("ir", "imperfect", "nosotros") == "íbamos"

def test_hacer_present():
    assert conjugate("hacer", "present", "yo") == "hago"
    assert conjugate("hacer", "present", "tú") == "haces"

def test_hacer_preterite():
    assert conjugate("hacer", "preterite", "yo") == "hice"
    assert conjugate("hacer", "preterite", "él") == "hizo"

def test_hacer_future():
    assert conjugate("hacer", "future", "yo") == "haré"

def test_tener_present():
    assert conjugate("tener", "present", "yo") == "tengo"
    assert conjugate("tener", "present", "tú") == "tienes"

def test_tener_future():
    assert conjugate("tener", "future", "yo") == "tendré"

def test_stem_changing_pensar():
    assert conjugate("pensar", "present", "yo") == "pienso"
    assert conjugate("pensar", "present", "nosotros") == "pensamos"  # no change

def test_stem_changing_poder():
    assert conjugate("poder", "present", "yo") == "puedo"
    assert conjugate("poder", "present", "nosotros") == "podemos"  # no change

def test_stem_changing_dormir():
    assert conjugate("dormir", "present", "yo") == "duermo"
    assert conjugate("dormir", "preterite", "él") == "durmió"

def test_stem_changing_pedir():
    assert conjugate("pedir", "present", "yo") == "pido"
    assert conjugate("pedir", "preterite", "él") == "pidió"

def test_conocer_present_yo():
    assert conjugate("conocer", "present", "yo") == "conozco"
    assert conjugate("conocer", "present", "tú") == "conoces"  # regular

def test_conducir_present_yo():
    assert conjugate("conducir", "present", "yo") == "conduzco"
    assert conjugate("conducir", "preterite", "yo") == "conduje"

def test_get_all_conjugations_returns_all_tenses():
    result = get_all_conjugations("hablar")
    tenses = {"present", "preterite", "imperfect", "future", "conditional", "subjunctive", "imperative"}
    assert set(result.keys()) == tenses
    assert result["present"]["yo"] == "hablo"
    assert result["imperative"]["tú"] == "habla"
