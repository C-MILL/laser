// void setup() {
//   Serial.begin(115200);
// }

// void loop() {
//   if (Serial.available() > 0) {
//     String command = Serial.readStringUntil('\n');
//     if (command == "PING") {
//       Serial.println("PONG");
//     } else {
//       Serial.print("Received: ");
//       Serial.println(command);
//       if (command == "10L") {
//         // Handle 10 steps left
//         Serial.println("Confirmed 10 steps left");
//       } else if (command == "10R") {
//         // Handle 10 steps right
//         Serial.println("Confirmed 10 steps right");
//       }
//     }
//   }
// }
