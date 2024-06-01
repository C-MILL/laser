void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    String incoming = Serial.readStringUntil('\n');
    Serial.print("Received: ");
    Serial.println(incoming);
  }
  delay(1000); // Add a delay to avoid flooding the serial port
}
