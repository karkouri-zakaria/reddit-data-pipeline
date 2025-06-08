{{ config(materialized='table') }}

{# Get all tables in 'raw' schema starting with 'reddit_' #}
{% set raw_tables = list_raw_tables()%}

{% if raw_tables | length > 0 %}
    with unioned_tables as (
        {% for table in raw_tables %}
            select
                id as post_id,
                title,
                url,
                body,
                cast(score as integer) as score,
                cast(num_comments as integer) as num_comments,
                to_timestamp(cast(created as double precision)) as created_at
            from {{ source('raw', table) }}
            {% if not loop.last %}union all{% endif %}
        {% endfor %}
    )
    select * from unioned_tables

{% else %}
    {# Fallback if no tables exist #}
    select
        null::varchar as post_id,
        null::varchar as title,
        null::varchar as url,
        null::varchar as body,
        null::integer as score,
        null::integer as num_comments,
        null::timestamp as created_at
    where false
{% endif %}