# hipaa_questions.py
# Complisstant - HIPAA Security Rule Question Library
# Core = fast onboarding. Full = complete coverage (Advanced).

def q(
    id: str,
    category: str,
    weight: int,
    question: str,
    citation: str,
    required: str,
    trigger_if: list[str],
    finding_title: str,
    default_likelihood: int,
    default_impact: int,
    recommendation: str,
):
    return {
        "id": id,
        "category": category,                 # Administrative / Physical / Technical / Program
        "weight": weight,                     # 1 (low) to 3 (high)
        "question": question,
        "citation": citation,
        "required": required,                 # Required / Addressable
        "trigger_if": trigger_if,             # usually ["No","Unsure"]
        "finding_title": finding_title,
        "default_likelihood": default_likelihood,
        "default_impact": default_impact,
        "recommendation": recommendation,
    }


# -----------------------------
# CORE 20 (high-impact, common gaps)
# -----------------------------
questions_core = [
    # ADMINISTRATIVE 164.308
    q("RA1","Administrative",3,"Do you perform a HIPAA security risk assessment at least annually (and after major changes)?",
      "164.308(a)(1)(ii)(A)","Required",["No","Unsure"],
      "Risk analysis not performed annually",3,3,
      "Perform and document a HIPAA Security Rule risk analysis at least annually and upon major environment changes."),

    q("RM1","Administrative",3,"Do you maintain a remediation plan for risks identified in the risk assessment (owners + due dates)?",
      "164.308(a)(1)(ii)(B)","Required",["No","Unsure"],
      "Risk management plan not maintained",3,3,
      "Maintain a risk management plan with assigned owners, timelines, and evidence of remediation progress."),

    q("SP1","Administrative",2,"Do you have a documented sanction policy for workforce members who violate HIPAA security policies?",
      "164.308(a)(1)(ii)(C)","Required",["No","Unsure"],
      "Sanction policy not documented",2,3,
      "Document and communicate a sanction policy for security violations and apply it consistently."),

    q("LOG1","Administrative",3,"Are information system activity logs reviewed on a routine basis (e.g., weekly/monthly)?",
      "164.308(a)(1)(ii)(D)","Required",["No","Unsure"],
      "Information system activity review not performed",3,3,
      "Establish and document routine log reviews for systems storing/transmitting ePHI and retain evidence of review."),

    q("ASR1","Administrative",2,"Is a HIPAA Security Officer formally assigned and documented?",
      "164.308(a)(2)","Required",["No","Unsure"],
      "Security responsibility not formally assigned",2,3,
      "Formally assign and document a Security Officer responsible for HIPAA Security Rule compliance activities."),

    q("WF1","Administrative",3,"Are user accounts approved before access is granted to systems containing ePHI?",
      "164.308(a)(3)(ii)(A)","Addressable",["No","Unsure"],
      "Workforce access authorization not controlled",3,3,
      "Implement a documented access authorization process requiring approval prior to granting access to ePHI systems."),

    q("TERM1","Administrative",3,"Are terminated employees removed/disabled from systems within 24 hours?",
      "164.308(a)(3)(ii)(C)","Addressable",["No","Unsure"],
      "Delayed termination of access",3,3,
      "Implement a deprovisioning process to disable accounts within 24 hours (or faster) upon termination."),

    q("SAT1","Administrative",2,"Do employees receive HIPAA security awareness training at least annually?",
      "164.308(a)(5)","Required",["No","Unsure"],
      "Security awareness training not performed annually",2,3,
      "Provide and document annual HIPAA security awareness training for all workforce members."),

    q("IR1","Administrative",3,"Do you have documented security incident response procedures (detect, respond, contain, recover, report)?",
      "164.308(a)(6)(i)","Required",["No","Unsure"],
      "Incident response procedures not documented",3,3,
      "Develop, approve, and test incident response procedures addressing detection, response, containment, and reporting."),

    q("BK1","Administrative",3,"Are backups performed at least daily for systems containing ePHI?",
      "164.308(a)(7)(ii)(A)","Required",["No","Unsure"],
      "Backups not performed daily",3,3,
      "Implement daily backups for ePHI systems and verify completion with reporting and alerts."),

    q("DR1","Administrative",2,"Do you have a documented disaster recovery plan for systems containing ePHI?",
      "164.308(a)(7)(ii)(B)","Required",["No","Unsure"],
      "Disaster recovery plan not documented",2,3,
      "Develop and maintain a disaster recovery plan covering restoration of ePHI systems and services."),

    q("TEST1","Administrative",2,"Are backups restored/tested at least quarterly (restore tests documented)?",
      "164.308(a)(7)(ii)(D)","Addressable",["No","Unsure"],
      "Backups not tested regularly",2,3,
      "Perform and document periodic restore tests to validate backup integrity and recovery objectives."),

    q("EVAL1","Administrative",2,"Do you perform periodic technical/non-technical evaluations of HIPAA security controls (at least annually)?",
      "164.308(a)(8)","Required",["No","Unsure"],
      "Periodic evaluations not performed",2,2,
      "Perform periodic evaluations of safeguards (technical and administrative) and document results and improvements."),

    q("BAA1","Administrative",3,"Do you maintain current Business Associate Agreements (BAAs) with all vendors that handle PHI?",
      "164.308(b)(1)","Required",["No","Unsure"],
      "Business Associate Agreements not maintained",3,3,
      "Inventory PHI-handling vendors and ensure executed BAAs are in place and reviewed periodically."),

    # PHYSICAL 164.310
    q("FAC1","Physical",2,"Is physical access to areas housing ePHI systems restricted (locks/badges/controlled keys)?",
      "164.310(a)(1)","Required",["No","Unsure"],
      "Facility access controls not implemented",2,3,
      "Restrict physical access to systems containing ePHI using locks, key control, badges, and visitor procedures."),

    q("WS1","Physical",2,"Do workstations automatically lock after a short period of inactivity?",
      "164.310(b)","Required",["No","Unsure"],
      "Workstation security controls not implemented",2,3,
      "Enable automatic screen lock and require users to lock devices when unattended."),

    q("DEV1","Physical",3,"Are all endpoints and portable devices that store or access ePHI encrypted (laptops, tablets, removable media)?",
      "164.310(d)(1)","Required",["No","Unsure"],
      "Device/media protections not implemented for ePHI",3,3,
      "Implement encryption and handling controls for devices/media storing or accessing ePHI and maintain inventory."),

    # TECHNICAL 164.312
    q("UID1","Technical",3,"Do users have unique user IDs (no shared accounts) for systems containing ePHI?",
      "164.312(a)(1)","Required",["No","Unsure"],
      "Unique user identification not enforced",3,3,
      "Require unique user IDs for all users and eliminate shared accounts; implement privileged account controls."),

    q("MFA1","Technical",3,"Is Multi-Factor Authentication (MFA) enabled for email, remote access, and administrative accounts?",
      "164.312(a)(1)","Addressable",["No","Unsure"],
      "Multi-factor authentication not implemented",3,3,
      "Enable MFA for email, VPN/remote access, EHR administrative access, and privileged accounts."),

    q("AUD1","Technical",3,"Are audit logs enabled and retained for systems containing ePHI (EHR, email, file systems, VPN)?",
      "164.312(b)","Required",["No","Unsure"],
      "Audit controls not implemented",3,3,
      "Enable audit logging on ePHI systems, retain logs per policy, and protect logs from alteration."),

    q("ENCREST1","Technical",3,"Is ePHI encrypted at rest on servers, endpoints, and portable devices?",
      "164.312(a)(2)(iv)","Addressable",["No","Unsure"],
      "Encryption at rest not implemented for ePHI",2,3,
      "Implement encryption at rest for endpoints, servers, and storage containing ePHI (full disk / database encryption)."),

    q("ENCTRANS1","Technical",3,"Is ePHI encrypted in transit (TLS for apps, VPN as needed, secure email/portal for PHI)?",
      "164.312(e)(1)","Addressable",["No","Unsure"],
      "Encryption in transit not consistently implemented",2,3,
      "Enforce TLS for all ePHI transmission paths and require secure email/portal workflows for PHI."),
]


