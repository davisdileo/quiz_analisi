# -*- coding: utf-8 -*-
"""Costruisce data/questions.json dando PRIORITA' alle domande modellate
sulle tracce d'esame reali del docente (bank/exam_*.py): disequazioni
esponenziali/logaritmiche, semplificazioni trigonometriche inverse, radici
n-esime di numeri complessi, studio di funzione (immagine/monotonia/
asintoti), integrali avanzati, teoremi con dimostrazione. Le domande
"generiche" (bank/ch1_reali.py ... ch7_integrale.py, extra_from_slides.py)
vengono usate SOLO come riempimento per i capitoli in cui il materiale
stile-esame non basta a raggiungere una base di 50 domande; le domande
curate a mano con grafici (data/questions_old_50.json) restano sempre
incluse.
"""
import json
import os
import random

import ch1_reali
import ch2_complessi
import ch3_funzioni
import ch4_limiti
import ch4_successioni
import ch5_continue
import ch6_differenziale
import ch7_integrale
import extra_from_slides
import exam_algebra
import exam_trig_inverse
import exam_complex_roots
import exam_function_study
import exam_integrali
import exam_teoremi
import exam_true_false2
import exam_complex_advanced
import exam_domains
import exam_integrali3
import exam_function_study2

HERE = os.path.dirname(__file__)
OLD_QUESTIONS = os.path.join(HERE, "..", "data", "questions_old_50.json")
OUT_PATH = os.path.join(HERE, "..", "data", "questions.json")

CHAPTER_NAME = {
    1: "Numeri reali",
    2: "Numeri complessi",
    3: "Funzioni reali",
    4: "Limiti",
    5: "Funzioni continue",
    6: "Calcolo differenziale",
    7: "Calcolo integrale",
}
NAME_TO_CHAPTER = {v: k for k, v in CHAPTER_NAME.items()}

MIN_PER_CHAPTER = 50

GENERIC_GENERATORS = {
    1: (ch1_reali, 101),
    2: (ch2_complessi, 202),
    3: (ch3_funzioni, 303),
    4: (ch4_limiti, 404),
    5: (ch5_continue, 505),
    6: (ch6_differenziale, 606),
    7: (ch7_integrale, 707),
}


def to_option_format(item, rng):
    """Converte {'text','correct','wrong':[...]} in {'text','options','correct':idx}."""
    opts = [item["correct"]] + list(item["wrong"])
    order = list(range(len(opts)))
    rng.shuffle(order)
    shuffled = [opts[i] for i in order]
    return {
        "text": item["text"],
        "options": shuffled,
        "correct": shuffled.index(item["correct"]),
        "image": item.get("image"),
    }


def load_curated_by_chapter():
    """Domande curate a mano (con eventuali grafici) — sempre incluse."""
    with open(OLD_QUESTIONS, encoding="utf-8") as f:
        old = json.load(f)
    by_chapter = {c: [] for c in range(1, 8)}
    for q in old:
        ch = NAME_TO_CHAPTER[q["topic"]]
        by_chapter[ch].append({
            "text": q["text"],
            "options": q["options"],
            "correct": q["correct"],
            "image": q.get("image"),
        })
    return by_chapter


