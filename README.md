# 🛡️ AEGIS PRO: Hybrid Ransomware Defense System

> **A real-time endpoint protection agent that combines Cloud Intelligence with Behavioral Heuristics to detect and block ransomware.**

---

## 🧠 How It Works (The Core Logic)
AEGIS PRO operates on a **Hybrid Detection Architecture**, meaning it does not rely on just one method. It monitors the file system in real-time and analyzes every modification event using two distinct layers:

### **Layer 1: Static Analysis (Cloud Intelligence)**
* **The Trigger:** When a process modifies a file, AEGIS immediately calculates the SHA-256 hash (digital fingerprint) of that process's executable.
* **The Check:** It sends this hash to the **VirusTotal API** to check against 70+ global antivirus engines.
* **The Verdict:** If the global consensus is "Malicious," the process is terminated immediately **before** it can do significant damage.
* **Target:** Known viruses and malware signatures.

### **Layer 2: Behavioral Analysis (The "Peeler" Algorithm)**
* **The Problem:** Brand new ransomware (Zero-Day) is not yet known to VirusTotal (0/70 detection).
* **The Solution:** AEGIS monitors the **Speed of IO Operations** (Input/Output).
* **The Logic:** Humans modify files slowly. Ransomware modifies files instantly.
* **The Threshold:** If a process modifies multiple files within a **0.15-second** window (configurable), it is flagged as a "Rapid Encryption Attack."
* **Target:** Zero-Day ransomware and unknown threats.

---

## 🛠️ Technical Implementation
The system is built in Python using the following core modules:
* **`watchdog`**: For event-driven file system monitoring (detects file writes in milliseconds).
* **`psutil`**: For process management (identifying PIDs and terminating malicious processes).
* **`requests`**: For communicating with the VirusTotal API.
* **`pywin32`**: For interacting with the Windows Kernel to determine process visibility.

---

## 📊 Attack Lifecycle Coverage
AEGIS PRO interrupts the Cyber Kill Chain at two critical stages:
1.  **Execution:** Blocks known payloads immediately upon launch (Layer 1).
2.  **Action on Objectives (Encryption):** Detects the encryption behavior and kills the process to limit data loss (Layer 2).

---

## 🚀 Installation & Usage

### 1. Prerequisites
* Windows 10/11
* Python 3.x
* A free VirusTotal API Key

### 2. Setup
Clone the repository and install the required libraries:
```bash
##3. Configuration
Open aegis_pro.py and insert your API Key:
# Inside aegis_pro.py
API_KEY = 'YOUR_VIRUSTOTAL_KEY_HERE'

##4. Running the Defense
Run the agent with Administrator privileges (required to kill processes):
python aegis_pro.py

##5. Testing (Safe Simulation)
WARNING: Only run the simulator in a controlled Virtual Machine (VM). Open a separate terminal and run:
python sim_attack.py
git clone [https://github.com/YOUR_USERNAME/AEGIS-Ransomware-Defense.git](https://github.com/YOUR_USERNAME/AEGIS-Ransomware-Defense.git)
cd AEGIS-Ransomware-Defense
pip install -r requirements.txt
