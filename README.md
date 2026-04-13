# 💸 ExpenseManager

A modern, interactive web-based expense tracking application built with **Streamlit** and **SQLite**, with seamless integration to **Google Sheets** for cloud synchronization.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Contributing](#contributing)

---

## ✨ Features

- **Multi-User Support**: Track expenses for multiple users
- **Category Management**: Organize expenses into custom categories
- **Interactive Dashboard**: Visualize spending patterns with charts and graphs
- **Google Sheets Integration**: Automatically sync expenses to Google Sheets
- **Expense Tracking**: Add, view, and manage expenses with detailed notes
- **Data Filtering**: Filter expenses by month and year
- **Responsive UI**: Clean, modern interface with custom styling
- **Configuration Panel**: Easy setup and management of users and categories

---

## 📁 Project Structure

```
ExpenseManager/
├── webapp.py                 # Main Streamlit application
├── css.py                    # Custom CSS and styling
├── requirements.txt          # Python dependencies
├── credentials.json          # Google API credentials (not in repo)
├── backend/
│   ├── db.py                # SQLite database management
│   └── sheets.py            # Google Sheets integration
├── pages/
│   ├── add_expense.py        # Add expense page
│   ├── dashboard.py          # Dashboard with analytics
│   ├── details.py            # Expense details and history
│   ├── configuration.py      # User and category configuration
│   └── developer_info.py     # Developer information
└── myenv/                    # Python virtual environment
```

---

## 📦 Prerequisites

- **Python 3.8+**
- **Pip** (Python package installer)
- **Google Cloud Project** with Sheets and Drive API enabled
- **Google Service Account** credentials

---

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd ExpenseManager
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

### 3. Activate the Virtual Environment

**On Windows:**
```bash
myenv\Scripts\activate
```

**On macOS/Linux:**
```bash
source myenv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Google Sheets Setup

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project

2. **Enable Required APIs**:
   - Enable Google Sheets API
   - Enable Google Drive API

3. **Create a Service Account**:
   - Go to "Service Accounts" in your project
   - Create a new service account
   - Generate a JSON key file
   - Save it as `credentials.json` in the project root

4. **Create a Google Sheet**:
   - Create a new Google Sheet named exactly **"ExpenseManager"**
   - Share the sheet with the service account email

5. **Add Credentials**:
   - Place `credentials.json` in the project root directory
   - **Note**: Add `credentials.json` to `.gitignore` to protect sensitive data

### Optional: Streamlit Secrets

For production, store credentials in Streamlit secrets instead of a local file:
- Create `.streamlit/secrets.toml`
- Add your Google credentials in the `secrets.toml` file

---

## 📖 Usage

### Run the Application

```bash
streamlit run webapp.py
```

The application will open at `http://localhost:8501` in your browser.

### Navigation

The app includes the following sections:

#### **User Section**
- **Details**: View expense history and detailed breakdowns

#### **Tools Section**
- **Add Expenses**: Create new expense records with user, category, and notes
- **Dashboard**: View analytics and visualizations of spending patterns
- **Configuration**: Manage users and expense categories

#### **Info Section**
- **Developer Info**: Information about the developer and project

---

## 🗄️ Database Schema

The application uses SQLite with the following structure:

### Users Table
```sql
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Category Table
```sql
CREATE TABLE Category (
    cat_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE
)
```

### Expenses Table
```sql
CREATE TABLE Expenses (
    exp_id INTEGER PRIMARY KEY,
    cat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    amount DECIMAL NOT NULL,
    note TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(cat_id) REFERENCES Category(cat_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
)
```

**Design Note**: Category IDs are stored instead of category names to optimize database storage and maintain referential integrity.

---

## 🔧 Key Technologies

| Library | Purpose |
|---------|---------|
| **Streamlit** | Web framework for building interactive apps |
| **SQLite3** | Local database engine |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive charts and visualizations |
| **gspread** | Google Sheets API client |
| **google-auth-oauthlib** | Google OAuth authentication |

---

## 📝 Default Setup

On first run, the application automatically:
- Creates the SQLite database (`backend/expenses.db`)
- Creates all required tables (Users, Category, Expenses)
- Populates default sample data if tables are empty

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request with a clear description

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Support

For issues or questions, please refer to the Developer Info page within the application or contact the developer.

---

**Happy Expense Tracking! 💰**
