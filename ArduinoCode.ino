/********************************************************************
 *  ESP32‑WROOM‑32D  |  Joystick (ADC) + NeoPixel ring (GPIO18)
 *  --------------------------------------------------------------
 *  • Sends:  UP / DOWN / LEFT / RIGHT / CENTER / PRESS   @115200 Bd
 *  • Receives:  GAME_START  or  GAME_END   (single tokens, \n‑ended)
 *    — both play the same rainbow‑swirl for ~3s.
 ********************************************************************/
#include <Adafruit_NeoPixel.h>
#include <driver/i2s.h>
#include <DFRobotDFPlayerMini.h> 

/* ----------------  USER WIRING  ---------------- */
#define JOY_X_PIN    27          // ADC2_CH7
#define JOY_Y_PIN    26          // ADC2_CH9
#define JOY_BTN_PIN  25          // LOW when pressed

#define RING_PIN     18          // DIN for WS2812 ring
#define NUM_LEDS     16

#define DF_RX 13    // ESP32  -> DFPlayer TX
#define DF_TX 4    // ESP32  -> DFPlayer RX

#define CENTER_X     2350
#define CENTER_Y     2600
#define DEADZONE     500
/* ---------------------------------------------- */

Adafruit_NeoPixel ring(NUM_LEDS, RING_PIN, NEO_GRB + NEO_KHZ800);

HardwareSerial dfSerial(2);           // use UART2
DFRobotDFPlayerMini dfplayer;

/* ------------ helpers ------------ */
String getDirection(int x, int y) {
  int dx = x - CENTER_X;
  int dy = y - CENTER_Y;
  long distSq = (long)dx * dx + (long)dy * dy;
  if (distSq < (long)DEADZONE * DEADZONE) return "CENTER";

  float angle = atan2(dy, dx) * 180.0 / PI;
  if      (angle >= -45 && angle <  45)   return "RIGHT";
  else if (angle >=  45 && angle < 135)   return "DOWN";
  else if (angle >= 135 || angle < -135)  return "LEFT";
  else                                    return "UP";
}

void showRainbow3s() {
  const uint32_t t_end = millis() + 3000;          // 3s
  while (millis() < t_end) {
    static uint16_t hue = 0;
    ring.rainbow(hue);
    ring.show();
    hue += 256;                                    // ~1rev pers
    delay(5);
  }
  ring.clear();
  ring.show();
}

void setup() {
  Serial.begin(115200);
  pinMode(JOY_BTN_PIN, INPUT_PULLUP);

  ring.begin();
  ring.clear();
  ring.show();

  dfSerial.begin(9600, SERIAL_8N1, DF_RX, DF_TX);
  if (dfplayer.begin(dfSerial)) {
    dfplayer.volume(25);                 // 0‑30
  } 
  else {
    Serial.println("DFPlayer init failed");
  }
}

void loop() {
  /* ---------- 1)  check inbound commands ---------- */
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "GAME_START" || cmd == "GAME_END") {
      showRainbow3s();
    }
    else if (cmd == "START_SND") {       // start‑button click
      dfplayer.stop();
      dfplayer.play(1);
    }
    else if (cmd == "END_SND") {         // winner screen
      dfplayer.play(2);
    }
    else if (cmd == "BG_START") {        // loop background
      dfplayer.loop(3);                  // /01/0003_BackgroundSound.mp3
    }
    else if (cmd == "BG_STOP") {         // stop loop
      dfplayer.stop();
     }
  }

  /* ---------- 2)  joystick → Serial prints ---------- */
  int joyX = analogRead(JOY_X_PIN);
  int joyY = analogRead(JOY_Y_PIN);
  int btn  = digitalRead(JOY_BTN_PIN);

  if (btn == LOW) {
    Serial.println("PRESS");
    delay(100);
    return;
  }

  String dir = getDirection(joyX, joyY);
  Serial.println(dir);

  delay(100);                          // 10Hz sample like original
}
