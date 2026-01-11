# 🎓 SQL Audio Lessons

Convert your SQL learning materials into audio lessons that you can listen to!

---

## 📁 Folder Structure

```
audio_lessons/
├── play_lesson.py          # Main script to play lessons
├── lessons/                # Lesson scripts (.txt files)
│   ├── not_operator.txt
│   ├── limit_offset.txt
│   └── where_vs_having.txt
└── README.md              # This file
```

---

## 🚀 How to Use

### **1. Install Dependencies**

```bash
pip install google-cloud-texttospeech python-dotenv
```

### **2. Set Up Google Cloud (Optional - for TTS)**

If you want actual audio generation:

1. Create a Google Cloud account
2. Enable the Text-to-Speech API
3. Create a service account and download the JSON key
4. Set environment variable:
   ```bash
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\key.json
   ```

### **3. List Available Lessons**

```bash
python play_lesson.py list
```

### **4. Play a Lesson**

```bash
python play_lesson.py not_operator
python play_lesson.py limit_offset
python play_lesson.py where_vs_having
```

---

## 📝 Creating New Lessons

1. Create a new `.txt` file in the `lessons/` folder
2. Write your lesson in plain text (write it like you're speaking)
3. Run `python play_lesson.py your_lesson_name`

**Tips for writing lesson scripts:**
- ✅ Write like you're speaking (conversational)
- ✅ Spell out symbols: "greater than" not ">"
- ✅ Say "open parenthesis" and "close parenthesis"
- ✅ Break complex ideas into short sentences
- ✅ Add pauses with periods

---

## 📚 Available Lessons

### **1. NOT Operator** (`not_operator.txt`)
- What NOT does
- Using NOT with IN
- Why NOT IN is cleaner than multiple ANDs

### **2. LIMIT and OFFSET** (`limit_offset.txt`)
- Basic LIMIT syntax
- Combining with ORDER BY
- Using OFFSET for pagination
- Finding Nth highest values

### **3. WHERE vs HAVING** (`where_vs_having.txt`)
- Difference between WHERE and HAVING
- When to use each
- Step-by-step execution example

---

## 🎵 How It Works

1. **Read** the lesson script from `lessons/your_lesson.txt`
2. **Display** the text on screen
3. **Convert** text to speech using Google Cloud TTS
4. **Save** as MP3 file
5. **Auto-play** the audio

---

## 💡 Tips

- Listen while reviewing your written guides
- Play lessons during commute or exercise
- Create custom lessons for topics you find difficult
- Adjust speaking rate in `play_lesson.py` (line 35)

---

## 🔧 Customization

Edit `play_lesson.py` to change:
- **Voice**: Line 29 (`name="en-US-Neural2-J"`)
- **Speed**: Line 35 (`speaking_rate=0.95`)
- **Language**: Line 28 (`language_code="en-US"`)

Available voices: https://cloud.google.com/text-to-speech/docs/voices

---

## 📖 Example Lesson Script Format

```
Welcome to the lesson on SQL JOINs.

A JOIN combines rows from two or more tables based on a related column.

The most common type is INNER JOIN.

INNER JOIN returns only rows where there is a match in both tables.

For example, SELECT star FROM orders JOIN customers ON orders dot customer ID equals customers dot customer ID.

This returns only orders that have a matching customer.

End of lesson.
```

---

## 🚀 Quick Start

```bash
# List lessons
python play_lesson.py list

# Play a lesson
python play_lesson.py not_operator
```

Happy learning! 🎓
