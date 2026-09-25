# Telegram AI Image Generator Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![pyTelegramBotAPI](https://img.shields.io/badge/TelegramBotAPI-4.12%2B-blue.svg)](https://github.com/eternnoir/pyTelegramBotAPI)

A Telegram Bot that integrates with the **FusionBrain (Kandinsky) REST API** to generate AI images from text prompts in real-time.

---

## 🚀 Key Features

* **REST API Integration**: Direct communication with FusionBrain API for model polling, prompt execution, and result tracking.
* **Base64 Decoding**: Converts binary Base64 strings returned by the API into image formats using `Pillow`.
* **Async Polling**: Status checking mechanism handling async generation tasks.
* **Automatic Resource Cleanup**: Ensures temporary generated image files are safely removed post-delivery.

---

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **Framework**: pyTelegramBotAPI
* **API Handling**: Requests, JSON, Base64
* **Image Processing**: Pillow (PIL)

---

## ⚙️ Configuration & Setup

### 1. Clone the repository
git clone [https://github.com/DrRafael/telegram-ai-image-generator.git](https://github.com/DrRafael/telegram-ai-image-generator.git)
cd telegram-ai-image-generator

### 2. Install dependencies
pip install -r requirements.txt

### 3. Configure API Credentials
Create a `config.py` file in the root directory:
```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
API_KEY = "YOUR_FUSIONBRAIN_API_KEY"
SECRET_KEY = "YOUR_FUSIONBRAIN_SECRET_KEY"
