# Structs in DuckDB 1.2

## Define some structs

```sql
SET VARIABLE struct1 = {'name': 'DuckDB', 'firstRelease': 2019};
SET VARIABLE struct2 = {'description': 'in-process SQL database'};
```

## struct_extract_at

Extract by index:

```sql
SELECT struct_extract_at(getvariable('struct1'), 1);
```

```sql
SELECT struct_extract_at(getvariable('struct1'), 2);
```

## struct_concat

```sql
SELECT struct_concat(
  getvariable('struct1'), 
  getvariable('struct2')
) AS duck;
```


## struct casting

You can cast to structs without all/any fields matching:

```sql
SELECT struct_concat(
  getvariable('struct1'), 
  getvariable('struct2')
)::STRUCT(name String, description String) AS duck;
```

```sql
SELECT struct_concat(
  getvariable('struct1'), 
  getvariable('struct2')
)::STRUCT(name String, description String, foo Int) AS duck;
```

## Predicate pushdown

Dataset: https://github.com/statsbomb/open-data

Create table:

```sql
CREATE OR REPLACE TABLE events AS
FROM read_json(
  'open-data/data/events/*.json',
  union_by_name=true, records=false
);
```

Export to Parquet:

```sql
COPY events 
TO 'events.parquet' 
(FORMAT PARQUET);
```

Query 1:

```sql
FROM events
SELECT json.possession_team.name, 
       count()
GROUP BY ALL
ORDER BY count() DESC
LIMIT 10;
```

Query 2:

```sql
FROM events
SELECT json.pass.recipient.name, count()
WHERE
  json.pass.height.name = 'High Pass'
AND
  json.pass.outcome.name = 'Incomplete'
AND 
  json.possession_team.name = 'Japan'
AND
  json.pass.recipient.name NOT NULL
GROUP BY ALL
ORDER BY count() DESC
LIMIT 5;
```

Query 2 (Parquet):

```sql
FROM 'events.parquet'
SELECT json.pass.recipient.name, count()
WHERE
  json.pass.height.name = 'High Pass'
AND
  json.pass.outcome.name = 'Incomplete'
AND 
  json.possession_team.name = 'Japan'
AND
  json.pass.recipient.name NOT NULL
GROUP BY ALL
ORDER BY count() DESC
LIMIT 5;
```

Query 2 (JSON):

```sql
FROM read_json(
  'open-data/data/events/*.json',
  union_by_name=true
)
SELECT pass.recipient.name, count()
WHERE
  pass.height.name = 'High Pass'
AND
  pass.outcome.name = 'Incomplete'
AND 
  possession_team.name = 'Japan'
AND
  pass.recipient.name NOT NULL
GROUP BY ALL
ORDER BY count() DESC
LIMIT 5;
```