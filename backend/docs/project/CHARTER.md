# Project Charter

## Business background

- Who is the client, what business domain the client is in.
- What business problems are we trying to address?

## Scope

- What data science solutions are we trying to build?
- What will we do?
- How is it going to be consumed by the customer?

## Personnel

- Who are on this project:

  - DS4A Team 19:

    - Project lead
    - PM
    - Data scientist(s):

      - Mario C. Velez-Gallego <marvelez@eafit.edu.co>
      - Andres Henao <andreshenao0622@gmail.com>
      - Andrés Pérez <andres.perez.g@gmail.com>
      - Juan Jose Buriticá <juanjoseb@gmail.com>
      - Juan Miguel Isaza Moreno <capitanisaza@gmail.com>
      - Miguel Jaramillo <mjaramilloj088@gmail.com>
      - Daniel Gomez <daniel6omez@gmail.com>
      - German Prieto - Teaching Assistant <g.prieto@correlation-one.com>
      - Jimmy Jing - Teaching Assistant <jimmy@correlation-one.com>

    - Solution Architect: Daniel Gomez <daniel6omez@gmail.com>

  - Client:
    - Data administrator
      - Andrés Argüelles <aarguelles@zetta-net.com>
    - Business contact
      - Victor Corredor <vcorredor@zetta-net.com>

## Metrics

- What are the qualitative objectives? (e.g. reduce user churn)
- What is a quantifiable metric (e.g. reduce the fraction of users with 4-week inactivity)
- Quantify what improvement in the values of the metrics are useful for the customer scenario (e.g. reduce the fraction of users with 4-week inactivity by 20%)
- What is the baseline (current) value of the metric? (e.g. current fraction of users with 4-week inactivity = 60%)
- How will we measure the metric? (e.g. A/B test on a specified subset for a specified period; or comparison of performance after implementation to baseline)

## Plan

- Phases (milestones), timeline, short description of what we'll do in each phase.

## Architecture

- Data
  - What data do we expect? Raw data in the customer data sources (e.g. on-prem files, SQL, on-prem Hadoop etc.)
- Data movement from on-prem to AWS to move either

  - all the data,
  - after some pre-aggregation on-prem,
  - Sampled data enough for modeling

- What tools and data storage/analytics resources will be used in the solution e.g.,
  - ASA for stream aggregation
  - HDI/Hive/R/Python for feature construction, aggregation and sampling
  - AWS for modeling and web service operationalization
- How will the score or operationalized web service(s) (RRS and/or BES) be consumed in the business workflow of the customer? If applicable, write down pseudo code for the APIs of the web service calls.
  - How will the customer use the model results to make decisions
  - Data movement pipeline in production
  - Make a 1 slide diagram showing the end to end data flow and decision architecture
    - If there is a substantial change in the customer's business workflow, make a before/after diagram showing the data flow.

## Communication

- How will we keep in touch? Weekly meetings?
- Who are the contact persons on both sides?