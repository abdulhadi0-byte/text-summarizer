"""
Text Summarizer
---------------
A pure-Python, dependency-free extractive text summarizer.

How it works (no AI, no external API, no NLTK):
1. Split the input text into sentences.
2. Tokenize words, lowercase them, strip punctuation, and remove stopwords.
3. Build a word-frequency table, normalized against the most frequent word.
4. Score every sentence by averaging the frequency scores of its words
   (averaging avoids unfairly favoring long sentences).
5. Pick the top N highest-scoring sentences, then output them back in
   their original order so the summary still reads naturally.

Usage:
    python summarizer.py "Some long text here." --sentences 3
    python summarizer.py --file article.txt --sentences 5
    echo "some text" | python summarizer.py --sentences 2
"""

import argparse
import re
import sys

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "aren't", "as", "at", "be", "because", "been",
    "before", "being", "below", "between", "both", "but", "by", "can",
    "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from",
    "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
    "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
    "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd",
    "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "shan't", "she", "she'd", "she'll", "she's", "should",
    "shouldn't", "so", "some", "such", "than", "that", "that's", "the",
    "their", "theirs", "them", "themselves", "then", "there", "there's",
    "these", "they", "they'd", "they'll", "they're", "they've", "this",
    "those", "through", "to", "too", "under", "until", "up", "very",
    "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's",
    "which", "while", "who", "who's", "whom", "why", "why's", "with",
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves",
}


def split_sentences(text):
    """Split text into sentences without external libraries."""
    text = text.strip().replace("\n", " ")
    # Split on ., !, or ? followed by whitespace (or end of string),
    # but keep the punctuation attached to the sentence.
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def tokenize_words(sentence):
    """Lowercase and strip punctuation to get clean words."""
    words = re.findall(r"[a-zA-Z']+", sentence.lower())
    return words


def build_word_frequencies(sentences):
    """Build a normalized frequency table, ignoring stopwords."""
    freq = {}
    for sentence in sentences:
        for word in tokenize_words(sentence):
            if word in STOPWORDS or len(word) <= 1:
                continue
            freq[word] = freq.get(word, 0) + 1

    if not freq:
        return {}

    max_freq = max(freq.values())
    return {word: count / max_freq for word, count in freq.items()}


def score_sentences(sentences, freq):
    """Score each sentence by the average frequency-weight of its words."""
    scores = []
    for sentence in sentences:
        words = [w for w in tokenize_words(sentence) if w not in STOPWORDS and len(w) > 1]
        if not words:
            scores.append(0.0)
            continue
        score = sum(freq.get(w, 0) for w in words) / len(words)
        scores.append(score)
    return scores


def summarize_text(text, num_sentences=3):
    """
    Summarize `text` down to `num_sentences` sentences.
    Returns a dict with the summary and some stats.
    """
    sentences = split_sentences(text)

    if len(sentences) <= num_sentences:
        summary = " ".join(sentences)
        kept_indices = set(range(len(sentences)))
    else:
        freq = build_word_frequencies(sentences)
        scores = score_sentences(sentences, freq)

        # Rank sentence indices by score, take the top N
        ranked = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)
        kept_indices = set(ranked[:num_sentences])

        # Output in original order so it reads naturally
        summary = " ".join(sentences[i] for i in sorted(kept_indices))

    original_words = len(re.findall(r"\S+", text))
    summary_words = len(re.findall(r"\S+", summary))
    compression = 0 if original_words == 0 else round((1 - summary_words / original_words) * 100, 1)

    return {
        "summary": summary,
        "total_sentences": len(sentences),
        "kept_sentences": len(kept_indices),
        "original_words": original_words,
        "summary_words": summary_words,
        "compression_percent": compression,
    }


def main():
    parser = argparse.ArgumentParser(description="Pure-Python extractive text summarizer (no AI/API).")
    parser.add_argument("text", nargs="?", help="Text to summarize (or pipe text via stdin).")
    parser.add_argument("--file", "-f", help="Path to a .txt file to summarize.")
    parser.add_argument("--sentences", "-n", type=int, default=3, help="Number of sentences in the summary (default: 3).")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            input_text = fh.read()
    elif args.text:
        input_text = args.text
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()
    else:
        parser.error("Provide text as an argument, use --file, or pipe text via stdin.")
        return

    result = summarize_text(input_text, args.sentences)

    print("\n--- SUMMARY ---")
    print(result["summary"])
    print("\n--- STATS ---")
    print(f"Sentences: {result['kept_sentences']}/{result['total_sentences']} kept")
    print(f"Words: {result['original_words']} -> {result['summary_words']} ({result['compression_percent']}% shorter)")


if __name__ == "__main__":
    main()