def load_exam_style_by_chapter():
    """Domande modellate sulle tracce d'esame del docente: queste sono il
    contenuto PRIORITARIO della banca dati (sostituiscono il vecchio pool
    generico ovunque siano sufficienti a coprire un capitolo)."""
    by_chapter = {c: [] for c in range(1, 8)}

    rng1 = random.Random(11001)
    for it in exam_algebra.build():
        by_chapter[1].append(to_option_format(it, rng1))

    rng2 = random.Random(11002)
    for it in exam_complex_roots.build():
        by_chapter[2].append(to_option_format(it, rng2))

    rng3 = random.Random(11003)
    for it in exam_trig_inverse.build():
        by_chapter[3].append(to_option_format(it, rng3))

    fstudy = exam_function_study.build_by_chapter()
    for ch, items in fstudy.items():
        rng = random.Random(11010 + ch)
        for it in items:
            by_chapter[ch].append(to_option_format(it, rng))

    rng7 = random.Random(11007)
    for it in exam_integrali.build():
        by_chapter[7].append(to_option_format(it, rng7))

    teoremi = exam_teoremi.build_tagged()
    for it in teoremi:
        rng = random.Random(11020 + it["chapter"])
        by_chapter[it["chapter"]].append(to_option_format(it, rng))

    # --- nuove famiglie dalle 7 tracce d'esame caricate successivamente ---
    tf2 = exam_true_false2.build_tagged()
    for it in tf2:
        rng = random.Random(11030 + it["chapter"])
        by_chapter[it["chapter"]].append(to_option_format(it, rng))

    rng_ca = random.Random(11040)
    for it in exam_complex_advanced.build():
        by_chapter[2].append(to_option_format(it, rng_ca))

    domains = exam_domains.build_by_chapter()
    for ch, items in domains.items():
        rng = random.Random(11050 + ch)
        for it in items:
            by_chapter[ch].append(to_option_format(it, rng))

    rng_i3 = random.Random(11060)
    for it in exam_integrali3.build():
        by_chapter[7].append(to_option_format(it, rng_i3))

    fstudy2 = exam_function_study2.build_by_chapter()
    for ch, items in fstudy2.items():
        rng = random.Random(11070 + ch)
        for it in items:
            by_chapter[ch].append(to_option_format(it, rng))

    return by_chapter


def load_generic_fill_by_chapter():
    """Vecchio materiale (generatori sympy generici per capitolo, piu' le
    domande aggiuntive tratte dalle slide del corso): usato solo come
    riempimento per i capitoli dove il materiale stile-esame non basta a
    raggiungere MIN_PER_CHAPTER domande."""
    fill = {c: [] for c in range(1, 8)}

    for ch, (module, seed) in GENERIC_GENERATORS.items():
        rng = random.Random(seed)
        for it in module.build():
            fill[ch].append(to_option_format(it, rng))

    rng4 = random.Random(909)
    for it in ch4_successioni.build():
        fill[4].append(to_option_format(it, rng4))

    slides = extra_from_slides.build()
    for ch, items in slides.items():
        rng = random.Random(1000 + ch)
        for it in items:
            fill[ch].append(to_option_format(it, rng))

    return fill


def main():
    curated = load_curated_by_chapter()
    exam_style = load_exam_style_by_chapter()
    generic_fill = load_generic_fill_by_chapter()

    final = []
    next_id = 1
    summary = {}

    for ch in range(1, 8):
        pool = []
        seen_texts = set()

        def extend(src):
            added = 0
            for q in src:
                if q["text"] in seen_texts:
                    continue
                pool.append(q)
                seen_texts.add(q["text"])
                added += 1
            return added

        n_curated = extend(curated[ch])
        n_exam = extend(exam_style[ch])

        n_fill = 0
        if len(pool) < MIN_PER_CHAPTER:
            for q in generic_fill[ch]:
                if len(pool) >= MIN_PER_CHAPTER:
                    break
                if q["text"] in seen_texts:
                    continue
                pool.append(q)
                seen_texts.add(q["text"])
                n_fill += 1

        rng = random.Random(20000 + ch)
        rng.shuffle(pool)

        for q in pool:
            entry = {
                "id": next_id,
                "chapter": ch,
                "topic": CHAPTER_NAME[ch],
                "text": q["text"],
                "options": q["options"],
                "correct": q["correct"],
            }
            if q.get("image"):
                entry["image"] = q["image"]
            final.append(entry)
            next_id += 1

        summary[CHAPTER_NAME[ch]] = (f"{len(pool)} totali (curate={n_curated}, stile-esame={n_exam}, "
                                      f"riempimento generico={n_fill})")

    # controllo qualità finale
    bad = 0
    for q in final:
        opts = q["options"]
        if len(opts) != 4 or len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA OPZIONI:", q["id"], q["text"])
        if not (0 <= q["correct"] < 4):
            bad += 1
            print("INDICE CORRETTO INVALIDO:", q["id"], q["text"])

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    print("Totale domande scritte:", len(final))
    for name, s in summary.items():
        print(f"  {name}: {s}")
    print("Domande con problemi:", bad)
    n_images = sum(1 for q in final if "image" in q)
    print("Domande con immagine:", n_images)


if __name__ == "__main__":
    main()
