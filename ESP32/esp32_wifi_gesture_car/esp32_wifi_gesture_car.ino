#include <ArduinoOTA.h>

// #include <MUIU8g2.h>
#include <U8g2lib.h>
#include <U8x8lib.h>
#include <WiFi.h>
#include <WiFiMulti.h>
 
const char* ssid = "IITI_2.4";
const char* password =  "";
WiFiServer wifiServer(80);
WiFiMulti wifiMulti;

U8G2_SSD1306_128X32_UNIVISION_1_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE, /* clock=*/ SCL, /* data=*/ SDA);

int m1a = 16;
int m1b = 17;
int m2a = 18;
int m2b = 4;

const int STRAIGHT_SPEED = 255;
const int TURN_SPEED = 127;

const int M1_TRIM = -15;
const int M2_TRIM = 0;

char uploadStr[20];

void setup() {
 
  Serial.begin(115200);
  delay(1000);
  
  pinMode(m1a, OUTPUT);
  pinMode(m1b, OUTPUT);
  pinMode(m2a, OUTPUT);
  pinMode(m2b, OUTPUT);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);

  motorStop();

  u8g2.begin();
  // WiFi.begin(ssid, password);
 
  wifiMulti.addAP("IITI", "");
  wifiMulti.addAP("IITI_2.4G", "");
  wifiMulti.addAP("IITI_2.4", "");
 
  // while (WiFi.status() != WL_CONNECTED) {
  //   delay(1000);
  //   Serial.println("Connecting to WiFi..");
  // }

  Serial.print("Connecting to WiFi..");

  // Serial.print("Connecting WiFi..");
  while(wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
  }
 
  Serial.println("\nConnected to the WiFi network");
  Serial.println(WiFi.localIP());
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  
  ArduinoOTA.setPassword("admin");

  ArduinoOTA
    .onStart([]() {
      String type;
      if (ArduinoOTA.getCommand() == U_FLASH)
        type = "sketch";
      else // U_SPIFFS
        type = "filesystem";

      // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
      Serial.println("Start updating " + type);
    })
    .onEnd([]() {
      Serial.println("\nEnd");
      uploadStr[0] = '@';
    })
    .onProgress([](unsigned int progress, unsigned int total) {
      Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
      sprintf(uploadStr, "Progress: %u%%\r", (progress / (total / 100)));
    })
    .onError([](ota_error_t error) {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });

  uploadStr[0] = '@';
  // sprintf(uploadStr, "Progress: %u%%\r", 10);

  ArduinoOTA.begin();
 
  wifiServer.begin();
}
 
void loop() { 
  ArduinoOTA.handle();
 
  WiFiClient client = wifiServer.available();
  if (client) {
    while (client.connected()) {
      while (client.available()>0) {
        char c = client.read();
        // Serial.print(c);
        // client.write(c);
        switch(c) {
          case 'F': {
            Serial.println("Forward");
            motorForward(STRAIGHT_SPEED); 
            break;
          }
          case 'S': {
            Serial.println("STOP");
            motorStop() ;
            break;
          }
          case 'B': {
            Serial.println("Backward");
            motorBackward(STRAIGHT_SPEED);
            break;
          }
          case 'U': {
            Serial.println("Up");
            break;
          }
          case 'D': {
            Serial.println("Dowm");
            break;
          }
          case 'X': {
            Serial.println("Land");
            motorStop();
            break;
          }
          case 'L': {
            Serial.println("Left");
            motorLeft(TURN_SPEED) ;
            break;
          }
          case 'R': {
            Serial.println("Right");
            motorRight(TURN_SPEED);
            break;
          }
          case 'N': {
            Serial.println("NULL");
            motorStop();
            break;
          }
          default:
            break;
        }
      }     
      delay(2);
    }
    client.stop();
    Serial.println("Client disconnected");
 
  }
  u8g2.setFont(u8g2_font_helvR14_tn);
  u8g2.firstPage();
  do {
    if(uploadStr[0] == '@') {
      u8g2.setCursor(63 - (u8g2.getStrWidth("10.202.5.30")/2), 15 + (u8g2.getAscent()/2));
      u8g2.print(WiFi.localIP().toString());
    }
    else {
      u8g2.setFont(u8g2_font_helvR10_tr);
      u8g2.setCursor(0, u8g2.getAscent()+1);
      u8g2.print("Uploading...");
      u8g2.setCursor(0, u8g2.getAscent()+17);
      u8g2.print((const char*)uploadStr);
    }
  } while ( u8g2.nextPage() );
}

void motorForward(int speed) {
  analogWrite(m1a, speed+M1_TRIM);
  analogWrite(m1b, LOW);
  analogWrite(m2a, speed+M2_TRIM);
  analogWrite(m2b, LOW);
}

void motorBackward(int speed) {
  analogWrite(m1a, LOW);
  analogWrite(m1b, speed+M1_TRIM);
  analogWrite(m2a, LOW);
  analogWrite(m2b, speed+M2_TRIM);
}

// * IF CASTOR WHEEL IS BEHIND
// M1 is right motor
// M2 is left motor

void motorLeft(int turnSpeed) {
  analogWrite(m1a, turnSpeed+M1_TRIM);
  analogWrite(m1b, LOW);
  analogWrite(m2a, LOW);
  analogWrite(m2b, turnSpeed+M2_TRIM);
}

void motorRight(int turnSpeed) {
  analogWrite(m1a, LOW);
  analogWrite(m1b, turnSpeed+M1_TRIM);
  analogWrite(m2a, turnSpeed+M2_TRIM);
  analogWrite(m2b, LOW);
}

void motorStop() {
  analogWrite(m1a, LOW);
  analogWrite(m1b, LOW);
  analogWrite(m2a, LOW);
  analogWrite(m2b, LOW);
}
