# Contributing to ClearPath Financing 🚀

First off, **thank you** for considering contributing to ClearPath Financing! It's people like you who make the open-source community such an amazing place to learn, inspire, and create.

This is a **beginner-friendly** project, and we welcome contributions from everyone—whether you're a seasoned developer or just writing your first line of code.

## 📜 Table of Contents
1.  [Code of Conduct](#code-of-conduct)
2.  [How Can I Contribute?](#how-can-i-contribute)
    *   [Reporting Bugs](#reporting-bugs)
    *   [Suggesting Enhancements](#suggesting-enhancements)
    *   [Your First Code Contribution](#your-first-code-contribution)
3.  [Development Setup Guide](#development-setup-guide)
4.  [Style Guidelines](#style-guidelines)
5.  [Pull Request Process](#pull-request-process)

---

## 🤝 Code of Conduct
This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainer.

> **tl;dr:** Be respectful, be kind, and help each other learn.

---

## 🛠 How Can I Contribute?

### 🐛 Reporting Bugs
If you find a bug (e.g., the calculator gives a wrong number, or the graph doesn't load), please create a **New Issue** using the following format:
*   **Title:** Clear description of the error.
*   **Steps to Reproduce:** 1. Go to page X, 2. Click button Y...
*   **Expected Behavior:** What should have happened?
*   **Screenshots:** If possible, add a screenshot.

### ✨ Suggesting Enhancements
Have an idea for a new feature? (e.g., "Add a Dark Mode toggle" or "Add an Insurance Calculator").
*   Open a **New Issue** with the label `enhancement`.
*   Explain why this feature would be useful to users.

### 💻 Your First Code Contribution
Unsure where to begin? You can look through the **Issues** tab for:
*   **`good first issue`**: These are small tasks intended for newcomers.
*   **`help wanted`**: These are tasks that need extra attention.

---

## ⚙️ Development Setup Guide

Follow these steps to set up the project locally on your machine.

### 1. Prerequisites
Ensure you have the following installed:
*   **Node.js** (v16 or higher)
*   **Python** (v3.10 or higher)
*   **MySQL Server** (v8.0)

### 2. Fork and Clone
1.  Click the **Fork** button at the top right of this page.
2.  Clone your forked repository:
    ```bash
    git clone https://github.com/YOUR-USERNAME/clearpath-financing.git
    cd clearpath-financing
    ```

### 3. Backend Setup (Python Flask)
1.  Navigate to the backend folder:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Database Configuration:**
    *   Open `app.py`.
    *   Update the `SQLALCHEMY_DATABASE_URI` line with your MySQL username and password:
        `mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/clearpath_db`
4.  Run the server:
    ```bash
    python app.py
    ```
    *Server should run at `http://127.0.0.1:5000`*

### 4. Frontend Setup (React Vite)
1.  Open a **new terminal** and navigate to the frontend folder:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    *App should run at `http://localhost:5173`*

---

## 🎨 Style Guidelines

### Python (Backend)
*   Follow **PEP 8** style guidelines.
*   Use clear variable names (e.g., `loan_amount` instead of `x`).
*   Add comments for complex logic (especially in the `calculate_true_cost` function).

### React (Frontend)
*   Use **Functional Components** with Hooks.
*   Keep components small and reusable.
*   Use **Tailwind CSS** classes for styling (avoid inline styles).

---

## 🔀 Pull Request Process

1.  **Create a Branch:** Always create a new branch for your work.
    ```bash
    git checkout -b feature/AmazingFeature
    ```
2.  **Commit Changes:** Write clear, descriptive commit messages.
    ```bash
    git commit -m "Add a new slider for down payment"
    ```
3.  **Push:** Push your branch to your fork.
    ```bash
    git push origin feature/AmazingFeature
    ```
4.  **Open a PR:** Go to the original repository and click **"Compare & pull request"**.
    *   Describe what you changed.
    *   Link any related Issues (e.g., "Closes #12").

---

## ❓ Need Help?
If you get stuck, feel free to open a **Discussion** or comment on an Issue. We are happy to help you get your environment set up!

**Happy Coding!** 🚀
