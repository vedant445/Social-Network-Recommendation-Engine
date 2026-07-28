# 🔥 Social Network Friend Recommendation Engine

A Python-based **Social Network Friend Recommendation System** built with **Streamlit** that simulates a real-world social networking platform. The application recommends friends based on user profiles, manages friend requests, detects friend communities, and provides an interactive dashboard for users.

---

## 📌 Features

- 👤 Create a personalized user profile
- 🤝 Intelligent friend recommendations
- 📤 Send friend requests
- 📥 Accept or reject incoming friend requests
- 📊 Track request status (Pending, Accepted, Rejected)
- 👥 Detect friend communities
- 🔄 Refresh recommendations dynamically
- 📈 Interactive dashboard built with Streamlit

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Logic |
| Streamlit | Web Interface |
| Pandas | Data Handling |
| NetworkX (Optional) | Graph Operations |
| Random | Recommendation Simulation |

---

## 📂 Project Structure

```
Social-Network-Friend-Recommendation/
│
├── app.py                  # Streamlit Application
├── social_network.py       # Recommendation Engine
├── requirements.txt
├── README.md
└── assets/
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/social-network-friend-recommendation.git
```

```bash
cd social-network-friend-recommendation
```

### 2. Create Virtual Environment (Optional)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your browser.

Default URL:

```
http://localhost:8501
```

---

## 📝 User Workflow

### Step 1

Create your profile by entering:

- Name
- Age
- City
- Interests
- Profession
- Skills
- Company
- Education
- Hobby
- Language

---

### Step 2

Generate personalized friend recommendations.

---

### Step 3

Select users and send friend requests.

---

### Step 4

Manage incoming requests by:

- Accepting
- Rejecting
- Leaving Pending

---

### Step 5

View

- Sent Requests
- Received Requests
- Overall Request Status
- Friend Communities

---

## 🧠 Recommendation Strategy

Recommendations are generated using profile similarity based on:

- Common interests
- Profession
- Skills
- City
- Education
- Company
- Mutual compatibility score

Each recommended user is assigned a recommendation score.

---

## 📊 Dashboard

The dashboard includes:

- Recommended Friends
- Incoming Requests
- Sent Requests
- Request Statistics
- Friend Communities

---

## 📸 Screenshots

Add screenshots here.

```
assets/
│
├── home.png
├── recommendations.png
├── requests.png
└── communities.png
```

Example:

```markdown
![Home](assets/home.png)
```

---

## 📦 Requirements

Example `requirements.txt`

```text
streamlit
pandas
networkx
```

Install using

```bash
pip install -r requirements.txt
```

---

## 🔮 Future Improvements

- AI-powered recommendation model
- Mutual friends recommendation
- Graph Neural Network (GNN) based recommendations
- User authentication
- Database integration (MySQL/PostgreSQL)
- Real-time notifications
- Chat functionality
- Friend suggestion explanation
- Community visualization using NetworkX

---

## 🎯 Learning Outcomes

This project demonstrates:

- Graph-based social networks
- Recommendation systems
- Python object-oriented programming
- Streamlit web development
- User interaction handling
- Data visualization
- Community detection concepts

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Vedant Maladkar**

B.Tech Data Science Student  
NMIMS MPSTME, Mumbai

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
