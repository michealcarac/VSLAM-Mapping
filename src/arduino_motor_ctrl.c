#define joyX A0   // X Equals left or right.
#define joyY A1   // Y Equals Direction Forward or Backwards

#define FORWARD_PIN  0
#define BACKWARD_PIN 1
#define LEFT_PIN     2
#define RIGHT_PIN    3


int R_Dir; // Right wheel
int L_Dir; // Left wheel

const int max_speed = 2000;
const int min_speed = -max_speed;

void setup() {
  Serial.begin(9600);
  Serial.write("M1:startup\r\n");
  Serial.write("M2:startup\r\n");

  // Define Max speed

  pinMode(FORWARD_PIN,  INPUT_PULLUP);
  pinMode(BACKWARD_PIN, INPUT_PULLUP);
  pinMode(LEFT_PIN,     INPUT_PULLUP);
  pinMode(RIGHT_PIN,    INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  int xValue = analogRead(joyX);
  int yValue = analogRead(joyY);


  // Maping the values from the Y direction of the Joystick, Forward or Backward
  if (yValue >= 515){
    R_Dir = map(yValue, 541, 1024, 0, max_speed);
    L_Dir = -R_Dir;
  }else if (yValue <= 490){
    R_Dir = map(yValue, 500, 0, 0, min_speed);
    L_Dir = -R_Dir;
  }else if (yValue < 515 && yValue > 490){
    R_Dir = 0;
    L_Dir = -R_Dir;
  }

  // Maping the values for Left and Right
  int dir = 0;
   if (xValue >= 531){                              // Turning Right
    dir = map(yValue, 503, 1024, 0, max_speed);
    R_Dir = -L_Dir - dir;
  }else if (xValue <= 510){                         // Turning Left
    dir = map(xValue, 503, 0, 0, min_speed);
    L_Dir = -R_Dir-dir;
  }

  if      (digitalRead(FORWARD_PIN) == LOW)  // Go forward
  {
    R_Dir = max_speed;
    L_Dir = -max_speed;
  }
  else if (digitalRead(BACKWARD_PIN) == LOW) // Go backwards
  {
    R_Dir = -max_speed;
    L_Dir = max_speed;
  }
  else if (digitalRead(LEFT_PIN) == LOW)     // Turn left
  {
    R_Dir = max_speed / 2;
    L_Dir = max_speed / 2;
  }
  else if (digitalRead(RIGHT_PIN) == LOW)    // Turn right
  {
    R_Dir = -max_speed / 2;;
    L_Dir = -max_speed / 2;;
  }

  Serial.write("M1: ");
  Serial.print(-L_Dir+20);
  Serial.write("\r\n");
  Serial.write("M2: ");
  Serial.print(R_Dir);
  Serial.write("\r\n");

  delay(500);
}