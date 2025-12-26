# 🏠 ClearPath Financing

![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)
![First Repo](https://img.shields.io/badge/First%20Open%20Source%20Project-blue)
![Stack](https://img.shields.io/badge/React-Python-MySQL-blueviolet)

> **A Privacy-First Mortgage Intelligence System built as a Progressive Web App (PWA).**

---

## 👋 A Note from the Creator

**Hello! This is my first ever Open Source repository.** 🚀

I built **ClearPath Financing** to solve a real problem: Mortgage calculators today hide costs and steal user data. I wanted to build a **Privacy-First** alternative that calculates the *True Cost* of ownership without asking for a phone number.

**I am looking for contributors!** Whether you are a student, a beginner, or a pro, I would love your help to improve this code, fix bugs, or add new features.

---

## 📖 About The Project

ClearPath Financing is a Full-Stack PWA that helps users analyze debt without the fear of spam calls.

**Key Modules:**
1.  **True_Worth:** A calculator that adds hidden costs (Tax + Maintenance) to the EMI.
2.  **Trends:** A real-time graph showing historical interest rate movements.
3.  **Exposure:** A comparison tool for bank offers vs. verified agents.
4.  **Privacy:** Uses anonymous UUIDs instead of login/email.

---

## 🛠️ Tech Stack

*   **Frontend:** React.js (Vite), Tailwind CSS, Framer Motion, Recharts.
*   **Backend:** Python (Flask), SQLAlchemy.
*   **Database:** MySQL.
*   **Deployment:** Netlify (Frontend), Render (Backend - *Work in Progress*).

---

## 🤝 How You Can Help (Call for Contributors)

I need help with the following tasks. Please feel free to pick any!

### 🟢 Beginner Friendly (Good First Issues)
- [ ] Improve the mobile responsiveness of the Navbar.
- [ ] Add tooltips to explain terms like "Repo Rate" or "Stamp Duty".
- [ ] Fix typo errors in the text content.
- [ ] Create a "404 Not Found" page in React.

### 🟡 Intermediate
- [ ] **PDF Export:** Implement `jspdf` to let users download their loan summary.
- [ ] **Dark/Light Mode:** Add a toggle to switch themes.
- [ ] **Form Validation:** Improve input checks in the Calculator.

### 🔴 Advanced
- [ ] **Insurance Module:** Create a new page for Health Insurance analysis.
- [ ] **Rate Limiting:** Add `Flask-Limiter` to the Python backend to prevent spam.
- [ ] **Docker:** Dockerize the application for easier setup.

---

## 🚀 Getting Started (Run it Locally)

If you want to contribute, here is how to run the project on your machine.

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/clearpath-financing.git
cd clearpath-financing
