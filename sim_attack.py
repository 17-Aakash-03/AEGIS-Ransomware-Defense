import os
import time

TARGET_DIR = os.path.join(os.getcwd(), "TestZone")

def create_bait():
    print("Creating bait files...")
    for i in range(5):
        with open(os.path.join(TARGET_DIR, f"finance_doc_{i}.txt"), "w") as f:
            f.write("CONFIDENTIAL DATA " * 50)

def launch_attack():
    print(f"--- LAUNCHING RANSOMWARE SIMULATION ---")
    time.sleep(3) # Wait for background execution
   
    for filename in os.listdir(TARGET_DIR):
        filepath = os.path.join(TARGET_DIR, filename)
        if not filename.endswith(".txt"): continue
       
        try:
            # RANSOMWARE PATTERN: Read -> Encrypt -> Write
            with open(filepath, "r") as f:
                data = f.read()
           
            encrypted = data[::-1] # Simple reversal encryption
           
            # This write happens milliseconds after the read
            with open(filepath, "w") as f:
                f.write(encrypted)
               
            print(f"[ATTACK] Encrypted {filename}")
        except:
            pass

if __name__ == "__main__":
    if not os.path.exists(TARGET_DIR): os.makedirs(TARGET_DIR)
    create_bait()
    input("Files created. Press ENTER to start the attack...")
    launch_attack()