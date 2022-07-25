/*

Need:

- a led with a 220 Ohm resistor, on pin 2 : indicates if the data are saved (led ON) or no (led OFF)
- a switch button on pin 4 (PULL-UP) : used to enable or desable the save data
- a push button on pin 7 (PULL-UP) : used to request to write in a new file
- a potentiometer on pin A5 : the data saved are the potentiometer's values

*/

// led save
const byte ledPin = 2;

// button to save a new file
const byte btnReadPin = 4;
byte btnReadState;
byte btnReadLastState;
unsigned long startTime;
bool startTimeResetRequested;

// button to create a new file
const byte btnNewPin = 7;
byte btnNewState;
byte btnNewLastState;
unsigned int btnNewDelay;
unsigned long lastTime;

// potentiometer
const byte potPin = A5;

const byte packageSize = 10;
byte  packageIndex;
String valuesToSend = "";

bool authorizedReading;

void setup() {
  Serial.begin(9600);
  
  pinMode(potPin, INPUT);
  pinMode(btnReadPin, INPUT_PULLUP);
  pinMode(btnNewPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  packageIndex = 0;
  authorizedReading = false;
  
  btnReadState = 1;
  btnReadLastState = btnReadState;
  btnNewState = 1;
  btnNewLastState = btnNewState;
  
  startTimeResetRequested = true;
  startTime = 0;
  btnNewDelay = 50;
  
  while (!Serial);
  lastTime = millis();
  Serial.println("Initialized");
  Serial.println("Led               pin: " + String(ledPin));
  Serial.println("Switch 'read'     pin: " + String(btnReadPin));
  Serial.println("Button 'new file' pin: " + String(btnNewPin));
  Serial.println("Potentiometer     pin: " + String(potPin));
  Serial.println("Package's size: " + String(packageSize));
  sendNew();
}

void loop() {
  checkReadSwitch();
  checkNewButton();
  if (!authorizedReading) {
    delay(100);
    return;
  }
  sendData();
  delay(10);
}

void checkReadSwitch() {
  btnReadState = digitalRead(btnReadPin);
  if (btnReadState != btnReadLastState) {
    authorizedReading = !((bool)btnReadState);
    digitalWrite(ledPin, authorizedReading);
    if (packageIndex != 0) {
      sendLast();
    }
    if (startTimeResetRequested) {
      resetStartTime();
    }
  }
  btnReadLastState = btnReadState;
}

void resetStartTime() {
  startTimeResetRequested = false;
  startTime = millis();
}

void checkNewButton() {
  if (millis() - lastTime > btnNewDelay) {
    lastTime = millis();
    btnNewState = digitalRead(btnNewPin);
    if (btnNewState != btnNewLastState && btnNewState == 0) {
      sendNew();
    }
    btnNewLastState = btnNewState;
  }
}

void sendNew() {
  if (packageIndex != 0) {
    sendLast();
  }
  startTimeResetRequested = true;
  Serial.println("-n 1");
  Serial.println("-mv 300");
  Serial.println("-aa 211 Potentiometer_position Time_(ms) Position");
  Serial.println("-aa 212 Potentiometer_variation Time_(ms) Varation");
  Serial.println("-al 1");
  Serial.println("-al 2");
  Serial.println("-cl 2 1 #1F85DE");
  Serial.println("-ml 1 1 None");
  Serial.println("-ml 2 1 None");
  Serial.println("-h Time_(ms) Position");
}

void sendData() {
  if (startTimeResetRequested) {
    resetStartTime();
  }
  valuesToSend += String(millis() - startTime) + " " + String(analogRead(potPin)) + " ; ";
  packageIndex++;
  if (packageIndex == packageSize) {
    sendLast();
  } 
}

void sendLast() {
  Serial.println("-lws 1 1 " + valuesToSend);
  delay(3); // add a little delay to be sure line is sent successfully (because it's a long line)
  Serial.println("-ld 1 1 2 1");
  packageIndex = 0;
  valuesToSend = "";
}
