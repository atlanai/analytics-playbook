# Semantic layers compared {#r7}

> [!RULE]
> The useful test for any layer is how far a metric can reach.

[Why a metric, and not a view](#ch-sv) makes the case for organizing context around the metric. This page is the reference behind it: how far a metric reaches in each of today's tools, and one model written in six syntaxes so you can see where the metric lives in each.

## How today's tools compare {#ch-sv-tools}

Every tool reviewed can join across tables. What differs is where the metric is defined and what bounds it. LookML, Malloy and Cube define a measure in one view, source or cube, and reach other tables through its joins. Snowflake semantic views, Databricks metric views, Apache Ossie (formerly OSI) and Genie hold metrics inside one view, model or agent. dbt MetricFlow can define a ratio metric at the top level of the project, from metrics in different semantic models, with entities as the join keys.

::: {.diagram #sv-reach}
Where each tool defines a metric and what bounds it, from public documentation checked on 27 October 2026.
:::

| Tool | Where the metric is defined | What bounds it |
|---|---|---|
| Looker (LookML) | In a view, one per table | The explore it is queried through |
| Malloy | In a source | The source and its joins |
| Cube | In a cube, usually one per table | The data model's joins, across several hops |
| Databricks metric views | In the view, rooted on one source table | The metric view; joins can run several levels deep |
| Databricks Genie | In a Genie Agent (formerly a Genie space) | The agent, up to 50 tables, views or metric views |
| Snowflake semantic views | Per logical table; derived metrics at view level | The view |
| Apache Ossie | In a dataset, or at model level beside the datasets | The model |
| dbt MetricFlow | Simple metrics on a semantic model; ratio and derived metrics at the top level | The join graph |

None of these ties verified SQL to an individual metric. Snowflake semantic views and Genie Agents keep verified or example SQL for the whole view or agent. The [metric spec template](#r2-5) keeps a metric's formula, named joins, dimensions and verified SQL together as one unit. We measured the SQL part of that <!-- E14 -->; the rest is design.

::: {.diagram #sv-feedback}
Feedback that lands in the model compiles the same way every time. Feedback kept beside it is text the agent has to reinterpret, and the pile grows with every fix.
:::

## One model in six syntaxes {#ch-sv-syntax}

Each snippet defines orders joined to customers, a revenue metric and a region dimension, adapted from each vendor's documentation and not run. Watch where the metric lives. Product names are their owners' trademarks; the comparison is drawn from public documentation on the date stated and is not an endorsement.

**Snowflake semantic view.** The metric is named per table; only the derived metric sits at view level.

```sql
CREATE SEMANTIC VIEW sales_sv
  TABLES (
    orders AS db.sch.orders PRIMARY KEY (order_id),
    customers AS db.sch.customers PRIMARY KEY (customer_id)
  )
  RELATIONSHIPS (
    orders_to_customers AS orders (customer_id) REFERENCES customers
  )
  FACTS ( orders.order_amount AS amount )
  DIMENSIONS ( customers.region AS customers.region )
  METRICS (
    orders.total_revenue AS SUM(orders.order_amount),
    customers.customer_count AS COUNT(customers.customer_id),
    revenue_per_customer AS orders.total_revenue / customers.customer_count
  );
```

**Databricks metric view.** Everything is rooted on one source table; joins can run several levels deep.

```yaml
version: 1.1
source: main.sales.orders
joins:
  - name: customers
    source: main.sales.customers
    on: source.customer_id = customers.customer_id
fields:
  - name: Region
    expr: customers.region
measures:
  - name: Total Revenue
    expr: SUM(amount)
```

**LookML.** Measures live in the view, joins in the explore, and drill paths hang off the measure.

```text
view: orders {
  sql_table_name: sales.orders ;;
  dimension: order_id { primary_key: yes sql: ${TABLE}.order_id ;; }
  measure: total_revenue {
    type: sum
    sql: ${TABLE}.amount ;;
    drill_fields: [order_id, customers.region]
  }
}
explore: orders {
  join: customers {
    sql_on: ${orders.customer_id} = ${customers.customer_id} ;;
    relationship: many_to_one
  }
}
```

**Malloy.** The source is the unit, and it reads like code.

```text
source: orders is duckdb.table('orders.parquet') extend {
  join_one: customers with customer_id
  measure: total_revenue is amount.sum()
  view: revenue_by_region is {
    group_by: customers.region
    aggregate: total_revenue
  }
}
```

**Apache Ossie.** A metric that spans datasets sits beside them, inside one model.

```yaml
name: sales
datasets:
  - name: orders
    source: sales.public.orders
    primary_key: [order_id]
  - name: customers
    source: sales.public.customers
    primary_key: [id]
relationships:
  - { name: orders_to_customers, from: orders, to: customers,
      from_columns: [customer_id], to_columns: [id] }
metrics:
  - name: total_revenue
    expression: { dialects: [{ dialect: ANSI_SQL, expression: SUM(orders.amount) }] }
```

**dbt MetricFlow.** Simple metrics sit with their model; the ratio metric sits at the top level and can combine metrics from different semantic models.

```yaml
models:
  - name: orders
    semantic_model: { enabled: true }
    columns:
      - name: order_id
        entity: { type: primary, name: order }
      - name: customer_id
        entity: { type: foreign, name: customer }
    metrics:
      - { name: total_revenue, type: simple, agg: sum, expr: amount }
      - { name: order_count, type: simple, agg: count, expr: order_id }
metrics:
  - name: average_order_value
    type: ratio
    numerator: total_revenue
    denominator: order_count
```

Read more: [Why a metric, and not a view](#ch-sv)
