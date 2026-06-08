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

## How Patient Data Gets Into the System

**The question:** "How would you actually get patient data into this API?"

**The answer:**
In production there are three main sources:

1. **EHR Integration via SMART on FHIR** — EHRs like Epic and Athenahealth
   expose FHIR R4 APIs. You authenticate with OAuth2 (SMART on FHIR),
   request a patient bundle, and POST it to the ingestion endpoint.
   This is the most common pattern for real-time data.

2. **Bulk FHIR Export (`$export`)** — For large ACOs with thousands of
   patients you don't pull one at a time. You trigger a bulk export,
   the EHR generates FHIR resource files asynchronously, and you process
   them in batch. This is how Aledade ingests data at scale.

3. **CMS Claims Data** — CMS sends ACOs structured claims data showing
   what was diagnosed and billed. This gets normalized alongside clinical
   data to catch gaps between what was documented and what was coded.

**In this project:** I simulate EHR integration by manually POSTing
FHIR R4 bundles — the same format a real EHR connection would send.
The ingestion layer doesn't care where the bundle comes from.
-->
