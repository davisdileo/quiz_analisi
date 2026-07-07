# -*- coding: utf-8 -*-
"""Combina le domande esistenti (curate a mano, con grafici) e quelle generate
per capitolo in un'unica banca dati da 50 domande per ciascuno dei 7 capitoli
(350 in totale), scritta in data/questions.json.
"""
import json
import os
import random

import ch1_reali
import ch2_complessi
import ch3_funzioni
import ch4_limiti
import ch5_continue
import ch6_differenziale
import ch7_integrale

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

GENERATORS = {
    1: (ch1_reali, 101),
    2: (ch2_complessi, 202),
    3: (ch3_funzioni, 303),
    4: (ch4_limiti, 404),
    5: (ch5_continue, 505),
    6: (ch6_differenziale, 606),
    7: (ch7_integrale, 707),
}


def load_existing_by_chapter():
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


def main():
    existing = load_existing_by_chapter()
    final = []
    next_id = 1
    summary = {}

    for ch in range(1, 8):
        pool = list(existing[ch])  # domande curate a mano (con eventuali grafici)
        seen_texts = {q["text"] for q in pool}

        module, seed = GENERATORS[ch]
        rng = random.Random(seed)
        generated_raw = module.build()
        generated = [to_option_format(it, rng) for it in generated_raw]

        for q in generated:
            if len(pool) >= 50:
                break
            if q["text"] in seen_texts:
                continue
            pool.append(q)
            seen_texts.add(q["text"])

        if len(pool) < 50:
            raise SystemExit(f"Capitolo {ch}: solo {len(pool)} domande disponibili, ne servono 50")

        pool = pool[:50]
        rng.shuffle(pool)  # mescola l'ordine curate/generate nel pool del capitolo

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

        summary[CHAPTER_NAME[ch]] = len(pool)

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
    print("Per capitolo:", summary)
    print("Domande con problemi:", bad)
    n_images = sum(1 for q in final if "image" in q)
    print("Domande con immagine:", n_images)


if __name__ == "__main__":
    main()
