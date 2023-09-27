SELECT
    ZANNOTATIONREPRESENTATIVETEXT as BroaderText,
    ZANNOTATIONSELECTEDTEXT as HighlightedText,
    ZANNOTATIONNOTE as Note,
    ZFUTUREPROOFING5 as Chapter,
    ZANNOTATIONCREATIONDATE as Created,
    ZANNOTATIONMODIFICATIONDATE as Modified,
    ZANNOTATIONASSETID,
    ZPLLOCATIONRANGESTART,
    ZANNOTATIONLOCATION
FROM
    ZAEANNOTATION
WHERE
    ZANNOTATIONSELECTEDTEXT IS NOT NULL
    AND ZANNOTATIONASSETID IN ('$asset_ids')
ORDER BY
    ZANNOTATIONASSETID ASC,
    Created ASC