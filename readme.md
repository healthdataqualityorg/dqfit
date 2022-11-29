# Data Quality Fitness Index Tool


## alpha

# Quickstart

[ WIP ]

# The Value of High-Quality Data: Measuring Fitness and Trust in [Longitudinal health records]

alt-title: Trust is all you need

Authors: Parker Holcomb; Ben Hamlin, DrPH; Brad Ryan, MD; Marc Overhage, MD […]

**Abstract.** A pure function implementation of data quality assessment would allow real-time scoring of “fitness for use” without requiring exchange of the data. Standards such as FHIR and USCDI provide part of the solution, however transmission protocols and schema conformance alone does not ensure the completeness, plausibility, or fitness for use of the data[1]. Given the privacy, regulatory, and business risks associated with transmitting and persisting patient medical records, the Data Quality Fitness Index Test is designed to run in a purely offline or containerized mode, eliminating the need for any PHI to go “over the wire”. Data are input as a list of FHIR Bundles (a “Cohort”) and fitness for use (a "Context") is addressed with a set of empirically tuned weights. Completeness and plausibility are scored at the PatientLevel and CohortLevel, by measuring 1) the weighted sum of information and 2) the weighted sum of data gaps. The result is two fold: a directional and relative index as a positive integer; with supporting visualizations optimized for intuitive understanding of the context and underlying data. 

This research explores how building trust in the data quality and fitness can help solve the cold start trust problem and reduce time to value when adopting new payment models. 

In short, we believe data quality improves when it’s indexed to value.


