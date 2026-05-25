# 🔐 Project 2 — Basic Encryption & Decryption

**DecodeLabs Cybersecurity Internship | Batch 2026**

---

## 📌 About
A Python program that encrypts and decrypts text using the **Caesar Cipher** technique. Built as Project 2 of the DecodeLabs Industrial Training Kit.

---

## ✅ Features
- Encrypts user text using Caesar Cipher logic
- Decrypts encrypted text back to original
- Displays both encrypted and decrypted output
- Handles spaces and punctuation (left unchanged)
- User can choose their own shift key
- Enhanced GUI with 4 tabs: Caesar, Vigenère, Brute Force, Frequency Analysis

---

## 🖥️ Screenshots

### CLI Version
<img width="1919" height="1023" alt="Screenshot 2026-05-25 221401" src="https://github.com/user-attachments/assets/cd9104fe-3135-469c-9285-300d6a374eb9" />

### Caesar Cipher Tab
<img width="786" height="731" alt="Screenshot 2026-05-25 222055" src="https://github.com/user-attachments/assets/a2caae08-2d78-492f-a6e7-1da6941b0ef9" />

### Vigenère Cipher Tab
<img width="779" height="718" alt="Screenshot 2026-05-25 222132" src="https://github.com/user-attachments/assets/6e11b272-2e35-4bbe-903e-43b7821f4a0b" />

### Brute Force Tab
<img width="782" height="724" alt="Screenshot 2026-05-25 222229" src="https://github.com/user-attachments/assets/26cbd2d5-d203-4f3b-a3be-84d325c95c00" />

### Frequency Analysis Tab
<img width="730" height="730" alt="Screenshot 2026-05-25 222416" src="https://github.com/user-attachments/assets/4c1c9cc0-7002-4d0e-8105-eff2af1c6f48" />

---

## 📁 Files
| File | Description |
|------|-------------|
| `caesar_cipher.py` | CLI version |
| `caesar_cipher_gui.py` | Enhanced PyQt5 GUI version |

---

## ▶️ How to Run

**CLI:**
```bash
python caesar_cipher.py
```

**GUI:**
```bash
pip install PyQt5 matplotlib
python caesar_cipher_gui.py
```

---

## 🧠 How It Works

**Encryption formula:**
```
E(x) = (x + n) % 26
```

**Decryption formula:**
```
D(x) = (x - n) % 26
```

Where `x` = letter position, `n` = shift key.

**Example with shift = 3:**
```
A → D
H → K
Hello World → Khoor Zruog
```

---

## 🧠 Concepts Used
- ASCII encoding — `ord()` converts letters to integers, `chr()` converts back
- Modular arithmetic `% 26` handles alphabet wrap-around
- Symmetric encryption — same key encrypts and decrypts
- Vigenère cipher — uses a repeating keyword instead of a fixed shift
- Brute force attack — demonstrates why Caesar cipher is weak (only 25 possible keys)
- Frequency analysis — letter distribution reveals patterns in ciphertext

---

## 🛠️ Built With
- Python 3
- PyQt5
- Matplotlib

---

*DecodeLabs Industrial Training Kit — Batch 2026*
