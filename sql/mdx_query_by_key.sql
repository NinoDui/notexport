SELECT
    key AS word,
    value AS meaning
FROM
    MDX_DICT
WHERE
    key in ('$target_words')