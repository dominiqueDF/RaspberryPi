#!/usr/bin/env python3

##
#  Simulateur d'alarme en Python sur Raspberry Pi
#  Utilisation d'une LED
#  et d'un capteur PIR sur port GPIO
#  Utilisation d'un modem GSM sur port USB avec gammu

import RPi.GPIO as GPIO
import time
import gammu

# Préparation du modem pour envoi de SMS
sm = gammu.StateMachine()
sm.ReadConfig()
sm.Init()

# Préparation du message à envoyer
message = {
    'Text': 'Mouvement détecté',
    'SMSC': {'Location': 1},
    'Number': '0612345678'
}

# Configuration des ports GPIO du Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
PIR = 7
LED = 18
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# Compteur de mouvements
mvtsNbr = 0

try:
    print("Ready")
    while True:
        # Si détection sur l'entrée du capteur PIR
        if GPIO.input(PIR):
            print("Mouvement détecté")
            mvtsNbr += 1
            # Allumage de la LED
            GPIO.output(LED, GPIO.HIGH)
            # Envoi d'un SMS au bout de 3 mouvements détectés
            if mvtsNbr == 3:
                mvtsNbr = 0
                print("Send sms")
                sm.SendSMS(message)
        # Attente de 3 secondes        
        time.sleep(3)
        # Extinction de la LED
        GPIO.output(LED, GPIO.LOW)
# Sortie si CTRL+C au clavier        
except KeyboardInterrupt:
    print("Exit")
    GPIO.cleanup()
