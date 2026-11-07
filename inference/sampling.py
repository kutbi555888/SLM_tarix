"""Model bergan sonli baholardan keyingi tokenni tanlaydi."""

import torch


def sample_next_token(
    logits,
    generated_ids,
    temperature=0.8,
    top_k=40,
    top_p=0.95,
    repetition_penalty=1.1,
    generator=None,
):
    if temperature < 0 or top_k < 0 or not 0 < top_p <= 1 or repetition_penalty < 1:
        raise ValueError("Token tanlash sozlamalari noto'g'ri.")
    scores = logits.float().clone()
    if generated_ids and repetition_penalty != 1:
        seen = torch.tensor(sorted(set(generated_ids)), device=scores.device)
        values = scores[seen]
        # Musbat baho bo'linadi, manfiy baho ko'paytiriladi: ikkalasi ham pasayadi.
        scores[seen] = torch.where(
            values > 0, values / repetition_penalty, values * repetition_penalty
        )
    if temperature == 0:
        return int(scores.argmax())
    scores = scores / temperature
    if 0 < top_k < scores.numel():
        threshold = torch.topk(scores, top_k).values[-1]
        scores[scores < threshold] = -torch.inf
    if top_p < 1:
        ordered, indices = torch.sort(scores, descending=True)
        remove = ordered.softmax(-1).cumsum(-1) > top_p
        # Chegarani oshirib yuborgan birinchi tokenni ham saqlaymiz.
        remove[1:] = remove[:-1].clone()
        remove[0] = False
        scores[indices[remove]] = -torch.inf
    return int(torch.multinomial(scores.softmax(-1), 1, generator=generator))
