#include <ESP8266WiFi.h>
#include <Blynk.h>
#include <BlynkSimpleEsp8266.h>
//#include <SPI.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS D2  // D2 = GPI04
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

#define BLYNK_PRINT Serial
BlynkTimer timer;

#define DHTTYPE DHT11    // DHT 11
#define dpin 0           //  dpin = pin 0 = D3  - connection for DHT11
DHT dht(dpin, DHTTYPE);  // dht is dht sensor number 1 (or we can write dht1)

int sensorPin = 5;  // Digital input from moisture sensor - D1 = GPI05
int output_value;

const int relayEnable = 2;  // D4= GPI02


char auth[] = "";  //Authentication code sent by Blynk
char ssid[] = "";  //WiFi SSID
char pass[] = "";  // Wifi password

namespace pin {
const byte tds_sensor = A0;  // TDS Sensor
}

namespace device {
float aref = 3.3;
}

namespace sensor {
float ec = 0;
unsigned int tds = 0;
float ecCalibration = 1;
}

void myTimerEvent() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int sensorValue = digitalRead(sensorPin);
  sensorValue = map(sensorValue, 1, 0, 0, 100);

  sensors.requestTemperatures();
  Serial.println(sensors.getTempCByIndex(0));  // water temp
  double waterTemp = sensors.getTempCByIndex(0);
  // waterTemp  = waterTemp*0.0625; // conversion accuracy is 0.0625 / LSB
  float rawEc = analogRead(pin::tds_sensor) * device::aref / 1024.0;  // aref = 3.3
                                                                      // read the analog value more stable by the median filtering algorithm, and convert to voltage value
  float temperatureCoefficient = 1.0 + 0.02 * (waterTemp - 25.0);
  // temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
  sensor::ec = (rawEc / temperatureCoefficient) * sensor::ecCalibration;
  // temperature and calibration compensation
  sensor::tds = (133.42 * pow(sensor::ec, 3) - 255.86 * sensor::ec * sensor::ec + 857.39 * sensor::ec) * 0.5;

  Blynk.virtualWrite(V0, sensorValue);               // V0 for moisture level
  Blynk.virtualWrite(V1, h);                         // V1 for Humidity value
  Blynk.virtualWrite(V2, t);                         //V2 is for Temperature
  Blynk.virtualWrite(V3, sensor::tds);               //V3 is for TDS value
  Blynk.virtualWrite(V4, waterTemp);                 // DS18B20: water temp
  Blynk.virtualWrite(V5, (32 + (1.8 * waterTemp)));  // DS18B20


  if (sensor::tds > 40) {
    Blynk.notify((String) "TDS value of water is  " + sensor::tds + " ppm");
    delay(1000);
  }
  if (t > 40) {
    Blynk.notify("Temperature over 40C!");
    delay(1000);
  }

  /* if (sensorValue < 20){
      Blynk.notify("Low Soil moisture level! Water supply is turned on!!");
      delay(1000);
    }*/
}

void setup()  // Runs first
{

  Serial.begin(115200);
  timer.setInterval(10000L, myTimerEvent);  // PUSH data every 5 seconds

  pinMode(relayEnable, OUTPUT);  // relayEnable = pin 2 - D4
  pinMode(sensorPin, INPUT);     // sensorPin = D1

  Blynk.begin(auth, ssid, pass);

  dht.begin();      // already specified pin 0 = D3
  sensors.begin();  // DS18B20
  Serial.println("Reading From the Sensors ...");
  delay(1000);
}



void loop() {
  // put your main code here, to run repeatedly:

  Blynk.run();
  timer.run();

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  Serial.print("Current humidity = ");
  Serial.print(h);
  Serial.print("%  ");
  Serial.print("temperature = ");
  Serial.print(t);
  Serial.println("C  ");


  int sensorValue = digitalRead(sensorPin);
  sensorValue = map(sensorValue, 1, 0, 0, 100);
  Serial.print("Mositure level = ");
  Serial.print(sensorValue);
  Serial.println("%");

  if (sensorValue < 20) {
    digitalWrite(relayEnable, LOW);
    Serial.println("Relay ON");
  } else {
    digitalWrite(relayEnable, HIGH);
    Serial.println("Relay OFF");
  }

  sensors.requestTemperatures();  // Send the command to get temperature readings

  Serial.print("Water Temperature is: ");

  Serial.println(sensors.getTempCByIndex(0));
  double waterTemp = sensors.getTempCByIndex(0);
  // waterTemp  = waterTemp*0.0625; // conversion accuracy is 0.0625 / LSB

  float rawEc = analogRead(pin::tds_sensor) * device::aref / 1024.0;

  // read the analog value more stable by the median filtering algorithm, and convert to voltage value

  float temperatureCoefficient = 1.0 + 0.02 * (waterTemp - 25.0);

  // temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));

  sensor::ec = (rawEc / temperatureCoefficient) * sensor::ecCalibration;  // temperature and calibration compensation
  sensor::tds = (133.42 * pow(sensor::ec, 3) - 255.86 * sensor::ec * sensor::ec + 857.39 * sensor::ec) * 0.5;

  //convert voltage value to tds value

  Serial.println((String) "TDS: " + sensor::tds + " ppm");
  Serial.print(F("EC:"));
  Serial.println(sensor::ec, 2);
  Serial.print(F(" Water Temperature:"));
  Serial.println(waterTemp, 2);
  Serial.print(F(""));
  delay(1000);
}


/* Map function - 

map(value, fromLow, fromHigh, toLow, toHigh)

Parameters

value: the number to map.
fromLow: the lower bound of the value’s current range.
fromHigh: the upper bound of the value’s current range.
toLow: the lower bound of the value’s target range.
toHigh: the upper bound of the value’s target range.

*/
