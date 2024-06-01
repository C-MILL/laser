#include <AccelStepper.h>

long receivedMMdistance = 0; // distance in mm from the computer
long receivedDelay = 0; // delay between two steps, received from the computer
long receivedAcceleration = 0; // acceleration value from computer
char receivedCommand; // character for commands
/* s = Start (CCW) // needs steps and speed values
 * b = open stepper 2 (CCW) // needs steps and speed values
 * p = open stepper 1 (CCW) // needs steps and speed values
 * c = close (CW) // needs steps and speed values
 * a = set acceleration // needs acceleration value
 * n = stop right now! // just the 'n' is needed
 */

bool newData, runallowed = false; // booleans for new data from serial, and runallowed flag

// direction Digital 9 (CCW), pulses Digital 8 (CLK)
AccelStepper stepper1(1, 5, 4);
AccelStepper stepper2(1, 18, 16);

void setup()
{
  Serial.begin(9600); // define baud rate
  Serial.println("Testing Accelstepper"); // print a message

  // setting up some default values for maximum speed and maximum acceleration
  stepper1.setMaxSpeed(2000); // SPEED = Steps / second
  stepper1.setAcceleration(1000); // ACCELERATION = Steps /(second)^2
  stepper2.setMaxSpeed(2000); // SPEED = Steps / second
  stepper2.setAcceleration(1000); // ACCELERATION = Steps /(second)^2

  stepper1.disableOutputs(); // disable outputs, so the motor is not getting warm (no current)
  stepper2.disableOutputs(); // disable outputs, so the motor is not getting warm (no current)
}

void loop()
{
  checkSerial(); // check serial port for new commands
  continuousRun(); // method to handle the motors
}

void continuousRun() // method for the motors
{
  if (runallowed == true)
  {
    if (abs(stepper1.currentPosition()) < receivedMMdistance || abs(stepper2.currentPosition()) < receivedMMdistance) // abs() is needed because of the '<'
    {
      stepper1.enableOutputs(); // enable pins
      stepper2.enableOutputs(); // enable pins
      stepper1.run(); // step the motor (this will step the motor by 1 step at each loop)
      stepper2.run(); // step the motor (this will step the motor by 1 step at each loop)
    }
    else // program enters this part if the required distance is completed
    {
      runallowed = false; // disable running -> the program will not try to enter this if-else anymore
      stepper1.disableOutputs(); // disable power
      stepper2.disableOutputs(); // disable power
      Serial.print("POS1: ");
      Serial.println(stepper1.currentPosition()); // print pos -> this will show you the latest relative number of steps
      Serial.print("POS2: ");
      Serial.println(stepper2.currentPosition()); // print pos -> this will show you the latest relative number of steps
      stepper1.setCurrentPosition(0); // reset the position to zero
      stepper2.setCurrentPosition(0); // reset the position to zero
      Serial.print("POS1: ");
      Serial.println(stepper1.currentPosition()); // print pos -> this will show you the latest relative number of steps; we check here if it is zero for real
      Serial.print("POS2: ");
      Serial.println(stepper2.currentPosition()); // print pos -> this will show you the latest relative number of steps; we check here if it is zero for real
    }
  }
  else // program enters this part if the runallowed is FALSE, we do not do anything
  {
    return;
  }
}

void checkSerial() // method for receiving the commands
{  
  if (Serial.available() > 0) // if something comes
  {
    receivedCommand = Serial.read(); // this will read the command character
    newData = true; // this creates a flag
  }

  if (newData == true) // if we received something (see above)
  {
    // START - MEASURE
    if (receivedCommand == 's') // this is the measure part
    {
      runallowed = true; // allow running
      receivedMMdistance = Serial.parseFloat(); // value for the steps
      receivedDelay = Serial.parseFloat(); // value for the speed

      Serial.print(receivedMMdistance); // print the values for checking
      Serial.print(receivedDelay);
      Serial.println(" Measure"); // print the action
      stepper1.setMaxSpeed(receivedDelay); // set speed
      stepper1.move(receivedMMdistance); // set distance
      stepper2.setMaxSpeed(receivedDelay); // set speed
      stepper2.move(receivedMMdistance); // set distance
    }
    // START - OPEN
    if (receivedCommand == 'p') // OPENING stepper 1
    {
      runallowed = true; // allow running
      receivedMMdistance = Serial.parseFloat(); // value for the steps
      receivedDelay = Serial.parseFloat(); // value for the speed

      stepper1.enableOutputs(); // enable pins
      stepper2.disableOutputs(); // disable pins
      Serial.print(receivedMMdistance); // print the values for checking
      Serial.print(receivedDelay);
      Serial.println(" OPEN"); // print the action
      stepper1.setMaxSpeed(receivedDelay); // set speed
      stepper1.move(receivedMMdistance); // set distance
      //stepper2.setMaxSpeed(receivedDelay); // set speed
      //stepper2.move(receivedMMdistance); // set distance

    }

        if (receivedCommand == 'b') // OPENING stepper 2
    {
      runallowed = true; // allow running
      receivedMMdistance = Serial.parseFloat(); // value for the steps
      receivedDelay = Serial.parseFloat(); // value for the speed

      stepper2.enableOutputs(); // enable pins
      stepper1.disableOutputs(); // disable pins
      Serial.print(receivedMMdistance); // print the values for checking
      Serial.print(receivedDelay);
      Serial.println(" OPEN"); // print the action
      //stepper1.setMaxSpeed(receivedDelay); // set speed
      //stepper1.move(receivedMMdistance); // set distance
      stepper2.setMaxSpeed(receivedDelay); // set speed
      stepper2.move(receivedMMdistance); // set distance

    }

    // START - CLOSE
    if (receivedCommand == 'c') // CLOSING - Rotates the motor in the opposite direction as opening
    {
      runallowed = true; // allow running
      receivedMMdistance = Serial.parseFloat(); // value for the steps
      receivedDelay = Serial.parseFloat(); // value for the speed

      Serial.print(receivedMMdistance);  // print the values for checking
      Serial.print(receivedDelay);
      Serial.println(" CLOSE"); // print action
      stepper1.setMaxSpeed(receivedDelay); // set speed
      stepper1.move(-1 * receivedMMdistance); // set distance - negative value flips the direction
      stepper2.setMaxSpeed(receivedDelay); // set speed
      stepper2.move(-1 * receivedMMdistance); // set distance - negative value flips the direction
    }

    // STOP - STOP
    if (receivedCommand == 'n') // immediately stops the motor
    {
      runallowed = false; // disable running
      stepper1.setCurrentPosition(0); // reset position
      stepper2.setCurrentPosition(0); // reset position
      Serial.println(" STOP"); // print action
      stepper1.stop(); // stop motor
      stepper1.disableOutputs(); // disable power
      stepper2.stop(); // stop motor
      stepper2.disableOutputs(); // disable power
    }

    // SET ACCELERATION
    if (receivedCommand == 'a') // Setting up a new acceleration value
    {
      runallowed = false; // we still keep running disabled, since we just update a variable
      receivedAcceleration = Serial.parseFloat(); // receive the acceleration from serial

      stepper1.setAcceleration(receivedAcceleration); // update the value of the variable
      stepper2.setAcceleration(receivedAcceleration); // update the value of the variable

      Serial.println(" ACC Updated"); // confirm update by message
    }
  }
  // after we went through the above tasks, newData becomes false again, so we are ready to receive new commands again.
  newData = false;
}
