# **BlinkDecoder**

This project is a simple Python program that uses your webcam to detect eye blinks and turn them into Morse Code. The program uses **OpenCV** to process video and **Mediapipe** to detect your face and eyes. You can blink in short or long patterns to spell out messages in Morse Code, which the program will translate into text.

---

## **What It Can Do**
- Detect eye blinks in real-time using your webcam.
- Convert blinks into Morse Code:
  - Short blink → `DOT (.)`
  - Long blink → `DASH (-)`
- Automatically decode the Morse Code into English text.
- Show what’s happening on your webcam feed, including:
  - Your current Morse Code.
  - Debug values for detecting your eye state (EAR).

---

## **How It Works**
1. **Detecting Your Eyes**:
   - The program uses Mediapipe's **Face Mesh** to identify key points on your face.
   - It calculates how open your eyes are by measuring the distance between specific points (Eye Aspect Ratio or EAR).

2. **Blinks**:
   - When your eyes close for a short time, it records a `DOT`.
   - When your eyes stay closed longer, it records a `DASH`.

3. **Morse Code Translation**:
   - As you blink, it builds a string of `DOTs` and `DASHes`.
   - When you stop blinking, it decodes your Morse Code into regular letters or numbers.

---

## **What You Need to Set It Up**

### **Things You’ll Need**
- Python (Version **3.7 to 3.10**).
- A computer with a webcam.
- The following Python libraries:
  - `opencv-python`
  - `mediapipe`

---

### **How to Set It Up**

1. **Download the Code**:
   - Clone this repository or copy the `blink_morse_code.py` file into a folder on your computer.

2. **Set Up Python**:
   - Make sure Python is installed.
   - Open your terminal or command prompt, and set up a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # For Mac or Linux
     venv\Scripts\activate     # For Windows
     ```

3. **Install the Required Libraries**:
   - Run this command to install the necessary Python libraries:
     ```bash
     pip install opencv-python mediapipe
     ```

4. **Run the Program**:
   - Type this command to start the program:
     ```bash
     python blink_morse_code.py
     ```

---

## **How to Use It**

1. **Start the Program**:
   - When you start the program, it will access your webcam.

2. **Blinking for Morse Code**:
   - Blink quickly for a **DOT (.)**.
   - Blink longer for a **DASH (-)**.

3. **Pausing Between Letters or Words**:
   - Pause for **0.8–1 second** for a **letter space**.
   - Pause for **1 second or more** for a **word space**.

4. **Exit**:
   - Press **`Q`** or the **ESC key** to quit the program.

5. **See Your Translated Message**:
   - After exiting, the program will print the Morse Code and the decoded message in the terminal.

---

## **Code Basics**

### **What the Program Does**
- **Tracks Your Eyes**: Finds key points on your face to measure how open your eyes are.
- **Detects Blinks**: Checks when your eyes are closed and for how long.
- **Builds Morse Code**: Adds `DOTs`, `DASHes`, and spaces as you blink.
- **Translates Code**: Turns the Morse Code into plain English when you're done.

### **Main Parts of the Code**
1. **Eye Aspect Ratio (EAR)**:
   - Measures how open or closed your eyes are.
   - Helps figure out if you’re blinking.

2. **Blink Classification**:
   - Short blink → `DOT`.
   - Long blink → `DASH`.

3. **Morse Code Translation**:
   - The program keeps a list of all `DOTs` and `DASHes` and translates them using a pre-defined dictionary.

---

## **What You'll See While Running**
- **On Your Webcam Feed**:
  - The current Morse Code displayed on the screen.
  - EAR values to show how open or closed your eyes are.

- **In the Terminal**:
  - It will print messages like:
    ```
    Detected: DOT (short blink)
    Detected: DASH (long blink)
    Current Morse Code: .... . .-.. .-.. ---
    ```

---

## **Examples**

1. Start the program:
   ```bash
   python blink_morse_code.py
   ```

2. Blink the code for "HELLO":
   - Blink short-short-short-short (....).
   - Blink short (.) for `E`.
   - Blink long-short-long-short (.-..).
   - Blink long-short-long-short again (.-..).
   - Blink long-long-long (---).

3. Exit the program by pressing `Q`.

4. See the result in the terminal:
   ```
   Final Morse Code: .... . .-.. .-.. ---
   Decoded Message: HELLO
   ```

---

## **What If Something Doesn't Work?**

### **Common Issues**
1. **Webcam Not Working**:
   - Check that no other app is using your webcam.
   - Restart the program.

2. **Eye Detection Not Accurate**:
   - Make sure you're in a well-lit room.
   - Keep your face in front of the camera.

3. **Program Too Slow**:
   - Reduce the resolution of the webcam in the code to improve speed.

---

## **Extra Stuff You Can Do**

1. **Adjust Blink Sensitivity**:
   - Change the `blink_threshold` to make it more or less sensitive to blinks:
     ```python
     blink_morse_code = BlinkMorseCode(blink_threshold=0.04)
     ```

2. **Customize the Morse Code Translation**:
   - Add new symbols or rules to the `morse_code_map` dictionary.

3. **Modify the Display**:
   - Update the `cv2.putText` lines to change what is shown on the video feed.

---

## **Dependencies**
- **OpenCV**: Handles the webcam and displays the video feed.
- **Mediapipe**: Detects your face and eyes for blink tracking.

---

## **Credits**
- Developed using **Google Mediapipe** for facial landmark detection.
- Utilizes **OpenCV** for video capture and visualization.

---
