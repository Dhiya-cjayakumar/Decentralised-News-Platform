Decentralised News Platform
A secure and intelligent news platform that detects fake news using Reinforcement Learning (RL) and stores verified, trustworthy news on a Blockchain. Users can read, submit, and verify news, ensuring information integrity in the digital age.

Project Overview
The Decentralised News Platform is a web-based system where:
Users can view only trusted news detected by a machine learning model.
Registered users can submit news articles, with optional images.
A Reinforcement Learning algorithm checks whether the news is real or fake.
Admins approve verified news, which is then stored immutably on a blockchain using cryptographic hashing.

Technologies Used
Frontend: HTML5, CSS3, JavaScript
Backend: Django (Python)
Machine Learning: Reinforcement Learning (Q-Learning or DRL)
NLP Libraries: NLTK / spaCy / Scikit-learn
Blockchain: Python-based custom blockchain (for news storage via hash)
Database: SQLite / PostgreSQL (can be configured)

✨ Key Features
✅ View only trusted news verified by ML
🔐 Secure login and user management
📝 Submit news articles with optional images
🤖 Automated fake news detection using NLP and RL
⛓️ Admin-approved news is added to a blockchain for permanent storage
🔎 Tamper-proof news tracking via hash values

Installation & Setup
Clone the Repository
git clone https://github.com/your-username/Decentralised-News-Platform.git
cd Decentralised-News-Platform
Create Virtual Environment & Install Requirements
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
Run Migrations & Start Server
python manage.py migrate
python manage.py runserver
Access the Platform
Visit http://127.0.0.1:8000 in your browser.

Machine Learning Model
Type: Reinforcement Learning (e.g., Deep Q-Learning)
Input: News headline, body text
Output: Fake / Real classification
Training Data: Custom-labeled dataset or public datasets like LIAR or FakeNewsNet

🔐 Blockchain Logic
Each verified news article is:
Hashed (SHA-256)
Added to a new block
Stored in the blockchain ledger
Admin-only control for block creation ensures trust

📁 Project Structure (Example)
Decentralised-News-Platform/
├── blockchain/           # Blockchain logic
├── ml_model/             # RL model scripts
├── news_app/             # Django app for news management
├── templates/            # HTML templates
├── static/               # CSS/JS/images
├── manage.py
├── requirements.txt
└── README.md

Author
Dhiya C Jayakumar
B.Tech CSE
Vidya Academy of Science and Technology

