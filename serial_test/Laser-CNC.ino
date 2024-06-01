// int PUL = 5; //define Pulse pin
// int DIR = 4; //define Direction pin
// int ENA = 34; //define Enable Pin
// void setup() {
//   pinMode (PUL, OUTPUT);
//   pinMode (DIR, OUTPUT);
//   pinMode (ENA, OUTPUT);
// }

// void loop() {
//   for (int i = 0; i < 6400; i++) // Forward 5000 steps
//   {
//     digitalWrite(DIR, LOW);
//     digitalWrite(ENA, HIGH);
//     digitalWrite(PUL, HIGH);
//     delayMicroseconds(50);
//     digitalWrite(PUL, LOW);
//     delayMicroseconds(50);
//   }
//   for (int i = 0; i < 6400; i++) // Backward 5000 steps
//   {
//     digitalWrite(DIR, HIGH);
//     digitalWrite(ENA, HIGH);
//     digitalWrite(PUL, HIGH);
//     delayMicroseconds(50);
//     digitalWrite(PUL, LOW);
//     delayMicroseconds(50);
//   }
// }

// int Pos_x = 0;
// int Pos_y = 0;


// void Motor_1_L(int Pos_x) {
//   digitalWrite(4, HIGH);
//   digitalWrite(13, LOW);

//   for (Pos_x = 0; Pos_x < 1000; Pos_x++)

//   {
//     digitalWrite(5, HIGH);
//     delayMicroseconds(1000);
//     digitalWrite(5, LOW);
//     delayMicroseconds(1000);
//   }
// }

// void Motor_1_R(int Pos_x) {
//   digitalWrite(13, HIGH);
//   digitalWrite(4, LOW);

//   for (Pos_x = 0; Pos_x < 1000; Pos_x++) {
//     digitalWrite(5, HIGH);
//     delayMicroseconds(1000);
//     digitalWrite(5, LOW);
//     delayMicroseconds(1000);
//   }
// }

// void Motor_2_L(int Pos_x) {
//   digitalWrite(16, HIGH);
//   digitalWrite(2, LOW);

//   for (Pos_x = 0; Pos_x < 1000; Pos_x++) {
//     digitalWrite(18, HIGH);
//     delayMicroseconds(1000);
//     digitalWrite(18, LOW);
//     delayMicroseconds(1000);
//   }
// }

// void Motor_2_R(int Pos_x) {
//   digitalWrite(2, HIGH);
//   digitalWrite(16, LOW);

//   for (Pos_x = 0; Pos_x < 1000; Pos_x++) {
//     digitalWrite(18, HIGH);
//     delayMicroseconds(100);
//     digitalWrite(18, LOW);
//     delayMicroseconds(100);
//   }
// }


// void setup() {
//   pinMode(34, OUTPUT);  //Enable Stepp 1
//   pinMode(5, OUTPUT);   //Puls Stepp 1
//   pinMode(4, OUTPUT);   //Direction Stepp 1
//   pinMode(13, OUTPUT);  //Direction - Stepp 1

//   pinMode(35, OUTPUT);  //Enable Stepp 2
//   pinMode(18, OUTPUT);  //Puls Stepp 2
//   pinMode(16, OUTPUT);  //Direction Stepp 2
//   pinMode(2, OUTPUT);   //Direction - Stepp 2

//   digitalWrite(34, LOW);
//   digitalWrite(35, LOW);

//   Serial.begin(115200);  // Ensure the baud rate matches
//   Serial.println("ESP32 ready");
// }

// void loop() {

//   //Motor_2_L(Pos_x);
//   //Motor_2_R(Pos_x);
//   Motor_2_L(Pos_x);
//   //Motor_2_R(Pos_x);
// }

// //init
// //baud rate = 115200
// //Arduino datenempfangsbereit
// //Pi sendet Daten
// //loop Arduino
// //{
// //Daten empfangen
// //Pi in Pause setzen
// //prüfen, ob keine Koordinate mehr verfügbar, fortführen wenn Koordinate vorhanden
// //Daten zu Position umwandeln
// //Stepp mit for an Position senden und überprüfen
// //Laser einschalten
// //delay
// //Laser ausschalten
// //Arduino datenempfangsbereit
// //Pi fortsetzen
// //Pi sendet Daten
// //}

// //Func Motor 1
