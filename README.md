# Distill — Text Summarizer

A dependency-free **extractive text summarizer**. No AI models, no API keys —
just a frequency-scoring algorithm written in plain Python (and ported to
plain JavaScript for the live web demo).

🔗 **Live demo:** enable GitHub Pages on this repo (see below) and it'll be
served straight from `docs/index.html`.

## How it works

1. Split the input into sentences.
2. Tokenize words, lowercase them, strip punctuation, and drop common
   stopwords ("the", "is", "and", ...).
3. Build a word-frequency table, normalized against the most frequent word.
4. Score each sentence by the **average** frequency-weight of its words
   (averaging avoids unfairly favoring long sentences).
5. Keep the top-N highest scoring sentences, then re-order them to match
   the original text so the summary still reads naturally.

This is a classic, well-known approach to extractive summarization —
no machine learning, no network calls, fully deterministic.

## Project structure

```
text-summarizer/
├── summarizer.py     # CLI + importable Python function
├── docs/
│   └── index.html    # Live web demo (same algorithm, in JS) — served via GitHub Pages
└── README.md
```

## Using the Python script

```bash
# Summarize text directly
python summarizer.py "Your long passage goes here." --sentences 3

# Summarize a text file
python summarizer.py --file article.txt --sentences 5

# Pipe text in
cat article.txt | python summarizer.py --sentences 3
```

Or import it in your own code:

```python
from summarizer import summarize_text

result = summarize_text(my_text, num_sentences=3)
print(result["summary"])
print(result["compression_percent"], "% shorter")
```

No external packages required — pure Python standard library.

## Using the web demo

Open `docs/index.html` in any browser, or push this repo to GitHub and turn
on **Pages**:

1. Push this repo to GitHub.
2. Go to **Settings → Pages**.
3. Under "Build and deployment", set **Source: Deploy from a branch**.
4. Set **Branch: main**, folder: **/docs**, then Save.
5. Your live demo will appear at `https://<your-username>.github.io/<repo-name>/`
   within a minute or two.

The web version runs entirely client-side — nothing is sent to a server,
so it works on GitHub Pages with zero backend.

## License

MIT — do whatever you like with it.
