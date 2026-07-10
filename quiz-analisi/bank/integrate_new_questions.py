# -*- coding: utf-8 -*-
"""Integra le 5 nuove famiglie di domande (generate dalle 7 tracce d'esame
caricate il 10/07) nella banca dati ESISTENTE (data/questions.json, 404
domande gia' in produzione), senza toccare nulla di cio' che c'e' gia'.

Nota: il file bank/data/questions_old_50.json (input curato con grafici
usato dalla pipeline completa build_bank.py) non e' piu' presente su
disco in questa sessione — e' un file di build, non necessario a runtime
(solo data/questions.json viene letto dal server). Per non perdere nulla
di cio' che e' gia' stato costruito e verificato, questo script si limita
ad AGGIUNGERE le nuove domande a quelle gia' presenti (dedup per testo),
invece di rieseguire l'intera pipeline da zero.
"""
import json
import os
import random

import exam_true_false2
import exam_complex_advanced
import exam_domains
import exam_integrali3
import exam_function_study2

HERE = os.path.dirname(__file__)
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


def to_option_format(item, rng):
    opts = [item["correct"]] + list(item["wrong"])
    order = list(range(len(opts)))
    rng.shuffle(order)
    shuffled = [opts[i] for i in order]
    return {
        "text": item["text"],
        "options": shuffled,
        "correct": shuffled.index(item["correct"]),
    }


def collect_new_by_chapter():
    by_chapter = {c: [] for c in range(1, 8)}

    tf2 = exam_true_false2.build_tagged()
    for it in tf2:
        rng = random.Random(31030 + it["chapter"])
        by_chapter[it["chapter"]].append(to_option_format(it, rng))

    rng_ca = random.Random(31040)
    for it in exam_complex_advanced.build():
        by_chapter[2].append(to_option_format(it, rng_ca))

    domains = exam_domains.build_by_chapter()
    for ch, items in domains.items():
        rng = random.Random(31050 + ch)
        for it in items:
            by_chapter[ch].append(to_option_format(it, rng))

    rng_i3 = random.Random(31060)
    for it in exam_integrali3.build():
        by_chapter[7].append(to_option_format(it, rng_i3))

    fstudy2 = exam_function_study2.build_by_chapter()
    for ch, items in fstudy2.items():
        rng = random.Random(31070 + ch)
        for it in items:
            by_chapter[ch].append(to_option_format(it, rng))

    return by_chapter


def main():
    with open(OUT_PATH, encoding="utf-8") as f:
        existing = json.load(f)

    seen_texts = {q["text"] for q in existing}
    next_id = max(q["id"] for q in existing) + 1

    new_by_chapter = collect_new_by_chapter()

    added_summary = {}
    all_new = []
    for ch in range(1, 8):
        rng = random.Random(40000 + ch)
        pool = [q for q in new_by_chapter[ch] if q["text"] not in seen_texts]
        rng.shuffle(pool)
        for q in pool:
            seen_texts.add(q["text"])
        added_summary[CHAPTER_NAME[ch]] = len(pool)
        all_new.extend((ch, q) for q in pool)

    for ch, q in all_new:
        entry = {
            "id": next_id,
            "chapter": ch,
            "topic": CHAPTER_NAME[ch],
            "text": q["text"],
            "options": q["options"],
            "correct": q["correct"],
        }
        existing.append(entry)
        next_id += 1

    # controllo qualità finale
    bad = 0
    for q in existing:
        opts = q["options"]
        if len(opts) != 4 or len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA OPZIONI:", q["id"], q["text"])
        if not (0 <= q["correct"] < 4):
            bad += 1
            print("INDICE CORRETTO INVALIDO:", q["id"], q["text"])
    dup_texts = len(existing) - len({q["text"] for q in existing})
    if dup_texts:
        bad += dup_texts
        print("TESTI DUPLICATI:", dup_texts)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print("Totale domande dopo integrazione:", len(existing))
    print("Nuove domande aggiunte per capitolo:")
    for name, n in added_summary.items():
        print(f"  {name}: +{n}")
    print("Domande con problemi:", bad)


if __name__ == "__main__":
    main()
