# Notexport (note + export)

Python tool for 
1. Export highlights and Notes from Apple Books to local CSV/Excel files
2. Fetch the word meaning
3. Create Anki Cards.

## Usage

```python
python main.py \
    --title <keywords in book title> \
    --output <your desired output path, data/booktitile_date.csv as default>
```

## Milestone

- [x] Dump Highlights & Notes to a local file, supporting filters by 1) book name 2) time range
- [x] Query local vocabulary mdx/sqlite database for word meaning.
- [ ] Create Anki Cards with contents in HTML format

## Acknowledge
1. [angela-zhao](https://github.com/angela-zhao) and her project [apple-books-annotations-exporter](https://github.com/angela-zhao/apple-books-annotations-exporter/tree/master)
2. [mmjang](https://github.com/mmjang) and his/her project [mdict-query](https://github.com/mmjang/mdict-query)

