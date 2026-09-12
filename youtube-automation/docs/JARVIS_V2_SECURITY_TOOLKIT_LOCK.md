# JARVIS V2 — Security Toolkit Lock

Status: LOCKED PROJECT REQUIREMENT

JARVIS V2 will include a legitimate cybersecurity / ethical-hacking toolkit for defensive security, authorized penetration testing, security development, auditing, monitoring, and forensics.

## Locked tool categories

- Network discovery: Nmap, Masscan
- Packet analysis: Wireshark, tcpdump
- Web security testing: Burp Suite, OWASP ZAP
- Vulnerability scanning: Nessus, OpenVAS/Greenbone
- DNS / security reconnaissance: dig, nslookup, Amass
- Directory/content discovery: ffuf, feroxbuster
- Web enumeration: httpx, WhatWeb
- Password auditing: Hashcat, John the Ripper
- Exploit research / authorized validation: Metasploit Framework
- Static code analysis: Semgrep, Bandit
- Dependency/security scanning: Trivy, OWASP Dependency-Check
- Container security: Trivy, Docker Scout
- Linux diagnostics: lsof, ss, strace
- Windows security/admin: PowerShell, Sysinternals Suite
- Log analysis / SOC: ELK/OpenSearch, Wazuh
- Cloud security: Prowler, ScoutSuite
- API testing: Burp Suite, OWASP ZAP, Postman
- Digital forensics: Autopsy, Volatility
- Identity / AD auditing: BloodHound (authorized environments only)

## JARVIS Security Center

The locked module structure is:

- Network Scanner
- Web Security
- Vulnerability Scanner
- API Security
- Code Security
- Container Security
- Windows Security
- Linux Security
- Log / SOC Monitor
- Cloud Security
- Forensics
- Identity / AD Auditing
- Security Reports

## Safety and authorization requirements

Security operations must be scoped to systems the user owns or is explicitly authorized to test. JARVIS must not implement credential theft, malware deployment, persistence, destructive actions, unauthorized access, or offensive intrusion workflows. Security actions should support scope/authorization checks, logging, and a human approval gate for consequential operations.

## Integration rule

These tools are a locked JARVIS V2 capability pool. They are not considered integrated merely because a tool is listed here. Each tool/category must be integrated through a controlled adapter/worker architecture, with tests and explicit dependencies documented. Existing JARVIS Core, Bridge, workflow, and eDEX UI architecture remains the integration target.
