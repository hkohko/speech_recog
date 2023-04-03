import subprocess
import sys
import json
import random
import time
from vosk import Model, KaldiRecognizer, SetLogLevel
import word as custom_Word

print(f'\n thanks to Nikolaiev Dmytro (https://gist.github.com/Winston-503) for the nifty json-dict-to-sentence class\n')

SAMPLE_RATE = 16000

SetLogLevel(0)

model = Model(r"K:\python\speechrecog\vosk-model-en-us-0.22")
# model = Model(lang="en-us")
rec = KaldiRecognizer(model, SAMPLE_RATE)
rec.SetWords(True)

def rds():
    return random.randint(1, 5000)

def create_txt():
    global rdx
    rdx = str(int((rds()*rds())/rds()+1))
    with open(f'{rdx}-{file}.txt', 'w') as f:
        pass
    print(f"\nFile created: {rdx}-{file}.txt")
    with open(f'timestamp-{rdx}-{file}.txt', 'w') as f:
        pass
    print(f"\nFile created: timestamp-{rdx}-{file}.txt\n")
def recog():
    global file
    try:
        file = str(input('Filename: '))
        create_txt()
        results = []
        with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                                    f'{file}',
                                    "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                                    stdout=subprocess.PIPE) as process:

            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                elif rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    results.append(res)
                    with open(f'{rdx}-{file}.txt', 'a') as tr:
                        tr.write(f'{res["text"]}\n')
                        print(res["text"])
                        
        res = json.loads(rec.FinalResult())
        results.append(res)
        with open(f'{rdx}-{file}.txt', 'a') as tr:
            tr.write(f'{res["text"]}\n')
            print(res["text"])

        list_of_Words = []
        for sentence in results:
            if len(sentence) == 1:
                continue
            for obj in sentence['result']:
                w = custom_Word.Word(obj)
                list_of_Words.append(w)
        
        for word in list_of_Words:
            with open(f'timestamp-{rdx}-{file}.txt', 'a') as tb:
                tb.write(f'{word.to_string()}\n')
        recog()
    except KeyboardInterrupt:
        print("Exiting...")
        time.sleep(1)
        exit(0)
recog()