# -----------------------------
# FULL LIBRARY (Advanced)
# Includes CORE + remaining Security Rule / related program requirements
# -----------------------------
questions_full = list(questions_core) + [

    # 164.308(a)(1) Security Management Process - extra detail
    q("SMP_SAN1","Administrative",1,"Do you document and apply security measures sufficient to reduce risks to a reasonable and appropriate level?",
      "164.308(a)(1)(i)","Required",["No","Unsure"],
      "Security management process not documented",2,2,
      "Document security measures and governance demonstrating risk reduction to a reasonable and appropriate level."),

    # 164.308(a)(3) Workforce Security - extra
    q("WF_SUP1","Administrative",1,"Is workforce supervision implemented where appropriate to protect ePHI (e.g., least privilege, oversight)?",
      "164.308(a)(3)(ii)(B)","Addressable",["No","Unsure"],
      "Workforce supervision not implemented",2,2,
      "Implement least privilege and supervisory review for access to ePHI systems as appropriate."),

    # 164.308(a)(4) Information Access Management
    q("IAM_ISO1","Administrative",2,"Do you have policies/procedures for authorizing access to ePHI systems based on role and job function?",
      "164.308(a)(4)(i)","Required",["No","Unsure"],
      "Information access management not documented",2,3,
      "Document role-based access policies and procedures for authorizing access to ePHI."),

    q("IAM_ACCESS1","Administrative",2,"Are access rights established, documented, and modified based on workforce role changes?",
      "164.308(a)(4)(ii)(C)","Addressable",["No","Unsure"],
      "Access establishment/modification not controlled",2,3,
      "Establish and document role-based access, and review/modify access promptly upon role changes."),

    # 164.308(a)(5) Security Awareness and Training - sub-specs
    q("SAT_REM1","Administrative",1,"Do you send periodic security reminders (e.g., phishing tips, policy reminders)?",
      "164.308(a)(5)(ii)(A)","Addressable",["No","Unsure"],
      "Security reminders not implemented",1,2,
      "Send periodic security reminders and document awareness communications."),

    q("SAT_PW1","Administrative",1,"Do you provide password management guidance (creation, storage, reuse, manager use)?",
      "164.308(a)(5)(ii)(D)","Addressable",["No","Unsure"],
      "Password management guidance not provided",1,2,
      "Provide password guidance/training and consider password managers where appropriate."),

    # 164.308(a)(6) Incident Procedures - reporting/response refinement
    q("IR_DOC1","Administrative",2,"Are security incidents tracked and documented, including outcomes and corrective actions?",
      "164.308(a)(6)(ii)","Required",["No","Unsure"],
      "Security incidents not documented",2,3,
      "Track incidents in a log/ticketing system and retain evidence of response and corrective actions."),

    # 164.308(a)(7) Contingency Plan - extra specs
    q("EMODE1","Administrative",1,"Do you have an emergency mode operation plan for maintaining critical operations during emergencies?",
      "164.308(a)(7)(ii)(C)","Addressable",["No","Unsure"],
      "Emergency mode operation plan not documented",2,2,
      "Develop an emergency mode operation plan to ensure critical functions continue while protecting ePHI."),

    q("CP_TEST1","Administrative",1,"Do you test and revise contingency plans periodically (beyond backup restore tests)?",
      "164.308(a)(7)(ii)(D)","Addressable",["No","Unsure"],
      "Contingency plan not tested/revised",2,2,
      "Test and revise contingency plans periodically; retain test evidence and updates."),

    q("CP_APP1","Administrative",1,"Do you perform applications/data criticality analysis to prioritize recovery sequencing?",
      "164.308(a)(7)(ii)(E)","Addressable",["No","Unsure"],
      "Criticality analysis not performed",1,2,
      "Perform criticality analysis to prioritize recovery of systems supporting patient care and ePHI."),

    # 164.308(a)(8) Evaluation already in core; add change-driven note
    q("EVAL_CHANGE1","Administrative",1,"Do you evaluate the impact of operational/environmental changes on HIPAA security safeguards?",
      "164.308(a)(8)","Required",["No","Unsure"],
      "Change impact evaluations not performed",1,2,
      "Evaluate changes (systems/vendors/workflows) for security impact and document results."),

    # 164.308(b)(1) BA contracts already in core; add BA oversight
    q("BA_OVR1","Administrative",1,"Do you periodically review vendors handling PHI (security posture, incidents, contract status)?",
      "164.308(b)(1)","Required",["No","Unsure"],
      "Business associate oversight not performed",2,2,
      "Implement periodic vendor review for PHI-handling vendors; track BAAs and security assurances."),

    # 164.310(a) Facility Access Controls - implementation specs
    q("FAC_PLAN1","Physical",1,"Do you maintain contingency operations procedures for facility access during emergencies?",
      "164.310(a)(2)(i)","Addressable",["No","Unsure"],
      "Facility contingency access procedures not documented",1,2,
      "Document facility access procedures during emergencies, including who can access systems and how access is controlled."),

    q("FAC_PLAN2","Physical",1,"Do you have a facility security plan describing physical safeguards and access controls?",
      "164.310(a)(2)(ii)","Addressable",["No","Unsure"],
      "Facility security plan not documented",1,2,
      "Document facility security plan including physical safeguards and access control mechanisms."),

    q("FAC_VAL1","Physical",1,"Is there a documented visitor access control procedure (sign-in, escort, logs)?",
      "164.310(a)(2)(iii)","Addressable",["No","Unsure"],
      "Visitor control not implemented",1,2,
      "Implement visitor sign-in/escort procedures and retain visitor logs per policy."),

    q("FAC_MAINT1","Physical",1,"Are facility maintenance records documented for repairs/modifications related to security of ePHI areas?",
      "164.310(a)(2)(iv)","Addressable",["No","Unsure"],
      "Facility maintenance records not maintained",1,1,
      "Maintain records of facility maintenance that could affect physical security of ePHI systems."),

    # 164.310(b) Workstation Use
    q("WS_USE1","Physical",1,"Do you have a workstation use policy defining proper functions, physical attributes, and environment controls?",
      "164.310(b)","Required",["No","Unsure"],
      "Workstation use policy not documented",1,2,
      "Document workstation use policy including permissible uses and environmental/physical controls."),

    # 164.310(c) Workstation Security (separate standard)
    q("WS_SEC1","Physical",2,"Are workstations positioned/configured to prevent unauthorized viewing/access (privacy screens, layout)?",
      "164.310(c)","Required",["No","Unsure"],
      "Workstation security not implemented",2,2,
      "Implement workstation physical protections (layout controls, privacy screens where needed) to prevent unauthorized access/viewing."),

    # 164.310(d) Device and Media Controls - more specs
    q("DM_DISP1","Physical",2,"Are devices/media containing ePHI disposed of securely (wiping/shredding) with records retained?",
      "164.310(d)(2)(i)","Required",["No","Unsure"],
      "Media disposal not controlled",2,3,
      "Implement secure media disposal procedures and retain destruction/wipe evidence."),

    q("DM_REUSE1","Physical",2,"Are devices/media re-used only after ePHI has been removed (secure wiping procedures)?",
      "164.310(d)(2)(ii)","Required",["No","Unsure"],
      "Media re-use not controlled",2,3,
      "Implement media re-use controls including secure wiping/verification before redeployment."),

    q("DM_ACC1","Physical",1,"Do you maintain accountability/inventory for hardware and electronic media that contain ePHI?",
      "164.310(d)(2)(iii)","Addressable",["No","Unsure"],
      "Media accountability not maintained",2,2,
      "Maintain inventory/accountability for devices/media containing ePHI, including assignment and location tracking."),

    q("DM_BACK1","Physical",1,"Do you create and maintain data backups before equipment movement (as needed) and protect data during transport?",
      "164.310(d)(2)(iv)","Addressable",["No","Unsure"],
      "Data backup and storage procedures for device movement not documented",1,2,
      "Document procedures for safeguarding ePHI during equipment movement/transport and ensure backup as needed."),

    # 164.312(a) Access Control - more
    q("AC_EMERG1","Technical",2,"Do you have an emergency access procedure for ePHI systems (break-glass) that is controlled and logged?",
      "164.312(a)(2)(ii)","Required",["No","Unsure"],
      "Emergency access procedure not documented",2,3,
      "Implement controlled emergency access procedures and ensure use is logged and reviewed."),

    q("AC_LOGOFF1","Technical",2,"Do systems automatically log off or lock sessions after inactivity?",
      "164.312(a)(2)(iii)","Addressable",["No","Unsure"],
      "Automatic logoff not implemented",2,2,
      "Configure session timeouts/auto-logoff for systems accessing ePHI based on risk and workflow."),

    q("AC_ENC1","Technical",3,"Is encryption implemented for ePHI as appropriate (addressable specification) and documented when not used?",
      "164.312(a)(2)(iv)","Addressable",["No","Unsure"],
      "Encryption decision not implemented/documented",2,3,
      "Implement encryption for ePHI or document equivalent compensating controls and rationale where encryption is not used."),

    # 164.312(c) Integrity
    q("INT1","Technical",2,"Do you implement mechanisms to corroborate that ePHI has not been altered or destroyed in an unauthorized manner?",
      "164.312(c)(1)","Required",["No","Unsure"],
      "Integrity controls not implemented",2,3,
      "Implement integrity controls such as access controls, checksums/auditing where applicable, and change management."),

    q("INT_AUTH1","Technical",1,"Are electronic mechanisms in place to authenticate ePHI (where appropriate)?",
      "164.312(c)(2)","Addressable",["No","Unsure"],
      "ePHI authentication mechanisms not implemented",1,2,
      "Implement ePHI authentication mechanisms where appropriate (e.g., digital signatures, hashes) or document alternatives."),

    # 164.312(d) Person or Entity Authentication
    q("AUTH1","Technical",2,"Do you verify that a person or entity seeking access to ePHI is the one claimed (authentication controls)?",
      "164.312(d)","Required",["No","Unsure"],
      "Person/entity authentication not enforced",2,3,
      "Implement strong authentication controls (unique IDs, MFA where appropriate) and reduce shared credentials."),

    # 164.312(e) Transmission Security - more
    q("TS_INTEG1","Technical",1,"Do you implement integrity controls to ensure ePHI is not improperly modified during transmission?",
      "164.312(e)(2)(i)","Addressable",["No","Unsure"],
      "Transmission integrity controls not implemented",1,2,
      "Implement integrity controls for transmissions (TLS, message integrity, secure protocols) and document configurations."),

    q("TS_ENC2","Technical",3,"Do you encrypt ePHI when transmitted over networks (including email and remote access)?",
      "164.312(e)(2)(ii)","Addressable",["No","Unsure"],
      "Transmission encryption not implemented",2,3,
      "Use encryption for ePHI transmissions (TLS/VPN/secure email portals) and restrict insecure channels."),

    # 164.314 Organizational Requirements
    q("ORG_BA1","Program",2,"Do you ensure business associate contracts/arrangements require appropriate safeguards for ePHI?",
      "164.314(a)(1)","Required",["No","Unsure"],
      "Business associate safeguards not contractually required",2,3,
      "Ensure BAAs/arrangements require safeguards and include reporting/incident obligations for ePHI protection."),

    q("ORG_GRP1","Program",1,"If applicable, are requirements for group health plans addressed (where relevant)?",
      "164.314(b)","Required",["No","Unsure"],
      "Organizational requirements for group health plans not addressed",1,1,
      "Where applicable, address HIPAA organizational requirements for group health plans and document applicability."),

    # 164.316 Policies and Documentation
    q("DOC1","Program",3,"Do you have written HIPAA security policies and procedures implemented and maintained?",
      "164.316(a)","Required",["No","Unsure"],
      "HIPAA security policies and procedures not maintained",2,3,
      "Maintain written HIPAA security policies/procedures aligned to the Security Rule and operational practices."),

    q("DOC2","Program",2,"Do you retain required HIPAA security documentation for at least six years and make it available as needed?",
      "164.316(b)(2)(i)","Required",["No","Unsure"],
      "HIPAA documentation retention not met",2,2,
      "Retain HIPAA security documentation for at least six years and ensure it is accessible for audits/investigations."),

    q("DOC3","Program",2,"Do you review and update HIPAA security documentation periodically and when environment changes occur?",
      "164.316(b)(2)(iii)","Required",["No","Unsure"],
      "HIPAA documentation not reviewed/updated",2,2,
      "Review and update HIPAA security documentation periodically and after material changes; retain evidence of review."),
]