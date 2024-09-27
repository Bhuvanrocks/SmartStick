// Pins
const int trigPin = 5;  // Trigger pin of the ultrasonic sensor
const int echoPin = 18; // Echo pin of the ultrasonic sensor
const int buzzerPin = 15; // Pin connected to the buzzer
unsigned long currentTime, previousTime, delayTime;

// Variables
long duration;
int distance;

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);

  // Set pin modes
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);
}

void loop() {
  currentTime = millis(); // Get the current time

  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Set the trigger pin high for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echo pin
  duration = pulseIn(echoPin, HIGH);

  // Calculate distance in cm
  distance = duration * 0.034 / 2;

  // Print distance on the serial monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // If distance is less than 20cm, buzz the buzzer
  if (distance < 100 && distance >= 2) {
    // Map distance to a delay time between 200 and 400 milliseconds
    delayTime = map(distance, 2, 100, 200, 400); 

    digitalWrite(buzzerPin, HIGH); // Turn the buzzer on

    // Control the buzzer's on-off timing
    if (currentTime - previousTime >= delayTime) {
      digitalWrite(buzzerPin, LOW); // Turn the buzzer off
      previousTime = currentTime;   // Reset the timer
    }
  } else {
    // Turn off the buzzer if the distance is more than 20cm
    digitalWrite(buzzerPin, LOW);
  }

  delay(100); // Short delay before the next measurement
}
