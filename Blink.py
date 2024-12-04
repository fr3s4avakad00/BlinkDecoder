import cv2
import mediapipe as mp
import time


class BlinkMorseCode:
    """
    A class to detect eye blinks and convert them into Morse Code.
    """

    def __init__(self, blink_threshold=0.03):
        """
        Initializes the Mediapipe Face Mesh, blink detection parameters, and Morse code storage.

        :param blink_threshold: EAR threshold below which eyes are considered closed.
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=False)

        self.blink_threshold = blink_threshold
        self.blink_start_time = 0
        self.last_blink_end = time.time()
        self.morse_code = ""
        self.morse_code_map = {
            ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
            "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
            "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
            "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
            "-.--": "Y", "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
            "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7",
            "---..": "8", "----.": "9", ".-.-.-": ".", "-.-.--": "!", "--..--": ","
        }

    @staticmethod
    def eye_aspect_ratio(landmarks, eye_indices):
        """
        Calculates the Eye Aspect Ratio (EAR) based on given facial landmarks.

        :param landmarks: Mediapipe facial landmarks.
        :param eye_indices: Indices of the upper and lower eye landmarks.
        :return: EAR value.
        """
        top = landmarks[eye_indices[0]]
        bottom = landmarks[eye_indices[1]]
        return abs(top.y - bottom.y)

    def decode_morse_code(self, morse):
        """
        Decodes the Morse code into English text.

        :param morse: Morse code string.
        :return: Decoded English text.
        """
        words = morse.strip().split("   ")  # Split Morse code into words by 3 spaces
        decoded = ""
        for word in words:
            for letter in word.split():  # Split each word into letters by single space
                decoded += self.morse_code_map.get(letter, " ◊ ")  # Get character or "∆" for invalid codes
            decoded += " "
        return decoded.strip()

    def process_frame(self, frame, results):
        """
        Processes a single video frame to detect blinks and update Morse code.

        :param frame: Current video frame.
        :param results: Mediapipe face landmarks result.
        :return: Updated frame with annotations.
        """
        left_ear, right_ear = 0.0, 0.0  # Default EAR values

        # Check if face landmarks are detected
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw face mesh on the frame
                self.mp_drawing.draw_landmarks(
                    frame, face_landmarks, self.mp_face_mesh.FACEMESH_TESSELATION,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )

                # Eye landmark indices for Mediapipe Face Mesh
                left_eye = [159, 145]  # Upper and lower lid
                right_eye = [386, 374]  # Upper and lower lid

                # Calculate EAR for both eyes
                left_ear = self.eye_aspect_ratio(face_landmarks.landmark, left_eye)
                right_ear = self.eye_aspect_ratio(face_landmarks.landmark, right_eye)

                # Print EAR values for debugging
                print(f"Left EAR: {left_ear:.2f}, Right EAR: {right_ear:.2f}")

                # Blink detection
                if left_ear < self.blink_threshold and right_ear < self.blink_threshold:  # Eyes closed
                    if self.blink_start_time == 0:  # Start blink
                        self.blink_start_time = time.time()
                else:  # Eyes open
                    if self.blink_start_time > 0:  # End blink
                        blink_duration = time.time() - self.blink_start_time
                        print(f"Blink Duration: {blink_duration:.2f} seconds")
                        self.blink_start_time = 0

                        # Classify blink as DOT or DASH
                        if blink_duration < 0.4:  # DOT
                            self.morse_code += "."
                            print("Detected: DOT (short blink)")
                        elif blink_duration < 0.8:  # DASH
                            self.morse_code += "-"
                            print("Detected: DASH (long blink)")
                        self.last_blink_end = time.time()

                # Space detection logic
                if time.time() - self.last_blink_end > 1.0:  # Word space
                    if not self.morse_code.endswith("   "):
                        self.morse_code += "   "
                        print("Detected: WORD SPACE")
                        self.last_blink_end = time.time()
                elif time.time() - self.last_blink_end > 0.8:  # Letter space
                    if not self.morse_code.endswith(" "):
                        self.morse_code += " "
                        print("Detected: LETTER SPACE")
                        self.last_blink_end = time.time()

        # Display real-time Morse code
        cv2.putText(frame, f"Morse Code: {self.morse_code}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 
        # Show EAR values on the frame (optional for debugging)
        cv2.putText(frame, f"Left EAR: {left_ear:.2f}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"Right EAR: {right_ear:.2f}", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def run(self):
        """
        Runs the main loop for video capture and blink detection.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access the camera.")
            return

        print("Blink to generate Morse Code. Press 'Q' to exit.")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)  # Flip horizontally for natural view
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(rgb_frame)

                # Process the current frame
                frame = self.process_frame(frame, results)

                # Display the frame
                cv2.imshow("Blink Morse Code", frame)

                # Exit on 'Q' key
                key = cv2.waitKey(1)  # Wait for 1ms
                if key == ord('q') or key == 27:  # Check for 'Q' or ESC key
                    break
        except KeyboardInterrupt:
            print("\nExiting on user interrupt...")
        finally:
            cap.release()
            cv2.destroyAllWindows()

        # Decode the final Morse code
        decoded_message = self.decode_morse_code(self.morse_code)
        print(f"Final Morse Code: {self.morse_code}")
        print(f"Decoded Message: {decoded_message}")


if __name__ == "__main__":
    blink_morse_code = BlinkMorseCode()
    blink_morse_code.run()
