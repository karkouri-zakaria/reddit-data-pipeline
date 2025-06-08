{% macro list_raw_tables() %}
    {% set query %}
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'raw'
    {% endset %}

    {% set results = run_query(query) %}
    {% if execute %}
        {% set table_names = results.columns[0].values() %}
    {% else %}
        {% set table_names = [] %}
    {% endif %}

    {{ return(table_names) }}
{% endmacro %}
