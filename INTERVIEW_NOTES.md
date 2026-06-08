<!--
I built:

"I built a REST API that accepts a FHIR R4 Bundle —
which is the standard format EHR systems use to exchange patient data —
extracts the patient's diagnoses, and maps each ICD-10 code to its corresponding HCC category using the CMS V28 model.
HCC stands for Hierarchical Condition Category — it's how Medicare measures patient complexity and calculates risk scores that directly affect how much ACOs like Aledade get paid."

Why it matters:

"If a patient has Type 2 diabetes documented in the EHR but it's not captured in their HCC risk score for the current year,
the practice loses revenue and the patient may not get the preventive care they need. My API surfaces that gap."

The gap detection layer applies comorbidity rules — clinical patterns that say 'if a patient has this condition, they commonly also have these related conditions.' If those related HCCs aren't documented in the current year, we flag them as care gaps and score them by clinical priority. A diabetic patient missing a CKD diagnosis scores higher than one missing a hypertension code because the revenue and clinical impact is greater. This gives the care team a prioritized worklist instead of a flat list of everything.

The API is fully stateful — when a FHIR bundle is ingested, the patient, their conditions, and their detected care gaps are all persisted to the database. A care manager can then query a patient's gap list at any time via a simple GET endpoint, sorted by clinical priority. This mirrors how a real care coordination workflow would work — ingest once from the EHR, query many times from the care team's dashboard.

I tested the gap detection engine across four different patient profiles — a diabetic patient, a heart failure patient, a COPD/diabetes comorbidity patient, and a CKD patient. During testing I caught a duplicate gap bug where the same HCC was being flagged twice when triggered by two different conditions. I fixed it by tracking already-flagged HCCs during detection so each gap only appears once in the prioritized list, regardless of how many conditions triggered it.
-->
