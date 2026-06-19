# Document Secret Sharing System with SHA-256 Based Share Authentication

## Overview

The Document Secret Sharing System (DSS) is a secure document protection framework that combines threshold-based secret sharing with SHA-256 hash authentication to ensure confidentiality, integrity, and secure reconstruction of sensitive files.

The system allows a document to be divided into multiple shares, where only a predefined minimum number of shares (threshold) can reconstruct the original document. Each share is authenticated using SHA-256 hashing, enabling detection of tampering and preventing unauthorized reconstruction.

This project was developed as part of a research initiative and was later published in a Scopus-indexed journal.

---

## Research Publication

**Title:** Document Secret Sharing with SHA-256 Based Share Authentication

**Journal:** Grenze International Journal of Engineering and Technology (GIJET)

**Volume:** 12, Issue 1 (January 2026)

**Indexing:** Scopus Indexed

---

## Problem Statement

Traditional file-sharing mechanisms often expose sensitive documents to risks such as:

* Unauthorized access
* Data leakage
* Share tampering
* Single-point failure during storage

The DSS system addresses these challenges by distributing document data into multiple secure shares and verifying share integrity before reconstruction.

---

## Key Features

### Secure Share Generation

* Split documents into multiple shares using threshold-based secret sharing.
* Configurable `(k,n)` architecture where:

  * `n` = total shares generated
  * `k` = minimum shares required for reconstruction

### SHA-256 Share Authentication

* Generates unique SHA-256 hashes for every share.
* Detects modified, corrupted, or forged shares before reconstruction.

### Secure Reconstruction

* Reconstructs the original document only when the threshold requirement is satisfied.
* Prevents reconstruction using insufficient or invalid shares.

### Graphical User Interface

* User-friendly desktop interface built with Tkinter.
* Simplifies share generation and reconstruction workflows.

### Multi-Format Support

* Supports secure sharing of various document types.

---

## Technology Stack

* Python
* SHA-256 Cryptographic Hashing
* Tkinter GUI

---

## My Contributions

* Implemented the majority of the system's development and coding.
* Built core share generation and reconstruction workflows.
* Integrated SHA-256 based share authentication.
* Developed the graphical user interface using Tkinter.
* Participated in system testing, debugging, and validation.
* Co-authored the research publication.

---

## Experimental Results

The published system demonstrated:

* 100% document reconstruction accuracy.
* Successful rejection of all tampered shares through SHA-256 verification.
* Share size overhead below 6%.
* Reconstruction times under 5 seconds for files up to 5 MB.
* Strong scalability across multiple threshold configurations.

---

## System Workflow

1. Upload a document.
2. Select threshold configuration `(k,n)`.
3. Generate secure document shares.
4. Generate SHA-256 authentication hashes.
5. Distribute shares securely.
6. Collect required shares.
7. Verify integrity using hash validation.
8. Reconstruct original document.

---

## Conference Presentation

The project was presented at an academic research conference, where the system architecture, implementation, and experimental results were demonstrated.

---

## Future Enhancements

* Cloud-based share storage
* Web application deployment
* Enhanced access control mechanisms
* Multi-factor authentication
* Blockchain-based share verification
* Support for larger file sizes and distributed environments

---

## Repository Structure

```text
Document-Secret-Sharing-System/
│
├── source_code/
├── gui/
├── sample_files/
├── screenshots/
├── research_paper/
└── README.md
```

---

## Disclaimer

This project was developed for educational and research purposes. The implementation demonstrates practical applications of threshold cryptography and integrity verification for secure document sharing.
