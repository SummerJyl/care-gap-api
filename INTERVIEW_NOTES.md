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

-->